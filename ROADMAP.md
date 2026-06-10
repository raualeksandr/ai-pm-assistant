# Vision

AI PM Assistant should become a practical assistant for turning meetings into clear project-management outputs. Long term, it should help teams move from raw conversations to summaries, decisions, risks, dependencies, next steps, user stories, and status updates with minimal manual cleanup. The product should remain approachable for individual users while growing toward team workflows, searchable history, and external tool integrations. The priority is reliable meeting intelligence first, then richer PM automation and product polish.

# Current Status

The project is currently a polished v1.0 Streamlit MVP. Users can paste meeting notes, upload `.txt` or `.md` notes, or upload `.mp3`, `.wav`, and `.m4a` audio files. Audio is transcribed locally with open-source Whisper, including timestamped transcript segments. Notes can be analyzed with a local rule-based analyzer or optional OpenAI analysis when `OPENAI_API_KEY` is configured. The app produces a summary, key decisions, action items, risks, open questions, a downloadable Markdown report, and an optional simple Notion page export.

# v1.0 - Meeting Intelligence MVP

Status: Done

Features:

- Done: Text input
- Done: `.txt` and `.md` upload
- Done: Audio upload (`.mp3`, `.wav`, `.m4a`)
- Done: Local Whisper transcription
- Done: Timestamped transcript segments
- Done: Summary generation
- Done: Key decisions
- Done: Action items
- Done: Risks
- Done: Open questions
- Done: Markdown export
- Done: Optional OpenAI analysis with fallback
- Done: Simple Notion page export
- Done: `start.bat` for one-click local launch

Priority notes:

- v1.0 is intentionally simple and portfolio-friendly.
- The app avoids databases, authentication, OAuth, Docker, LangChain, vector databases, agents, and backend services.
- Future work should improve reliability and polish without changing the lightweight architecture.

# Milestone 2 - Meeting Intelligence Pro

Status: Planned

Features:

- Speaker diarization
- Better meeting segmentation
- Improved transcript cleaning
- Multi-language support

Priority notes:

- Start with transcript cleaning and segmentation before diarization.
- Timestamped segments are already available in v1.0; this milestone should focus on improving transcript quality and speaker handling.
- Treat multi-language support as a quality and configuration task, not only a UI option.

# Milestone 3 - PM Assistant

Status: Partially Done

Features:

- Done: Risks extraction
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

Status: Partially Done

Features:

- Done: Create simple Notion pages manually from an analyzed meeting
- Sync meeting reports
- Meeting database
- Searchable meeting history

Priority notes:

- Manual export to a Notion page is complete in v1.0.
- Define a stable internal report schema before implementing Notion database sync.
- Searchable history should depend on stored meeting records, not only generated Markdown files.

# Milestone 5 - Productization

Status: Partially Done

Features:

- setup.bat
- Done: start.bat
- Windows packaging
- Better UI/UX
- Settings page
- Error handling

Priority notes:

- Add `setup.bat` before full Windows packaging; `start.bat` is already available for local launch.
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

1. Add automated tests for `ai_analyzer.py`, `audio_transcriber.py`, and `notion_exporter.py`.
2. Improve audio transcription error handling by detecting missing `ffmpeg`, unsupported/empty transcription results, and Whisper model load failures with clear user-facing messages.
3. Add `setup.bat` for first-time Windows setup.
4. Add real screenshots and a short demo GIF to replace README placeholders.
5. Extend action items with owner and due date while keeping a simple fallback path.
