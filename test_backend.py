"""Backend test suite for NoteScript ML pipeline and exports."""

import os
import shutil
import time

from exports import build_code_py, build_main_notes_md, build_revision_md
from pipeline import run_pipeline


def test_backend_run() -> None:
    """Run pipeline twice on a short public video to verify execution and caching."""
    # Test with a short public video (Me at the zoo - 19 seconds)
    test_video_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    test_db = "test_backend.db"

    temp_dir = "temp_test_exports"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    progress_log = []

    def on_progress(msg: str, frac: float) -> None:
        progress_log.append(f"[{frac*100:3.0f}%] {msg}")

    print("=" * 60)
    print("RUN 1: Executing pipeline from scratch...")
    print("=" * 60)
    t0 = time.time()
    result1 = run_pipeline(
        video_url=test_video_url,
        folder="",
        notebook_file="",
        segment_minutes=5,
        resolution="LOW",
        progress=on_progress,
        db_path=test_db,
    )
    run1_duration = time.time() - t0
    print(f"Run 1 completed in {run1_duration:.2f}s")
    print(f"Video Title: {result1['video_info']['title']}")
    print(f"Total segments: {result1['total_segments']}")

    # Build exports
    notes_md = build_main_notes_md(result1)
    rev_md = build_revision_md(result1)
    code_py = build_code_py(result1)

    print(f"\nExported lengths:")
    print(f"  - Notes (.md):    {len(notes_md)} characters")
    print(f"  - Revision (.md): {len(rev_md)} characters")
    print(f"  - Code (.py):     {len(code_py)} characters")

    notes_path = os.path.join(temp_dir, "notes.md")
    rev_path = os.path.join(temp_dir, "revision.md")
    code_path = os.path.join(temp_dir, "code.py")

    with open(notes_path, "w", encoding="utf-8") as f:
        f.write(notes_md)
    with open(rev_path, "w", encoding="utf-8") as f:
        f.write(rev_md)
    with open(code_path, "w", encoding="utf-8") as f:
        f.write(code_py)

    print(f"\nSaved exported files to: {temp_dir}/")

    print("\n" + "=" * 60)
    print("RUN 2: Executing pipeline again (verifying cache hit)...")
    print("=" * 60)
    t1 = time.time()
    progress_log.clear()
    result2 = run_pipeline(
        video_url=test_video_url,
        folder="",
        notebook_file="",
        segment_minutes=5,
        resolution="LOW",
        progress=on_progress,
        db_path=test_db,
    )
    run2_duration = time.time() - t1
    print(f"Run 2 completed in {run2_duration:.2f}s")
    assert run2_duration < 5.0, f"Run 2 was expected to be fast from cache, took {run2_duration}s"
    print("Cache hit confirmed: Run 2 was served immediately from database!")

    print("\n" + "=" * 60)
    print("FIRST 40 LINES OF EXPORTED NOTES FILE:")
    print("=" * 60)
    lines = notes_md.split("\n")
    for idx, line in enumerate(lines[:40], start=1):
        print(f"{idx:2d} | {line}")

    # Cleanup temp db
    if os.path.exists(test_db):
        os.remove(test_db)


if __name__ == "__main__":
    test_backend_run()
