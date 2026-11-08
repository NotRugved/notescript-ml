"""Export generators for NoteScript ML."""

from yt_extractor import parse_time

def _create_youtube_timestamp_link(video_id: str, timestamp_str: str) -> str:
    """Convert timestamp text to a clickable markdown youtu.be link."""
    seconds = parse_time(timestamp_str)
    if seconds is None:
        seconds = 0
    return f"[{timestamp_str}](https://youtu.be/{video_id}?t={seconds})"


def build_main_notes_md(result: dict) -> str:
    """Generate comprehensive markdown study notes string from pipeline result."""
    video_info = result.get("video_info", {})
    video_id = video_info.get("video_id", "")
    title = video_info.get("title", "Lecture Notes")
    video_url = video_info.get("video_url") or f"https://www.youtube.com/watch?v={video_id}"

    revision = result.get("revision", {})
    summary = revision.get("one_line_summary", "").strip()

    merged = result.get("merged_notes", {})

    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"**Video Link:** [{video_url}]({video_url})")
    lines.append("")
    if summary:
        lines.append(f"**Summary:** {summary}")
        lines.append("")

    # 1. Theory
    lines.append("## Theory")
    lines.append("")
    theory_list = merged.get("theory_sections", [])
    if len(theory_list) == 0:
        lines.append("*No theory sections identified.*")
        lines.append("")
    else:
        for item in theory_list:
            heading = item.get("heading", "Concept")
            ts = item.get("timestamp", "00:00")
            ts_link = _create_youtube_timestamp_link(video_id, ts)
            content = item.get("content", "").strip()
            lines.append(f"### {heading} ({ts_link})")
            lines.append("")
            lines.append(content)
            lines.append("")

    # 2. Intuition
    lines.append("## Intuition")
    lines.append("")
    intuition_list = merged.get("intuition", [])
    if len(intuition_list) == 0:
        lines.append("*No intuition notes identified.*")
        lines.append("")
    else:
        for item in intuition_list:
            ts = item.get("timestamp", "00:00")
            ts_link = _create_youtube_timestamp_link(video_id, ts)
            text = item.get("text", "").strip()
            lines.append(f"- ({ts_link}) {text}")
        lines.append("")

    # 3. Code
    lines.append("## Code")
    lines.append("")
    code_list = merged.get("code_blocks", [])
    if len(code_list) == 0:
        lines.append("*No code blocks identified.*")
        lines.append("")
    else:
        for item in code_list:
            code_title = item.get("title", "Code Snippet")
            label = item.get("label", "on-screen")
            ts = item.get("timestamp", "00:00")
            ts_link = _create_youtube_timestamp_link(video_id, ts)
            explanation = item.get("explanation", "").strip()
            code_body = item.get("code", "").strip()

            lines.append(f"### {code_title} [{label}] ({ts_link})")
            if explanation:
                lines.append(explanation)
                lines.append("")
            lines.append("```python")
            lines.append(code_body)
            lines.append("```")
            lines.append("")

    # 4. Analogies
    lines.append("## Analogies")
    lines.append("")
    analogy_list = merged.get("analogies", [])
    if len(analogy_list) == 0:
        lines.append("*No analogies identified.*")
        lines.append("")
    else:
        for item in analogy_list:
            ts = item.get("timestamp", "00:00")
            ts_link = _create_youtube_timestamp_link(video_id, ts)
            analogy = item.get("analogy", "").strip()
            explains = item.get("explains", "").strip()
            lines.append(f"- ({ts_link}) **Analogy:** {analogy} — *Explains:* {explains}")
        lines.append("")

    # 5. Common Mistakes
    lines.append("## Common Mistakes")
    lines.append("")
    mistake_list = merged.get("common_mistakes", [])
    if len(mistake_list) == 0:
        lines.append("*No common mistakes identified.*")
        lines.append("")
    else:
        for item in mistake_list:
            mistake = item.get("mistake", "").strip()
            why = item.get("why", "").strip()
            fix = item.get("fix", "").strip()
            source = item.get("source", "teacher")
            ts = item.get("timestamp")
            ts_part = ""
            if ts:
                ts_link = _create_youtube_timestamp_link(video_id, ts)
                ts_part = f" ({ts_link})"

            lines.append(f"- **Mistake [{source}]:** {mistake}{ts_part}")
            if why:
                lines.append(f"  - *Why:* {why}")
            if fix:
                lines.append(f"  - *Fix:* {fix}")
        lines.append("")

    # 6. Formulas & Key Terms
    lines.append("## Formulas & Key Terms")
    lines.append("")
    formula_list = merged.get("formulas", [])
    term_list = merged.get("key_terms", [])

    lines.append("### Formulas")
    if len(formula_list) == 0:
        lines.append("*No formulas recorded.*")
    else:
        for item in formula_list:
            name = item.get("name", "").strip()
            formula = item.get("formula", "").strip()
            meaning = item.get("meaning", "").strip()
            lines.append(f"- **{name}:** `{formula}` — {meaning}")
    lines.append("")

    lines.append("### Key Terms")
    if len(term_list) == 0:
        lines.append("*No key terms recorded.*")
    else:
        for item in term_list:
            term = item.get("term", "").strip()
            meaning = item.get("meaning", "").strip()
            lines.append(f"- **{term}:** {meaning}")
    lines.append("")

    return "\n".join(lines)


