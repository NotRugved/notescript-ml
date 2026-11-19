"""Pre-deployment validation suite for NoteScript ML."""
import os
import sys
import datetime
import importlib
import py_compile
import sqlite3
import tempfile

TEST_DB = "test_deploy.db"
PASS = "✅"
FAIL = "❌"
results = []

def report(label: str, ok: bool, detail: str = ""):
    """Record a test result."""
    icon = PASS if ok else FAIL
    msg = f"{icon} {label}"
    if detail:
        msg += f" — {detail}"
    print(msg)
    results.append(ok)

# ── 1. DB FUNCTIONS ───────────────────────────────────────────────────────────
print("\n── 1. Database functions ──")

import database

database.init_db(TEST_DB)
report("init_db creates tables", os.path.exists(TEST_DB))

# save_video
database.save_video("vid_test_1", "Test Title", "Day 1", "http://example.com", TEST_DB)
database.save_video("vid_test_2", "Test Title 2", "Day 2", "http://example.com", TEST_DB)
report("save_video executes without error", True)

# get_progress_stats
ps = database.get_progress_stats(TEST_DB)
report("get_progress_stats returns dict", isinstance(ps, dict) and "total_videos" in ps)
report("total_videos count correct", ps["total_videos"] == 2)

# get_streak_stats — seed 3 consecutive + 1 gap so we can verify
connection = sqlite3.connect(TEST_DB)
cursor = connection.cursor()
today = datetime.date.today()
# Insert 3 consecutive days ending yesterday, plus one 3-days-ago (already there is a gap)
dates_to_insert = [
    today - datetime.timedelta(days=2),
    today - datetime.timedelta(days=1),
    today,
]
for d in dates_to_insert:
    ts = d.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO videos (video_id, title, day_label, duration_seconds, created_at) VALUES (?, ?, ?, ?, ?)",
        (f"streak_{d}", f"Streak {d}", "streak", 600, ts),
    )
# Add a day with a gap to test max_streak separately
gap_day = today - datetime.timedelta(days=5)
cursor.execute(
    "INSERT INTO videos (video_id, title, day_label, duration_seconds, created_at) VALUES (?, ?, ?, ?, ?)",
    ("streak_gap", "Streak Gap", "streak", 600, gap_day.strftime("%Y-%m-%d %H:%M:%S")),
)
connection.commit()
connection.close()

streak = database.get_streak_stats(TEST_DB)
report("get_streak_stats returns dict", isinstance(streak, dict) and "current_streak" in streak)
report("current_streak >= 3 (today + 2 prior days)", streak["current_streak"] >= 3, f"got {streak['current_streak']}")
report("max_streak >= 3", streak["max_streak"] >= 3, f"got {streak['max_streak']}")

# get_daily_activity
activity = database.get_daily_activity(TEST_DB)
report("get_daily_activity returns dict", isinstance(activity, dict))
report("get_daily_activity has today entry", today.strftime("%Y-%m-%d") in activity)

# save_quiz_result + get_quiz_results
database.save_quiz_result("quiz_001", "vid_test_1", 10, 8, 120, "gradient descent,overfitting", TEST_DB)
qr = database.get_quiz_results(TEST_DB)
report("save_quiz_result + get_quiz_results round-trip", len(qr) >= 1)
report("quiz result score correct", qr[0]["score"] == 8)

