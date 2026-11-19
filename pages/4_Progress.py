"""Course Roadmap & Curriculum Coverage Dashboard for NoteScript ML."""
import streamlit as st
from ui_components import apply_theme, show_sidebar_common
from database import get_progress_stats, list_videos
from pipeline import load_cached_result
from yt_extractor import format_time

st.set_page_config(page_title="Course Roadmap - NoteScript ML", page_icon="📊", layout="wide")
apply_theme()
show_sidebar_common()

st.markdown("# 📊 100 DAYS OF ML — CURRICULUM ROADMAP")
st.caption(
    "Track the complete CampusX '100 Days of Machine Learning' curriculum archive. "
    "Every indexed lecture contains detailed Hinglish notes, intuition, formulas, runnable Python code, and revision packs."
)

# ── High-Level Course Metrics ────────────────────────────────────────────────
stats = get_progress_stats()
all_videos = list_videos()

total_vids = stats.get("total_videos", 0) if stats else len(all_videos)
days_covered = stats.get("days_covered", 0) if stats else 0
completion_pct = min(int(days_covered / 100.0 * 100), 100)

total_duration_sec = 0
for v in all_videos:
    total_duration_sec += int(v.get("duration_seconds", 0) or 0)

dur_hours = total_duration_sec // 3600
dur_mins = (total_duration_sec % 3600) // 60
duration_display = f"{dur_hours}h {dur_mins}m" if dur_hours > 0 else f"{dur_mins}m"

m1, m2, m3, m4 = st.columns(4)
m1.metric("Indexed Lectures", total_vids)
m2.metric("Days Covered", f"{days_covered} / 100")
m3.metric("Curriculum Completion", f"{completion_pct}%")
m4.metric("Study Content Duration", duration_display)

st.progress(min(days_covered / 100.0, 1.0), text=f"{completion_pct}% of the 100 Days of Machine Learning curriculum ready")

st.divider()

# ── 100 Days Curriculum Phases ───────────────────────────────────────────────
st.markdown("### 🗺️ Curriculum Phases")

curriculum_phases = [
    {
        "phase": "Phase 1: Foundations & Exploratory Data Analysis",
        "range": "Days 1 – 20",
        "topics": "Python for ML, NumPy, Pandas, Data Cleaning, Univariate & Bivariate EDA, SQL & CSV Handling",
    },
    {
        "phase": "Phase 2: Feature Engineering & Data Preprocessing",
        "range": "Days 21 – 40",
        "topics": "Imputation, Encoding, Feature Scaling, Outlier Detection, Function Transformers, Pipelines",
    },
    {
        "phase": "Phase 3: Core Supervised Learning Algorithms",
        "range": "Days 41 – 70",
        "topics": "Simple & Multiple Linear Regression, Gradient Descent, Logistic Regression, Decision Trees, SVM, KNN",
    },
    {
        "phase": "Phase 4: Ensemble Techniques & Model Evaluation",
        "range": "Days 71 – 85",
        "topics": "Bagging, Random Forests, Boosting (AdaBoost, Gradient Boost, XGBoost), Hyperparameter Tuning, Metrics",
    },
    {
        "phase": "Phase 5: Unsupervised Learning & Neural Networks",
        "range": "Days 86 – 100",
        "topics": "K-Means, Hierarchical Clustering, PCA, t-SNE, Perceptron, Neural Networks Architecture, Production Deployment",
    },
]

col_p1, col_p2 = st.columns(2)
for idx in range(len(curriculum_phases)):
    phase_data = curriculum_phases[idx]
    target_col = col_p1 if idx % 2 == 0 else col_p2
    with target_col:
        with st.container(border=True):
            st.markdown(f"**{phase_data['phase']}**")
            st.caption(f"🗓️ {phase_data['range']}")
            st.write(phase_data["topics"])

st.divider()

# ── Indexed Lectures Directory ───────────────────────────────────────────────
st.markdown("### 📚 Ready Lectures Archive")

if len(all_videos) == 0:
    st.info("No lecture notes indexed yet. Check back soon or request notes from the administrator!")
else:
    st.write(f"Showing **{len(all_videos)}** complete lecture notes ready for study and review:")

    for v in all_videos:
        vid_id = v.get("video_id", "")
        title = v.get("title", "Untitled Lecture")
        day_lbl = v.get("day_label", "")
        sec = int(v.get("duration_seconds", 0) or 0)
        dur_str = format_time(sec) if sec > 0 else "N/A"

        with st.container(border=True):
            c_info, c_actions = st.columns([4, 2])
            with c_info:
                if day_lbl:
                    st.markdown(f"`{day_lbl}` **{title}**")
                else:
                    st.markdown(f"**{title}**")
                st.caption(f"⏱ Video Duration: {dur_str} · ✅ Includes: Theory, Intuition, Code, Formulas, Quiz")
            with c_actions:
                sub_c1, sub_c2 = st.columns(2)
                with sub_c1:
                    if st.button("📖 Notes", key=f"btn_notes_{vid_id}", use_container_width=True):
                        cached_result = load_cached_result(vid_id)
                        if cached_result:
                            st.session_state["pipeline_result"] = cached_result
                            st.switch_page("pages/3_Notes.py")
                with sub_c2:
                    if st.button("🎯 Quiz", key=f"btn_quiz_{vid_id}", use_container_width=True):
                        st.switch_page("pages/5_Quiz.py")
