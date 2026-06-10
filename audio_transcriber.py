import os
import tempfile

import streamlit as st
import whisper


SUPPORTED_AUDIO_EXTENSIONS = (".mp3", ".wav", ".m4a")
DEFAULT_SPEAKER = "Speaker 1"


@st.cache_resource
def load_whisper_model(model_name: str):
    return whisper.load_model(model_name)


def transcribe_audio(
    audio_bytes: bytes,
    file_name: str,
    model_name: str,
) -> tuple[str, list[dict[str, str | float]]]:
    suffix = get_audio_suffix(file_name)
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name

        model = load_whisper_model(model_name)
        result = model.transcribe(temp_path)
        transcript_text = str(result.get("text", "")).strip()
        segments = build_transcript_segments(result.get("segments", []))
        return transcript_text, segments
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def build_transcript_segments(raw_segments: list[dict]) -> list[dict[str, str | float]]:
    segments = []

    for segment in raw_segments:
        text = str(segment.get("text", "")).strip()
        if not text:
            continue

        segments.append(
            {
                "start": float(segment.get("start", 0)),
                "end": float(segment.get("end", 0)),
                "text": text,
                "speaker": DEFAULT_SPEAKER,
            }
        )

    return segments


def format_timestamp(seconds: float) -> str:
    total_seconds = max(0, int(seconds))
    minutes = total_seconds // 60
    remaining_seconds = total_seconds % 60
    return f"{minutes:02d}:{remaining_seconds:02d}"


def get_audio_suffix(file_name: str) -> str:
    _, extension = os.path.splitext(file_name.lower())
    if extension in SUPPORTED_AUDIO_EXTENSIONS:
        return extension

    return ".mp3"
