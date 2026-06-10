# Project Context

## 1. Project vision

AI PM Assistant is a lightweight project-management assistant for turning meeting notes into practical follow-up artifacts. The MVP is aimed at project managers, product managers, business analysts, recruiters, and other coordination-heavy roles that need to quickly extract summaries, decisions, action items, risks, and unresolved questions from raw meeting notes.

The product direction is intentionally pragmatic: keep the app usable without paid AI access, while allowing higher-quality AI analysis and simple Notion export when optional local credentials are configured.

## 2. Current architecture

The application is a small Python Streamlit app with four main modules:

- `app.py`: Streamlit UI, upload controls, analysis mode selection, results rendering, and Markdown report download.
- `ai_analyzer.py`: rule-based analysis, optional OpenAI analysis, API key loading, and normalization of model output.
- `audio_transcriber.py`: local Whisper model loading and audio transcription.
- `notion_exporter.py`: optional Notion page export using a local integration token and parent page ID.

Current data flow:

```text
Text input, uploaded text file, or uploaded audio file
        |
        v
Streamlit UI (app.py)
        |
        +-- Local Whisper transcription (audio_transcriber.py)
        |
        v
Analyzer layer (ai_analyzer.py)
        |
        +-- Rule-based analyzer
        |
        +-- Optional OpenAI analyzer
        |
        v
Rendered PM outputs and downloadable Markdown report
```

The app has no database, backend service, authentication, or persistent project storage yet.

## 3. Implemented features

- Paste meeting notes into a large Streamlit text area.
- Upload `.txt` and `.md` meeting-note files.
- Upload `.mp3`, `.wav`, and `.m4a` audio files.
- Transcribe uploaded audio locally with open-source Whisper.
- Store and display timestamped transcript segments for audio uploads.
- Choose between `tiny` and `base` Whisper transcription models.
- Analyze notes with a local rule-based analyzer, including PM Analysis 2.0 risk extraction.
- Optionally analyze notes with the OpenAI API when `OPENAI_API_KEY` is available.
- Fall back to rule-based analysis when OpenAI analysis is unavailable or fails.
- Extract and display:
  - Summary
  - Key decisions
  - Action items
  - Risks
  - Open questions
- Download results as a timestamped Markdown report.
- Include timestamped transcripts in Markdown exports when audio segment data is available.
- Export analysis results to a simple Notion child page when Notion settings are configured locally.
- Keep local secrets out of source control with `.env.example` and `.gitignore`.

## 4. GitHub repository status

- Local branch: `main`
- Remote tracking branch: `origin/main`
- Remote URL: `https://github.com/raualeksandr/ai-pm-assistant.git`
- Current status at the time this file was created: clean working tree, with `main` tracking `origin/main`.

No open pull request, issue tracker state, release tags, or CI status were inspected from GitHub itself. This section reflects local Git metadata only.

## 5. Current roadmap

The roadmap from the current README is:

- Improve summary quality and formatting.
- Add owner and due-date extraction for action items.
- Add richer file handling for longer documents.
- Add report templates for different audiences.
- Add persistent analysis history.
- Add tests for the rule-based analyzer.
- Add deployment instructions.
- Add screenshots and a short demo GIF.
- Add speaker labels and timestamps for audio transcripts.

Recommended near-term roadmap order:

1. Add tests around `ai_analyzer.py`.
2. Improve OpenAI response validation and error handling.
3. Add owner/due-date extraction to action items.
4. Add persistent local history or export management.
5. Add deployment documentation once the app shape is more stable.

## 6. Technical decisions and rationale

- Streamlit is used because the MVP benefits from a fast, low-boilerplate UI for file upload, text entry, analysis controls, and downloads.
- Rule-based analysis is the default so the app works offline and without an OpenAI API key.
- OpenAI analysis is optional to keep the architecture flexible and allow better extraction quality without making API access mandatory.
- OpenAI credentials are loaded from `.env` through `python-dotenv`, keeping secrets out of committed files.
- Notion credentials are also loaded from `.env`; the app creates simple child pages and does not use databases, OAuth, or sync.
- OpenAI analysis currently uses `gpt-4.1-mini`, balancing capability and cost for structured meeting-note extraction.
- OpenAI responses are requested as JSON and normalized before use, so UI rendering can rely on the same shape for both local and AI analysis.
- Audio transcription uses open-source Whisper locally, so uploaded audio is not sent to the OpenAI API by the transcription path.
- Whisper models are cached with `st.cache_resource` to avoid reloading the selected model on every Streamlit rerun.
- Temporary audio files are created for Whisper compatibility and deleted in a `finally` block.
- Markdown export is generated in-app rather than through a document service to keep the MVP simple and portable.

