"""Main Dashboard."""
import streamlit as st
from urllib.parse import quote
from ui_components import apply_theme, show_sidebar_common
from database import init_db, get_queue_summary
from ai_processor import check_api_status

# Ensure all database tables exist on startup
init_db()

st.set_page_config(page_title="NoteScript ML", page_icon="⚙️", layout="wide")
apply_theme()
show_sidebar_common()

# Glitch header
st.markdown("""
<div class="ns-header">
  <div class="ns-title" data-text="NOTESCRIPT ML">NOTESCRIPT ML</div>
  <div class="ns-tagline">CampusX 100 Days of ML — notes that actually stick.</div>
</div>
""", unsafe_allow_html=True)

# Active Batch Queue Banner if items are pending or paused
queue_stats = get_queue_summary()
if queue_stats.get("paused_quota", 0) > 0 or queue_stats.get("pending", 0) > 0:
    api_check = check_api_status()
    api_is_ready = api_check.get("available", False)
    with st.container(border=True):
        col_q_msg, col_q_btn = st.columns([3, 1])
        with col_q_msg:
            status_indicator = "🟢" if api_is_ready else "⏸️"
            st.markdown(
                f"{status_indicator} **Active Batch Queue:** {queue_stats.get('completed', 0)} completed, "
                f"{queue_stats.get('paused_quota', 0)} paused (quota), {queue_stats.get('pending', 0)} pending."
            )
            if api_is_ready:
                st.caption("✨ Gemini API is online and ready! You can continue generating notes now.")
            else:
                st.caption(f"⏳ API Status: {api_check.get('message', 'Quota reset pending')}")
        with col_q_btn:
            if st.button("⚡ Open Queue / Resume", type="primary", use_container_width=True):
                st.switch_page("pages/1_Generator.py")

# Terminal frame wrapping the factory animation
st.markdown("""
<div class="ns-terminal">
  <div class="ns-terminal-bar">
    <span class="ns-terminal-dot" style="background:#ff2b2b;"></span>
    <span class="ns-terminal-dot" style="background:#ffb000;"></span>
    <span class="ns-terminal-dot" style="background:#22c55e;"></span>
    <span style="margin-left:8px;">notescript-ml — note generator v1.0</span>
  </div>
""", unsafe_allow_html=True)

try:
    with open("ui/factory.html", "r", encoding="utf-8") as f:
        factory_html = f.read()
    data_url = "data:text/html;charset=utf-8," + quote(factory_html)
    st.iframe(data_url, height=460)
except FileNotFoundError:
    st.markdown(
        "<div style='padding:40px;text-align:center;color:#333;font-family:Space Mono,monospace;'>"
        "[ FACTORY ANIMATION NOT FOUND ]</div>",
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

# Nav buttons
col_gen, col_lib, col_prog, col_quiz = st.columns(4)
with col_gen:
    if st.button("🚀 Generator", type="primary", use_container_width=True):
        st.switch_page("pages/1_Generator.py")
with col_lib:
    if st.button("📚 Library", type="secondary", use_container_width=True):
        st.switch_page("pages/2_Library.py")
with col_prog:
    if st.button("📊 Progress", type="secondary", use_container_width=True):
        st.switch_page("pages/4_Progress.py")
with col_quiz:
    if st.button("🎯 Quiz", type="secondary", use_container_width=True):
        st.switch_page("pages/5_Quiz.py")
