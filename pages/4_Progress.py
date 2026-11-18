"""User Progress Dashboard Page."""
import streamlit as st
from ui_components import apply_theme, show_sidebar_common
from database import get_progress_stats, list_videos

st.set_page_config(page_title="Progress - NoteScript ML", page_icon="📊", layout="wide")
apply_theme()
show_sidebar_common()

st.header("📊 Your Learning Progress")

stats = get_progress_stats()
saved = list_videos()

if not stats:
    st.info("No progress tracked yet. Generate notes for some lectures to get started!")
else:
    # High-level Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Videos Processed", stats["total_videos"])
    c2.metric("Days Covered", stats["days_covered"])

    progress = min(stats["days_covered"] / 100.0, 1.0)
    c3.metric("Overall Completion", f"{int(progress * 100)}%")

    st.markdown("### 🎯 100 Days of ML Progress")
    st.progress(progress)
