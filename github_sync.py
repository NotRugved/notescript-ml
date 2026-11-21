"""GitHub synchronization module for NoteScript ML."""
import base64
import json
import os
import time
import urllib.error
import urllib.request


def get_github_token() -> str:
    """Retrieve GitHub token from environment variables or Streamlit secrets."""
    token = os.getenv("GITHUB_TOKEN", "").strip()
    if token:
        return token
    # Fallback: try Streamlit secrets (available on Streamlit Community Cloud)
    try:
        import streamlit as st
        token = st.secrets.get("GITHUB_TOKEN", "")
        if token:
            return token.strip()
    except Exception:
        pass
    return ""


def get_github_repo() -> str:
    """Retrieve GitHub target repository slug (owner/repo)."""
    return os.getenv("GITHUB_REPO", "NotRugved/notescript-ml").strip()


# ── Low-level GitHub API helpers ──────────────────────────────────────────────

def _github_headers(token: str) -> dict:
    """Build standard GitHub API request headers."""
    headers = {
        "User-Agent": "NoteScriptML",
        "Accept": "application/vnd.github.v3+json",
    }
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def get_remote_file_sha(file_path: str, token: str = "", repo: str = "") -> str:
    """Fetch the current git blob SHA for a file on GitHub if it exists."""
    if not token:
        token = get_github_token()
    if not repo:
        repo = get_github_repo()
    if not repo:
        return ""

    url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
    request = urllib.request.Request(url, headers=_github_headers(token))
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            if response.status == 200:
                payload = json.loads(response.read().decode("utf-8"))
                return payload.get("sha", "")
    except Exception:
        return ""
    return ""


def _put_file_to_github(
    file_path: str,
    content_bytes: bytes,
    commit_message: str,
    token: str = "",
    repo: str = "",
) -> tuple[bool, str]:
    """Upload or update a single file on GitHub via the Contents API."""
    if not token:
        token = get_github_token()
    if not repo:
        repo = get_github_repo()
    if not token:
        return False, "GITHUB_TOKEN not configured."
    if not repo:
        return False, "GITHUB_REPO not configured."

    b64_content = base64.b64encode(content_bytes).decode("utf-8")
    existing_sha = get_remote_file_sha(file_path, token, repo)

    body_dict = {
        "message": commit_message,
        "content": b64_content,
        "branch": "main",
    }
    if existing_sha:
        body_dict["sha"] = existing_sha

    serialized_data = json.dumps(body_dict).encode("utf-8")
    url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
    headers = _github_headers(token)
    headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=serialized_data, method="PUT", headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            if response.status in (200, 201):
                return True, "OK"
            return False, f"GitHub returned HTTP status {response.status}"
    except urllib.error.HTTPError as http_err:
        if http_err.code == 403:
            return False, "GitHub 403 Forbidden: Ensure your GITHUB_TOKEN has 'Contents: Read and write' permission."
        if http_err.code == 422:
            return False, f"GitHub 422: SHA mismatch or invalid content for {file_path}"
        return False, f"GitHub sync failed (HTTP {http_err.code}): {http_err.reason}"
    except Exception as exc:
        return False, f"GitHub sync network error: {exc}"


def _download_github_file(file_path: str, token: str = "", repo: str = "") -> bytes | None:
    """Download raw bytes of a file from GitHub. Returns None on failure."""
    if not repo:
        repo = get_github_repo()
    if not token:
        token = get_github_token()

    url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
    request = urllib.request.Request(url, headers=_github_headers(token))
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            meta = json.loads(response.read().decode("utf-8"))
    except Exception:
        return None

    download_url = meta.get("download_url", "")
    content_b64 = meta.get("content", "")

    try:
        if download_url:
            raw_req = urllib.request.Request(download_url, headers={"User-Agent": "NoteScriptML"})
            with urllib.request.urlopen(raw_req, timeout=30) as raw_resp:
                return raw_resp.read()
        elif content_b64:
            # Strip whitespace that GitHub injects into base64 content
            cleaned = content_b64.replace("\n", "").replace(" ", "")
            return base64.b64decode(cleaned)
    except Exception:
        return None
    return None


