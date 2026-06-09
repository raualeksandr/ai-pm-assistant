# AI PM Assistant

AI PM Assistant is a lightweight Streamlit application that turns meeting notes into practical project-management outputs. It is designed as an MVP for recruiters, Project Managers, Business Analysts, and Product Managers who want to quickly review project discussions, capture decisions, identify action items, and surface unresolved questions.

The current version supports rule-based analysis by default and includes OpenAI integration support for future AI-powered analysis when an API key is provided locally.

## Features

- Paste meeting notes into a large editable text area.
- Upload `.txt` or `.md` meeting-note files.
- Upload `.mp3`, `.wav`, or `.m4a` audio files and transcribe them locally.
- Analyze notes using a simple rule-based analyzer.
- Optional OpenAI analysis mode with rule-based fallback.
- Extract and display:
  - Summary
  - Key decisions
  - Action items
  - Open questions
- Download the analysis as a Markdown report.
- Keep secrets out of source control with `.env.example` and `.gitignore`.

## Architecture

The project is intentionally small and easy to understand:

- `app.py` contains the Streamlit user interface.
- `ai_analyzer.py` contains analysis logic.
- `audio_transcriber.py` contains local Whisper transcription logic.
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
Summary, decisions, actions, questions, Markdown export
```

## Screenshots

Screenshots will be added as the UI evolves.

Suggested placeholders:

- Main note input screen
- Analysis results screen
- Markdown report download flow

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

4. Install `ffmpeg` for local audio transcription.

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

## Usage

1. Start the Streamlit app:

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

6. Review the generated summary, key decisions, action items, and open questions.

7. Click `Download Report` to export the results as a Markdown file.

## Future Roadmap

- Improve summary quality and formatting.
- Add owner and due-date extraction for action items.
- Add richer file handling for longer documents.
- Add report templates for different audiences.
- Add persistent analysis history.
- Add tests for the rule-based analyzer.
- Add deployment instructions.
- Add screenshots and a short demo GIF.
- Add speaker labels and timestamps for audio transcripts.

## Technologies Used

- Python
- Streamlit
- OpenAI Python SDK
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
+-- requirements.txt
```

## Notes

- `.env` is intentionally ignored and should not be committed.
- `.env.example` is tracked so other contributors know which environment variables are required.
- The default rule-based analyzer keeps the MVP usable without paid API access or external services.
- Audio transcription runs locally, but the first Whisper run may download the selected model.