# queue functions
q_id = database.add_to_queue(1, "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "Lecture 1", TEST_DB)
report("add_to_queue returns id", isinstance(q_id, int) and q_id > 0)
q_items = database.get_queue(TEST_DB)
report("get_queue returns items", len(q_items) == 1 and q_items[0]["status"] == "pending")
database.update_queue_status(q_id, "paused_quota", "Quota exhausted", TEST_DB)
q_items_updated = database.get_queue(TEST_DB)
report("update_queue_status updates status", q_items_updated[0]["status"] == "paused_quota")
q_summary = database.get_queue_summary(TEST_DB)
report("get_queue_summary reflects counts", q_summary.get("paused_quota", 0) == 1)

# ── 2. EXTRACTOR — URL parsing (no network) ───────────────────────────────────
print("\n── 2. Extractor URL parsing ──")

import yt_extractor

url_cases = [
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
    ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
    ("https://www.youtube.com/shorts/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
    ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL1234&index=5", "dQw4w9WgXcQ"),
]
for url, expected in url_cases:
    got = yt_extractor.get_video_id(url)
    report(f"get_video_id: {url[:50]}…", got == expected, f"got '{got}'")

# ── 3. EXPORTS — build from mock result ───────────────────────────────────────
print("\n── 3. Export builders ──")

import exports

mock_result = {
    "video_info": {"title": "Test Lecture", "video_id": "abc123", "duration": 600},
    "merged_notes": {
        "theory_sections": [{"heading": "Intro", "timestamp": "00:00", "content": "Test content"}],
        "intuition": [],
        "code_blocks": [{"title": "Demo", "label": "official", "timestamp": "02:00", "explanation": "Demo code", "code": "print('hello')"}],
        "analogies": [],
        "common_mistakes": [],
        "formulas": [],
        "key_terms": [{"term": "ML", "meaning": "Machine Learning"}],
    },
    "revision": {
        "one_line_summary": "Test summary",
        "cheat_sheet": "## Cheat Sheet\n- Key point",
        "flashcards": [{"q": "What is ML?", "a": "Machine Learning"}],
        "quiz": [{"question": "Q1?", "options": ["A", "B", "C", "D"], "answer_index": 0, "explanation": "Because A."}],
        "interview_questions": [{"q": "Tell me about ML", "a": "It is a field of AI"}],
    },
}

notes_md = exports.build_main_notes_md(mock_result)
report("build_main_notes_md non-empty", len(notes_md) > 100)
report("build_main_notes_md contains heading", "Intro" in notes_md)

rev_md = exports.build_revision_md(mock_result)
report("build_revision_md non-empty", len(rev_md) > 100)
report("build_revision_md has flashcard", "What is ML?" in rev_md)

code_py = exports.build_code_py(mock_result)
report("build_code_py non-empty", len(code_py) > 20)
report("build_code_py contains code", "print" in code_py)

# ── 4. PIPELINE CACHE ─────────────────────────────────────────────────────────
print("\n── 4. Pipeline cache ──")

from pipeline import load_cached_result

cached = load_cached_result("UZPfbG0jNec")
if cached is None:
    report("load_cached_result (live DB)", False, "no cached result for UZPfbG0jNec — skipped")
else:
    report("load_cached_result returns dict", isinstance(cached, dict))
    has_keys = "video_info" in cached and "merged_notes" in cached and "revision" in cached
    report("cached result has required keys", has_keys)

# ── 5. SYNTAX CHECK — all .py files ──────────────────────────────────────────
print("\n── 5. Syntax check (py_compile) ──")

py_files = [
    "app.py", "database.py", "ai_processor.py", "pipeline.py",
    "exports.py", "yt_extractor.py", "ui_components.py",
    "pages/1_Generator.py", "pages/2_Library.py", "pages/3_Notes.py",
    "pages/4_Progress.py", "pages/5_Quiz.py",
]
for f in py_files:
    if not os.path.exists(f):
        report(f"py_compile {f}", False, "file not found")
        continue
    try:
        py_compile.compile(f, doraise=True)
        report(f"py_compile {f}", True)
    except py_compile.PyCompileError as e:
        report(f"py_compile {f}", False, str(e))

# ── 6. IMPORT CHAIN ───────────────────────────────────────────────────────────
print("\n── 6. Import chain ──")

for mod in ["database", "pipeline", "exports", "yt_extractor", "ui_components"]:
    try:
        importlib.import_module(mod)
        report(f"import {mod}", True)
    except Exception as e:
        report(f"import {mod}", False, str(e))

# ── 7. THEME CSS ──────────────────────────────────────────────────────────────
print("\n── 7. Theme assets ──")

report("ui/theme.css exists", os.path.exists("ui/theme.css"))
if os.path.exists("ui/theme.css"):
    with open("ui/theme.css", "r", encoding="utf-8") as f:
        css = f.read()
    report("ui/theme.css non-empty", len(css) > 100)

# ── 8. ADMIN ACCESS CONTROL ───────────────────────────────────────────────────
print("\n── 8. Admin access control ──")

import ui_components
from dotenv import load_dotenv
load_dotenv()

active_code = os.getenv("ADMIN_ACCESS_CODE", "")
report("verify_admin_code accepts valid env code", ui_components.verify_admin_code(active_code) is True)
report("verify_admin_code rejects incorrect code", ui_components.verify_admin_code("wrong_passcode_xyz") is False)
report("verify_admin_code rejects empty code", ui_components.verify_admin_code("") is False)
report("is_admin_authenticated defaults to False", ui_components.is_admin_authenticated() is False)

# ── CLEANUP & SUMMARY ─────────────────────────────────────────────────────────
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)
    print(f"\n🧹 Removed {TEST_DB}")

total = len(results)
passed = sum(1 for r in results if r)
failed = total - passed
print(f"\n{'='*48}")
print(f"Results: {passed}/{total} passed  |  {failed} failed")
if failed == 0:
    print("🚀 All checks passed — ready for deployment!")
else:
    print("⚠️  Fix failures above before deploying.")
    sys.exit(1)
