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
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id TEXT,
                video_id TEXT,
                total_questions INTEGER,
                score INTEGER,
                time_taken_seconds INTEGER,
                topic_weaknesses TEXT,
                created_at TEXT
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS generation_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day_num INTEGER,
                video_url TEXT,
                title TEXT,
                status TEXT,
                error_message TEXT,
                created_at TEXT,
                updated_at TEXT
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


def get_cached_playlist(
    playlist_url: str,
    max_age_hours: float = 24.0,
    db_path: str = "notescript.db",
) -> list[dict] | None:
    """Retrieve cached playlist items if they exist and are younger than max_age_hours."""
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT position, video_id, title, fetched_at
            FROM playlist
            WHERE playlist_url = ?
            ORDER BY position ASC
            """,
            (playlist_url,),
        )
        rows = cursor.fetchall()
        if len(rows) == 0:
            return None

        # Check age using the first row's fetched_at timestamp
        first_row = rows[0]
        fetched_at_str = first_row[3]

        try:
            fetched_time_struct = time.strptime(fetched_at_str, "%Y-%m-%d %H:%M:%S")
            fetched_epoch = time.mktime(fetched_time_struct)
        except ValueError:
            cleaned_str = fetched_at_str.replace("T", " ").replace("Z", "")
            if "." in cleaned_str:
                cleaned_parts = cleaned_str.split(".")
                cleaned_str = cleaned_parts[0]
            fetched_time_struct = time.strptime(cleaned_str, "%Y-%m-%d %H:%M:%S")
            fetched_epoch = time.mktime(fetched_time_struct)

        current_epoch = time.time()
        age_hours = (current_epoch - fetched_epoch) / 3600.0

        if age_hours > max_age_hours:
            return None

        result = []
        # Explicit loop to unpack rows into dicts without list comprehensions
        for row in rows:
            item = {
                "position": row[0],
                "video_id": row[1],
                "title": row[2],
            }
            result.append(item)
        return result
    finally:
        connection.close()


def save_cached_playlist(
    playlist_url: str,
    items: list[dict],
    db_path: str = "notescript.db",
) -> None:
    """Save playlist items to database with current timestamp."""
    fetched_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        # Clear existing rows for this playlist before inserting refreshed items
        cursor.execute("DELETE FROM playlist WHERE playlist_url = ?", (playlist_url,))
        for item in items:
            cursor.execute(
                """
                INSERT INTO playlist (playlist_url, video_id, title, position, fetched_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    playlist_url,
                    item.get("video_id", ""),
                    item.get("title", ""),
                    item.get("position", 0),
                    fetched_at,
                ),
            )
        connection.commit()
    finally:
        connection.close()


def search_notes(query: str, db_path: str = "notescript.db") -> list[dict]:
    """Search videos whose title, day_label, or segment content matches query."""
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        search_pattern = f"%{query}%"
        cursor.execute(
            """
            SELECT DISTINCT v.video_id, v.title, v.day_label, v.duration_seconds, v.created_at
            FROM videos v
            LEFT JOIN segments s ON v.video_id = s.video_id
            WHERE v.title LIKE ? OR v.day_label LIKE ? OR s.json_text LIKE ?
            ORDER BY v.created_at DESC
            """,
            (search_pattern, search_pattern, search_pattern),
        )
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(
                {
                    "video_id": row[0],
                    "title": row[1],
                    "day_label": row[2],
                    "duration_seconds": row[3],
                    "created_at": row[4],
                }
            )
        return result
    finally:
        connection.close()


def get_progress_stats(db_path: str = "notescript.db") -> dict:
    """Get overall progress stats (total videos, days covered)."""
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(DISTINCT video_id) FROM videos")
        total_videos = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(DISTINCT day_label) FROM videos WHERE day_label IS NOT NULL AND day_label != ''")
        days_covered = cursor.fetchone()[0]
        return {"total_videos": total_videos, "days_covered": days_covered}
    finally:
        connection.close()


