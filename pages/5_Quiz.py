"""Quiz Page — interactive quiz from saved revision packs."""
import time
import uuid
import datetime
import streamlit as st
from ui_components import apply_theme, show_sidebar_common
from database import list_videos
from pipeline import load_cached_result

st.set_page_config(page_title="Quiz - NoteScript ML", page_icon="🎯", layout="wide")
apply_theme()
show_sidebar_common()

st.markdown("# 🎯 QUIZ YOURSELF")

# ── Initialise session state keys ─────────────────────────────────────────────
for key, default in [
    ("quiz_active", False),
    ("quiz_questions", []),
    ("quiz_q_index", 0),
    ("quiz_answers", {}),
    ("quiz_start_time", None),
    ("quiz_q_start_time", None),
    ("quiz_done", False),
    ("quiz_id", ""),
    ("quiz_source_vid", ""),
    ("quiz_time_limit", False),
    ("quiz_time_per_q", 120),
]:
    if key not in st.session_state:
        st.session_state[key] = default


def _load_questions(video_id: str, count: int) -> list:
    """Pull quiz questions from one or all saved revision packs."""
    questions = []
    if video_id == "__all__":
        saved = list_videos()
        for v in saved:
            cached = load_cached_result(v.get("video_id", ""))
            if cached:
                rev = cached.get("revision", {})
                for q in rev.get("quiz", []):
                    q["_source_video"] = v.get("title", v.get("video_id", ""))
                    questions.append(q)
    else:
        cached = load_cached_result(video_id)
        if cached:
            rev = cached.get("revision", {})
            vid_title = cached.get("video_info", {}).get("title", video_id)
            for q in rev.get("quiz", []):
                q["_source_video"] = vid_title
                questions.append(q)
    # Trim to requested count using explicit slice (index loop)
    if len(questions) > count:
        trimmed = []
        for i in range(count):
            trimmed.append(questions[i])
        questions = trimmed
    return questions


def _fmt_time(seconds: int) -> str:
    """Format seconds as mm:ss."""
    m = seconds // 60
    s = seconds % 60
    return f"{m:02d}:{s:02d}"


