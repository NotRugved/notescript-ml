"""Main Dashboard."""
import streamlit as st
from urllib.parse import quote
from ui_components import apply_theme, show_sidebar_common

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
