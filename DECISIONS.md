# Decision Log

## 1. Local-first architecture instead of cloud-first

- Decision: Build the project as a local-first application before adding hosted services.
- Date: 2026-06-10
- Status: Accepted
- Context: The MVP needs to be easy to run, inexpensive to test, and safe for users who may process sensitive meeting notes or audio.
- Alternatives Considered: Cloud-first web app, hosted backend API, managed transcription pipeline, database-backed SaaS architecture.
- Reasoning: Local-first keeps setup simple, reduces operating cost, avoids premature infrastructure work, and gives users more control over meeting data.
- Consequences: The app is easier to prototype and trust, but collaboration, persistence, multi-device access, and centralized administration will require later architecture work.

## 2. Whisper instead of OpenAI Transcription API

- Decision: Use local open-source Whisper for audio transcription.
- Date: 2026-06-10
- Status: Accepted
- Context: The app supports audio upload and needs transcription without requiring paid API access for every user.
- Alternatives Considered: OpenAI Transcription API, third-party speech-to-text services, browser-based speech recognition, manual transcript upload only.
- Reasoning: Local Whisper supports the local-first direction, works without an API key, and keeps audio processing on the user's machine.
- Consequences: Audio privacy and offline usability improve, but users must install `ffmpeg`, initial model downloads can be slow, and performance depends on local hardware.

## 3. Streamlit for MVP UI

- Decision: Use Streamlit for the first working user interface.
- Date: 2026-06-10
- Status: Accepted
- Context: The project needs a functional interface for text input, file upload, audio upload, analysis controls, result display, and report download.
- Alternatives Considered: Flask, FastAPI with a separate frontend, React/Next.js, desktop UI frameworks.
- Reasoning: Streamlit allows rapid development of data-oriented workflows with minimal UI boilerplate, which fits the current MVP stage.
- Consequences: The product can move quickly, but advanced UI customization, complex routing, and product-grade interaction design may eventually require a different frontend.

## 4. GitHub as the source of truth

- Decision: Use GitHub as the canonical source for project code and documentation.
- Date: 2026-06-10
- Status: Accepted
- Context: The project needs a clear collaboration and continuity model as documentation, roadmap, and implementation evolve.
- Alternatives Considered: Local-only development, cloud drive folders, Notion as the primary project source, separate code and documentation systems.
- Reasoning: GitHub provides version history, branches, pull requests, issue tracking, and a familiar workflow for future contributors.
- Consequences: Contributors should keep project decisions, roadmap, setup instructions, and code changes in the repository. Product planning may live elsewhere later, but repo documentation should remain authoritative for implementation context.

## 5. Notion before Jira

- Decision: Prioritize Notion integration before Jira integration.
- Date: 2026-06-10
- Status: Proposed
- Context: The near-term product is focused on meeting reports, searchable history, and lightweight PM artifacts rather than enterprise issue tracking.
- Alternatives Considered: Jira first, Linear first, Trello first, no external workspace integration.
- Reasoning: Notion is better aligned with flexible meeting notes, PM summaries, databases, and knowledge capture. Jira is valuable for engineering execution, but it requires more structured issue schemas and workflow assumptions.
- Consequences: Early integrations will favor documentation and meeting history. Jira support can be added later once extracted action items, risks, dependencies, and user stories have a stable internal schema.

## 6. Markdown export as the primary output format

- Decision: Use Markdown as the primary export format for generated meeting reports.
- Date: 2026-06-10
- Status: Accepted
- Context: The MVP needs a portable output that users can save, share, edit, and paste into other tools.
- Alternatives Considered: PDF, DOCX, HTML, Notion-only export, database-only storage.
- Reasoning: Markdown is simple to generate, readable as plain text, version-control friendly, and compatible with GitHub, Notion, documentation tools, and many editors.
- Consequences: Export remains lightweight and maintainable, but advanced formatting, branding, comments, and rich document layouts will require additional export formats later.

## 7. Rule-based analysis as fallback when AI is unavailable

- Decision: Keep rule-based analysis as the fallback path when OpenAI analysis is unavailable.
- Date: 2026-06-10
- Status: Accepted
- Context: The app should remain usable when `OPENAI_API_KEY` is missing, the OpenAI request fails, or the user wants local-only behavior.
- Alternatives Considered: Require AI analysis, disable analysis without an API key, use a local LLM immediately, return an error instead of fallback results.
- Reasoning: A deterministic fallback improves reliability, supports the local-first principle, and lets users test the product without external services.
- Consequences: Users always receive some output, but fallback quality is limited by keyword matching and simple sentence splitting. Future work should improve extraction quality while preserving graceful degradation.
