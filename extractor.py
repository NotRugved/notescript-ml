"""Extractor module for NoteScript ML."""

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

from dotenv import load_dotenv
import yt_dlp

from database import (
    get_cache,
    get_cached_playlist,
    save_cached_playlist,
    set_cache,
)

# Load environment variables for GITHUB_TOKEN
load_dotenv()


class VideoInfo(dict):
    """Dictionary subclass supporting tuple unpacking for (title, duration_seconds, video_id)."""

    def __iter__(self):
        yield self["title"]
        yield self["duration_seconds"]
        yield self["video_id"]


def get_video_id(url: str) -> str:
    """Extract YouTube video ID from various URL formats using split and find."""
    if not url:
        return ""

    clean_url = url.strip()
    candidate = ""

    # Check for watch?v= parameter in URL
    v_pos = clean_url.find("v=")
    if v_pos != -1:
        after_v = clean_url[v_pos + 2 :]
        candidate = after_v
    # Check for short URLs like youtu.be/
    elif clean_url.find("youtu.be/") != -1:
        y_pos = clean_url.find("youtu.be/")
        after_domain = clean_url[y_pos + 9 :]
        candidate = after_domain
    # Check for shorts URLs
    elif clean_url.find("/shorts/") != -1:
        s_pos = clean_url.find("/shorts/")
        after_shorts = clean_url[s_pos + 8 :]
        candidate = after_shorts
    # Check for embed URLs
    elif clean_url.find("/embed/") != -1:
        e_pos = clean_url.find("/embed/")
        after_embed = clean_url[e_pos + 7 :]
        candidate = after_embed
    # Check if raw 11-character video ID was passed directly
    elif len(clean_url) == 11 and clean_url.find("/") == -1 and clean_url.find("?") == -1:
        candidate = clean_url

    if not candidate:
        return ""

    # Truncate at URL delimiters to strip extra parameters
    delimiters = ["&", "?", "#", "/"]
    for delim in delimiters:
        d_pos = candidate.find(delim)
        if d_pos != -1:
            candidate = candidate[:d_pos]

    candidate = candidate.strip()
    if len(candidate) == 11:
        return candidate
    return ""