def _list_github_directory(dir_path: str, token: str = "", repo: str = "") -> list[dict]:
    """List items in a GitHub directory. Returns list of dicts with 'name' and 'type'."""
    if not repo:
        repo = get_github_repo()
    if not token:
        token = get_github_token()

    url = f"https://api.github.com/repos/{repo}/contents/{dir_path}"
    request = urllib.request.Request(url, headers=_github_headers(token))
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            items = json.loads(response.read().decode("utf-8"))
            if not isinstance(items, list):
                return []
            return items
    except Exception:
        return []


# ── generated_notes/ push (admin) ────────────────────────────────────────────

def push_notes_to_github(
    video_id: str,
    main_notes_md: str,
    revision_pack_md: str,
    code_py: str,
    metadata: dict,
    progress_callback=None,
) -> tuple[int, int, list[str]]:
    """Push 4 files for one lecture into generated_notes/<video_id>/ on GitHub.

    Returns (pushed_count, total_files, list_of_errors).
    """
    token = get_github_token()
    repo = get_github_repo()
    if not token:
        return 0, 4, ["GITHUB_TOKEN not configured."]

    base_path = f"generated_notes/{video_id}"
    files_to_push = [
        (f"{base_path}/main_notes.md", main_notes_md.encode("utf-8")),
        (f"{base_path}/revision_pack.md", revision_pack_md.encode("utf-8")),
        (f"{base_path}/code.py", code_py.encode("utf-8")),
        (f"{base_path}/metadata.json", json.dumps(metadata, indent=2, ensure_ascii=False).encode("utf-8")),
    ]

    # Save to local generated_notes/ directory as well
    local_dir = os.path.join("generated_notes", video_id)
    try:
        os.makedirs(local_dir, exist_ok=True)
        with open(os.path.join(local_dir, "main_notes.md"), "w", encoding="utf-8") as f:
            f.write(main_notes_md)
        with open(os.path.join(local_dir, "revision_pack.md"), "w", encoding="utf-8") as f:
            f.write(revision_pack_md)
        with open(os.path.join(local_dir, "code.py"), "w", encoding="utf-8") as f:
            f.write(code_py)
        with open(os.path.join(local_dir, "metadata.json"), "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

    pushed = 0
    errors = []
    for idx, (fpath, fbytes) in enumerate(files_to_push):
        if progress_callback:
            progress_callback(f"Pushing {fpath.split('/')[-1]}...", (idx + 1) / len(files_to_push))

        ok, msg = _put_file_to_github(
            fpath,
            fbytes,
            f"notes: add {video_id}/{fpath.split('/')[-1]}",
            token,
            repo,
        )
        if ok:
            pushed = pushed + 1
        else:
            errors.append(f"{fpath}: {msg}")

        # Small delay to stay within GitHub API secondary rate limits
        if idx < len(files_to_push) - 1:
            time.sleep(0.5)

    return pushed, len(files_to_push), errors


def push_all_new_notes(db_path: str = "notescript.db", progress_callback=None) -> tuple[int, int, list[str]]:
    """Push notes for all locally-cached videos that are not yet on GitHub.

    Returns (total_pushed_lectures, total_lectures, list_of_errors).
    """
    from database import list_videos
    from pipeline import load_cached_result
    from exports import build_main_notes_md, build_revision_md, build_code_py

    token = get_github_token()
    repo = get_github_repo()
    if not token:
        return 0, 0, ["GITHUB_TOKEN not configured."]

    # List which video_id folders already exist on GitHub
    remote_items = _list_github_directory("generated_notes", token, repo)
    remote_ids = set()
    for item in remote_items:
        if item.get("type") == "dir":
            remote_ids.add(item.get("name", ""))

    local_videos = list_videos(db_path)
    all_errors = []
    total_pushed = 0
    total_new = 0

    for v in local_videos:
        vid = v.get("video_id", "")
        if not vid:
            continue
        if vid in remote_ids:
            continue  # Already on GitHub

        result = load_cached_result(vid, db_path)
        if result is None:
            continue

        total_new = total_new + 1

        if progress_callback:
            progress_callback(
                f"Pushing lecture: {v.get('title', vid)[:40]}...",
                total_new / max(len(local_videos), 1),
            )

        main_md = build_main_notes_md(result)
        rev_md = build_revision_md(result)
        code = build_code_py(result)
        metadata = {
            "video_id": vid,
            "title": v.get("title", ""),
            "day_label": v.get("day_label", ""),
            "duration_seconds": v.get("duration_seconds", 0),
            "video_url": f"https://www.youtube.com/watch?v={vid}",
            "pushed_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        }

        pushed, _, errs = push_notes_to_github(vid, main_md, rev_md, code, metadata)
        if pushed > 0:
            total_pushed = total_pushed + 1
        for e in errs:
            all_errors.append(e)

        # Delay between lectures to respect rate limits
        time.sleep(1.0)

    return total_pushed, total_new, all_errors


# ── generated_notes/ pull (hydration for new users) ──────────────────────────

def hydrate_from_generated_notes(db_path: str = "notescript.db") -> tuple[int, list[str]]:
    """Fetch all lectures from generated_notes/ (local disk and GitHub) and merge into local SQLite.

    Returns (hydrated_count, list_of_errors).
    This function is safe to call repeatedly; it skips videos already in the local database.
    """
    from database import list_videos, save_video, save_segment, save_revision

    local_videos = list_videos(db_path)
    local_ids = set()
    for v in local_videos:
        local_ids.add(v.get("video_id", ""))

    hydrated = 0
    errors = []

    # 1. Hydrate from local generated_notes/ directory first if present
    local_dir = "generated_notes"
    if os.path.isdir(local_dir):
        for entry in os.listdir(local_dir):
            entry_path = os.path.join(local_dir, entry)
            if os.path.isdir(entry_path) and entry not in local_ids:
                meta_path = os.path.join(entry_path, "metadata.json")
                if os.path.exists(meta_path):
                    try:
                        with open(meta_path, "r", encoding="utf-8") as mf:
                            metadata = json.load(mf)
                        title = metadata.get("title", "")
                        day_label = metadata.get("day_label", "")
                        duration = int(metadata.get("duration_seconds", 0) or 0)
                        save_video(entry, title, day_label, duration, db_path)

                        notes_text = ""
                        npath = os.path.join(entry_path, "main_notes.md")
                        if os.path.exists(npath):
                            with open(npath, "r", encoding="utf-8") as nf:
                                notes_text = nf.read()

                        code_text = ""
                        cpath = os.path.join(entry_path, "code.py")
                        if os.path.exists(cpath):
                            with open(cpath, "r", encoding="utf-8") as cf:
                                code_text = cf.read()

                        synthetic_segment = _parse_md_to_segment(notes_text, code_text)
                        run_key = "local_hydrated"
                        save_segment(entry, 0, run_key, json.dumps(synthetic_segment, ensure_ascii=False), db_path)

                        rpath = os.path.join(entry_path, "revision_pack.md")
                        if os.path.exists(rpath):
                            with open(rpath, "r", encoding="utf-8") as rf:
                                rev_text = rf.read()
                            synthetic_revision = _parse_revision_md(rev_text)
                            if synthetic_revision:
                                save_revision(entry, run_key, json.dumps(synthetic_revision, ensure_ascii=False), db_path)

                        hydrated = hydrated + 1
                        local_ids.add(entry)
                    except Exception as err:
                        errors.append(f"{entry} (local): {err}")

    # 2. Check remote GitHub repository for any additional folders
    token = get_github_token()
    repo = get_github_repo()
    remote_items = _list_github_directory("generated_notes", token, repo)
    remote_video_ids = []
    for item in remote_items:
        if item.get("type") == "dir":
            remote_video_ids.append(item.get("name", ""))

    for vid in remote_video_ids:
        if vid in local_ids:
            continue  # Already hydrated or present locally

        # Download metadata.json
        meta_bytes = _download_github_file(f"generated_notes/{vid}/metadata.json", token, repo)
        if meta_bytes is None:
            errors.append(f"{vid}: failed to download metadata.json")
            continue

        try:
            metadata = json.loads(meta_bytes.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as parse_err:
            errors.append(f"{vid}: invalid metadata.json: {parse_err}")
            continue

        title = metadata.get("title", "")
        day_label = metadata.get("day_label", "")
        duration = int(metadata.get("duration_seconds", 0) or 0)
        save_video(vid, title, day_label, duration, db_path)

        notes_bytes = _download_github_file(f"generated_notes/{vid}/main_notes.md", token, repo)
        rev_bytes = _download_github_file(f"generated_notes/{vid}/revision_pack.md", token, repo)
        code_bytes = _download_github_file(f"generated_notes/{vid}/code.py", token, repo)

        notes_text = ""
        if notes_bytes:
            notes_text = notes_bytes.decode("utf-8", errors="replace")

        code_text = ""
        if code_bytes:
            code_text = code_bytes.decode("utf-8", errors="replace")

        synthetic_segment = _parse_md_to_segment(notes_text, code_text)
        run_key = "github_hydrated"
        save_segment(vid, 0, run_key, json.dumps(synthetic_segment, ensure_ascii=False), db_path)

        if rev_bytes:
            rev_text = rev_bytes.decode("utf-8", errors="replace")
            synthetic_revision = _parse_revision_md(rev_text)
            if synthetic_revision:
                save_revision(vid, run_key, json.dumps(synthetic_revision, ensure_ascii=False), db_path)

        # Also save to local disk if generated_notes/ exists
        local_vid_dir = os.path.join("generated_notes", vid)
        try:
            os.makedirs(local_vid_dir, exist_ok=True)
            if notes_bytes:
                with open(os.path.join(local_vid_dir, "main_notes.md"), "wb") as nf:
                    nf.write(notes_bytes)
            if rev_bytes:
                with open(os.path.join(local_vid_dir, "revision_pack.md"), "wb") as rf:
                    rf.write(rev_bytes)
            if code_bytes:
                with open(os.path.join(local_vid_dir, "code.py"), "wb") as cf:
                    cf.write(code_bytes)
            with open(os.path.join(local_vid_dir, "metadata.json"), "w", encoding="utf-8") as mf:
                json.dump(metadata, mf, indent=2, ensure_ascii=False)
        except Exception:
            pass

        hydrated = hydrated + 1
        local_ids.add(vid)
        time.sleep(0.3)

    return hydrated, errors


def _parse_md_to_segment(notes_md: str, code_py: str) -> dict:
    """Parse exported markdown and code back into a segment-shaped dict for SQLite storage."""
    segment = {
        "theory_sections": [],
        "intuition": [],
        "code_blocks": [],
        "analogies": [],
        "common_mistakes": [],
        "formulas": [],
        "key_terms": [],
    }

    # Extract theory sections by splitting on ### headings under ## Theory
    current_heading = ""
    current_content_lines = []
    in_theory = False
    in_code_section = False
    in_analogies = False
    in_mistakes = False
    in_formulas = False
    in_key_terms = False

    lines = notes_md.split("\n")
    for line in lines:
        stripped = line.strip()

        # Track which top-level section we are in
        if stripped.startswith("## Theory"):
            in_theory = True
            in_code_section = False
            in_analogies = False
            in_mistakes = False
            in_formulas = False
            in_key_terms = False
            continue
        elif stripped.startswith("## Intuition"):
            # Flush theory
            if current_heading and in_theory:
                segment["theory_sections"].append({
                    "heading": current_heading,
                    "timestamp": "00:00",
                    "content": "\n".join(current_content_lines).strip(),
                })
                current_heading = ""
                current_content_lines = []
            in_theory = False
            continue
        elif stripped.startswith("## Code"):
            if current_heading and in_theory:
                segment["theory_sections"].append({
                    "heading": current_heading,
                    "timestamp": "00:00",
                    "content": "\n".join(current_content_lines).strip(),
                })
                current_heading = ""
                current_content_lines = []
            in_theory = False
            in_code_section = True
            continue
        elif stripped.startswith("## Analogies"):
            if current_heading and in_theory:
                segment["theory_sections"].append({
                    "heading": current_heading,
                    "timestamp": "00:00",
                    "content": "\n".join(current_content_lines).strip(),
                })
                current_heading = ""
                current_content_lines = []
            in_theory = False
            in_code_section = False
            in_analogies = True
            continue
        elif stripped.startswith("## Common Mistakes"):
            in_analogies = False
            in_mistakes = True
            continue
        elif stripped.startswith("## Formulas"):
            in_mistakes = False
            in_formulas = True
            continue
        elif stripped.startswith("### Formulas"):
            in_formulas = True
            continue
        elif stripped.startswith("### Key Terms"):
            in_formulas = False
            in_key_terms = True
            continue
        elif stripped.startswith("## ") and not stripped.startswith("## Theory"):
            # Any other h2 resets everything
            if current_heading and in_theory:
                segment["theory_sections"].append({
                    "heading": current_heading,
                    "timestamp": "00:00",
                    "content": "\n".join(current_content_lines).strip(),
                })
                current_heading = ""
                current_content_lines = []
            in_theory = False
            in_code_section = False
            in_analogies = False
            in_mistakes = False
            in_formulas = False
            in_key_terms = False
            continue

        # Parse theory subsections
        if in_theory and stripped.startswith("### "):
            # Flush previous heading
            if current_heading:
                segment["theory_sections"].append({
                    "heading": current_heading,
                    "timestamp": "00:00",
                    "content": "\n".join(current_content_lines).strip(),
                })
                current_content_lines = []
            # Extract heading text (strip ### and any trailing timestamp link)
            heading_text = stripped[4:].strip()
            paren_pos = heading_text.rfind("(")
            if paren_pos > 0:
                heading_text = heading_text[:paren_pos].strip()
            current_heading = heading_text
            continue

        if in_theory and current_heading:
            current_content_lines.append(line)

        # Parse key terms
        if in_key_terms and stripped.startswith("- **"):
            colon_pos = stripped.find(":**")
            if colon_pos > 4:
                term = stripped[4:colon_pos].strip()
                meaning = stripped[colon_pos + 3:].strip()
                segment["key_terms"].append({"term": term, "meaning": meaning})

        # Parse formulas
        if in_formulas and stripped.startswith("- **"):
            colon_pos = stripped.find(":**")
            if colon_pos > 4:
                name = stripped[4:colon_pos].strip()
                rest = stripped[colon_pos + 3:].strip()
                # Try to extract formula in backticks
                bt1 = rest.find("`")
                bt2 = rest.find("`", bt1 + 1) if bt1 >= 0 else -1
                formula = ""
                meaning = rest
                if bt1 >= 0 and bt2 > bt1:
                    formula = rest[bt1 + 1:bt2]
                    dash_pos = rest.find("—", bt2)
                    if dash_pos > 0:
                        meaning = rest[dash_pos + 1:].strip()
                    else:
                        meaning = rest[bt2 + 1:].strip()
                segment["formulas"].append({"name": name, "formula": formula, "meaning": meaning})

    # Flush last theory section
    if current_heading and in_theory:
        segment["theory_sections"].append({
            "heading": current_heading,
            "timestamp": "00:00",
            "content": "\n".join(current_content_lines).strip(),
        })

    # If we failed to extract any theory, store the whole markdown as one big section
    if len(segment["theory_sections"]) == 0 and len(notes_md.strip()) > 0:
        segment["theory_sections"].append({
            "heading": "Lecture Notes",
            "timestamp": "00:00",
            "content": notes_md.strip(),
        })

    # Parse code blocks from code.py export
    if code_py:
        code_lines = code_py.split("\n")
        current_block_title = ""
        current_block_label = "on-screen"
        current_block_ts = "00:00"
        current_code_lines = []

        for cline in code_lines:
            cstripped = cline.strip()
            if cstripped.startswith("# Block ") and ":" in cstripped:
                # Flush previous block
                if current_block_title and len(current_code_lines) > 0:
                    segment["code_blocks"].append({
                        "title": current_block_title,
                        "label": current_block_label,
                        "timestamp": current_block_ts,
                        "explanation": "",
                        "code": "\n".join(current_code_lines).strip(),
                    })
                    current_code_lines = []

                # Parse block header:  # Block 1: Title | Label: official | Timestamp: 05:30
                parts = cstripped.split("|")
                block_part = parts[0].strip()
                colon_idx = block_part.find(":")
                if colon_idx > 0:
                    current_block_title = block_part[colon_idx + 1:].strip()
                else:
                    current_block_title = block_part

                current_block_label = "on-screen"
                current_block_ts = "00:00"
                for p in parts:
                    p_stripped = p.strip()
                    if p_stripped.startswith("Label:"):
                        current_block_label = p_stripped[6:].strip()
                    elif p_stripped.startswith("Timestamp:"):
                        current_block_ts = p_stripped[10:].strip()
                continue

            if cstripped.startswith("#=") or cstripped.startswith("# VERIFY:"):
                continue
            if cstripped.startswith('"""') and "extracted from" in cstripped.lower():
                continue

            if current_block_title:
                current_code_lines.append(cline)

        # Flush last code block
        if current_block_title and len(current_code_lines) > 0:
            segment["code_blocks"].append({
                "title": current_block_title,
                "label": current_block_label,
                "timestamp": current_block_ts,
                "explanation": "",
                "code": "\n".join(current_code_lines).strip(),
            })

    return segment


def _parse_revision_md(rev_md: str) -> dict:
    """Parse exported revision_pack.md back into the revision JSON structure."""
    revision = {
        "one_line_summary": "",
        "cheat_sheet": "",
        "flashcards": [],
        "quiz": [],
        "interview_questions": [],
    }

    lines = rev_md.split("\n")
    in_summary = False
    in_cheat = False
    in_flashcards = False
    in_quiz = False
    in_interview = False
    in_quiz_answers = False
    cheat_lines = []

    current_fc_q = ""
    current_fc_a = ""

    current_quiz_q = ""
    current_quiz_opts = []

    current_int_q = ""
    current_int_a_lines = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("**One-Line Summary:**"):
            revision["one_line_summary"] = stripped[len("**One-Line Summary:**"):].strip()
            continue

        if stripped == "## Cheat Sheet":
            in_cheat = True
            in_flashcards = False
            in_quiz = False
            in_interview = False
            in_quiz_answers = False
            continue
        elif stripped == "## Flashcards":
            if in_cheat:
                revision["cheat_sheet"] = "\n".join(cheat_lines).strip()
                cheat_lines = []
            in_cheat = False
            in_flashcards = True
            in_quiz = False
            in_interview = False
            continue
        elif stripped == "## Quiz":
            # Flush last flashcard
            if current_fc_q:
                revision["flashcards"].append({"q": current_fc_q, "a": current_fc_a})
                current_fc_q = ""
                current_fc_a = ""
            in_flashcards = False
            in_quiz = True
            in_interview = False
            continue
        elif stripped == "### Quiz Answers & Explanations":
            # Flush last quiz question
            if current_quiz_q:
                revision["quiz"].append({
                    "question": current_quiz_q,
                    "options": current_quiz_opts,
                    "answer_index": 0,
                    "explanation": "",
                })
                current_quiz_q = ""
                current_quiz_opts = []
            in_quiz_answers = True
            in_quiz = False
            continue
        elif stripped == "## Interview Questions":
            in_quiz_answers = False
            in_quiz = False
            in_flashcards = False
            in_interview = True
            continue

        if in_cheat:
            cheat_lines.append(line)

        if in_flashcards:
            if stripped.startswith("**Q:**"):
                # Flush previous card
                if current_fc_q:
                    revision["flashcards"].append({"q": current_fc_q, "a": current_fc_a})
                current_fc_q = stripped[len("**Q:**"):].strip()
                current_fc_a = ""
            elif stripped.startswith("**A:**"):
                current_fc_a = stripped[len("**A:**"):].strip()

        if in_quiz and not in_quiz_answers:
            if stripped.startswith("#### Question"):
                # Flush previous
                if current_quiz_q:
                    revision["quiz"].append({
                        "question": current_quiz_q,
                        "options": current_quiz_opts,
                        "answer_index": 0,
                        "explanation": "",
                    })
                colon_pos = stripped.find(":")
                if colon_pos > 0:
                    current_quiz_q = stripped[colon_pos + 1:].strip()
                else:
                    current_quiz_q = stripped
                current_quiz_opts = []
            elif stripped.startswith("- ["):
                bracket_close = stripped.find("]")
                if bracket_close > 2:
                    opt_text = stripped[bracket_close + 1:].strip()
                    current_quiz_opts.append(opt_text)

        if in_quiz_answers:
            if stripped.startswith("- **Q"):
                # Parse: - **Q1 Answer:** Option 2 — explanation text
                answer_part = stripped.split(":**", 1)
                if len(answer_part) == 2:
                    rest = answer_part[1].strip()
                    # Find quiz index
                    q_num_str = answer_part[0].strip()
                    q_num = 0
                    for ch in q_num_str:
                        if ch.isdigit():
                            q_num = q_num * 10 + int(ch)

                    dash_pos = rest.find("—")
                    opt_str = rest
                    explanation = ""
                    if dash_pos > 0:
                        opt_str = rest[:dash_pos].strip()
                        explanation = rest[dash_pos + 1:].strip()

                    # Extract answer index from "Option X"
                    answer_idx = 0
                    opt_str_stripped = opt_str.replace("Option", "").strip()
                    if opt_str_stripped.isdigit():
                        answer_idx = int(opt_str_stripped)

                    # Apply to the matching quiz entry (1-indexed)
                    idx = q_num - 1
                    if 0 <= idx < len(revision["quiz"]):
                        revision["quiz"][idx]["answer_index"] = answer_idx
                        revision["quiz"][idx]["explanation"] = explanation

        if in_interview:
            if stripped.startswith("### Q") and ":" in stripped:
                # Flush previous
                if current_int_q:
                    revision["interview_questions"].append({
                        "q": current_int_q,
                        "a": "\n".join(current_int_a_lines).strip(),
                    })
                    current_int_a_lines = []
                colon_pos = stripped.find(":")
                current_int_q = stripped[colon_pos + 1:].strip()
            elif stripped.startswith("**Answer:**"):
                current_int_a_lines.append(stripped[len("**Answer:**"):].strip())
            elif current_int_q and stripped:
                current_int_a_lines.append(stripped)

    # Flush remaining
    if in_cheat:
        revision["cheat_sheet"] = "\n".join(cheat_lines).strip()
    if current_fc_q:
        revision["flashcards"].append({"q": current_fc_q, "a": current_fc_a})
    if current_quiz_q:
        revision["quiz"].append({
            "question": current_quiz_q,
            "options": current_quiz_opts,
            "answer_index": 0,
            "explanation": "",
        })
    if current_int_q:
        revision["interview_questions"].append({
            "q": current_int_q,
            "a": "\n".join(current_int_a_lines).strip(),
        })

    return revision


# ── Legacy compatibility ─────────────────────────────────────────────────────

def push_db_to_github(db_path: str = "notescript.db") -> tuple[bool, str]:
    """Push local SQLite database to GitHub repository via Contents API (legacy)."""
    token = get_github_token()
    repo = get_github_repo()
    if not token:
        return False, "GITHUB_TOKEN not configured."
    if not repo:
        return False, "GITHUB_REPO not configured."
    if not os.path.exists(db_path):
        return False, f"Local database file {db_path} does not exist."

    try:
        with open(db_path, "rb") as db_file:
            db_bytes = db_file.read()
    except Exception as read_err:
        return False, f"Failed reading database file: {read_err}"

    return _put_file_to_github(
        "notescript.db",
        db_bytes,
        "sync: update notescript.db with new lecture notes [skip ci]",
        token,
        repo,
    )


def pull_db_from_github(target_path: str = "notescript.db") -> tuple[bool, str]:
    """Download the latest database from GitHub if local file is missing or empty."""
    raw_bytes = _download_github_file("notescript.db")
    if raw_bytes is None:
        return False, "Failed to download notescript.db from GitHub."
    try:
        with open(target_path, "wb") as out_file:
            out_file.write(raw_bytes)
        return True, "Database successfully restored from GitHub."
    except Exception as write_err:
        return False, f"Failed writing database file: {write_err}"
