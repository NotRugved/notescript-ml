"""Generator Page — Single Lecture and Multi-Day Batch Queue."""
import os
import streamlit as st
from ui_components import apply_theme, render_admin_bar, render_admin_gate, show_sidebar_common
from yt_extractor import (
    find_day_candidates,
    get_video_id,
    list_day_folders,
    list_notebooks,
    list_playlist,
    suggest_folders,
)
from pipeline import load_cached_result, run_pipeline
from database import (
    add_to_queue,
    clear_queue,
    delete_queue_item,
    get_queue,
    get_queue_summary,
    update_queue_status,
)
from ai_processor import check_api_status
from github_sync import push_notes_to_github, push_all_new_notes

st.set_page_config(page_title="Generator - NoteScript ML", page_icon="🚀", layout="wide")
apply_theme()
show_sidebar_common()

# Enforce Admin Gatekeeper
if not render_admin_gate():
    st.stop()

render_admin_bar()
st.header("🚀 Note Generator")

# Global Config Popover in the header row
col_title, col_cfg = st.columns([4, 1])
with col_cfg:
    with st.popover("⚙️ Config"):
        segment_minutes = st.selectbox("Segment Length (m)", options=[5, 10, 15], index=1)
        high_quality = st.toggle("High Quality", value=False)
        resolution = "HIGH" if high_quality else "LOW"
        if high_quality:
            st.warning("⚠️ High resolution uses more quota!")

