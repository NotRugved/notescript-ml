# NoteScript ML — Project Rules (read fully before every task)

## Product
Streamlit app. User gives a CampusX "100 Days of Machine Learning" video (YouTube link, or a
day number + playlist link). App outputs detailed Hinglish study notes in separate sections,
shown as tabs or side-by-side columns, plus downloadable files:
main notes (.md), revision pack (.md), all code (.py).

## Environment
- Windows, PowerShell, `uv` only (`uv add`, `uv run`). Never pip.
- Packages: streamlit, google-genai, python-dotenv, yt-dlp. Everything else stdlib
  (json, sqlite3, urllib, time, os).
- .env keys: GEMINI_API_KEY, GEMINI_MODEL, PLAYLIST_URL, GITHUB_TOKEN (optional).
  Never hardcode secrets or the model name. .env must be in .gitignore.
- Verify any SDK syntax (google-genai, yt-dlp) against official docs or by running it.
  If unsure, say so and test. Never guess an API.

## Coding style (I am a learner reading this code)
- Explicit multi-line `for`/`while` loops. NO list comprehensions, map/filter, lambda,
  or regular expressions anywhere. Parse text with split/find/strip and loops.
- Small single-purpose functions, each with a one-line docstring.
- Short comments explaining WHY. Clear variable names. Type hints are fine.
- UI exception: ui/theme.css and ui/intro.html are the only non-Python files. Static
  CSS/HTML only, no JavaScript. app.py loads them with st.markdown(unsafe_allow_html=True).

## Files
- database.py: SQLite (notescript.db)
- extractor.py: video/playlist info (yt-dlp, no downloads), segment plan, GitHub notebooks
- ai_processor.py: all Gemini calls
- pipeline.py: orchestrates a full run, takes a progress callback
- exports.py: builds the 3 downloadable files as strings
- app.py: Streamlit UI only. No business logic.
- ui/theme.css, ui/intro.html, .streamlit/config.toml, test_backend.py

## Progress callback contract
progress(message: str, fraction: float)  # fraction 0.0 to 1.0
Messages: "Reading video info", "Loading official notebook", "Watching segment 3 of 9",
"Merging segments", "Building revision pack", "Done".

## AI behaviour
- Segment call: pass the YouTube URL as a video part with start/end offsets (a segment).
  Default 10 minutes. Default media resolution LOW; HIGH is a user toggle.
- Output is JSON only (response_mime_type application/json). Parse with json.loads;
  on failure retry once asking for valid JSON, then raise a clear error.
- Retry rate-limit/transient errors 3 times with growing sleeps. On a daily-quota error,
  stop cleanly, keep finished segments, and tell the user to resume tomorrow.
- Notes language: Hinglish in Roman script (Hindi sentence flow, English technical terms).
  Never Devanagari.
- Never invent teacher statements. Unclear audio/screen -> write "unclear in video".
- Code labels: "official" (copied from the repo notebook), "on-screen" (seen in video,
  not in notebook), "reconstructed" (only described verbally; keep minimal).
- Timestamps are ABSOLUTE video time "MM:SS" (or "H:MM:SS"). After parsing, if a timestamp
  falls outside its segment range, add the segment start offset.

## Segment JSON contract
  theory_sections: list of {heading, timestamp, content}    content = detailed Hinglish markdown
  intuition: list of {timestamp, text}
  code_blocks: list of {title, label, timestamp, explanation, code}
  analogies: list of {timestamp, analogy, explains}         only ones the teacher actually used
  common_mistakes: list of {mistake, why, fix, timestamp, source}   source: "teacher" or "added"
  formulas: list of {name, formula, meaning}
  key_terms: list of {term, meaning}

## Revision JSON contract (one text-only call over merged notes)
  one_line_summary, cheat_sheet (markdown), flashcards: list of {q, a} (15),
  quiz: list of {question, options (4), answer_index, explanation} (10),
  interview_questions: list of {q, a} (5)

## Cache rules
- segments table key: (video_id, seg_index, run_key). run_key = segment minutes + resolution
  + notebook path. Save each segment immediately after it succeeds. Reruns skip cached ones.

## Process
- Plan first, then implement. After each file, run it once. Show me what you verified.
- Commit to git after each finished step with a clear message.