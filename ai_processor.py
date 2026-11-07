"""AI processor module for NoteScript ML."""

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any

from dotenv import load_dotenv

from extractor import format_time, parse_time

load_dotenv()


class QuotaExhaustedError(Exception):
    """Exception raised when Gemini daily quota is exhausted."""


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


def _execute_gemini_request(payload: dict, timeout_seconds: int = 120) -> str:
    """Send a direct JSON payload to the Gemini generateContent REST endpoint."""
    api_key = os.getenv("GEMINI_API_KEY", "")
    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
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


def call_with_retry(payload: dict) -> str:
    """Execute Gemini request with 3 retries on transient errors and catch daily quota limits."""
    retry_delays = [5, 15, 40]
    last_exception = None

    for attempt in range(4):
        try:
            return _execute_gemini_request(payload)
        except urllib.error.HTTPError as http_error:
            error_status = http_error.code
            try:
                error_body = http_error.read().decode("utf-8")
            except Exception:
                error_body = str(http_error)

            lower_body = error_body.lower()
            # Check for daily quota exhaustion
            if "quota" in lower_body and ("daily" in lower_body or "per_day" in lower_body or "perday" in lower_body or "free_tier_requests" in lower_body):
                if error_status == 429:
                    raise QuotaExhaustedError("Gemini API daily quota exhausted. Please resume tomorrow.")

            # Check for retryable rate limits or server errors
            if error_status == 429 or error_status >= 500:
                last_exception = http_error
                if attempt < len(retry_delays):
                    time.sleep(retry_delays[attempt])
                    continue
            raise RuntimeError(f"Gemini API returned error {error_status}: {error_body}") from http_error
        except (urllib.error.URLError, TimeoutError, OSError) as network_error:
            last_exception = network_error
            if attempt < len(retry_delays):
                time.sleep(retry_delays[attempt])
                continue
            raise RuntimeError(f"Network error communicating with Gemini API: {network_error}") from network_error

    if last_exception is not None:
        raise last_exception
    raise RuntimeError("Call failed after maximum retry attempts.")


def _clean_json_text(raw_text: str) -> str:
    """Strip markdown code fence wrappers from JSON output."""
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        first_line = lines[0]
        if "```" in first_line:
            lines = lines[1:]
        if len(lines) > 0 and lines[len(lines) - 1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    return cleaned


def _parse_or_retry_json(payload: dict) -> dict:
    """Parse JSON response from API, retrying once if syntax is invalid."""
    raw_text = call_with_retry(payload)
    cleaned = _clean_json_text(raw_text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Retry once asking explicitly for strict valid JSON
        retry_payload = dict(payload)
        contents = retry_payload.get("contents", [])
        if len(contents) > 0:
            prompt_part = {"text": "The previous response was not valid JSON. Please fix and return ONLY valid raw JSON."}
            contents[0]["parts"].append(prompt_part)
        raw_text_retry = call_with_retry(retry_payload)
        cleaned_retry = _clean_json_text(raw_text_retry)
        try:
            return json.loads(cleaned_retry)
        except json.JSONDecodeError as decode_error:
            raise RuntimeError(f"Failed to parse valid JSON from Gemini output: {cleaned_retry[:300]}") from decode_error


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
                    # If outside segment range with buffer, offset by segment start
                    if parsed_sec < start_seconds or parsed_sec > (end_seconds + 30):
                        parsed_sec = parsed_sec + start_seconds
                    item["timestamp"] = format_time(parsed_sec)
                else:
                    item["timestamp"] = format_time(start_seconds)

    return data


def summarize_segment(
    video_url: str,
    start_seconds: int,
    end_seconds: int,
    notebook_text: str = "",
    resolution: str = "LOW",
    total_duration: int = 0,
) -> dict:
    """Summarize a video segment using Gemini API and return the structured note dict."""
    user_prompt = f"""Video segment start: {format_time(start_seconds)} ({start_seconds}s)
Video segment end: {format_time(end_seconds)} ({end_seconds}s)
Total video duration: {format_time(total_duration)} ({total_duration}s)

OFFICIAL NOTEBOOK CONTENT:
{notebook_text if notebook_text else 'None provided.'}

Watch this segment carefully. Output detailed study notes in Hinglish Roman script matching the Segment JSON contract."""

    # Map resolution string
    mapped_resolution = "MEDIA_RESOLUTION_LOW"
    if str(resolution).upper() == "HIGH":
        mapped_resolution = "MEDIA_RESOLUTION_HIGH"

    payload = {
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

    raw_dict = _parse_or_retry_json(payload)
    fixed_dict = fix_timestamps(raw_dict, start_seconds, end_seconds)
    return fixed_dict


def build_revision(merged_notes_text: str) -> dict:
    """Generate revision pack (summary, cheat sheet, flashcards, quiz, interview questions)."""
    user_prompt = f"""Here are the complete merged study notes for this Machine Learning lecture:

{merged_notes_text}

Generate the revision pack following the Revision JSON contract."""

    payload = {
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

    revision_dict = _parse_or_retry_json(payload)
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
