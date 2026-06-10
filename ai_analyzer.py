import json
import os
import re

from dotenv import load_dotenv


ACTION_KEYWORDS = ("need to", "should", "must", "action", "task")
DECISION_KEYWORDS = ("decided", "agreed", "approved")
RISK_KEYWORDS = (
    "risk",
    "blocker",
    "issue",
    "concern",
    "problem",
    "delay",
    "dependency",
    "cannot",
    "blocked",
    "stuck",
    "at risk",
)


def split_sentences(text: str) -> list[str]:
    return [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text.strip())
        if sentence.strip()
    ]


def analyze_rule_based(text: str) -> dict[str, str | list[str]]:
    sentences = split_sentences(text)
    lowercase_sentences = [(sentence, sentence.lower()) for sentence in sentences]

    key_decisions = [
        sentence
        for sentence, lowercase_sentence in lowercase_sentences
        if any(keyword in lowercase_sentence for keyword in DECISION_KEYWORDS)
    ]
    action_items = [
        sentence
        for sentence, lowercase_sentence in lowercase_sentences
        if any(keyword in lowercase_sentence for keyword in ACTION_KEYWORDS)
    ]
    risks = [
        sentence
        for sentence, lowercase_sentence in lowercase_sentences
        if any(keyword in lowercase_sentence for keyword in RISK_KEYWORDS)
    ]
    open_questions = [
        sentence
        for sentence in sentences
        if sentence.endswith("?")
    ]

    summary_sentences = sentences[:2]
    summary = " ".join(summary_sentences)
    if not summary:
        summary = "No meeting notes were provided."

    return {
        "summary": summary,
        "key_decisions": key_decisions,
        "action_items": action_items,
        "risks": risks,
        "open_questions": open_questions,
    }


def get_openai_api_key() -> str | None:
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")


def has_openai_api_key() -> bool:
    return bool(get_openai_api_key())


def analyze_with_openai(text: str) -> dict[str, str | list[str]]:
    api_key = get_openai_api_key()
    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing.")

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "Analyze meeting notes for a project manager. Return only valid "
                    "JSON with exactly these keys: summary, key_decisions, "
                    "action_items, risks, open_questions. The summary must be a "
                    "string. The other fields must be arrays of strings."
                ),
            },
            {
                "role": "user",
                "content": text,
            },
        ],
    )

    return normalize_analysis(json.loads(response.output_text))


def normalize_analysis(analysis: dict) -> dict[str, str | list[str]]:
    normalized = {
        "summary": str(analysis.get("summary", "")).strip(),
        "key_decisions": ensure_string_list(analysis.get("key_decisions", [])),
        "action_items": ensure_string_list(analysis.get("action_items", [])),
        "risks": ensure_string_list(analysis.get("risks", [])),
        "open_questions": ensure_string_list(analysis.get("open_questions", [])),
    }

    if not normalized["summary"]:
        normalized["summary"] = "No summary was generated."

    return normalized


def ensure_string_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]

    if isinstance(value, str) and value.strip():
        return [value.strip()]

    return []
