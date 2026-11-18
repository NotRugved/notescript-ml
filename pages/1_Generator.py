"""Generator Page."""
import streamlit as st
import os
from ui_components import apply_theme, show_sidebar_common
from yt_extractor import (
    find_day_candidates,
    get_video_id,
    list_day_folders,
    list_notebooks,
    list_playlist,
    suggest_folders,
)
from pipeline import run_pipeline

st.set_page_config(page_title="Generator - NoteScript ML", page_icon="🚀", layout="wide")
apply_theme()
show_sidebar_common()

st.header("🚀 Generate New Notes")
col_input, col_config = st.columns([4, 1])

with col_config:
    with st.popover("⚙️ Config"):
        segment_minutes = st.selectbox("Segment Length (m)", options=[5, 10, 15], index=1)
        high_quality = st.toggle("High Quality", value=False)
        resolution = "HIGH" if high_quality else "LOW"
        if high_quality:
            st.warning("⚠️ High resolution uses more quota!")

with col_input:
    input_mode = st.radio("Select Input Mode", options=["Video link", "Day number"], horizontal=True)

target_video_url = ""
target_folder = ""
target_notebook = ""

if input_mode == "Video link":
    url_input = st.text_input("YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")
    if url_input:
        extracted_id = get_video_id(url_input)
        if not extracted_id:
            st.error("Invalid YouTube URL.")
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
            with st.spinner("Fetching..."):
                playlist_items = list_playlist(playlist_url)
                st.session_state["playlist_candidates"] = find_day_candidates(playlist_items, day_num)

    candidates = st.session_state.get("playlist_candidates", [])
    if candidates:
        labels = [f"{c['title']} (Pos: {c['position']})" for c in candidates]
        chosen = st.selectbox("Select Matching Video", options=labels)
        selected = next((c for c in candidates if f"{c['title']} (Pos: {c['position']})" == chosen), None)
        if selected:
            target_video_url = f"https://www.youtube.com/watch?v={selected['video_id']}"
            st.success(f"Selected: **{selected['title']}**")

if st.button("🚀 Generate Notes", type="primary", disabled=(not target_video_url)):
    status_container = st.status("Initializing...", expanded=True)
    progress_bar = st.progress(0.0)
    try:
        pipeline_output = run_pipeline(target_video_url, folder=target_folder, notebook_file=target_notebook, segment_minutes=segment_minutes, resolution=resolution, progress=lambda m, f: (status_container.update(label=f"**{m}** ({int(f*100)}%)"), progress_bar.progress(f)))
        st.session_state["pipeline_result"] = pipeline_output
        status_container.update(label="✅ Success!", state="complete")
        st.switch_page("pages/3_Notes.py")
    except Exception as e:
        status_container.update(label=f"❌ Error: {e}", state="error")
