"""Progress Dashboard Page — heatmap + quiz history."""
import datetime
import streamlit as st
from ui_components import apply_theme, show_sidebar_common
from database import get_progress_stats, get_daily_activity, get_quiz_results

st.set_page_config(page_title="Progress - NoteScript ML", page_icon="📊", layout="wide")
apply_theme()
show_sidebar_common()

st.markdown("# 📊 YOUR LEARNING PROGRESS")

# ── High-level stats ──────────────────────────────────────────────────────────
stats = get_progress_stats()
if not stats or stats.get("total_videos", 0) == 0:
    st.info("No progress yet. Generate notes for some lectures to get started!")
else:
    c1, c2, c3 = st.columns(3)
    c1.metric("Videos Processed", stats["total_videos"])
    c2.metric("Days Covered", stats["days_covered"])
    pct = min(int(stats["days_covered"] / 100.0 * 100), 100)
    c3.metric("100-Day Completion", f"{pct}%")
    st.progress(min(stats["days_covered"] / 100.0, 1.0), text=f"{pct}% of 100 Days of ML")

st.divider()

# ── GitHub-style activity heatmap ─────────────────────────────────────────────
st.markdown("### 🟥 Daily Activity Heatmap")

activity = get_daily_activity()

# Build a 52-week × 7-day grid anchored to today
today = datetime.date.today()
# Step back to the most recent Monday so the grid starts on Monday
days_since_monday = today.weekday()          # Mon=0, Sun=6
grid_end = today
grid_start = grid_end - datetime.timedelta(weeks=52) + datetime.timedelta(days=1)
# Align start to Monday
while grid_start.weekday() != 0:
    grid_start -= datetime.timedelta(days=1)

# Collect all dates into a dict for fast lookup
date_counts = {}
current = grid_start
while current <= grid_end:
    key = current.strftime("%Y-%m-%d")
    date_counts[key] = activity.get(key, 0)
    current += datetime.timedelta(days=1)

# Find max count for colour scaling
max_count = 1
for v in date_counts.values():
    if v > max_count:
        max_count = v

def _cell_colour(count: int) -> str:
    """Return hex colour for a given count (3-tier: dark → amber → red)."""
    if count == 0:
        return "#1a1a1a"
    intensity = count / max_count
    if intensity < 0.4:
        return "#5a2800"       # dim amber-brown — low
    if intensity < 0.75:
        return "#ffb000"       # amber — medium
    return "#ff2b2b"           # vibrant red — high

# Build columns: collect weeks
weeks = []
week = []
current = grid_start
while current <= grid_end:
    week.append(current)
    if current.weekday() == 6:   # Sunday — end of week
        weeks.append(week)
        week = []
    current += datetime.timedelta(days=1)
if week:
    weeks.append(week)

# Build month labels row
month_labels_html = "<div style='display:flex;gap:3px;margin-left:28px;margin-bottom:4px;'>"
prev_month = None
for week_days in weeks:
    first_day = week_days[0]
    if first_day.month != prev_month:
        label = first_day.strftime("%b")
        prev_month = first_day.month
        month_labels_html += f"<div style='width:14px;font-size:9px;color:#888;'>{label}</div>"
    else:
        month_labels_html += "<div style='width:14px;'></div>"
month_labels_html += "</div>"

# Build day-of-week labels + grid
day_labels = ["M", "T", "W", "T", "F", "S", "S"]
grid_html = "<div style='display:flex;gap:3px;'>"

# Day-of-week column
grid_html += "<div style='display:flex;flex-direction:column;gap:3px;margin-right:4px;'>"
for lbl in day_labels:
    grid_html += f"<div style='height:14px;width:14px;font-size:9px;color:#888;line-height:14px;'>{lbl}</div>"
grid_html += "</div>"

# Week columns
for week_days in weeks:
    grid_html += "<div style='display:flex;flex-direction:column;gap:3px;'>"
    # Pad top if first week doesn't start on Monday
    if len(week_days) < 7:
        pad = week_days[0].weekday()
        for _ in range(pad):
            grid_html += "<div style='width:14px;height:14px;'></div>"
    for day in week_days:
        key = day.strftime("%Y-%m-%d")
        count = date_counts.get(key, 0)
        colour = _cell_colour(count)
        tip = f"{day.strftime('%b %d')}: {count} video(s)"
        grid_html += (
            f"<div title='{tip}' style='width:14px;height:14px;background:{colour};"
            f"border-radius:2px;transition:transform 0.1s ease,box-shadow 0.1s ease;"
            f"cursor:pointer;' "
            f"onmouseover=\"this.style.transform='scale(1.3)';this.style.boxShadow='0 0 6px {colour}';\" "
            f"onmouseout=\"this.style.transform='scale(1)';this.style.boxShadow='none';\""
            f"></div>"
        )
    grid_html += "</div>"

