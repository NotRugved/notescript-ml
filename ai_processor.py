"""AI processor module for NoteScript ML with Primary Gemini API and FreeLLMAPI fallback."""

import copy
import json
import os
import re
import time
import urllib.error
import urllib.request
from typing import Any

from dotenv import load_dotenv
from openai import APIConnectionError, APIError, OpenAI, RateLimitError

from yt_extractor import format_time, parse_time

load_dotenv()


class QuotaExhaustedError(Exception):
    """Exception raised when both primary and fallback LLM quotas are exhausted."""


SYSTEM_INSTRUCTION_SEGMENT = """You are an expert machine learning teacher creating study notes from ONE segment of a CampusX '100 Days of Machine Learning' lecture. You can see and hear the video segment. The student will use these notes to revise for exams and interviews, so be detailed.

Language: Hinglish in Roman script. Hindi sentence flow with English technical terms, for example 'Gradient descent ek optimization algorithm hai jo loss ko minimize karta hai'. Never use Devanagari.

Rules:
- Stay faithful to the video. Do not add topics the teacher did not cover. If audio or screen is unclear, write 'unclear in video'. Never invent teacher statements.
- theory_sections: cover every concept in order. For each: heading, timestamp, and content (detailed markdown containing what it is, why it is needed, step-by-step working, and the math with meaning of every symbol). Be thorough.
- intuition: the teacher's plain-language 'samajh' of the concept, separate from theory.
- code_blocks: complete, runnable snippets. If OFFICIAL NOTEBOOK text is provided and the teacher's code matches it, copy from the notebook exactly and label 'official'. Code seen on screen but not in the notebook is 'on-screen'. Code only described aloud is 'reconstructed' and must stay minimal. Add a Hinglish explanation line by line where useful.
- analogies: ONLY real-life examples, stories or analogies the teacher actually used, with the timestamp. Explain what each analogy is teaching.
- common_mistakes: pitfalls the teacher mentioned (source 'teacher') and clearly standard ones for this topic (source 'added'). Include why it happens and the fix.
- formulas and key_terms: collect them with short Hinglish meanings.
- Timestamps are ABSOLUTE video time in MM:SS (or H:MM:SS), not relative to this segment.
- Output ONLY valid JSON matching this schema:
{
  "theory_sections": [{"heading": "...", "timestamp": "MM:SS", "content": "..."}],
  "intuition": [{"timestamp": "MM:SS", "text": "..."}],
  "code_blocks": [{"title": "...", "label": "official/on-screen/reconstructed", "timestamp": "MM:SS", "explanation": "...", "code": "..."}],
  "analogies": [{"timestamp": "MM:SS", "analogy": "...", "explains": "..."}],
  "common_mistakes": [{"mistake": "...", "why": "...", "fix": "...", "timestamp": "MM:SS", "source": "teacher/added"}],
  "formulas": [{"name": "...", "formula": "...", "meaning": "..."}],
  "key_terms": [{"term": "...", "meaning": "..."}]
}"""

SYSTEM_INSTRUCTION_REVISION = """You are an expert machine learning educator creating a quick revision pack from a lecture's merged notes.
Produce concise, highly memorable study material in Hinglish (Roman script, technical terms in English).

Output ONLY valid JSON matching this schema:
{
  "one_line_summary": "single concise takeaway sentence",
  "cheat_sheet": "markdown table or bulleted summary of key facts and algorithms",
  "flashcards": [
    {"q": "question", "a": "answer"} // exactly 15 cards
  ],
  "quiz": [
    {
      "question": "question text",
      "options": ["option 0", "option 1", "option 2", "option 3"],
      "answer_index": 0, // integer 0-3
      "explanation": "why this option is correct"
    } // exactly 10 questions
  ],
  "interview_questions": [
    {"q": "interview question", "a": "in-depth model interview answer"} // exactly 5 questions
  ]
}
No markdown fences, no extra commentary."""


# ── GEMINI PRIMARY CALLS ──────────────────────────────────────────────────────

