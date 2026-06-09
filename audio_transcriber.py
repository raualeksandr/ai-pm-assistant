import os
import tempfile

import streamlit as st
import whisper


SUPPORTED_AUDIO_EXTENSIONS = (".mp3", ".wav", ".m4a")


@st.cache_resource
def load_whisper_model(model_name: str):
    return whisper.load_model(model_name)


def transcribe_audio(audio_bytes: bytes, file_name: str, model_name: str) -> str:
    suffix = get_audio_suffix(file_name)
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name

        model = load_whisper_model(model_name)
        result = model.transcribe(temp_path)
        return str(result.get("text", "")).strip()
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def get_audio_suffix(file_name: str) -> str:
    _, extension = os.path.splitext(file_name.lower())
    if extension in SUPPORTED_AUDIO_EXTENSIONS:
        return extension

    return ".mp3"