def get_daily_activity(db_path: str = "notescript.db") -> dict:
    """Return a dict mapping date strings to count of videos processed that day."""
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT DATE(created_at) AS day, COUNT(*) AS cnt
            FROM videos
            GROUP BY DATE(created_at)
            ORDER BY day ASC
            """
        )
        rows = cursor.fetchall()
        result = {}
        for row in rows:
            result[row[0]] = row[1]
        return result
    finally:
        connection.close()


def save_quiz_result(
    quiz_id: str,
    video_id: str,
    total_questions: int,
    score: int,
    time_taken_seconds: int,
    topic_weaknesses: str,
    db_path: str = "notescript.db",
) -> None:
    """Save a completed quiz result to the quiz_attempts table."""
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id TEXT,
                video_id TEXT,
                total_questions INTEGER,
                score INTEGER,
                time_taken_seconds INTEGER,
                topic_weaknesses TEXT,
                created_at TEXT
            )
            """
        )
        created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cursor.execute(
            """
            INSERT INTO quiz_attempts
            (quiz_id, video_id, total_questions, score, time_taken_seconds, topic_weaknesses, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (quiz_id, video_id, total_questions, score, time_taken_seconds, topic_weaknesses, created_at),
        )
        connection.commit()
    finally:
        connection.close()


def get_streak_stats(db_path: str = "notescript.db") -> dict:
    """Compute current and max daily learning streaks from video activity dates."""
    import datetime
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT DISTINCT DATE(created_at) FROM videos ORDER BY DATE(created_at) ASC"
        )
        rows = cursor.fetchall()
        if not rows:
            return {"current_streak": 0, "max_streak": 0}

        dates = []
        for row in rows:
            dates.append(datetime.date.fromisoformat(row[0]))

        # Compute max streak
        max_streak = 1
        current_run = 1
        for i in range(1, len(dates)):
            if (dates[i] - dates[i - 1]).days == 1:
                current_run += 1
                if current_run > max_streak:
                    max_streak = current_run
            else:
                current_run = 1

        # Current streak: count backwards from today
        date_set = set()
        for d in dates:
            date_set.add(d)
        today = datetime.date.today()
        current_streak = 0
        check = today
        while check in date_set:
            current_streak += 1
            check -= datetime.timedelta(days=1)

        return {"current_streak": current_streak, "max_streak": max_streak}
    finally:
        connection.close()


def get_quiz_results(db_path: str = "notescript.db") -> list[dict]:
    """Retrieve all quiz attempt results ordered by most recent first."""
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT quiz_id, video_id, total_questions, score, time_taken_seconds,
                   topic_weaknesses, created_at
            FROM quiz_attempts
            ORDER BY id DESC
            """
        )
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(
                {
                    "quiz_id": row[0],
                    "video_id": row[1],
                    "total_questions": row[2],
                    "score": row[3],
                    "time_taken_seconds": row[4],
                    "topic_weaknesses": row[5],
                    "created_at": row[6],
                }
            )
        return result
    finally:
        connection.close()


def add_to_queue(day_num: int, video_url: str, title: str, db_path: str = "notescript.db") -> int:
    """Add a new lecture video into the generation queue."""
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cursor.execute(
            """
            INSERT INTO generation_queue (day_num, video_url, title, status, error_message, created_at, updated_at)
            VALUES (?, ?, ?, 'pending', '', ?, ?)
            """,
            (day_num, video_url, title, now_str, now_str),
        )
        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()


def get_queue(db_path: str = "notescript.db") -> list[dict]:
    """Retrieve all items in the generation queue ordered by day_num."""
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id, day_num, video_url, title, status, error_message, created_at, updated_at
            FROM generation_queue
            ORDER BY day_num ASC, id ASC
            """
        )
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(
                {
                    "id": row[0],
                    "day_num": row[1],
                    "video_url": row[2],
                    "title": row[3],
                    "status": row[4],
                    "error_message": row[5],
                    "created_at": row[6],
                    "updated_at": row[7],
                }
            )
        return result
    finally:
        connection.close()


def update_queue_status(queue_id: int, status: str, error_message: str = "", db_path: str = "notescript.db") -> None:
    """Update status and optional error message for a queue item."""
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cursor.execute(
            """
            UPDATE generation_queue
            SET status = ?, error_message = ?, updated_at = ?
            WHERE id = ?
            """,
            (status, error_message, now_str, queue_id),
        )
        connection.commit()
    finally:
        connection.close()


def delete_queue_item(queue_id: int, db_path: str = "notescript.db") -> None:
    """Delete an item from the generation queue by id."""
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM generation_queue WHERE id = ?", (queue_id,))
        connection.commit()
    finally:
        connection.close()


def clear_queue(only_completed: bool = False, db_path: str = "notescript.db") -> None:
    """Clear items from the generation queue."""
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        if only_completed:
            cursor.execute("DELETE FROM generation_queue WHERE status = 'completed'")
        else:
            cursor.execute("DELETE FROM generation_queue")
        connection.commit()
    finally:
        connection.close()


def get_queue_summary(db_path: str = "notescript.db") -> dict:
    """Get counts of queue items grouped by status."""
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT status, COUNT(*) FROM generation_queue GROUP BY status")
        rows = cursor.fetchall()
        counts = {
            "total": 0,
            "pending": 0,
            "in_progress": 0,
            "completed": 0,
            "paused_quota": 0,
            "failed": 0,
        }
        for row in rows:
            st_name = row[0]
            st_count = row[1]
            if st_name in counts:
                counts[st_name] = st_count
            counts["total"] = counts["total"] + st_count
        return counts
    finally:
        connection.close()