tab_single, tab_batch = st.tabs(["⚡ Single Lecture", "📋 Batch Queue (Multi-Day)"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: SINGLE LECTURE
# ══════════════════════════════════════════════════════════════════════════════
with tab_single:
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
            playlist_url = st.text_input("Playlist URL", value=default_playlist, key="single_playlist_url")
        if st.button("Find video for Day"):
            if not playlist_url:
                st.error("Please provide a valid playlist URL.")
            else:
                with st.spinner("Fetching playlist..."):
                    playlist_items = list_playlist(playlist_url)
                    st.session_state["playlist_candidates"] = find_day_candidates(playlist_items, day_num)

        candidates = st.session_state.get("playlist_candidates", [])
        if len(candidates) > 0:
            labels = []
            for c in candidates:
                labels.append(f"{c['title']} (Pos: {c['position']})")
            chosen = st.selectbox("Select Matching Video", options=labels)
            selected = None
            for c in candidates:
                if f"{c['title']} (Pos: {c['position']})" == chosen:
                    selected = c
                    break
            if selected is not None:
                target_video_url = f"https://www.youtube.com/watch?v={selected['video_id']}"
                st.success(f"Selected: **{selected['title']}**")

    if st.button("🚀 Generate Notes", type="primary", disabled=(not target_video_url), key="btn_gen_single"):
        status_box = st.status("Initializing generation...", expanded=True)
        bar = st.progress(0.0)

        def single_progress_callback(msg: str, frac: float) -> None:
            """Update status container and progress bar."""
            status_box.update(label=f"**{msg}** ({int(frac * 100)}%)")
            bar.progress(frac)

        try:
            pipeline_output = run_pipeline(
                target_video_url,
                folder=target_folder,
                notebook_file=target_notebook,
                segment_minutes=segment_minutes,
                resolution=resolution,
                progress=single_progress_callback,
            )
            st.session_state["pipeline_result"] = pipeline_output
            if pipeline_output.get("partial"):
                status_box.update(label="⏸️ Partial save: daily quota hit. Resume tomorrow!", state="complete")
            else:
                status_box.update(label="✅ Success!", state="complete")
            # Push generated notes files to GitHub for sharing
            from exports import build_main_notes_md, build_revision_md, build_code_py
            import time as _time
            _vid_id = pipeline_output["video_info"]["video_id"]
            _meta = {
                "video_id": _vid_id,
                "title": pipeline_output["video_info"].get("title", ""),
                "day_label": pipeline_output["video_info"].get("day_label", ""),
                "duration_seconds": pipeline_output["video_info"].get("duration_seconds", 0),
                "video_url": pipeline_output["video_info"].get("video_url", ""),
                "pushed_at": _time.strftime("%Y-%m-%d %H:%M:%S", _time.localtime()),
            }
            push_notes_to_github(
                _vid_id,
                build_main_notes_md(pipeline_output),
                build_revision_md(pipeline_output),
                build_code_py(pipeline_output),
                _meta,
            )
            st.switch_page("pages/3_Notes.py")
        except Exception as exc:
            status_box.update(label=f"❌ Error: {exc}", state="error")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: BATCH QUEUE (MULTI-DAY)
# ══════════════════════════════════════════════════════════════════════════════
with tab_batch:
    st.markdown("### 📋 Multi-Day Learning Queue")
    st.caption(
        "Queue 10 days of lectures at once. If Gemini hits daily quota, your progress "
        "is saved automatically. Next time you open NoteScript ML, the system checks the API "
        "and resumes right where you left off!"
    )

    # 1. API Status Banner
    api_check = check_api_status()
    api_ok = api_check.get("available", False)
    api_msg = api_check.get("message", "")

    status_cols = st.columns([2, 1, 1])
    with status_cols[0]:
        if api_ok:
            st.success(f"🟢 **API Status:** {api_msg}")
        else:
            st.warning(f"🟡 **API Status:** {api_msg}")
    with status_cols[1]:
        if st.button("🔄 Check API Status", key="btn_check_api", use_container_width=True):
            st.rerun()
    with status_cols[2]:
        if st.button("☁️ Sync to GitHub", key="btn_manual_sync_gh", use_container_width=True):
            with st.spinner("Syncing generated notes to GitHub..."):
                pushed_cnt, total_cnt, sync_errs = push_all_new_notes()
                if pushed_cnt > 0:
                    st.success(f"✅ Successfully synced {pushed_cnt} lecture(s) to GitHub generated_notes/!")
                elif total_cnt == 0:
                    st.info("ℹ️ All lecture notes are already synced on GitHub!")
                else:
                    err_summary = "; ".join(sync_errs) if sync_errs else "Unknown error"
                    st.error(f"❌ Sync failed: {err_summary}")

    st.divider()

    # 2. Queue Creation Form
    st.markdown("#### ➕ Add Days to Queue")
    bq_col_plist, bq_col_start, bq_col_end = st.columns([3, 1, 1])
    with bq_col_plist:
        default_plist = os.getenv("PLAYLIST_URL", "")
        batch_playlist = st.text_input("CampusX Playlist URL", value=default_plist, key="batch_playlist_url")
    with bq_col_start:
        start_day = st.number_input("Start Day", min_value=1, max_value=100, value=1, step=1)
    with bq_col_end:
        end_day = st.number_input("End Day", min_value=1, max_value=100, value=10, step=1)

    if st.button(f"📥 Queue Days {start_day} to {end_day}", key="btn_queue_days"):
        if not batch_playlist:
            st.error("Please provide a valid playlist URL.")
        elif start_day > end_day:
            st.error("Start Day cannot be greater than End Day.")
        else:
            with st.spinner(f"Finding videos for Days {start_day} to {end_day}..."):
                playlist_items = list_playlist(batch_playlist)
                existing_queue = get_queue()
                existing_days = set()
                for item in existing_queue:
                    existing_days.add(item["day_num"])

                added_count = 0
                day_cursor = start_day
                while day_cursor <= end_day:
                    if day_cursor not in existing_days:
                        candidates = find_day_candidates(playlist_items, day_cursor)
                        if len(candidates) > 0:
                            best_video = candidates[0]
                            vid_url = f"https://www.youtube.com/watch?v={best_video['video_id']}"
                            add_to_queue(day_cursor, vid_url, best_video["title"])
                            added_count += 1
                    day_cursor += 1

                st.success(f"Successfully added {added_count} days to the queue!")
                st.rerun()

    st.divider()

    # 3. Queue Summary & Controls
    summary = get_queue_summary()
    queue_items = get_queue()

    st.markdown("#### 📊 Queue Status")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Queued", summary["total"])
    m2.metric("⏳ Pending", summary["pending"])
    m3.metric("🔄 In Progress", summary["in_progress"])
    m4.metric("⏸️ Paused (Quota)", summary["paused_quota"])
    m5.metric("✅ Completed", summary["completed"])

    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2, 1, 1])
    with ctrl_col1:
        can_run = (summary["pending"] > 0 or summary["paused_quota"] > 0)
        run_label = "⚡ Resume Queue" if summary["paused_quota"] > 0 else "⚡ Process Queue"
        start_queue_btn = st.button(
            run_label,
            type="primary",
            disabled=(not can_run),
            key="btn_start_queue",
        )
    with ctrl_col2:
        if st.button("🧹 Clear Completed", key="btn_clear_comp"):
            clear_queue(only_completed=True)
            st.rerun()
    with ctrl_col3:
        if st.button("🗑️ Clear Entire Queue", key="btn_clear_all"):
            clear_queue(only_completed=False)
            st.rerun()

    # 4. Queue Processor Loop
    if start_queue_btn:
        st.markdown("---")
        batch_status = st.status("Starting batch queue processing...", expanded=True)
        batch_bar = st.progress(0.0)

        items_to_process = []
        for item in queue_items:
            if item["status"] in ("pending", "paused_quota"):
                items_to_process.append(item)

        total_in_batch = len(items_to_process)
        processed_count = 0
        quota_stopped = False

        for q_item in items_to_process:
            q_id = q_item["id"]
            d_num = q_item["day_num"]
            v_url = q_item["video_url"]
            t_title = q_item["title"]

            update_queue_status(q_id, "in_progress")
            batch_status.update(label=f"Processing Day {d_num}: {t_title[:35]}...")

            def batch_progress_cb(msg: str, frac: float) -> None:
                """Progress callback for batch item."""
                overall_frac = (processed_count + frac) / total_in_batch
                batch_status.update(label=f"Day {d_num}: **{msg}** ({int(frac * 100)}%)")
                batch_bar.progress(overall_frac)

            try:
                pipeline_output = run_pipeline(
                    v_url,
                    segment_minutes=segment_minutes,
                    resolution=resolution,
                    progress=batch_progress_cb,
                )
                if pipeline_output.get("partial"):
                    # Quota hit during processing
                    quota_stopped = True
                    update_queue_status(
                        q_id,
                        "paused_quota",
                        "Daily API quota exhausted. Partial segments saved. Will resume automatically.",
                    )
                    batch_status.update(
                        label=f"⏸️ Paused at Day {d_num}: Gemini daily quota limit hit. Saved partial notes!",
                        state="error",
                    )
                    break
                else:
                    update_queue_status(q_id, "completed")
                    processed_count += 1
            except Exception as exc:
                exc_str = str(exc)
                if "quota" in exc_str.lower() or "429" in exc_str:
                    quota_stopped = True
                    update_queue_status(
                        q_id,
                        "paused_quota",
                        "Daily quota limit reached. Resumes when API resets.",
                    )
                    batch_status.update(
                        label=f"⏸️ Paused at Day {d_num}: Quota limit reached. Saved progress!",
                        state="error",
                    )
                    break
                else:
                    update_queue_status(q_id, "failed", exc_str)
                    processed_count += 1

        if quota_stopped:
            # Sync notes progress to GitHub
            push_all_new_notes()
            st.warning(
                "⏸️ **Batch queue paused due to Gemini daily quota limit.**\n\n"
                "All completed notes and partial video segments are safely stored in your database. "
                "Next time you open the app (or when the API resets), click **Resume Queue** to continue!"
            )
        else:
            # Sync full batch completion to GitHub
            push_all_new_notes()
            batch_status.update(label="🎉 Batch processing finished!", state="complete")
            st.success("All queued lectures have been successfully processed!")
            st.rerun()

    # 5. List Queue Items
    st.markdown("#### 📋 Queued Lectures")
    if len(queue_items) == 0:
        st.info("Queue is currently empty. Use the form above to add lectures.")
    else:
        for q in queue_items:
            q_id = q["id"]
            day_str = f"Day {q['day_num']}"
            title_str = q["title"]
            status_str = q["status"]

            # Choose badge
            if status_str == "completed":
                badge = "✅ Completed"
            elif status_str == "paused_quota":
                badge = "⏸️ Paused (API Quota)"
            elif status_str == "in_progress":
                badge = "🔄 In Progress"
            elif status_str == "failed":
                badge = "❌ Failed"
            else:
                badge = "⏳ Pending"

            with st.container(border=True):
                c_info, c_badge, c_action = st.columns([4, 2, 2])
                with c_info:
                    st.markdown(f"**{day_str}:** {title_str}")
                    if q.get("error_message"):
                        st.caption(f"ℹ️ {q['error_message']}")
                with c_badge:
                    st.markdown(f"`{badge}`")
                with c_action:
                    sub_c1, sub_c2 = st.columns(2)
                    with sub_c1:
                        if status_str == "completed":
                            vid_id = get_video_id(q["video_url"])
                            if st.button("📖 Notes", key=f"btn_view_{q_id}"):
                                cached_res = load_cached_result(vid_id)
                                if cached_res:
                                    st.session_state["pipeline_result"] = cached_res
                                    st.switch_page("pages/3_Notes.py")
                    with sub_c2:
                        if st.button("🗑️", key=f"btn_del_{q_id}", help="Delete item from queue"):
                            delete_queue_item(q_id)
                            st.rerun()