def _execute_gemini_request(payload: dict, timeout_seconds: int = 120) -> str:
    """Send JSON payload directly to the primary Gemini generateContent endpoint."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is missing.")

    endpoint_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    serialized_payload = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        endpoint_url,
        data=serialized_payload,
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        response_bytes = response.read()
        response_data = json.loads(response_bytes.decode("utf-8"))

    candidates = response_data.get("candidates", [])
    if len(candidates) == 0:
        raise RuntimeError(f"No response candidates returned: {response_data}")

    first_candidate = candidates[0]
    content = first_candidate.get("content", {})
    parts = content.get("parts", [])
    if len(parts) == 0:
        raise RuntimeError("No parts found in model candidate response.")

    text_parts = []
    for part in parts:
        if "text" in part:
            text_parts.append(part["text"])

    return "".join(text_parts)


def _call_gemini_with_retry(payload: dict) -> str:
    """Execute Gemini request with retries on transient errors."""
    retry_delays = [3, 8]
    last_exception = None

    for attempt in range(3):
        try:
            return _execute_gemini_request(payload)
        except urllib.error.HTTPError as http_error:
            last_exception = http_error
            error_status = http_error.code
            try:
                error_body = http_error.read().decode("utf-8")
            except Exception:
                error_body = str(http_error)

            lower_body = error_body.lower()
            if "quota" in lower_body or error_status == 429:
                raise QuotaExhaustedError("Gemini daily quota exhausted.")
            if error_status >= 500:
                if attempt < len(retry_delays):
                    time.sleep(retry_delays[attempt])
                    continue
            raise RuntimeError(f"Gemini API error {error_status}: {error_body}") from http_error
        except (urllib.error.URLError, TimeoutError, OSError) as net_err:
            last_exception = net_err
            if attempt < len(retry_delays):
                time.sleep(retry_delays[attempt])
                continue
            raise RuntimeError(f"Network error communicating with Gemini: {net_err}") from net_err

    if last_exception is not None:
        raise last_exception
    raise RuntimeError("Gemini call failed after retries.")


# ── FREELLMAPI FALLBACK CALLS ─────────────────────────────────────────────────

def get_freellmapi_client() -> OpenAI:
    """Instantiate OpenAI client for the local FreeLLMAPI router."""
    base_url = os.getenv("LLM_BASE_URL", "http://127.0.0.1:31415/v1").strip()
    api_key = os.getenv("LLM_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("LLM_API_KEY environment variable is missing.")
    return OpenAI(base_url=base_url, api_key=api_key)


def _call_freellmapi(
    messages: list[dict],
    temperature: float = 0.2,
    max_tokens: int = 8192,
) -> str:
    """Send chat completion to local FreeLLMAPI router with 8192 max tokens."""
    client = get_freellmapi_client()
    model = os.getenv("LLM_MODEL", "auto:notescript-ml").strip()

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    choices = response.choices
    if len(choices) == 0:
        raise RuntimeError("No choices returned by FreeLLMAPI router.")

    content = choices[0].message.content
    if not content:
        raise RuntimeError("Empty response content from FreeLLMAPI router.")

    return content


def _call_freellmapi_with_retry(
    messages: list[dict],
    temperature: float = 0.2,
    max_tokens: int = 8192,
) -> str:
    """Execute FreeLLMAPI request with backoff retries."""
    retry_delays = [3, 8]
    last_exception = None

    for attempt in range(3):
        try:
            return _call_freellmapi(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except (RateLimitError, APIError) as api_err:
            last_exception = api_err
            err_str = str(api_err).lower()
            if "quota" in err_str or "429" in err_str:
                raise QuotaExhaustedError("FreeLLMAPI quota exhausted.")
            if attempt < len(retry_delays):
                time.sleep(retry_delays[attempt])
                continue
            raise RuntimeError(f"FreeLLMAPI error: {api_err}") from api_err
        except APIConnectionError as conn_err:
            last_exception = conn_err
            base_url = os.getenv("LLM_BASE_URL", "http://127.0.0.1:31415/v1")
            raise RuntimeError(f"Cannot reach FreeLLMAPI router at {base_url}: {conn_err}") from conn_err
        except Exception as generic_err:
            last_exception = generic_err
            if attempt < len(retry_delays):
                time.sleep(retry_delays[attempt])
                continue
            raise RuntimeError(f"Error communicating with FreeLLMAPI: {generic_err}") from generic_err

    if last_exception is not None:
        raise last_exception
    raise RuntimeError("FreeLLMAPI call failed after retries.")


# ── ORCHESTRATION WITH DUAL-TIER FALLBACK ──────────────────────────────────────

def _clean_json_text(raw_text: str) -> str:
    """Strip markdown code fence wrappers and extract clean JSON string."""
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _execute_with_fallback(
    gemini_payload: dict,
    openai_messages: list[dict],
    temperature: float = 0.2,
    max_tokens: int = 8192,
) -> str:
    """Attempt primary Gemini API first; on failure, seamlessly fall back to local FreeLLMAPI."""
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    freellm_key = os.getenv("LLM_API_KEY", "").strip()

    gemini_failed = False
    gemini_error = ""

    # Tier 1: Try Primary Google Gemini API
    if gemini_key:
        try:
            return _call_gemini_with_retry(gemini_payload)
        except Exception as exc:
            gemini_failed = True
            gemini_error = str(exc)

    # Tier 2: Fall back to local FreeLLMAPI router
    if freellm_key:
        try:
            return _call_freellmapi_with_retry(
                messages=openai_messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except QuotaExhaustedError:
            raise
        except Exception as fl_exc:
            raise RuntimeError(
                f"Both Primary Gemini and FreeLLMAPI fallback failed. Gemini: {gemini_error} | FreeLLMAPI: {fl_exc}"
            ) from fl_exc

    if gemini_failed:
        raise RuntimeError(f"Primary Gemini call failed and no FreeLLMAPI fallback available: {gemini_error}")
    raise RuntimeError("No LLM API keys configured (neither GEMINI_API_KEY nor LLM_API_KEY).")


def _parse_or_retry_json(
    gemini_payload: dict,
    openai_messages: list[dict],
    temperature: float = 0.2,
    max_tokens: int = 8192,
) -> dict:
    """Parse JSON response from dual-engine pipeline, retrying if formatting fails."""
    raw_text = _execute_with_fallback(
        gemini_payload=gemini_payload,
        openai_messages=openai_messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    cleaned = _clean_json_text(raw_text)

    try:
        return json.loads(cleaned, strict=False)
    except json.JSONDecodeError:
        # Regex search for outer JSON bracket payload
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0), strict=False)
            except json.JSONDecodeError:
                pass

        # Retry once asking for clean raw JSON
        retry_gemini = copy.deepcopy(gemini_payload)
        gemini_contents = retry_gemini.get("contents", [])
        if len(gemini_contents) > 0:
            gemini_contents[0]["parts"].append(
                {"text": "The previous response had invalid JSON. Return ONLY raw valid JSON."}
            )

        retry_openai = copy.deepcopy(openai_messages)
        retry_openai.append(
            {
                "role": "user",
                "content": "The previous response had invalid JSON. Return ONLY raw valid JSON matching the schema.",
            }
        )

        raw_text_retry = _execute_with_fallback(
            gemini_payload=retry_gemini,
            openai_messages=retry_openai,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        cleaned_retry = _clean_json_text(raw_text_retry)
        try:
            return json.loads(cleaned_retry, strict=False)
        except json.JSONDecodeError:
            match_retry = re.search(r"\{.*\}", cleaned_retry, re.DOTALL)
            if match_retry:
                try:
                    return json.loads(match_retry.group(0), strict=False)
                except json.JSONDecodeError:
                    pass

            raise RuntimeError(
                f"Failed to parse valid JSON from LLM output: {cleaned_retry[:300]}"
            )


# ── TIME NORMALIZATION & CONTRACT ENFORCEMENT ─────────────────────────────────

def fix_timestamps(data: dict, start_seconds: int, end_seconds: int) -> dict:
    """Adjust out-of-range timestamps and ensure required segment list keys exist."""
    if isinstance(data, list):
        if len(data) > 0 and isinstance(data[0], dict):
            data = data[0]
        else:
            data = {}
    elif not isinstance(data, dict):
        data = {}

    required_list_keys = [
        "theory_sections",
        "intuition",
        "code_blocks",
        "analogies",
        "common_mistakes",
        "formulas",
        "key_terms",
    ]

    for list_key in required_list_keys:
        if list_key not in data or not isinstance(data[list_key], list):
            data[list_key] = []

    # Normalize theory_sections
    for item in data.get("theory_sections", []):
        if not isinstance(item, dict):
            continue
        if "heading" not in item or not item["heading"]:
            if "title" in item and item["title"]:
                item["heading"] = item["title"]
            elif "concept" in item and item["concept"]:
                item["heading"] = item["concept"]
            else:
                item["heading"] = "Core Concept"
        if "content" not in item or not item["content"]:
            parts = []
            if "concept_explanation" in item and item["concept_explanation"]:
                parts.append(str(item["concept_explanation"]))
            if "why_it_is_needed" in item and item["why_it_is_needed"]:
                parts.append("### Why It Is Needed\n" + str(item["why_it_is_needed"]))
            if "step_by_step_working" in item and item["step_by_step_working"]:
                working = item["step_by_step_working"]
                if isinstance(working, list):
                    working_lines = []
                    for step in working:
                        working_lines.append(f"- {step}")
                    parts.append("### Step-by-Step Working\n" + "\n".join(working_lines))
                else:
                    parts.append("### Step-by-Step Working\n" + str(working))
            if "mathematical_formulation" in item and item["mathematical_formulation"]:
                parts.append("### Mathematical Formulation\n" + str(item["mathematical_formulation"]))
            item["content"] = "\n\n".join(parts)

    # Normalize code_blocks
    for item in data.get("code_blocks", []):
        if not isinstance(item, dict):
            continue
        if "title" not in item or not item["title"]:
            if "heading" in item and item["heading"]:
                item["title"] = item["heading"]
            elif "name" in item and item["name"]:
                item["title"] = item["name"]
            else:
                item["title"] = "Code Implementation"

    # Iterate over all list sections that contain timestamp fields
    for list_key in required_list_keys:
        items = data[list_key]
        for item in items:
            if isinstance(item, dict) and "timestamp" in item:
                raw_ts = item["timestamp"]
                parsed_sec = parse_time(str(raw_ts))
                if parsed_sec is not None:
                    if parsed_sec < start_seconds or parsed_sec > (end_seconds + 30):
                        parsed_sec = parsed_sec + start_seconds
                    item["timestamp"] = format_time(parsed_sec)
                else:
                    item["timestamp"] = format_time(start_seconds)

    return data


# ── PUBLIC API METHODS ────────────────────────────────────────────────────────

def summarize_segment(
    video_url: str,
    start_seconds: int,
    end_seconds: int,
    notebook_text: str = "",
    resolution: str = "LOW",
    total_duration: int = 0,
) -> dict:
    """Summarize a video segment using Primary Gemini with FreeLLMAPI fallback."""
    notebook_section = notebook_text if notebook_text else "None provided."

    user_prompt = f"""VIDEO INFORMATION:
