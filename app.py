from datetime import datetime

import streamlit as st

from ai_analyzer import analyze_rule_based, analyze_with_openai, has_openai_api_key


def render_list(items: list[str]) -> None:
    for item in items:
        st.markdown(f"- {item}")


def format_markdown_list(items: list[str]) -> str:
    if not items:
        return "- None found"

    return "\n".join(f"- {item}" for item in items)


def build_markdown_report(analysis: dict[str, str | list[str]]) -> str:
    return "\n\n".join(
        [
            "# Meeting Report",
            "## Summary",
            str(analysis["summary"]),
            "## Key decisions",
            format_markdown_list(analysis["key_decisions"]),
            "## Action items",
            format_markdown_list(analysis["action_items"]),
            "## Open questions",
            format_markdown_list(analysis["open_questions"]),
        ]
    )


st.set_page_config(page_title="AI Project Manager Assistant", page_icon="PM")

st.title("AI Project Manager Assistant")
st.write("Paste meeting notes below and analyze them into project-management outputs.")

meeting_notes = st.text_area(
    "Meeting notes",
    height=300,
    placeholder="Paste meeting notes here...",
)

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

        st.subheader("Summary")
        st.write(analysis["summary"])

        st.subheader("Key decisions")
        render_list(analysis["key_decisions"])

        st.subheader("Action items")
        render_list(analysis["action_items"])

        st.subheader("Open questions")
        render_list(analysis["open_questions"])

        report = build_markdown_report(analysis)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")

        st.download_button(
            "Download Report",
            data=report,
            file_name=f"meeting_report_{timestamp}.md",
            mime="text/markdown",
        )
