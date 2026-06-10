from datetime import datetime

import streamlit as st

from ai_analyzer import analyze_rule_based, analyze_with_openai, has_openai_api_key
from audio_transcriber import format_timestamp, transcribe_audio
from notion_exporter import export_analysis_to_notion


TranscriptSegment = dict[str, str | float]


def render_list(items: list[str]) -> None:
    for item in items:
        st.markdown(f"- {item}")


def format_markdown_list(items: list[str]) -> str:
    if not items:
        return "- None found"

    return "\n".join(f"- {item}" for item in items)


def format_transcript_segment(segment: TranscriptSegment) -> str:
    start = format_timestamp(float(segment.get("start", 0)))
    end = format_timestamp(float(segment.get("end", 0)))
    speaker = str(segment.get("speaker", "Speaker 1"))
    text = str(segment.get("text", "")).strip()
    return f"[{start} - {end}] {speaker}: {text}"


def format_markdown_transcript(segments: list[TranscriptSegment]) -> str:
    return "\n".join(format_transcript_segment(segment) for segment in segments)


def build_markdown_report(
    analysis: dict[str, str | list[str]],
    transcript_segments: list[TranscriptSegment] | None = None,
) -> str:
    sections = ["# Meeting Report"]

    if transcript_segments:
        sections.extend(
            [
                "## Transcript",
                format_markdown_transcript(transcript_segments),
            ]
        )

    sections.extend(
        [
            "## Summary",
            str(analysis["summary"]),
            "## Key decisions",
            format_markdown_list(analysis["key_decisions"]),
            "## Action items",
            format_markdown_list(analysis["action_items"]),
            "## Risks",
            format_markdown_list(analysis["risks"]),
            "## Open questions",
            format_markdown_list(analysis["open_questions"]),
        ]
    )

    return "\n\n".join(sections)


st.set_page_config(page_title="AI Project Manager Assistant", page_icon="PM")

st.title("AI Project Manager Assistant")
st.write("Paste meeting notes below and analyze them into project-management outputs.")

if "meeting_notes" not in st.session_state:
    st.session_state["meeting_notes"] = ""

if "transcript_segments" not in st.session_state:
    st.session_state["transcript_segments"] = []

if "transcript_text" not in st.session_state:
    st.session_state["transcript_text"] = ""

if "analysis" not in st.session_state:
    st.session_state["analysis"] = None

if "analysis_source_text" not in st.session_state:
    st.session_state["analysis_source_text"] = ""

if "analysis_transcript_segments" not in st.session_state:
    st.session_state["analysis_transcript_segments"] = []

uploaded_file = st.file_uploader(
    "Upload meeting notes",
    type=["txt", "md"],
)

if uploaded_file is not None:
    text_file_signature = (uploaded_file.name, uploaded_file.size)
    if st.session_state.get("last_text_file") != text_file_signature:
        st.session_state["meeting_notes"] = uploaded_file.getvalue().decode(
            "utf-8",
            errors="replace",
        )
        st.session_state["transcript_segments"] = []
        st.session_state["transcript_text"] = ""
        st.session_state["analysis"] = None
        st.session_state["analysis_source_text"] = ""
        st.session_state["analysis_transcript_segments"] = []
        st.session_state["last_text_file"] = text_file_signature

    st.caption(f"Uploaded file: {uploaded_file.name}")

whisper_model = st.selectbox(
    "Transcription model",
    ["tiny", "base"],
)

uploaded_audio = st.file_uploader(
    "Upload audio meeting notes",
    type=["mp3", "wav", "m4a"],
)

if uploaded_audio is not None:
    st.caption(f"Uploaded audio file: {uploaded_audio.name}")
    audio_file_signature = (uploaded_audio.name, uploaded_audio.size, whisper_model)
    if st.session_state.get("last_audio_file") != audio_file_signature:
        with st.spinner("Transcribing audio locally..."):
            try:
                transcript_text, transcript_segments = transcribe_audio(
                    uploaded_audio.getvalue(),
                    uploaded_audio.name,
                    whisper_model,
                )
                st.session_state["meeting_notes"] = transcript_text
                st.session_state["transcript_text"] = transcript_text
                st.session_state["transcript_segments"] = transcript_segments
                st.session_state["analysis"] = None
                st.session_state["analysis_source_text"] = ""
                st.session_state["analysis_transcript_segments"] = []
                st.session_state["last_audio_file"] = audio_file_signature
            except Exception as error:
                st.error(
                    "Audio transcription failed. Make sure ffmpeg is installed and "
                    "available on your PATH."
                )
                st.caption(f"Details: {error}")

meeting_notes = st.text_area(
    "Meeting notes",
    key="meeting_notes",
    height=300,
    placeholder="Paste meeting notes here...",
)

current_transcript_segments = (
    st.session_state["transcript_segments"]
    if meeting_notes == st.session_state.get("transcript_text")
    else []
)

if current_transcript_segments:
    st.subheader("Transcript with timestamps")
    for segment in current_transcript_segments:
        st.write(format_transcript_segment(segment))

analysis_mode = st.radio(
    "Analysis mode",
    ["Rule-based analysis", "OpenAI analysis"],
    horizontal=True,
)

if st.button("Analyze", type="primary"):
    if not meeting_notes.strip():
        st.warning("Please paste meeting notes before analyzing.")
    else:
        if analysis_mode == "OpenAI analysis":
            if has_openai_api_key():
                try:
                    analysis = analyze_with_openai(meeting_notes)
                except Exception as error:
                    st.warning(
                        "OpenAI analysis failed. Showing rule-based analysis instead."
                    )
                    st.caption(f"Details: {error}")
                    analysis = analyze_rule_based(meeting_notes)
            else:
                st.warning(
                    "OPENAI_API_KEY is missing. Add it to a local .env file to use "
                    "OpenAI analysis. Showing rule-based analysis instead."
                )
                analysis = analyze_rule_based(meeting_notes)
        else:
            analysis = analyze_rule_based(meeting_notes)

        st.session_state["analysis"] = analysis
        st.session_state["analysis_source_text"] = meeting_notes
        st.session_state["analysis_transcript_segments"] = current_transcript_segments

analysis = (
    st.session_state["analysis"]
    if meeting_notes == st.session_state.get("analysis_source_text")
    else None
)

if analysis:
    st.subheader("Summary")
    st.write(analysis["summary"])

    st.subheader("Key decisions")
    render_list(analysis["key_decisions"])

    st.subheader("Action items")
    render_list(analysis["action_items"])

    st.subheader("Risks")
    render_list(analysis["risks"])

    st.subheader("Open questions")
    render_list(analysis["open_questions"])

    analysis_transcript_segments = st.session_state["analysis_transcript_segments"]
    report = build_markdown_report(analysis, analysis_transcript_segments)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    st.download_button(
        "Download Report",
        data=report,
        file_name=f"meeting_report_{timestamp}.md",
        mime="text/markdown",
    )

    if st.button("Export to Notion"):
        result = export_analysis_to_notion(
            analysis,
            transcript_segments=analysis_transcript_segments,
        )
        if result["success"]:
            st.success(f"Exported to Notion: {result['url']}")
        else:
            st.error(result["error"])