Video URL: {video_url}
Segment start: {format_time(start_seconds)} ({start_seconds}s)
Segment end: {format_time(end_seconds)} ({end_seconds}s)
Total video duration: {format_time(total_duration)} ({total_duration}s)

OFFICIAL NOTEBOOK CONTENT:
{notebook_section}

Watch and analyze this lecture segment carefully. Output detailed study notes in Hinglish Roman script matching the Segment JSON contract."""

    # Map resolution string for Gemini
    mapped_resolution = "MEDIA_RESOLUTION_LOW"
    if str(resolution).upper() == "HIGH":
        mapped_resolution = "MEDIA_RESOLUTION_HIGH"

    gemini_payload = {
        "systemInstruction": {
            "parts": [{"text": SYSTEM_INSTRUCTION_SEGMENT}]
        },
        "contents": [
            {
                "parts": [
                    {
                        "file_data": {
                            "mime_type": "video/mp4",
                            "file_uri": video_url,
                        },
                        "video_metadata": {
                            "start_offset": f"{start_seconds}s",
                            "end_offset": f"{end_seconds}s",
                        },
                    },
                    {"text": user_prompt},
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "mediaResolution": mapped_resolution,
            "temperature": 0.2,
        },
    }

    openai_messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTION_SEGMENT},
        {"role": "user", "content": user_prompt},
    ]

    raw_dict = _parse_or_retry_json(
        gemini_payload=gemini_payload,
        openai_messages=openai_messages,
        temperature=0.2,
        max_tokens=8192,
    )
    fixed_dict = fix_timestamps(raw_dict, start_seconds, end_seconds)
    return fixed_dict


def build_revision(merged_notes_text: str) -> dict:
    """Generate revision pack using Primary Gemini with FreeLLMAPI fallback."""
    user_prompt = f"""Here are the complete merged study notes for this Machine Learning lecture:

