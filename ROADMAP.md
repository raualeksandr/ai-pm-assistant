# Vision

AI PM Assistant should become a practical assistant for turning meetings into clear project-management outputs. Long term, it should help teams move from raw conversations to summaries, decisions, risks, dependencies, next steps, user stories, and status updates with minimal manual cleanup. The product should remain approachable for individual users while growing toward team workflows, searchable history, and external tool integrations. The priority is reliable meeting intelligence first, then richer PM automation and product polish.

# Current Status

The project is currently a Streamlit MVP. Users can paste meeting notes, upload `.txt` or `.md` notes, or upload `.mp3`, `.wav`, and `.m4a` audio files. Audio is transcribed locally with open-source Whisper, using selectable `tiny` or `base` models. Notes can be analyzed with a local rule-based analyzer or optional OpenAI analysis when `OPENAI_API_KEY` is configured. The app currently produces a summary, key decisions, action items, open questions, and a downloadable Markdown report.

# Milestone 1 - Meeting Intelligence MVP

Status: In Progress

Features:

- Audio upload (mp3, wav, m4a)
- Local Whisper transcription
- Summary generation
- Action items
- Decisions
- Open questions
- Markdown export

Priority notes:

- Most feature pieces are implemented.
- The milestone should be considered complete after basic analyzer tests, clearer transcription errors, and a quick manual validation pass for text upload, audio upload, OpenAI fallback, and Markdown export.

# Milestone 2 - Meeting Intelligence Pro

Status: Planned

Features:

- Speaker diarization
- Timestamps
- Better meeting segmentation
- Improved transcript cleaning
- Multi-language support

Priority notes:

- Start with transcript cleaning and segmentation before diarization.
- Add timestamps before speaker diarization if using Whisper segment output.
- Treat multi-language support as a quality and configuration task, not only a UI option.

# Milestone 3 - PM Assistant

Status: Planned

Features:

- Risks extraction
- Dependencies extraction
- Next steps generation
- Stakeholder identification
- User stories
- Acceptance criteria
- Project status summary

Priority notes:

- Extend the analyzer output schema before changing the UI heavily.
- Add risks, dependencies, and next steps before user stories and acceptance criteria.
- Project status summaries should use the richer extracted fields once they exist.

# Milestone 4 - Notion Integration

Status: Planned

Features:

- Create Notion pages automatically
- Sync meeting reports
- Meeting database
- Searchable meeting history

Priority notes:

- Define a stable internal report schema before implementing Notion sync.
- Start with manual export to a Notion page, then add database sync.
- Searchable history should depend on stored meeting records, not only generated Markdown files.

# Milestone 5 - Productization

Status: Planned

Features:

- setup.bat
- start.bat
- Windows packaging
- Better UI/UX
- Settings page
- Error handling

Priority notes:

- Add `setup.bat` and `start.bat` before full Windows packaging.
- Move API key, model choice, and transcription settings into a settings page once the app has more configuration.
- Improve error handling continuously, but reserve packaging work until the MVP flow is stable.

# Backlog

Nice-to-have ideas:

- Zoom integration
- Google Meet integration
- Calendar integration
- Team workspaces
- Local LLM support
- Desktop application

# Next Sprint

1. Add automated tests for `ai_analyzer.py`, covering sentence splitting, rule-based extraction, output normalization, and empty input handling.
2. Improve audio transcription error handling by detecting missing `ffmpeg`, unsupported/empty transcription results, and Whisper model load failures with clear user-facing messages.
3. Extend the analysis output and Markdown report to include structured action-item fields for owner and due date, with rule-based fallback behavior when those fields are not found.
