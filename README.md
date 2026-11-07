# NoteScript ML 🎓🕷️

> **CampusX 100 Days of ML, notes that actually stick.**

NoteScript ML is a neo-brutalist Streamlit application that transforms CampusX *"100 Days of Machine Learning"* video lectures into structured, comprehensive **Hinglish study notes** in Roman script (Hindi sentence flow with English technical terms).

It integrates directly with the official CampusX GitHub repository notebooks to extract and cross-verify code implementations, provides an interactive revision pack (flashcards, quiz, cheat sheet, interview prep), and exports downloadable study materials.

---

## ✨ Features

- **Hinglish Study Notes**: Roman script notes preserving intuitive Hindi explanations with technical English concepts. No Devanagari, no hallucinations.
- **Segmented Video Processing**: Processes lectures in 5–15 minute segments using Google's Gemini multimodal video API with start/end offsets.
- **GitHub Repository Sync**: Automatically fetches and cross-verifies code with official `.ipynb` notebooks from `campusx-official/100-days-of-machine-learning`.
- **Code Categorization**: Classifies every snippet as `official` (verified against repo notebook), `on-screen` (seen in video), or `reconstructed` (verbal description only).
- **Interactive Revision Pack**:
  - 1-line key takeaway summary
  - Cheat sheet table / bullet list
  - 15 interactive flashcards (expandable)
  - 10 interactive quiz questions with answer verification & explanations
  - 5 in-depth interview questions & model answers
- **Flexible Layouts**: Switch effortlessly between a 7-section **Tabbed View** and a multi-column **Split View**.
- **Full Exports**: One-click downloads for:
  - `main_notes.md` — Complete markdown study notes with timestamped YouTube links (`https://youtu.be/<id>?t=<sec>`).
  - `revision_pack.md` — Structured revision material.
  - `code.py` — Clean Python script containing all extracted code blocks with verification comments.
- **SQLite Persistent Caching**: Saves every segment as soon as it succeeds. Re-running a video skips completed segments instantly, allowing smooth resumes after daily quota pauses.
- **Miles Morales Neo-Brutalist Theme**: Custom dark theme with sharp `#ff2b2b` accents, hard offset shadows, jumping interactive controls, Space Mono typography, and a pure-CSS spider-web intro animation.

---

## 🚀 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/notescript-ml.git
cd notescript-ml
```

### 2. Install dependencies with `uv`
NoteScript ML is built strictly with [`uv`](https://docs.astral.sh/uv/) (no `pip`):
```bash
uv sync
```

### 3. Configure environment variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Open `.env` and configure:
```env
# Required: Obtain from https://aistudio.google.com
GEMINI_API_KEY=your_key_here

# Recommended model: gemini-3.5-flash or gemini-3.8-flash
GEMINI_MODEL=gemini-3.5-flash

# Optional: CampusX 100 Days of Machine Learning Playlist URL
PLAYLIST_URL=https://www.youtube.com/playlist?list=PLKnIA16_Rmvbr7zKYQuBfsVkjoLcJgxHH

# Optional: GitHub Personal Access Token (avoids GitHub API 60 req/hr rate limits)
GITHUB_TOKEN=
```

---

## 💻 How to Run

Launch the Streamlit app using `uv run`:
```bash
uv run streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 📖 How to Use

### Mode 1: Video Link
1. Select **"Video link"** on the main screen.
2. Paste any YouTube URL (`watch?v=`, `youtu.be/`, `embed/`, or `shorts/`).
3. (Optional) Choose the matching folder in the CampusX GitHub repository and select the target `.ipynb` notebook.
4. Click **"Generate Study Notes"**.

### Mode 2: Day Number
1. Select **"Day number"**.
2. Enter a lecture day number (1 to 100).
3. Confirm or paste the playlist URL, then click **"Find videos"**.
4. The app retrieves matching playlist entries and presents candidates in a dropdown — never guessing silently for the user.
5. Select your video and click **"Generate Study Notes"**.

### Library Sidebar
- All completed and partial runs are saved to the local SQLite database (`notescript.db`).
- Click any lecture title in the **📚 My Library** sidebar to instantly load all notes, flashcards, quiz, and downloads without making API calls.

---

## ⚠️ Known Limitations & Design Notes

1. **Gemini API Quota**:
   - The free-tier Gemini API has daily request/token limits (~20 requests/day on some preview models). Long lectures broken into multiple segments may reach the daily limit.
   - If quota is reached, NoteScript ML catches `QuotaExhaustedError`, sets `partial=True`, saves all completed segments in SQLite, and alerts you. Rerun the same video tomorrow and it will pick up exactly where it left off without reprocessing completed segments.
2. **Hinglish Style**:
   - Notes follow Roman script with Hindi conversational flow and English technical terms. While consistently natural, exact fluency and phrasing may vary across segments. Timestamps are absolute video times (`MM:SS`) aligned with segment boundaries.
3. **Reconstructed Code**:
   - Code labelled `reconstructed` represents concepts the instructor explained verbally without showing full code on screen or in the notebook. Review and verify reconstructed blocks before using them in production.
4. **Direct REST API Calls for YouTube URLs**:
   - YouTube video processing uses direct REST calls with start/end offset metadata, as high-level SDK wrappers can experience timeout hangs on large video URIs. Each segment typically takes 15–30 seconds on first run.
5. **GitHub API Caching**:
   - Directory structures and notebook contents from GitHub are cached in SQLite for 24 hours to stay well within GitHub's public API limits. Provide a `GITHUB_TOKEN` in `.env` if you make extensive calls.

---

## 🛠️ Tech Stack

- **Framework**: Streamlit
- **Package & Environment Management**: `uv`
- **Multimodal AI**: Google Gemini API (`gemini-3.5-flash`, `gemini-3.8-flash`) via `urllib.request` REST endpoints
- **Video Metadata & Ingestion**: `yt-dlp`
- **Database**: SQLite (`notescript.db`) with plain parameterized SQL
- **Styling**: Custom Neo-Brutalist CSS (`ui/theme.css`, `ui/intro.html`) with Google Fonts Space Mono & DM Sans