{merged_notes_text}

Generate the revision pack following the Revision JSON contract."""

    gemini_payload = {
        "systemInstruction": {
            "parts": [{"text": SYSTEM_INSTRUCTION_REVISION}]
        },
        "contents": [
            {
                "parts": [
                    {"text": user_prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.3,
        },
    }

    openai_messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTION_REVISION},
        {"role": "user", "content": user_prompt},
    ]

    revision_dict = _parse_or_retry_json(
        gemini_payload=gemini_payload,
        openai_messages=openai_messages,
        temperature=0.3,
        max_tokens=8192,
    )

    if isinstance(revision_dict, list):
        if len(revision_dict) > 0 and isinstance(revision_dict[0], dict):
            revision_dict = revision_dict[0]
        else:
            revision_dict = {}
    elif not isinstance(revision_dict, dict):
        revision_dict = {}

    # Validate structure and provide fallbacks if missing
    if "one_line_summary" not in revision_dict:
        revision_dict["one_line_summary"] = ""
    if "cheat_sheet" not in revision_dict:
        revision_dict["cheat_sheet"] = ""
    if "flashcards" not in revision_dict or not isinstance(revision_dict["flashcards"], list):
        revision_dict["flashcards"] = []
    if "quiz" not in revision_dict or not isinstance(revision_dict["quiz"], list):
        revision_dict["quiz"] = []
    if "interview_questions" not in revision_dict or not isinstance(revision_dict["interview_questions"], list):
        revision_dict["interview_questions"] = []

    return revision_dict


def check_api_status() -> dict:
    """Check connectivity to Primary Gemini API, falling back to FreeLLMAPI router status."""
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash").strip()

    # Check Primary Gemini
    gemini_ok = False
    gemini_msg = ""
    if gemini_key:
        endpoint_url = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent?key={gemini_key}"
        payload = {
            "contents": [{"parts": [{"text": "hi"}]}],
            "generationConfig": {"maxOutputTokens": 2},
        }
        serialized_payload = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            endpoint_url,
            data=serialized_payload,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=8) as response:
                if response.status == 200:
                    return {"available": True, "message": f"Online & ready (Gemini {gemini_model})"}
        except urllib.error.HTTPError as http_error:
            if http_error.code == 429:
                gemini_msg = f"Gemini quota limit active (429)"
            elif http_error.code == 503:
                gemini_msg = f"Gemini server busy (503)"
            else:
                gemini_msg = f"Gemini error {http_error.code}"
        except Exception as exc:
            gemini_msg = f"Gemini connection error: {exc}"

    # If Gemini is not operational, test local FreeLLMAPI fallback
    freellm_key = os.getenv("LLM_API_KEY", "").strip()
    freellm_base = os.getenv("LLM_BASE_URL", "http://127.0.0.1:31415/v1").strip()
    freellm_model = os.getenv("LLM_MODEL", "auto:notescript-ml").strip()

    if freellm_key:
        try:
            client = OpenAI(base_url=freellm_base, api_key=freellm_key, timeout=8.0)
            res = client.chat.completions.create(
                model=freellm_model,
                messages=[{"role": "user", "content": "ping"}],
                max_tokens=2,
            )
            if res and res.choices and len(res.choices) > 0:
                fallback_reason = f" [Gemini: {gemini_msg}]" if gemini_msg else ""
                return {
                    "available": True,
                    "message": f"Online via FreeLLMAPI fallback ({freellm_model}){fallback_reason}",
                }
        except APIConnectionError:
            pass
        except Exception as fl_exc:
            pass

    if gemini_msg:
        return {"available": False, "message": f"Primary unavailable: {gemini_msg}. FreeLLMAPI offline."}
    return {"available": False, "message": "No API keys configured or providers reachable."}
