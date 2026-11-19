"""GitHub synchronization module for NoteScript ML."""
import base64
import json
import os
import urllib.error
import urllib.request


def get_github_token() -> str:
    """Retrieve GitHub token from environment variables."""
    return os.getenv("GITHUB_TOKEN", "").strip()


def get_github_repo() -> str:
    """Retrieve GitHub target repository slug (owner/repo)."""
    return os.getenv("GITHUB_REPO", "NotRugved/notescript-ml").strip()


def get_remote_file_sha(file_path: str = "notescript.db") -> str:
    """Fetch the current git blob SHA for a file on GitHub if it exists."""
    token = get_github_token()
    repo = get_github_repo()
    if not token or not repo:
        return ""

    url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
    headers = {
        "Authorization": f"token {token}",
        "User-Agent": "NoteScriptML",
        "Accept": "application/vnd.github.v3+json",
    }
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            if response.status == 200:
                payload = json.loads(response.read().decode("utf-8"))
                return payload.get("sha", "")
    except Exception:
        return ""
    return ""


def push_db_to_github(db_path: str = "notescript.db") -> tuple[bool, str]:
    """Push local SQLite database to GitHub repository via Contents API."""
    token = get_github_token()
    repo = get_github_repo()
    if not token:
        return False, "GITHUB_TOKEN not configured."
    if not repo:
        return False, "GITHUB_REPO not configured."
    if not os.path.exists(db_path):
        return False, f"Local database file {db_path} does not exist."

    # Read binary database file
    try:
        with open(db_path, "rb") as db_file:
            db_bytes = db_file.read()
    except Exception as read_err:
        return False, f"Failed reading database file: {read_err}"

    b64_content = base64.b64encode(db_bytes).decode("utf-8")
    existing_sha = get_remote_file_sha("notescript.db")

    body_dict = {
        "message": "sync: update notescript.db with new lecture notes [skip ci]",
        "content": b64_content,
        "branch": "main",
    }
    if existing_sha:
        body_dict["sha"] = existing_sha

    serialized_data = json.dumps(body_dict).encode("utf-8")
    url = f"https://api.github.com/repos/{repo}/contents/notescript.db"
    headers = {
        "Authorization": f"token {token}",
        "User-Agent": "NoteScriptML",
        "Content-Type": "application/json",
        "Accept": "application/vnd.github.v3+json",
    }
    request = urllib.request.Request(url, data=serialized_data, method="PUT", headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            if response.status in (200, 201):
                return True, "Database successfully committed to GitHub."
            return False, f"GitHub returned HTTP status {response.status}"
    except urllib.error.HTTPError as http_err:
        if http_err.code == 403:
            return (
                False,
                "GitHub 403 Forbidden: Ensure your GITHUB_TOKEN has 'Contents: Read and write' permission.",
            )
        return False, f"GitHub sync failed (HTTP {http_err.code}): {http_err.reason}"
    except Exception as exc:
        return False, f"GitHub sync network error: {exc}"


def pull_db_from_github(target_path: str = "notescript.db") -> tuple[bool, str]:
    """Download the latest database from GitHub if local file is missing or empty."""
    token = get_github_token()
    repo = get_github_repo()
    if not token or not repo:
        return False, "Missing GITHUB_TOKEN or GITHUB_REPO."

    url = f"https://api.github.com/repos/{repo}/contents/notescript.db"
    headers = {
        "Authorization": f"token {token}",
        "User-Agent": "NoteScriptML",
        "Accept": "application/vnd.github.v3+json",
    }
    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            if response.status != 200:
                return False, f"GitHub returned HTTP status {response.status}"
            meta = json.loads(response.read().decode("utf-8"))
    except Exception as err:
        return False, f"Failed fetching file metadata: {err}"

    download_url = meta.get("download_url", "")
    content_b64 = meta.get("content", "")

    try:
        if download_url:
            raw_req = urllib.request.Request(download_url, headers={"User-Agent": "NoteScriptML"})
            with urllib.request.urlopen(raw_req, timeout=30) as raw_resp:
                raw_bytes = raw_resp.read()
        elif content_b64:
            raw_bytes = base64.b64decode(content_b64)
        else:
            return False, "No downloadable content found in GitHub response."

        with open(target_path, "wb") as out_file:
            out_file.write(raw_bytes)
        return True, "Database successfully restored from GitHub."
    except Exception as write_err:
        return False, f"Failed writing database file: {write_err}"