def get_video_info(url: str) -> VideoInfo:
    """Extract video metadata using yt-dlp without downloading media."""
    ydl_opts = {
        "skip_download": True,
        "quiet": True,
        "no_warnings": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                raise RuntimeError(f"Could not retrieve video information for: {url}")

            title = info.get("title", "")
            duration = int(info.get("duration", 0) or 0)
            video_id = info.get("id") or get_video_id(url)

            return VideoInfo(
                {
                    "title": title,
                    "duration_seconds": duration,
                    "video_id": video_id,
                }
            )
    except Exception as error:
        raise RuntimeError(f"Failed to extract video info for {url}: {error}") from error


def plan_segments(duration_seconds: int, segment_minutes: int | float) -> list[dict]:
    """Plan segment breakdown merging small tails under 60 seconds into previous segment."""
    step_seconds = int(segment_minutes * 60)
    if duration_seconds <= 0 or step_seconds <= 0:
        return []

    segments = []
    # Loop over start times to construct non-overlapping segments
    for current_start in range(0, duration_seconds, step_seconds):
        current_end = current_start + step_seconds
        if current_end > duration_seconds:
            current_end = duration_seconds

        tail_seconds = current_end - current_start
        # Merge tiny trailing segment into the preceding one
        if tail_seconds < 60 and len(segments) > 0:
            previous_segment = segments[len(segments) - 1]
            previous_segment["end_seconds"] = current_end
        else:
            new_segment = {
                "index": len(segments),
                "start_seconds": current_start,
                "end_seconds": current_end,
            }
            segments.append(new_segment)

    return segments


def format_time(seconds: int) -> str:
    """Format seconds integer into MM:SS or H:MM:SS string."""
    total_seconds = int(seconds)
    hours = total_seconds // 3600
    remainder = total_seconds % 3600
    minutes = remainder // 60
    secs = remainder % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def parse_time(text: str) -> int | None:
    """Parse MM:SS or H:MM:SS text into seconds integer using split."""
    if not text:
        return None

    clean_text = text.strip()
    parts = clean_text.split(":")

    if len(parts) == 2:
        try:
            mins = int(parts[0])
            secs = int(parts[1])
            if mins < 0 or secs < 0 or secs >= 60:
                return None
            return mins * 60 + secs
        except ValueError:
            return None
    elif len(parts) == 3:
        try:
            hours = int(parts[0])
            mins = int(parts[1])
            secs = int(parts[2])
            if hours < 0 or mins < 0 or mins >= 60 or secs < 0 or secs >= 60:
                return None
            return hours * 3600 + mins * 60 + secs
        except ValueError:
            return None

    return None


def list_playlist(playlist_url: str, db_path: str = "notescript.db") -> list[dict]:
    """Extract flat playlist entries with position, video_id, and title, cached for 24h."""
    # Check cached playlist table first to avoid redundant network calls
    cached_items = get_cached_playlist(playlist_url, 24.0, db_path)
    if cached_items is not None and len(cached_items) > 0:
        return cached_items

    ydl_opts = {
        "extract_flat": True,
        "quiet": True,
        "no_warnings": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            if not info:
                return []

            entries = info.get("entries", [])
            items = []
            position_counter = 1
            for entry in entries:
                if entry is None:
                    continue
                v_id = entry.get("id") or ""
                v_title = entry.get("title") or ""
                if not v_id:
                    continue
                item = {
                    "position": position_counter,
                    "video_id": v_id,
                    "title": v_title,
                }
                items.append(item)
                position_counter = position_counter + 1

            if len(items) > 0:
                save_cached_playlist(playlist_url, items, db_path)
            return items
    except Exception as error:
        raise RuntimeError(f"Failed to extract playlist for {playlist_url}: {error}") from error


def _split_words(text: str) -> list[str]:
    """Split text into alphanumeric words by looping over characters."""
    words = []
    current_chars = []
    for char in text:
        # Check if character is alphanumeric
        if char.isalnum():
            current_chars.append(char)
        else:
            if len(current_chars) > 0:
                words.append("".join(current_chars))
                current_chars = []
    if len(current_chars) > 0:
        words.append("".join(current_chars))
    return words


def find_day_candidates(playlist_items: list[dict], day_number: int | str) -> list[dict]:
    """Find playlist items matching day_number word, or fallback to matching position."""
    target_str = str(day_number).strip()
    try:
        target_int = int(target_str)
        padded_str = f"{target_int:02d}"
    except ValueError:
        target_int = None
        padded_str = target_str

    matches = []
    # Search for an exact word match in each title
    for item in playlist_items:
        title = item.get("title", "")
        words = _split_words(title)
        has_match = False
        for word in words:
            if word == target_str or word == padded_str:
                has_match = True
                break
        if has_match:
            candidate = {
                "position": item.get("position"),
                "video_id": item.get("video_id"),
                "title": item.get("title"),
                "position_guess": False,
            }
            matches.append(candidate)

    if len(matches) > 0:
        return matches

    # If no title matched, fall back to matching playlist position
    if target_int is not None:
        for item in playlist_items:
            if item.get("position") == target_int:
                fallback_item = {
                    "position": item.get("position"),
                    "video_id": item.get("video_id"),
                    "title": item.get("title"),
                    "position_guess": True,
                }
                return [fallback_item]

    return []


def _github_request(url: str) -> bytes:
    """Perform an HTTP GET request using urllib with optional authorization."""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "NoteScript-ML")
    token = os.getenv("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read()
    except urllib.error.HTTPError as error:
        # Retry raw downloads without token if authorization is rejected
        if token and "raw.githubusercontent.com" in url and (error.code == 401 or error.code == 403):
            req_no_auth = urllib.request.Request(url)
            req_no_auth.add_header("User-Agent", "NoteScript-ML")
            with urllib.request.urlopen(req_no_auth, timeout=30) as retry_response:
                return retry_response.read()
        raise


def list_day_folders(db_path: str = "notescript.db") -> list[str]:
    """List top-level directory names from the official GitHub repository."""
    cache_key = "github_top_level_folders"
    cached = get_cache(cache_key, 24.0, db_path)
    if cached is not None:
        try:
            return json.loads(cached)
        except json.JSONDecodeError:
            pass

    url = "https://api.github.com/repos/campusx-official/100-days-of-machine-learning/contents/"
    raw_data = _github_request(url)
    items = json.loads(raw_data.decode("utf-8"))

    folders = []
    # Explicit loop to collect directories only
    for item in items:
        if item.get("type") == "dir":
            folders.append(item.get("name", ""))

    set_cache(cache_key, json.dumps(folders), db_path)
    return folders


def suggest_folders(day_number: int | str, folders: list[str]) -> list[str]:
    """Suggest matching folders starting with day + day_number followed by a non-digit."""
    target_str = str(day_number).strip().lower()
    prefix = "day" + target_str
    prefix_len = len(prefix)

    alt_prefix = None
    try:
        val = int(target_str)
        alt_prefix = "day" + f"{val:02d}"
    except ValueError:
        pass

    suggested = []
    # Check each folder against target prefix followed by non-digit
    for folder in folders:
        folder_lower = folder.lower().strip()
        is_match = False

        if folder_lower.startswith(prefix):
            if len(folder_lower) == prefix_len:
                is_match = True
            else:
                next_char = folder_lower[prefix_len]
                if not next_char.isdigit():
                    is_match = True

        if not is_match and alt_prefix is not None and alt_prefix != prefix:
            alt_len = len(alt_prefix)
            if folder_lower.startswith(alt_prefix):
                if len(folder_lower) == alt_len:
                    is_match = True
                else:
                    next_char = folder_lower[alt_len]
                    if not next_char.isdigit():
                        is_match = True

        if is_match:
            suggested.append(folder)

    return suggested


def list_notebooks(folder: str, db_path: str = "notescript.db") -> list[str]:
    """List .ipynb files in a specific repository folder."""
    cache_key = f"github_notebooks_{folder}"
    cached = get_cache(cache_key, 24.0, db_path)
    if cached is not None:
        try:
            return json.loads(cached)
        except json.JSONDecodeError:
            pass

    encoded_folder = urllib.parse.quote(folder)
    url = f"https://api.github.com/repos/campusx-official/100-days-of-machine-learning/contents/{encoded_folder}"
    raw_data = _github_request(url)
    items = json.loads(raw_data.decode("utf-8"))

    notebooks = []
    # Explicit loop to collect notebook files
    for item in items:
        name = item.get("name", "")
        if name.endswith(".ipynb"):
            notebooks.append(name)

    set_cache(cache_key, json.dumps(notebooks), db_path)
    return notebooks


def get_notebook_text(
    folder: str,
    filename: str,
    max_chars: int = 60000,
    db_path: str = "notescript.db",
) -> str:
    """Download and extract formatted Markdown and Code blocks from a GitHub notebook."""
    cache_key = f"github_nb_text_{folder}_{filename}_{max_chars}"
    cached = get_cache(cache_key, 24.0, db_path)
    if cached is not None:
        return cached

    encoded_folder = urllib.parse.quote(folder)
    url = f"https://api.github.com/repos/campusx-official/100-days-of-machine-learning/contents/{encoded_folder}"
    raw_folder_data = _github_request(url)
    items = json.loads(raw_folder_data.decode("utf-8"))

    download_url = None
    for item in items:
        if item.get("name") == filename:
            download_url = item.get("download_url")
            break

    if not download_url:
        encoded_filename = urllib.parse.quote(filename)
        download_url = f"https://raw.githubusercontent.com/campusx-official/100-days-of-machine-learning/main/{encoded_folder}/{encoded_filename}"

    nb_bytes = _github_request(download_url)
    nb_json = json.loads(nb_bytes.decode("utf-8"))

    cells = nb_json.get("cells", [])
    blocks = []
    # Extract source text from markdown and code cells only
    for cell in cells:
        cell_type = cell.get("cell_type", "")
        source_raw = cell.get("source", "")
        if isinstance(source_raw, list):
            source_lines = []
            for line in source_raw:
                source_lines.append(line)
            source_text = "".join(source_lines).strip()
        else:
            source_text = str(source_raw).strip()

        if not source_text:
            continue

        if cell_type == "markdown":
            block = f"## Markdown\n{source_text}"
            blocks.append(block)
        elif cell_type == "code":
            block = f"## Code\n{source_text}"
            blocks.append(block)

    full_text = "\n\n".join(blocks)
    # Truncate text if exceeding maximum character limit
    if len(full_text) > max_chars:
        truncation_note = "\n\n[Note: Official notebook content truncated at max_chars limit]"
        cut_point = max_chars - len(truncation_note)
        if cut_point > 0:
            full_text = full_text[:cut_point] + truncation_note
        else:
            full_text = full_text[:max_chars]

    set_cache(cache_key, full_text, db_path)
    return full_text
