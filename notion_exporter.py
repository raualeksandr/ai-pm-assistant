import os
from datetime import datetime
from typing import Any

from dotenv import load_dotenv


Analysis = dict[str, str | list[str]]
TranscriptSegment = dict[str, str | float]


def load_notion_config() -> dict[str, str | None]:
    load_dotenv()

    token = os.getenv("NOTION_TOKEN")
    parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID")
    missing = []

    if not token:
        missing.append("NOTION_TOKEN")

    if not parent_page_id:
        missing.append("NOTION_PARENT_PAGE_ID")

    error = None
    if missing:
        error = "Missing Notion configuration: " + ", ".join(missing)

    return {
        "token": token,
        "parent_page_id": parent_page_id,
        "error": error,
    }


def export_analysis_to_notion(
    analysis: Analysis,
    transcript_segments: list[TranscriptSegment] | None = None,
    title: str | None = None,
) -> dict[str, Any]:
    config = load_notion_config()
    if config["error"]:
        return {"success": False, "error": config["error"]}

    try:
        from notion_client import Client
    except ImportError:
        return {
            "success": False,
            "error": "notion-client is not installed. Run pip install -r requirements.txt.",
        }

    page_title = title or (
        f"Meeting Analysis - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

    try:
        notion = Client(auth=config["token"])
        page = notion.pages.create(
            parent={"page_id": config["parent_page_id"]},
            properties={
                "title": {
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": page_title},
                        }
                    ]
                }
            },
        )

        blocks = build_analysis_blocks(analysis, transcript_segments or [])
        for block_batch in chunk_blocks(blocks):
            notion.blocks.children.append(page["id"], children=block_batch)

        return {
            "success": True,
            "url": page.get("url", ""),
            "error": None,
        }
    except Exception as error:
        return {
            "success": False,
            "error": f"Notion export failed: {error}",
        }


def build_analysis_blocks(
    analysis: Analysis,
    transcript_segments: list[TranscriptSegment],
) -> list[dict]:
    blocks = []

    blocks.extend(section_blocks("Summary", str(analysis.get("summary", ""))))
    blocks.extend(section_blocks("Key Decisions", analysis.get("key_decisions", [])))
    blocks.extend(section_blocks("Action Items", analysis.get("action_items", [])))
    blocks.extend(section_blocks("Risks", analysis.get("risks", [])))
    blocks.extend(section_blocks("Open Questions", analysis.get("open_questions", [])))

    if transcript_segments:
        transcript_lines = [
            format_transcript_segment(segment)
            for segment in transcript_segments
        ]
        blocks.extend(section_blocks("Transcript", transcript_lines))

    return blocks


def section_blocks(title: str, items: str | list[str]) -> list[dict]:
    blocks = [heading_block(title)]

    if isinstance(items, str):
        item_list = [items]
        block_factory = paragraph_block
    else:
        item_list = items or ["None found"]
        block_factory = bulleted_list_item_block

    for item in item_list:
        text = str(item).strip() or "None found"
        for chunk in chunk_text(text):
            blocks.append(block_factory(chunk))

    return blocks


def heading_block(text: str) -> dict:
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": rich_text(text)},
    }


def paragraph_block(text: str) -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": rich_text(text)},
    }


def bulleted_list_item_block(text: str) -> dict:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": rich_text(text)},
    }


def rich_text(text: str) -> list[dict]:
    return [
        {
            "type": "text",
            "text": {"content": text},
        }
    ]


def chunk_text(text: str, limit: int = 1900) -> list[str]:
    return [text[index:index + limit] for index in range(0, len(text), limit)] or [""]


def chunk_blocks(blocks: list[dict], limit: int = 100) -> list[list[dict]]:
    return [blocks[index:index + limit] for index in range(0, len(blocks), limit)]


def format_timestamp(seconds: float) -> str:
    total_seconds = max(0, int(seconds))
    minutes = total_seconds // 60
    remaining_seconds = total_seconds % 60
    return f"{minutes:02d}:{remaining_seconds:02d}"


def format_transcript_segment(segment: TranscriptSegment) -> str:
    start = format_timestamp(float(segment.get("start", 0)))
    end = format_timestamp(float(segment.get("end", 0)))
    speaker = str(segment.get("speaker", "Speaker 1"))
    text = str(segment.get("text", "")).strip()
    return f"[{start} - {end}] {speaker}: {text}"
