"""UI component helpers for NoteScript ML."""
import os
import secrets
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

    if is_admin_authenticated():
        st.sidebar.divider()
        st.sidebar.caption("👑 **Admin Mode Active**")
        if st.sidebar.button("🔒 Logout Admin", key="sidebar_admin_logout", use_container_width=True):
            st.session_state["is_admin"] = False
            st.rerun()


def is_admin_authenticated() -> bool:
    """Check if the current session holds active admin privileges."""
    admin_flag = st.session_state.get("is_admin", False)
    return bool(admin_flag is True)


def verify_admin_code(entered_code: str) -> bool:
    """Verify input code against ADMIN_ACCESS_CODE from environment securely."""
    expected_code = os.getenv("ADMIN_ACCESS_CODE", "")
    if not expected_code or not entered_code:
        return False
    # Use secrets.compare_digest to prevent timing attacks
    clean_entered = entered_code.strip()
    clean_expected = expected_code.strip()
    return secrets.compare_digest(clean_entered, clean_expected)


def render_admin_gate() -> bool:
    """Display authentication screen if not logged in as admin, or return True."""
    if is_admin_authenticated():
        return True

    st.markdown("## 🔒 Admin Access Required")
    st.info(
        "**Note Generation is restricted to the administrator.**\n\n"
        "AI processing consumes Google Gemini API quotas. Only authorized administrators "
        "may generate new lecture notes or run multi-day batch queues.\n\n"
        "✨ **Learners & Visitors:** You can freely read completed notes in the "
        "[📚 Library](pages/2_Library.py), download full study packs (.md & .py), "
        "check your [📊 Progress](pages/4_Progress.py), and test your knowledge in the [🎯 Quiz](pages/5_Quiz.py)!"
    )

    with st.container(border=True):
        st.markdown("### 🔑 Administrator Login")
        passcode = st.text_input(
            "Enter Admin Passcode",
            type="password",
            placeholder="Passcode...",
            key="input_admin_passcode",
        )
        col_btn, col_empty = st.columns([1, 3])
        with col_btn:
            submit_login = st.button("🔓 Unlock Generator", type="primary", use_container_width=True)

        if submit_login:
            if verify_admin_code(passcode):
                st.session_state["is_admin"] = True
                st.success("Admin access granted!")
                st.rerun()
            else:
                st.error("❌ Incorrect admin passcode. Please check your credentials.")

    return False


def render_admin_bar() -> None:
    """Render top admin status bar with logout button."""
    col_badge, col_logout = st.columns([4, 1])
    with col_badge:
        st.caption("👑 **Logged in as Administrator** — Full generation and queue control unlocked.")
    with col_logout:
        if st.button("🔒 Logout", key="btn_admin_top_logout", use_container_width=True):
            st.session_state["is_admin"] = False
            st.rerun()

