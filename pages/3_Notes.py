"""Note Viewer Page for NoteScript ML."""
import streamlit as st
from ui_components import apply_theme, show_sidebar_common
from yt_extractor import parse_time
from exports import build_code_py, build_main_notes_md, build_revision_md

st.set_page_config(page_title="Notes - NoteScript ML", page_icon="📖", layout="wide")
apply_theme()
show_sidebar_common()

result = st.session_state.get("pipeline_result")
if not result:
    st.info("No lecture selected. Go to Generator or Library.")
else:
    video_info = result.get("video_info", {})
    st.header(video_info.get("title", "Lecture Notes"))

    # Export Buttons
    col_dl1, col_dl2, col_dl3 = st.columns(3)
    with col_dl1: st.download_button("📥 Notes (.md)", build_main_notes_md(result), "notes.md", mime="text/markdown", use_container_width=True)
    with col_dl2: st.download_button("📥 Revision (.md)", build_revision_md(result), "rev.md", mime="text/markdown", use_container_width=True)
    with col_dl3: st.download_button("📥 Code (.py)", build_code_py(result), "code.py", mime="text/x-python", use_container_width=True)

    st.divider()
    all_sections = ["Theory", "Intuition", "Code", "Analogies", "Common Mistakes", "Formulas & Key Terms", "Revision"]
    tabs = st.tabs(all_sections)

    def render(section):
        merged = result.get("merged_notes", {})
        v_id = video_info.get("video_id", "")

        if section == "Theory":
            for t in merged.get("theory_sections", []):
                with st.container(border=True):
                    st.markdown(f"### {t.get('heading', 'Concept')}")
                    st.markdown(t.get("content", ""))
        elif section == "Intuition":
            for item in merged.get("intuition", []):
                with st.container(border=True):
                    st.markdown(f"**{item.get('text', '')}**")
        elif section == "Code":
            for c in merged.get("code_blocks", []):
                with st.container(border=True):
                    st.markdown(f"**{c.get('title', 'Snippet')}**")
                    st.code(c.get("code", ""), language="python")
        elif section == "Analogies":
            for a in merged.get("analogies", []):
                with st.container(border=True):
                    st.markdown(f"**Analogy:** {a.get('analogy', '')}")
                    st.caption(f"Explains: {a.get('explains', '')}")
        elif section == "Common Mistakes":
            for m in merged.get("common_mistakes", []):
                with st.container(border=True):
                    st.markdown(f"**Mistake:** {m.get('mistake', '')}")
                    st.markdown(f"- *Why:* {m.get('why', '')}")
                    st.markdown(f"- *Fix:* {m.get('fix', '')}")
        elif section == "Formulas & Key Terms":
            st.markdown("#### Formulas")
            for f in merged.get("formulas", []):
                with st.container(border=True):
                    st.markdown(f"**{f.get('name', '')}**: `{f.get('formula', '')}`")
            st.markdown("#### Key Terms")
            for k in merged.get("key_terms", []):
                with st.container(border=True):
                    st.markdown(f"**{k.get('term', '')}**: {k.get('meaning', '')}")
        elif section == "Revision":
            rev = result.get("revision", {})
            st.markdown("### Cheat Sheet")
            st.markdown(rev.get("cheat_sheet", "*No cheat sheet*"))
            st.markdown("### Flashcards")
            for fc in rev.get("flashcards", []):
                with st.expander(f"🃏 {fc.get('q', 'Question')}"):
                    st.write(fc.get("a", "Answer"))

    for tab, section in zip(tabs, all_sections):
        with tab: render(section)
