"""Pipeline orchestrator for NoteScript ML."""

import json
from typing import Callable, Optional

from ai_processor import QuotaExhaustedError, build_revision, summarize_segment
from database import (
    get_revision,
    get_segment,
    init_db,
    list_videos,
    save_revision,
    save_segment,
    save_video,
)
from yt_extractor import (
    get_notebook_text,
    get_video_id,
    get_video_info,
    plan_segments,
)


def _render_merged_notes_to_text(merged_notes: dict) -> str:
    """Render merged notes into clean structured markdown text for revision prompt."""
    sections = []

    # Theory sections
    theory_items = merged_notes.get("theory_sections", [])
    if len(theory_items) > 0:
        sections.append("# Theory Sections")
        for item in theory_items:
            heading = item.get("heading", "Topic")
            timestamp = item.get("timestamp", "")
            content = item.get("content", "")
            sections.append(f"## {heading} ({timestamp})\n{content}")

    # Intuition
    intuition_items = merged_notes.get("intuition", [])
    if len(intuition_items) > 0:
        sections.append("# Intuition")
        for item in intuition_items:
            timestamp = item.get("timestamp", "")
            text = item.get("text", "")
            sections.append(f"- ({timestamp}) {text}")

    # Code blocks
    code_items = merged_notes.get("code_blocks", [])
    if len(code_items) > 0:
        sections.append("# Code Blocks")
        for item in code_items:
            title = item.get("title", "")
            label = item.get("label", "")
            code = item.get("code", "")
            explanation = item.get("explanation", "")
            sections.append(f"### {title} [{label}]\n{explanation}\n```python\n{code}\n```")

    # Analogies
    analogy_items = merged_notes.get("analogies", [])
    if len(analogy_items) > 0:
        sections.append("# Analogies")
        for item in analogy_items:
            timestamp = item.get("timestamp", "")
            analogy = item.get("analogy", "")
            explains = item.get("explains", "")
            sections.append(f"- ({timestamp}) {analogy} -> Explains: {explains}")

    # Common Mistakes
    mistake_items = merged_notes.get("common_mistakes", [])
    if len(mistake_items) > 0:
        sections.append("# Common Mistakes")
        for item in mistake_items:
            mistake = item.get("mistake", "")
            why = item.get("why", "")
            fix = item.get("fix", "")
            sections.append(f"- Mistake: {mistake}\n  Why: {why}\n  Fix: {fix}")

    # Formulas
    formula_items = merged_notes.get("formulas", [])
    if len(formula_items) > 0:
        sections.append("# Formulas")
        for item in formula_items:
            name = item.get("name", "")
            formula = item.get("formula", "")
            meaning = item.get("meaning", "")
            sections.append(f"- {name}: `{formula}` -> {meaning}")

    # Key Terms
    term_items = merged_notes.get("key_terms", [])
    if len(term_items) > 0:
        sections.append("# Key Terms")
        for item in term_items:
            term = item.get("term", "")
            meaning = item.get("meaning", "")
            sections.append(f"- **{term}**: {meaning}")

    return "\n\n".join(sections)


def _merge_segments(segment_dicts: list[dict]) -> dict:
    """Concatenate and de-duplicate list fields across segment dictionaries in order."""
    merged = {
        "theory_sections": [],
        "intuition": [],
        "code_blocks": [],
        "analogies": [],
        "common_mistakes": [],
        "formulas": [],
        "key_terms": [],
    }

    # Concatenate basic sequential sections
    for seg in segment_dicts:
        for item in seg.get("theory_sections", []):
            merged["theory_sections"].append(item)
        for item in seg.get("intuition", []):
            merged["intuition"].append(item)
        for item in seg.get("code_blocks", []):
            merged["code_blocks"].append(item)
        for item in seg.get("analogies", []):
            merged["analogies"].append(item)
        for item in seg.get("common_mistakes", []):
            merged["common_mistakes"].append(item)

    # De-duplicate formulas by lowercase name
    seen_formulas = []
    for seg in segment_dicts:
        for formula_item in seg.get("formulas", []):
            name = formula_item.get("name", "").strip().lower()
            if name and name not in seen_formulas:
                seen_formulas.append(name)
                merged["formulas"].append(formula_item)

    # De-duplicate key_terms by lowercase term
    seen_terms = []
    for seg in segment_dicts:
        for term_item in seg.get("key_terms", []):
            term = term_item.get("term", "").strip().lower()
            if term and term not in seen_terms:
                seen_terms.append(term)
                merged["key_terms"].append(term_item)

    return merged


