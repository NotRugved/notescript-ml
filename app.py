"""Main Dashboard."""
import streamlit as st
from ui_components import apply_theme, show_sidebar_common

st.set_page_config(page_title="NoteScript ML", page_icon="⚙️", layout="wide")
apply_theme()
show_sidebar_common()

# Load Factory Animation via components.html (raw HTML, no sanitization)
try:
    with open("ui/factory.html", "r", encoding="utf-8") as f:
        factory_html = f.read()
    st.components.v1.html(factory_html, height=480, scrolling=False)
except FileNotFoundError:
    st.error("Factory animation file not found.")

col_gen, col_lib, col_prog = st.columns(3)
with col_gen:
    if st.button("🚀 Enter Generator", type="primary", use_container_width=True):
        st.switch_page("pages/1_Generator.py")
with col_lib:
    if st.button("📚 Open Library", type="secondary", use_container_width=True):
        st.switch_page("pages/2_Library.py")
with col_prog:
    if st.button("📊 View Progress", type="secondary", use_container_width=True):
        st.switch_page("pages/4_Progress.py")
