"""Library Page."""
import streamlit as st
from ui_components import apply_theme, show_sidebar_common
from database import list_videos, search_notes
from pipeline import load_cached_result

st.set_page_config(page_title="Library - NoteScript ML", page_icon="📚", layout="wide")
apply_theme()
show_sidebar_common()

st.markdown("""
<style>
    .library-card {
        padding: 10px;
        margin-bottom: 8px;
        border: 1px solid #333;
        border-radius: 4px;
        transition: all 0.2s ease;
    }
    .library-card:hover {
        border-color: #ff2b2b;
        transform: translateX(4px);
    }
    .library-title {
        font-size: 0.9rem;
        font-weight: bold;
    }
    .library-btn {
        font-size: 0.7rem;
        padding: 4px 8px;
    }
</style>
""", unsafe_allow_html=True)

st.header("📚 Your Lecture Library")
search_query = st.text_input("🔍 Search your notes...", placeholder="e.g. gradient descent")
saved = search_notes(search_query) if search_query else list_videos()

if not saved:
    st.info("No saved notes found.")
else:
    for v in saved:
        with st.container(border=True):
            cols = st.columns([3, 1])
            cols[0].write(f"<p class='library-title'>{v['title']}</p>", unsafe_allow_html=True)
            if cols[1].button("Open", key=f"lib_view_{v['video_id']}"):
                cached = load_cached_result(v['video_id'])
                if cached:
                    st.session_state["pipeline_result"] = cached
                    st.switch_page("pages/3_Notes.py")