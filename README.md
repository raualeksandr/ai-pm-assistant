# AI PM Assistant

AI PM Assistant is a lightweight Streamlit application that turns meeting notes into practical project-management outputs. It is designed as an MVP for recruiters, Project Managers, Business Analysts, and Product Managers who want to quickly review project discussions, capture decisions, identify action items, flag risks, and surface unresolved questions.

The app works locally with rule-based analysis by default, supports optional OpenAI analysis when an API key is provided, transcribes audio with local Whisper, and can export reports to Markdown or a simple Notion page.

## Portfolio Value

This project demonstrates a practical AI product workflow without hiding the core logic behind heavy frameworks. It shows:

- End-to-end product thinking from raw meeting input to PM-ready outputs.
- Local-first defaults with optional AI and Notion integrations.
- Simple, readable Python modules that are easy to review in a portfolio.
- Real PM use cases: summaries, decisions, action items, risks, questions, transcripts, and exports.
- Sensible scope control: no database, auth layer, backend service, agents, or complex deployment stack.

## Features

- Paste meeting notes into a large editable text area.
- Upload `.txt` or `.md` meeting-note files.
- Upload `.mp3`, `.wav`, or `.m4a` audio files and transcribe them locally.
- Review timestamped transcript segments for audio uploads.
- Analyze notes using a simple rule-based analyzer with PM Analysis 2.0 risk extraction.
- Optional OpenAI analysis mode with rule-based fallback.
- Simple Notion export to a child page under a configured parent page.
- Extract and display:
  - Summary
  - Key decisions
  - Action items
  - Risks
  - Open questions
- Download the analysis as a Markdown report.
- Include timestamped audio transcripts in Markdown reports when available.
- Export the analysis to Notion when local Notion settings are configured.
- Keep secrets out of source control with `.env.example` and `.gitignore`.

## Demo Usage

Try this sample note in the app:

```text
The team approved the beta launch for July. Design needs to finish the onboarding screens by Friday. The payment API dependency is blocked, so the release timeline is at risk. Can support prepare the customer FAQ before launch?
```

Expected output:

- Summary of the meeting note.
- Key decision: beta launch approved.
- Action items for design and support.
- Risk related to the blocked payment API dependency.
- Open question about customer FAQ preparation.
- Markdown download, plus optional Notion export when configured.

For an audio demo, upload an `.mp3`, `.wav`, or `.m4a` file and review the timestamped transcript before exporting the report.

## Screenshots and Demo GIF

Placeholders for portfolio assets:

- `docs/screenshots/main-input.png` - note input, upload controls, and analysis mode.
- `docs/screenshots/analysis-results.png` - summary, decisions, actions, risks, and questions.
- `docs/screenshots/timestamped-transcript.png` - audio transcript with timestamps.
- `docs/screenshots/notion-export.png` - generated Notion page.
- `docs/demo.gif` - short end-to-end demo from note input to export.

## Architecture

The project is intentionally small and easy to understand:

- `app.py` contains the Streamlit user interface.
- `ai_analyzer.py` contains analysis logic.
- `audio_transcriber.py` contains local Whisper transcription logic.
- `notion_exporter.py` contains optional Notion page export logic.
- Rule-based analysis is the default path and requires no API key.
- OpenAI analysis is available as an optional mode.
- If `OPENAI_API_KEY` is missing or the OpenAI request fails, the app falls back to rule-based analysis.
- Audio transcription uses local open-source Whisper and does not call the OpenAI API.

```text
User input, uploaded text file, or uploaded audio file
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
        +-- OpenAI analyzer, optional
        |
        v
Summary, decisions, actions, risks, questions, Markdown and Notion export
```

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd ai-pm-assistant
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Optional for audio transcription: install `ffmpeg`.

Whisper requires the `ffmpeg` system binary to read `.mp3`, `.wav`, and `.m4a` files.

On Windows, one simple option is:

```bash
winget install Gyan.FFmpeg
```

After installation, restart your terminal and confirm it is available:

```bash
ffmpeg -version
```

5. Optional: configure OpenAI analysis.

Copy the example environment file and add your own API key:

```bash
copy .env.example .env
```

Then update `.env`:

```env
OPENAI_API_KEY=your_api_key_here
```

The app works without an API key by using rule-based analysis.

6. Optional: configure Notion export.

Create a Notion integration, copy its internal integration token into `.env`, share the target Notion page with that integration, and copy the target page ID into `.env`:

```env
NOTION_TOKEN=your_notion_integration_token_here
NOTION_PARENT_PAGE_ID=your_notion_parent_page_id_here
```

## Usage

1. Start the Streamlit app with the helper script on Windows:

```bat
start.bat
```

Or run Streamlit directly:

```bash
streamlit run app.py
```

2. Paste meeting notes manually, upload a `.txt` or `.md` file, or upload an audio file.

3. For audio files, choose a local Whisper model:

- `tiny`: fastest first-run option and the default MVP choice.
- `base`: better quality, but slower and larger.

4. Choose an analysis mode:

- `Rule-based analysis`: local, deterministic, and available by default.
- `OpenAI analysis`: uses the OpenAI API when `OPENAI_API_KEY` is configured.

5. Click `Analyze`.

6. Review the generated summary, key decisions, action items, risks, and open questions.

7. For audio uploads, review the timestamped transcript lines above the analysis controls.

8. Click `Download Report` to export the results as a Markdown file.

9. If Notion is configured, click `Export to Notion` to create a child page under the configured parent page.

## Future Roadmap

- Improve summary quality and formatting.
- Add owner and due-date extraction for action items.
- Add richer file handling for longer documents.
- Add report templates for different audiences.
- Add persistent analysis history.
- Add tests for the rule-based analyzer.
- Add deployment instructions.
- Add screenshots and a short demo GIF.
- Improve speaker labels for audio transcripts.

## Technologies Used

- Python
- Streamlit
- OpenAI Python SDK
- Notion Python SDK
- Open-source Whisper
- PyTorch
- python-dotenv
- Markdown export

## Repository Structure

```text
ai-pm-assistant/
+-- .env.example
+-- .gitignore
+-- README.md
+-- ai_analyzer.py
+-- audio_transcriber.py
+-- app.py
+-- notion_exporter.py
+-- requirements.txt
+-- start.bat
```

## Notes

- `.env` is intentionally ignored and should not be committed.
- `.env.example` is tracked so other contributors know which environment variables are required.
- The default rule-based analyzer keeps the MVP usable without paid API access or external services.
- Audio transcription runs locally, but the first Whisper run may download the selected model.
- Notion export is optional and uses only local `.env` configuration.