grid_html += "</div>"

legend_html = (
    "<div style='display:flex;align-items:center;gap:6px;margin-top:10px;"
    "font-size:11px;color:#666;font-family:Space Mono,monospace;'>"
    "<span>LESS</span>"
    "<div style='width:12px;height:12px;background:#1a1a1a;border:1px solid #333;'></div>"
    "<div style='width:12px;height:12px;background:#5a2800;'></div>"
    "<div style='width:12px;height:12px;background:#ffb000;'></div>"
    "<div style='width:12px;height:12px;background:#ff2b2b;'></div>"
    "<span>MORE</span>"
    "</div>"
)

full_heatmap = (
    "<div style='background:#111;padding:16px;border:2px solid #fff;"
    "box-shadow:4px 4px 0 #ff2b2b;display:inline-block;'>"
    + month_labels_html
    + grid_html
    + legend_html
    + "</div>"
)

st.markdown(full_heatmap, unsafe_allow_html=True)

st.divider()

# ── Quiz history ───────────────────────────────────────────────────────────────
st.markdown("### 🎯 Quiz History")

quiz_results = get_quiz_results()
if not quiz_results:
    st.info("No quizzes taken yet. Head to the Quiz page to test yourself!")
else:
    # Aggregate stats
    total_quizzes = len(quiz_results)
    total_score = 0
    total_possible = 0
    best_pct = 0
    weakness_counts = {}

    for r in quiz_results:
        sc = r.get("score", 0)
        tot = r.get("total_questions", 1) or 1
        total_score += sc
        total_possible += tot
        pct = int(sc / tot * 100)
        if pct > best_pct:
            best_pct = pct
        weaknesses_str = r.get("topic_weaknesses", "") or ""
        for topic in weaknesses_str.split(","):
            topic = topic.strip()
            if topic:
                weakness_counts[topic] = weakness_counts.get(topic, 0) + 1

    avg_pct = int(total_score / total_possible * 100) if total_possible > 0 else 0

    qa, qb, qc = st.columns(3)
    qa.metric("Total Quizzes", total_quizzes)
    qb.metric("Best Score", f"{best_pct}%")
    qc.metric("Average Score", f"{avg_pct}%")

    if weakness_counts:
        st.markdown("#### 🔴 Topic Weaknesses")
        # Sort by frequency descending
        sorted_topics = []
        for topic, count in weakness_counts.items():
            sorted_topics.append((count, topic))
        sorted_topics.sort(reverse=True)
        for count, topic in sorted_topics[:10]:
            st.markdown(f"- **{topic}** — wrong {count}×")

    st.markdown("#### 📋 Recent Attempts")
    for r in quiz_results[:20]:
        sc = r.get("score", 0)
        tot = r.get("total_questions", 1) or 1
        pct = int(sc / tot * 100)
        secs = r.get("time_taken_seconds", 0) or 0
        mins = secs // 60
        rem_secs = secs % 60
        time_str = f"{mins}m {rem_secs}s" if mins > 0 else f"{secs}s"
        date_str = (r.get("created_at") or "")[:10]
        vid_id = r.get("video_id", "")[:20]
        colour = "#ff2b2b" if pct < 60 else ("#e6a817" if pct < 80 else "#22c55e")
        card = (
            f"<div style='border:2px solid #fff;padding:12px 16px;margin-bottom:8px;"
            f"box-shadow:3px 3px 0 #ff2b2b;background:#111;'>"
            f"<span style='font-family:Space Mono,monospace;font-size:0.85rem;color:#aaa;'>"
            f"{date_str} · {vid_id}</span><br>"
            f"<span style='font-size:1.4rem;font-weight:700;color:{colour};'>{sc}/{tot}</span>"
            f"<span style='color:#aaa;'> ({pct}%)</span>"
            f"<span style='float:right;color:#888;font-size:0.85rem;'>⏱ {time_str}</span>"
            f"</div>"
        )
        st.markdown(card, unsafe_allow_html=True)