def build_revision_md(result: dict) -> str:
    """Generate revision pack markdown string including flashcards, quiz, and interview questions."""
    video_info = result.get("video_info", {})
    title = video_info.get("title", "Lecture")
    revision = result.get("revision", {})

    lines = []
    lines.append(f"# Revision Pack: {title}")
    lines.append("")

    summary = revision.get("one_line_summary", "").strip()
    if summary:
        lines.append(f"**One-Line Summary:** {summary}")
        lines.append("")

    # Cheat sheet
    lines.append("## Cheat Sheet")
    lines.append("")
    cheat_sheet = revision.get("cheat_sheet", "").strip()
    if cheat_sheet:
        lines.append(cheat_sheet)
    else:
        lines.append("*No cheat sheet available.*")
    lines.append("")

    # Flashcards
    lines.append("## Flashcards")
    lines.append("")
    flashcards = revision.get("flashcards", [])
    if len(flashcards) == 0:
        lines.append("*No flashcards generated.*")
    else:
        for idx, card in enumerate(flashcards, start=1):
            q = card.get("q", "").strip()
            a = card.get("a", "").strip()
            lines.append(f"### Card {idx}")
            lines.append(f"**Q:** {q}")
            lines.append("")
            lines.append(f"**A:** {a}")
            lines.append("")

    # Quiz
    lines.append("## Quiz")
    lines.append("")
    quiz = revision.get("quiz", [])
    if len(quiz) == 0:
        lines.append("*No quiz questions generated.*")
    else:
        for idx, q_item in enumerate(quiz, start=1):
            question = q_item.get("question", "").strip()
            options = q_item.get("options", [])
            lines.append(f"#### Question {idx}: {question}")
            for opt_idx, opt in enumerate(options):
                lines.append(f"- [{opt_idx}] {opt}")
            lines.append("")

        lines.append("### Quiz Answers & Explanations")
        lines.append("")
        for idx, q_item in enumerate(quiz, start=1):
            ans_idx = q_item.get("answer_index", 0)
            explanation = q_item.get("explanation", "").strip()
            lines.append(f"- **Q{idx} Answer:** Option {ans_idx} — {explanation}")
        lines.append("")

    # Interview Questions
    lines.append("## Interview Questions")
    lines.append("")
    interviews = revision.get("interview_questions", [])
    if len(interviews) == 0:
        lines.append("*No interview questions generated.*")
    else:
        for idx, item in enumerate(interviews, start=1):
            q = item.get("q", "").strip()
            a = item.get("a", "").strip()
            lines.append(f"### Q{idx}: {q}")
            lines.append("")
            lines.append(f"**Answer:** {a}")
            lines.append("")

    return "\n".join(lines)


def build_code_py(result: dict) -> str:
    """Extract and combine all code blocks in order into a single executable .py file."""
    video_info = result.get("video_info", {})
    title = video_info.get("title", "Lecture Code")
    merged = result.get("merged_notes", {})
    code_blocks = merged.get("code_blocks", [])

    lines = []
    lines.append(f'"""Code extracted from: {title}"""')
    lines.append("")

    if len(code_blocks) == 0:
        lines.append("# No code blocks recorded for this video.")
        return "\n".join(lines)

    for idx, block in enumerate(code_blocks, start=1):
        block_title = block.get("title", f"Snippet {idx}")
        label = block.get("label", "on-screen")
        ts = block.get("timestamp", "00:00")
        code = block.get("code", "").strip()

        lines.append("#" + "=" * 70)
        lines.append(f"# Block {idx}: {block_title} | Label: {label} | Timestamp: {ts}")
        if label == "reconstructed":
            lines.append("# VERIFY: Reconstructed from verbal description only")
        lines.append("#" + "=" * 70)
        lines.append(code)
        lines.append("")
        lines.append("")

    return "\n".join(lines)
