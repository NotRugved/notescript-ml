"""Streamlit user interface for NoteScript ML."""

import os
from dotenv import load_dotenv
import streamlit as st

from database import list_videos
from exports import build_code_py, build_main_notes_md, build_revision_md
from extractor import (
    find_day_candidates,
    get_video_id,
    list_day_folders,
    list_notebooks,
    list_playlist,
    parse_time,
    suggest_folders,
)
from pipeline import load_cached_result, run_pipeline

load_dotenv()

st.set_page_config(
    page_title="NoteScript ML",
    page_icon="🎓",
    layout="wide",
)

# Load Miles Morales theme CSS
if os.path.exists("ui/theme.css"):
    with open("ui/theme.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Show spider-web intro animation only once per session
if not st.session_state.get("intro_shown", False):
    if os.path.exists("ui/intro.html"):
        with open("ui/intro.html", "r", encoding="utf-8") as f:
            st.markdown(f.read(), unsafe_allow_html=True)
    st.session_state["intro_shown"] = True

# App header block
st.markdown("""
<div class="ns-header">
  <span class="ns-title">NOTESCRIPT ML</span>
  <span class="ns-tagline">CampusX 100 Days of ML, notes that actually stick.</span>
</div>
""", unsafe_allow_html=True)


# Initialize session state keys
if "pipeline_result" not in st.session_state:
    st.session_state["pipeline_result"] = None
if "quiz_answers" not in st.session_state:
    st.session_state["quiz_answers"] = {}
if "quiz_checked" not in st.session_state:
    st.session_state["quiz_checked"] = {}


# ==============================================================================
# SIDEBAR
# ==============================================================================
with st.sidebar:
    st.header("⚙️ Configuration")

    segment_minutes = st.selectbox(
        "Segment Length (minutes)",
        options=[5, 10, 15],
        index=1,
        help="Break video into chunks of this length.",
    )

    high_quality = st.toggle("Video Quality: High", value=False)
    if high_quality:
        resolution = "HIGH"
        st.warning("⚠️ High resolution reads on-screen code better but uses significantly more quota!")
    else:
        resolution = "LOW"

    st.divider()
    st.header("📚 My Library")
    saved_videos = list_videos()
    if len(saved_videos) == 0:
        st.info("No saved notes yet.")
    else:
        for v in saved_videos:
            v_id = v.get("video_id", "")
            v_title = v.get("title", v_id)
            btn_label = f"📖 {v_title[:32]}..." if len(v_title) > 35 else f"📖 {v_title}"
            if st.button(btn_label, key=f"lib_{v_id}"):
                cached = load_cached_result(v_id)
                if cached is not None:
                    st.session_state["pipeline_result"] = cached
                    st.session_state["quiz_answers"] = {}
                    st.session_state["quiz_checked"] = {}
                    st.rerun()


# ==============================================================================
# MAIN INPUT SECTION
# ==============================================================================
input_mode = st.radio("Select Input Mode", options=["Video link", "Day number"], horizontal=True)

target_video_url = ""
target_folder = ""
target_notebook = ""

if input_mode == "Video link":
    url_input = st.text_input("YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")
    if url_input:
        extracted_id = get_video_id(url_input)
        if not extracted_id:
            st.error("Invalid YouTube URL. Please enter a valid watch, youtu.be, embed, or shorts link.")
        else:
            target_video_url = f"https://www.youtube.com/watch?v={extracted_id}"
else:
    col_day, col_plist = st.columns([1, 3])
    with col_day:
        day_num = st.number_input("Day Number", min_value=1, max_value=100, value=1)
    with col_plist:
        default_playlist = os.getenv("PLAYLIST_URL", "")
        playlist_url = st.text_input("Playlist URL", value=default_playlist)

    if st.button("Find videos"):
        if not playlist_url:
            st.error("Please provide a valid playlist URL.")
        else:
            with st.spinner("Fetching playlist videos..."):
                playlist_items = list_playlist(playlist_url)
                candidates = find_day_candidates(playlist_items, day_num)
                st.session_state["playlist_candidates"] = candidates

    candidates = st.session_state.get("playlist_candidates", [])
    if len(candidates) > 0:
        candidate_options = []
        for c in candidates:
            candidate_options.append(f"{c['title']} (Position: {c['position']})")

        chosen_label = st.selectbox("Select Matching Video", options=candidate_options)
        # Find selected item
        selected_cand = None
        for c in candidates:
            if f"{c['title']} (Position: {c['position']})" == chosen_label:
                selected_cand = c
                break

        if selected_cand:
            if selected_cand.get("position_guess", False):
                st.warning("⚠️ No title matched the exact day number. This candidate was guessed based on playlist position. Please verify.")
            target_video_url = f"https://www.youtube.com/watch?v={selected_cand['video_id']}"
            st.success(f"Selected: **{selected_cand['title']}**")


# ==============================================================================
# GITHUB NOTEBOOK MAPPING SECTION
# ==============================================================================
st.subheader("📓 Official Repo Notebook (Optional)")

all_folders = ["None"]
try:
    repo_folders = list_day_folders()
    for f in repo_folders:
        all_folders.append(f)
except Exception:
    repo_folders = []

preselected_idx = 0
if input_mode == "Day number":
    suggested = suggest_folders(day_num, repo_folders)
    if len(suggested) == 1:
        match_folder = suggested[0]
        if match_folder in all_folders:
            preselected_idx = all_folders.index(match_folder)

selected_folder_choice = st.selectbox(
    "Day Folder in 100-Days Repo",
    options=all_folders,
    index=preselected_idx,
    help="When 'None' is selected, code seen on screen will be labelled 'on-screen' or 'reconstructed'.",
)

if selected_folder_choice != "None":
    target_folder = selected_folder_choice
    available_notebooks = list_notebooks(target_folder)
    if len(available_notebooks) > 0:
        target_notebook = st.selectbox("Select Notebook File", options=available_notebooks)
    else:
        st.info("No .ipynb notebooks found in this folder.")


# ==============================================================================
# RUN ACTION & PROGRESS
# ==============================================================================
generate_clicked = st.button("🚀 Generate Notes", type="primary", disabled=(not target_video_url))

if generate_clicked:
    st.session_state["quiz_answers"] = {}
    st.session_state["quiz_checked"] = {}

    status_container = st.status("Initializing note generation...", expanded=True)
    progress_bar = st.progress(0.0)

    def ui_progress(message: str, fraction: float) -> None:
        status_container.update(label=f"**{message}** ({int(fraction * 100)}%)")
        progress_bar.progress(fraction)

    try:
        pipeline_output = run_pipeline(
            video_url=target_video_url,
            folder=target_folder,
            notebook_file=target_notebook,
            segment_minutes=segment_minutes,
            resolution=resolution,
            progress=ui_progress,
        )
        st.session_state["pipeline_result"] = pipeline_output
        status_container.update(label="✅ Notes successfully generated!", state="complete", expanded=False)
    except Exception as run_err:
        status_container.update(label=f"❌ Error during generation: {run_err}", state="error")
        st.error(f"Pipeline execution failed: {run_err}")


# ==============================================================================
# DISPLAY RESULTS
# ==============================================================================
result = st.session_state.get("pipeline_result")

if result:
    st.divider()

    # Check for partial status
    if result.get("partial", False):
        done_seg = result.get("stopped_at_index", 0)
        total_seg = result.get("total_segments", 1)
        st.warning(f"⚠️ **Partial Run:** Finished {done_seg} of {total_seg} segments. Run again later to resume; finished segments are saved.")

    video_info = result.get("video_info", {})
    st.header(video_info.get("title", "Lecture Notes"))

    summary_text = result.get("revision", {}).get("one_line_summary", "")
    if summary_text:
        st.info(f"💡 **Takeaway:** {summary_text}")

    # Export Buttons
    col_dl1, col_dl2, col_dl3 = st.columns(3)
    notes_str = build_main_notes_md(result)
    rev_str = build_revision_md(result)
    code_str = build_code_py(result)

    safe_title = "".join(c for c in video_info.get("title", "notes") if c.isalnum() or c in (" ", "-", "_")).strip()
    safe_title = safe_title.replace(" ", "_")

    with col_dl1:
        st.download_button(
            "📥 Download Notes (.md)",
            data=notes_str,
            file_name=f"{safe_title}_notes.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with col_dl2:
        st.download_button(
            "📥 Download Revision Pack (.md)",
            data=rev_str,
            file_name=f"{safe_title}_revision.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with col_dl3:
        st.download_button(
            "📥 Download Code (.py)",
            data=code_str,
            file_name=f"{safe_title}_code.py",
            mime="text/x-python",
            use_container_width=True,
        )

    st.markdown("---")

    # Section selection & Layout
    all_sections = ["Theory", "Intuition", "Code", "Analogies", "Common Mistakes", "Formulas & Key Terms", "Revision"]
    selected_sections = st.multiselect("Display Sections", options=all_sections, default=all_sections)

    layout_mode = st.radio("Layout Mode", options=["Tabs", "Split view"], horizontal=True)

    def render_section(section_name: str) -> None:
        merged = result.get("merged_notes", {})
        v_id = video_info.get("video_id", "")

        if section_name == "Theory":
            st.subheader("📖 Theory")
            theory_items = merged.get("theory_sections", [])
            if len(theory_items) == 0:
                st.write("No theory sections recorded.")
            for t in theory_items:
                ts = t.get("timestamp", "00:00")
                sec = parse_time(ts) or 0
                yt_link = f"https://youtu.be/{v_id}?t={sec}"
                st.markdown(f"### {t.get('heading', 'Concept')} [⏱️ {ts}]({yt_link})")
                st.markdown(t.get("content", ""))

        elif section_name == "Intuition":
            st.subheader("💡 Intuition")
            intuition_items = merged.get("intuition", [])
            if len(intuition_items) == 0:
                st.write("No intuition notes recorded.")
            for item in intuition_items:
                ts = item.get("timestamp", "00:00")
                sec = parse_time(ts) or 0
                yt_link = f"https://youtu.be/{v_id}?t={sec}"
                st.markdown(f"- **[⏱️ {ts}]({yt_link})** {item.get('text', '')}")

        elif section_name == "Code":
            st.subheader("💻 Code")
            code_items = merged.get("code_blocks", [])
            if len(code_items) == 0:
                st.write("No code blocks recorded.")
            for c in code_items:
                ts = c.get("timestamp", "00:00")
                sec = parse_time(ts) or 0
                yt_link = f"https://youtu.be/{v_id}?t={sec}"
                label = c.get("label", "on-screen")
                st.markdown(f"**{c.get('title', 'Snippet')}** `[{label}]` — [⏱️ {ts}]({yt_link})")
                if c.get("explanation"):
                    st.caption(c.get("explanation"))
                st.code(c.get("code", ""), language="python")

        elif section_name == "Analogies":
            st.subheader("🎭 Analogies")
            analogy_items = merged.get("analogies", [])
            if len(analogy_items) == 0:
                st.write("No analogies recorded.")
            for a in analogy_items:
                ts = a.get("timestamp", "00:00")
                sec = parse_time(ts) or 0
                yt_link = f"https://youtu.be/{v_id}?t={sec}"
                st.markdown(f"- **[⏱️ {ts}]({yt_link}) Analogy:** {a.get('analogy', '')}")
                st.caption(f"Explains: {a.get('explains', '')}")

        elif section_name == "Common Mistakes":
            st.subheader("⚠️ Common Mistakes")
            mistake_items = merged.get("common_mistakes", [])
            if len(mistake_items) == 0:
                st.write("No common mistakes recorded.")
            for m in mistake_items:
                source = m.get("source", "teacher")
                st.markdown(f"**Mistake (`{source}`):** {m.get('mistake', '')}")
                if m.get("why"):
                    st.markdown(f"- *Why it happens:* {m.get('why')}")
                if m.get("fix"):
                    st.markdown(f"- *Fix:* {m.get('fix')}")
                st.divider()

        elif section_name == "Formulas & Key Terms":
            st.subheader("📐 Formulas & Key Terms")
            f_col, k_col = st.columns(2)
            with f_col:
                st.markdown("#### Formulas")
                for f in merged.get("formulas", []):
                    st.markdown(f"- **{f.get('name', '')}**: `{f.get('formula', '')}`\n  *{f.get('meaning', '')}*")
            with k_col:
                st.markdown("#### Key Terms")
                for k in merged.get("key_terms", []):
                    st.markdown(f"- **{k.get('term', '')}**: {k.get('meaning', '')}")

        elif section_name == "Revision":
            st.subheader("🎯 Revision Pack")
            rev = result.get("revision", {})

            st.markdown("### Cheat Sheet")
            st.markdown(rev.get("cheat_sheet", "*No cheat sheet*"))

            st.markdown("### Flashcards")
            flashcards = rev.get("flashcards", [])
            for idx, fc in enumerate(flashcards, start=1):
                with st.expander(f"🃏 Card {idx}: {fc.get('q', 'Question')}"):
                    st.write(fc.get("a", "Answer"))

            st.markdown("### Interactive Quiz")
            quiz = rev.get("quiz", [])
            for q_idx, q_item in enumerate(quiz):
                q_text = q_item.get("question", "")
                opts = q_item.get("options", [])
                correct_idx = q_item.get("answer_index", 0)
                explanation = q_item.get("explanation", "")

                st.markdown(f"**Q{q_idx + 1}: {q_text}**")
                choice = st.radio(
                    "Options",
                    options=range(len(opts)),
                    format_func=lambda i: opts[i] if i < len(opts) else "",
                    key=f"quiz_opt_{q_idx}",
                    label_visibility="collapsed",
                )

                if st.button(f"Check Answer {q_idx + 1}", key=f"btn_quiz_{q_idx}"):
                    st.session_state["quiz_checked"][q_idx] = True

                if st.session_state.get("quiz_checked", {}).get(q_idx):
                    if choice == correct_idx:
                        st.success(f"✅ Correct! Option {choice}: {explanation}")
                    else:
                        st.error(f"❌ Incorrect. Correct was Option {correct_idx}. Explanation: {explanation}")

            st.markdown("### Interview Questions")
            for i_idx, iq in enumerate(rev.get("interview_questions", []), start=1):
                with st.expander(f"💼 Question {i_idx}: {iq.get('q', '')}"):
                    st.write(iq.get("a", ""))

    if len(selected_sections) > 0:
        if layout_mode == "Tabs":
            tabs = st.tabs(selected_sections)
            for tab, section in zip(tabs, selected_sections):
                with tab:
                    render_section(section)
        else:
            # Split view
            if len(selected_sections) > 3:
                st.warning("⚠️ Split view supports up to 3 sections side-by-side. Showing the first 3.")
                active_cols = selected_sections[:3]
            else:
                active_cols = selected_sections

            cols = st.columns(len(active_cols))
            for col, sec in zip(cols, active_cols):
                with col:
                    render_section(sec)