# ── RESULTS SCREEN ─────────────────────────────────────────────────────────────
if st.session_state["quiz_done"]:
    questions = st.session_state["quiz_questions"]
    answers = st.session_state["quiz_answers"]
    score = 0
    wrong_topics = []

    for i in range(len(questions)):
        q = questions[i]
        correct_idx = q.get("answer_index", 0)
        opts = q.get("options", [])
        correct_ans = opts[correct_idx] if correct_idx < len(opts) else ""
        user_ans = answers.get(i, "")
        if user_ans == correct_ans:
            score += 1
        else:
            # Topic weakness = first 60 chars of question text
            snippet = q.get("question", "")[:60].strip()
            wrong_topics.append(snippet)

    total = len(questions)
    pct = int(score / total * 100) if total > 0 else 0
    elapsed = int(time.time() - (st.session_state["quiz_start_time"] or time.time()))
    colour = "#ff2b2b" if pct < 60 else ("#e6a817" if pct < 80 else "#22c55e")

    st.markdown(
        f"<div style='border:2px solid #fff;padding:32px;box-shadow:6px 6px 0 #ff2b2b;"
        f"background:#1a1a1a;text-align:center;animation:card-pop 0.4s ease both;'>"
        f"<div class='ns-score' style='color:{colour};'>{score}/{total}</div>"
        f"<div style='font-family:Space Mono,monospace;font-size:1rem;color:#aaa;"
        f"margin-top:8px;letter-spacing:0.06em;'>{pct}% · ⏱ {_fmt_time(elapsed)}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown("### Question Review")
    for i in range(len(questions)):
        q = questions[i]
        correct_idx = q.get("answer_index", 0)
        opts = q.get("options", [])
        correct_ans = opts[correct_idx] if correct_idx < len(opts) else ""
        user_ans = answers.get(i, "")
        is_correct = user_ans == correct_ans
        icon = "✅" if is_correct else "❌"
        with st.expander(f"{icon} Q{i + 1}: {q.get('question', '')[:80]}"):
            for j in range(len(opts)):
                opt = opts[j]
                if opt == correct_ans and opt == user_ans:
                    st.markdown(f"**✅ {opt}** ← your answer (correct)")
                elif opt == correct_ans:
                    st.markdown(f"**✅ {opt}** ← correct answer")
                elif opt == user_ans:
                    st.markdown(f"~~❌ {opt}~~ ← your answer")
                else:
                    st.markdown(f"&nbsp;&nbsp;{opt}")
            st.caption(f"Explanation: {q.get('explanation', '')}")
            st.caption(f"Source: {q.get('_source_video', '')}")

    if wrong_topics:
        st.markdown("### 🔴 Topic Weaknesses")
        for t in wrong_topics:
            st.markdown(f"- {t}")

    col_act1, col_act2 = st.columns([1, 1])
    with col_act1:
        if st.button("🔄 Take Another Quiz", type="primary", use_container_width=True):
            for key in [
                "quiz_active",
                "quiz_questions",
                "quiz_q_index",
                "quiz_answers",
                "quiz_start_time",
                "quiz_q_start_time",
                "quiz_done",
                "quiz_id",
                "quiz_source_vid",
            ]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    with col_act2:
        if st.button("📚 Browse More Lectures", use_container_width=True):
            st.switch_page("pages/2_Library.py")
    st.stop()


# ── ACTIVE QUIZ SCREEN ────────────────────────────────────────────────────────
if st.session_state["quiz_active"]:
    questions = st.session_state["quiz_questions"]
    total = len(questions)
    idx = st.session_state["quiz_q_index"]

    if idx >= total:
        st.session_state["quiz_done"] = True
        st.rerun()

    q = questions[idx]
    opts = q.get("options", [])

    # Progress bar
    st.progress((idx + 1) / total, text=f"Question {idx + 1} of {total}")

    # Timer
    if st.session_state["quiz_time_limit"]:
        elapsed_q = int(time.time() - (st.session_state["quiz_q_start_time"] or time.time()))
        remaining = max(0, st.session_state["quiz_time_per_q"] - elapsed_q)
        timer_colour = "#ff2b2b" if remaining < 30 else "#ffffff"
        st.markdown(
            f"<div style='text-align:right;font-family:Space Mono,monospace;"
            f"color:{timer_colour};font-size:1.2rem;'>⏱ {_fmt_time(remaining)}</div>",
            unsafe_allow_html=True,
        )
        if remaining == 0 and str(idx) not in st.session_state["quiz_answers"]:
            st.session_state["quiz_answers"][idx] = ""
            st.session_state["quiz_q_index"] = idx + 1
            st.session_state["quiz_q_start_time"] = time.time()
            st.rerun()

    # Question card
    st.markdown(
        f"<div class='ns-quiz-card'>"
        f"<div style='font-family:Space Mono,monospace;font-size:0.75rem;color:#666;"
        f"text-transform:uppercase;letter-spacing:0.08em;'>Question {idx + 1} / {total}</div>"
        f"<div style='font-size:1.05rem;margin-top:10px;line-height:1.5;'>{q.get('question', '')}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # Radio — use current saved answer as default
    saved_ans = st.session_state["quiz_answers"].get(idx, None)
    default_idx = 0
    if saved_ans is not None and saved_ans in opts:
        default_idx = opts.index(saved_ans)

    chosen = st.radio(
        "Select your answer:",
        options=opts,
        index=default_idx,
        key=f"quiz_radio_{idx}",
        label_visibility="collapsed",
    )
    st.session_state["quiz_answers"][idx] = chosen

    col_prev, col_next, col_submit = st.columns([1, 1, 2])

    with col_prev:
        if idx > 0:
            if st.button("← Previous"):
                st.session_state["quiz_q_index"] = idx - 1
                st.rerun()

    with col_next:
        if idx < total - 1:
            if st.button("Next →"):
                st.session_state["quiz_q_index"] = idx + 1
                st.session_state["quiz_q_start_time"] = time.time()
                st.rerun()

    with col_submit:
        answered_count = len(st.session_state["quiz_answers"])
        if st.button(f"✅ Submit Quiz ({answered_count}/{total} answered)", type="primary"):
            # Fill any unanswered with blank
            for i in range(total):
                if i not in st.session_state["quiz_answers"]:
                    st.session_state["quiz_answers"][i] = ""
            st.session_state["quiz_done"] = True
            st.rerun()

    st.stop()


# ── CONFIG SCREEN ─────────────────────────────────────────────────────────────
st.markdown("### Configure Your Quiz")

saved_videos = list_videos()
if not saved_videos:
    st.info("No saved notes yet. Generate notes for some lectures first.")
    st.stop()

# Source selector
source_options = ["All saved notes"]
source_ids = ["__all__"]
for v in saved_videos:
    title = v.get("title", v.get("video_id", ""))
    short = title[:60] if len(title) > 60 else title
    source_options.append(short)
    source_ids.append(v.get("video_id", ""))

col_src, col_cnt, col_timer = st.columns([3, 1, 1])

with col_src:
    src_choice = st.selectbox("Question Source", options=source_options)
    chosen_vid_idx = source_options.index(src_choice)
    chosen_vid_id = source_ids[chosen_vid_idx]

with col_cnt:
    q_count = st.selectbox("Questions", options=[5, 10, 15, 20, 25], index=1)

with col_timer:
    use_timer = st.toggle("⏱ Timer", value=False)
    time_per_q = 120
    if use_timer:
        time_per_q = st.selectbox("Secs / Q", options=[60, 90, 120, 180], index=2)

# Preview count
preview_questions = _load_questions(chosen_vid_id, q_count)
available = len(preview_questions)
if available == 0:
    st.warning("No quiz questions found for the selected source. Try a different video.")
elif available < q_count:
    st.warning(f"Only {available} questions available — quiz will use all {available}.")

st.markdown(f"**{available} question(s) available.** Ready when you are.")

if st.button("🚀 Start Quiz", type="primary", disabled=(available == 0)):
    st.session_state["quiz_active"] = True
    st.session_state["quiz_questions"] = preview_questions
    st.session_state["quiz_q_index"] = 0
    st.session_state["quiz_answers"] = {}
    st.session_state["quiz_start_time"] = time.time()
    st.session_state["quiz_q_start_time"] = time.time()
    st.session_state["quiz_done"] = False
    st.session_state["quiz_id"] = str(uuid.uuid4())[:8]
    st.session_state["quiz_source_vid"] = chosen_vid_id
    st.session_state["quiz_time_limit"] = use_timer
    st.session_state["quiz_time_per_q"] = time_per_q
    st.rerun()
