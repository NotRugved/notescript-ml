"""UI component helpers for NoteScript ML."""
import os
import streamlit as st
from database import list_videos, search_notes, get_progress_stats
from pipeline import load_cached_result

def apply_theme():
    """Load the Miles Morales theme CSS."""
    try:
        with open("ui/theme.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

def show_sidebar_common():
    """Common UI components for the sidebar: navigation only."""
    st.sidebar.page_link("app.py", label="🏠 Dashboard")
    st.sidebar.page_link("pages/1_Generator.py", label="🚀 Generator")
    st.sidebar.page_link("pages/2_Library.py", label="📚 Library")
    st.sidebar.page_link("pages/4_Progress.py", label="📊 Progress")
    st.sidebar.page_link("pages/5_Quiz.py", label="🎯 Quiz")