## 7. Next priorities

Highest-value next work:

- Add automated tests for `split_sentences`, `analyze_rule_based`, `normalize_analysis`, and `ensure_string_list`.
- Make OpenAI JSON parsing more robust if the model returns malformed or partial JSON.
- Improve transcript speaker labels beyond the current default single-speaker label.
- Add owner and due-date extraction, either rule-based first or through a richer OpenAI schema.
- Improve the report format so action items can include owner, due date, and status fields.
- Add clearer error states for missing `ffmpeg`, failed model downloads, unsupported audio, and empty transcription output.
- Add screenshots to the README once the UI stabilizes.

## 8. Known limitations

- Rule-based extraction is keyword-driven and may miss implied decisions, action items, or risks.
- The current summary is only the first two detected sentences in rule-based mode.
- OpenAI analysis does not currently use a strict structured-output schema.
- There are no automated tests yet.
- There is no persistence of uploaded files, transcripts, analyses, or reports.
- There is no authentication, multi-user model, project/workspace concept, or role-based access.
- Notion export requires a Notion integration token and a shared parent page.
- Audio transcription requires `ffmpeg` to be installed and available on `PATH`.
- The first local Whisper run may download model weights and can be slow.
- Larger audio files may be slow or memory-intensive depending on the machine.
- Transcript timestamps are available for local Whisper audio uploads.
- Speaker labels currently default to `Speaker 1`; real diarization is not implemented.
- The UI is functional but still MVP-level; no screenshots or polished empty/loading states are committed yet.

## 9. Setup instructions

1. Clone the repository:

```bash
git clone https://github.com/raualeksandr/ai-pm-assistant.git
cd ai-pm-assistant
```

2. Create and activate a virtual environment on Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Install `ffmpeg` for local audio transcription.

On Windows:

```bash
winget install Gyan.FFmpeg
```

Then restart the terminal and verify:

```bash
ffmpeg -version
```

5. Optional: configure OpenAI analysis.

```bash
copy .env.example .env
```

Edit `.env`:

```env
OPENAI_API_KEY=your_api_key_here
NOTION_TOKEN=your_notion_integration_token_here
NOTION_PARENT_PAGE_ID=your_notion_parent_page_id_here
```

6. Run the app:

```bash
streamlit run app.py
```

The app remains usable without `.env` or `OPENAI_API_KEY` by using rule-based analysis.

## 10. Important implementation notes

- `st.session_state["meeting_notes"]` is the central UI state for pasted, uploaded, and transcribed notes.
- `st.session_state["transcript_segments"]` stores timestamped transcript segments for the current audio transcription.
- Uploaded text files replace the current meeting notes only when the uploaded file signature changes.
- Uploaded audio files replace the current meeting notes only when the audio file name, size, or selected Whisper model changes.
- `analyze_rule_based` returns the same logical shape as `analyze_with_openai`: `summary`, `key_decisions`, `action_items`, `risks`, and `open_questions`.
- `normalize_analysis` protects the UI from missing fields or non-list values in AI output.
- `format_markdown_list` writes `- None found` for empty sections in exported reports.
- `build_markdown_report` includes timestamped transcript lines when audio segments are available, but does not include source filename, model name, owner fields, or due dates.
- `notion_exporter.py` creates one child page with simple headings, paragraphs, and bulleted lists.
- The OpenAI client is imported lazily inside `analyze_with_openai`, so the app can still run rule-based mode even if OpenAI configuration is not used.
- `audio_transcriber.py` writes uploaded audio bytes to a temporary file because Whisper expects a file path.
- `audio_transcriber.py` converts Whisper segment output into simple `{start, end, text, speaker}` dictionaries.
- Temporary audio files are removed after transcription, even if transcription raises an exception.
- `.env` and `.env.*` are ignored, while `.env.example` remains tracked.
- The repository currently has no test runner configuration, formatter configuration, CI workflow, or deployment configuration.