def run_pipeline(
    video_url: str,
    folder: str = "",
    notebook_file: str = "",
    segment_minutes: int | float = 10,
    resolution: str = "LOW",
    progress: Optional[Callable[[str, float], None]] = None,
    db_path: str = "notescript.db",
) -> dict:
    """Run full note generation pipeline with caching, quota handling, and progress updates."""
    init_db(db_path)

    def report_progress(msg: str, frac: float) -> None:
        if progress is not None:
            progress(msg, frac)

    # 1. Video information
    report_progress("Reading video info", 0.05)
    video_info = get_video_info(video_url)
    video_id = video_info.get("video_id") or get_video_id(video_url)
    title = video_info.get("title", "")
    duration_seconds = int(video_info.get("duration_seconds", 0) or 0)

    # Save to videos table
    day_label = ""
    title_lower = title.lower()
    day_pos = title_lower.find("day")
    if day_pos != -1:
        # Extract day label from title
        day_label = title[day_pos : day_pos + 10].split("-")[0].split(":")[0].strip()
    save_video(video_id, title, day_label, duration_seconds, db_path)

    # 2. Notebook loading
    notebook_text = ""
    notebook_path = ""
    if folder and notebook_file:
        report_progress("Loading official notebook", 0.10)
        notebook_path = f"{folder}/{notebook_file}"
        notebook_text = get_notebook_text(folder, notebook_file, max_chars=60000, db_path=db_path)

    # 3. Plan segments
    run_key = f"{segment_minutes}_{resolution.upper()}_{notebook_path}"
    planned_segments = plan_segments(duration_seconds, segment_minutes)
    total_segments = len(planned_segments)
    if total_segments == 0:
        total_segments = 1
        planned_segments = [{"index": 0, "start_seconds": 0, "end_seconds": duration_seconds}]

    processed_segment_dicts = []
    partial_flag = False
    stopped_at_index = total_segments

    # 4. Process segments sequentially
    for seg in planned_segments:
        idx = seg["index"]
        start_sec = seg["start_seconds"]
        end_sec = seg["end_seconds"]

        # Calculate progress fraction across segments (0.15 to 0.80)
        frac = 0.15 + (0.65 * (idx / total_segments))
        report_progress(f"Watching segment {idx + 1} of {total_segments}", frac)

        # Check segment cache
        cached_json = get_segment(video_id, idx, run_key, db_path)
        if cached_json is not None:
            try:
                parsed_seg = json.loads(cached_json)
                processed_segment_dicts.append(parsed_seg)
                continue
            except json.JSONDecodeError:
                pass

        # Call Gemini AI processor
        try:
            seg_result = summarize_segment(
                video_url=video_url,
                start_seconds=start_sec,
                end_seconds=end_sec,
                notebook_text=notebook_text,
                resolution=resolution,
                total_duration=duration_seconds,
            )
            # Save immediately on success
            save_segment(video_id, idx, run_key, json.dumps(seg_result), db_path)
            processed_segment_dicts.append(seg_result)
        except QuotaExhaustedError:
            partial_flag = True
            stopped_at_index = idx
            break

    # 5. Merge segments
    report_progress("Merging segments", 0.85)
    merged_notes = _merge_segments(processed_segment_dicts)

    # 6. Build revision pack
    revision_data = {}
    if len(processed_segment_dicts) > 0:
        report_progress("Building revision pack", 0.90)
        cached_revision = get_revision(video_id, run_key, db_path)
        if cached_revision is not None:
            try:
                revision_data = json.loads(cached_revision)
            except json.JSONDecodeError:
                pass

        if not revision_data:
            merged_text = _render_merged_notes_to_text(merged_notes)
            try:
                revision_data = build_revision(merged_text)
                save_revision(video_id, run_key, json.dumps(revision_data), db_path)
            except QuotaExhaustedError:
                partial_flag = True

    report_progress("Done", 1.0)

    return {
        "video_info": {
            "video_id": video_id,
            "title": title,
            "duration_seconds": duration_seconds,
            "day_label": day_label,
            "video_url": video_url,
        },
        "merged_notes": merged_notes,
        "revision": revision_data,
        "notebook_used": notebook_path,
        "partial": partial_flag,
        "stopped_at_index": stopped_at_index,
        "total_segments": total_segments,
        "run_key": run_key,
    }


def load_cached_result(video_id: str, db_path: str = "notescript.db") -> Optional[dict]:
    """Load previously completed note run for a video from the database."""
    videos = list_videos(db_path)
    target_video = None
    for v in videos:
        if v.get("video_id") == video_id:
            target_video = v
            break

    if target_video is None:
        return None

    # Load all saved segments for this video
    # Check segment indices sequentially starting from 0
    segment_dicts = []
    seg_idx = 0
    detected_run_key = ""

    # Probe cached segments
    while True:
        # Check segment using detected or wildcard query
        found = False
        import sqlite3

        conn = sqlite3.connect(db_path)
        try:
            cur = conn.cursor()
            if detected_run_key:
                cur.execute(
                    "SELECT run_key, json_text FROM segments WHERE video_id = ? AND seg_index = ? AND run_key = ?",
                    (video_id, seg_idx, detected_run_key),
                )
            else:
                cur.execute(
                    "SELECT run_key, json_text FROM segments WHERE video_id = ? AND seg_index = ? ORDER BY rowid DESC LIMIT 1",
                    (video_id, seg_idx),
                )
            row = cur.fetchone()
            if row is not None:
                detected_run_key = row[0]
                try:
                    seg_obj = json.loads(row[1])
                    segment_dicts.append(seg_obj)
                    found = True
                except json.JSONDecodeError:
                    pass
        finally:
            conn.close()

        if not found:
            break
        seg_idx = seg_idx + 1

    if len(segment_dicts) == 0:
        return None

    merged_notes = _merge_segments(segment_dicts)

    # Load cached revision
    revision_data = {}
    if detected_run_key:
        rev_json = get_revision(video_id, detected_run_key, db_path)
        if rev_json is not None:
            try:
                revision_data = json.loads(rev_json)
            except json.JSONDecodeError:
                pass

    return {
        "video_info": {
            "video_id": target_video.get("video_id", video_id),
            "title": target_video.get("title", ""),
            "duration_seconds": target_video.get("duration_seconds", 0),
            "day_label": target_video.get("day_label", ""),
            "video_url": f"https://www.youtube.com/watch?v={video_id}",
        },
        "merged_notes": merged_notes,
        "revision": revision_data,
        "notebook_used": detected_run_key,
        "partial": False,
        "stopped_at_index": len(segment_dicts),
        "total_segments": len(segment_dicts),
        "run_key": detected_run_key,
    }
