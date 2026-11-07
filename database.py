"""Database management module for NoteScript ML."""

import sqlite3
import time


def init_db(db_path: str = "notescript.db") -> None:
    """Initialize SQLite database with required tables if they do not exist."""
    # Ensure all tables are created before the application performs queries.
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS videos (
                video_id TEXT PRIMARY KEY,
                title TEXT,
                day_label TEXT,
                duration_seconds INTEGER,
                created_at TEXT
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS segments (
                video_id TEXT,
                seg_index INTEGER,
                run_key TEXT,
                json_text TEXT,
                PRIMARY KEY (video_id, seg_index, run_key)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS revision (
                video_id TEXT,
                run_key TEXT,
                json_text TEXT,
                PRIMARY KEY (video_id, run_key)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS playlist (
                playlist_url TEXT,
                video_id TEXT,
                title TEXT,
                position INTEGER,
                fetched_at TEXT
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS github_cache (
                key TEXT PRIMARY KEY,
                json_text TEXT,
                fetched_at TEXT
            )
            """
        )
        connection.commit()
    finally:
        connection.close()


def save_video(
    video_id: str,
    title: str,
    day_label: str,
    duration_seconds: int,
    db_path: str = "notescript.db",
) -> None:
    """Save or update video metadata in the videos table."""
    # Record creation timestamp for sorting and display.
    created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO videos (video_id, title, day_label, duration_seconds, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (video_id, title, day_label, duration_seconds, created_at),
        )
        connection.commit()
    finally:
        connection.close()


def list_videos(db_path: str = "notescript.db") -> list[dict]:
    """Retrieve all saved videos from the database."""
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT video_id, title, day_label, duration_seconds, created_at
            FROM videos
            ORDER BY created_at DESC
            """
        )
        rows = cursor.fetchall()
        result = []
        # Explicit loop to construct dictionary items without list comprehensions.
        for row in rows:
            video_item = {
                "video_id": row[0],
                "title": row[1],
                "day_label": row[2],
                "duration_seconds": row[3],
                "created_at": row[4],
            }
            result.append(video_item)
        return result
    finally:
        connection.close()


def get_segment(
    video_id: str,
    seg_index: int,
    run_key: str,
    db_path: str = "notescript.db",
) -> str | None:
    """Fetch the cached JSON text of a processed video segment."""
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT json_text FROM segments
            WHERE video_id = ? AND seg_index = ? AND run_key = ?
            """,
            (video_id, seg_index, run_key),
        )
        row = cursor.fetchone()
        if row is not None:
            return row[0]
        return None
    finally:
        connection.close()


def save_segment(
    video_id: str,
    seg_index: int,
    run_key: str,
    json_text: str,
    db_path: str = "notescript.db",
) -> None:
    """Save or update processed segment JSON text in the database."""
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO segments (video_id, seg_index, run_key, json_text)
            VALUES (?, ?, ?, ?)
            """,
            (video_id, seg_index, run_key, json_text),
        )
        connection.commit()
    finally:
        connection.close()


def get_revision(
    video_id: str,
    run_key: str,
    db_path: str = "notescript.db",
) -> str | None:
    """Fetch the cached revision pack JSON text for a video and run key."""
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT json_text FROM revision
            WHERE video_id = ? AND run_key = ?
            """,
            (video_id, run_key),
        )
        row = cursor.fetchone()
        if row is not None:
            return row[0]
        return None
    finally:
        connection.close()


def save_revision(
    video_id: str,
    run_key: str,
    json_text: str,
    db_path: str = "notescript.db",
) -> None:
    """Save or update revision pack JSON text for a video and run key."""
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO revision (video_id, run_key, json_text)
            VALUES (?, ?, ?)
            """,
            (video_id, run_key, json_text),
        )
        connection.commit()
    finally:
        connection.close()


def get_cache(
    key: str,
    max_age_hours: float,
    db_path: str = "notescript.db",
) -> str | None:
    """Retrieve cached data if it exists and has not exceeded max age in hours."""
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT json_text, fetched_at FROM github_cache
            WHERE key = ?
            """,
            (key,),
        )
        row = cursor.fetchone()
        if row is None:
            return None

        json_text = row[0]
        fetched_at_str = row[1]

        # Calculate cache age in hours to verify freshness.
        try:
            fetched_time_struct = time.strptime(fetched_at_str, "%Y-%m-%d %H:%M:%S")
            fetched_epoch = time.mktime(fetched_time_struct)
        except ValueError:
            try:
                cleaned_str = fetched_at_str.replace("T", " ").replace("Z", "")
                if "." in cleaned_str:
                    cleaned_parts = cleaned_str.split(".")
                    cleaned_str = cleaned_parts[0]
                fetched_time_struct = time.strptime(cleaned_str, "%Y-%m-%d %H:%M:%S")
                fetched_epoch = time.mktime(fetched_time_struct)
            except ValueError:
                fetched_epoch = float(fetched_at_str)

        current_epoch = time.time()
        age_hours = (current_epoch - fetched_epoch) / 3600.0

        if age_hours <= max_age_hours:
            return json_text
        return None
    finally:
        connection.close()


def set_cache(
    key: str,
    text: str,
    db_path: str = "notescript.db",
) -> None:
    """Store or update cached text with current timestamp."""
    fetched_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO github_cache (key, json_text, fetched_at)
            VALUES (?, ?, ?)
            """,
            (key, text, fetched_at),
        )
        connection.commit()
    finally:
        connection.close()
