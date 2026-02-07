import re
from typing import Any, Dict, List

from bs4 import BeautifulSoup, NavigableString, Tag


def convert_hansard_to_markdown(html_content: str) -> Dict[str, Any]:
    """
    Convert Hansard HTML content to structured markdown format.
    Handles multiple formats: old table-based (with variants) and new semantic HTML.

    Args:
        html_content: The HTML content from the Hansard API

    Returns:
        Dictionary with metadata and markdown content
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Detect format type
    has_meta_tags = bool(soup.find_all("meta", attrs={"name": True}))
    has_paragraphs = bool(soup.find_all("p"))

    if has_meta_tags and not has_paragraphs:
        # Old format (1959-2000s style with meta tags and tables)
        return _convert_old_format(soup)
    elif has_paragraphs:
        # New format (2010s-present with semantic HTML)
        return _convert_new_format(soup)
    else:
        # Fallback
        return _convert_generic_format(soup)


def _clean_text(text: str) -> str:
    """
    Clean text by removing column/page markers and extra whitespace.
    """
    # Remove column markers (e.g., "Column: 2200")
    text = re.sub(r"Column:\s*\d+", "", text)

    # Remove page markers (e.g., "Page: 63")
    text = re.sub(r"Page:\s*\d+", "", text)

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    # Remove leading nbsp entities
    text = re.sub(r"^(&nbsp;)+", "", text)

    # Trim
    text = text.strip()

    return text


def _convert_old_format(soup: BeautifulSoup) -> Dict[str, Any]:
    """Convert old table-based Hansard format (pre-2000s)"""
    metadata: Dict[str, str] = {}

    # Extract metadata from meta tags
    for meta in soup.find_all("meta"):
        name = meta.get("name")
        content = meta.get("content")
        if name and content:
            metadata[name] = content

    markdown_lines = []

    # Add metadata header
    markdown_lines.append("# Budget Speech")
    markdown_lines.append("")
    if metadata.get("Sit_Date"):
        markdown_lines.append(f"**Date:** {metadata['Sit_Date']}")
    if metadata.get("Title"):
        markdown_lines.append(f"**Title:** {metadata['Title']}")
    if metadata.get("MP_Speak"):
        markdown_lines.append(f"**Speakers:** {metadata['MP_Speak']}")
    markdown_lines.append("")
    markdown_lines.append("---")
    markdown_lines.append("")

    # Extract body content
    body = soup.find("body")
    if not body or isinstance(body, NavigableString):
        return {"metadata": metadata, "markdown": "\n".join(markdown_lines), "raw_text": ""}

    # Remove metadata tables at the beginning
    for table in body.find_all("table", limit=2):
        table.decompose()

    # Remove ALL column/page markers (font tags with size="1")
    for font in body.find_all("font", size="1"):
        font.decompose()

    # Also remove any bold tags that contain column/page markers
    for bold in body.find_all("b"):
        text = bold.get_text(strip=True)
        if text.startswith("Column:") or text.startswith("Page:"):
            bold.decompose()

    # Process content
    current_paragraph: List[str] = []

    for element in body.descendants:
        # Section headers in italics
        if isinstance(element, Tag) and element.name == "i":
            # Flush current paragraph
            if current_paragraph:
                para_text = " ".join(current_paragraph).strip()
                para_text = _clean_text(para_text)
                if para_text:
                    markdown_lines.append(para_text)
                    markdown_lines.append("")
                current_paragraph = []

            text = element.get_text(strip=True)
            text = _clean_text(text)
            if text:
                markdown_lines.append(f"## {text}")
                markdown_lines.append("")

        # Section headers in centered divs
        elif (
            isinstance(element, Tag) and element.name == "div" and element.get("align") == "center"
        ):
            # Flush current paragraph
            if current_paragraph:
                para_text = " ".join(current_paragraph).strip()
                para_text = _clean_text(para_text)
                if para_text:
                    markdown_lines.append(para_text)
                    markdown_lines.append("")
                current_paragraph = []

            text = element.get_text(strip=True)
            text = _clean_text(text)
            if text and text not in ["ANNUAL BUDGET STATEMENT", "BUDGET"]:
                markdown_lines.append(f"## {text}")
                markdown_lines.append("")

        # Speaker names (bold text with colons)
        elif isinstance(element, Tag) and element.name == "b":
            # Skip if it's a column/page marker
            text = element.get_text(strip=True)
            if text.startswith("Column:") or text.startswith("Page:"):
                continue

            # Flush current paragraph
            if current_paragraph:
                para_text = " ".join(current_paragraph).strip()
                para_text = _clean_text(para_text)
                if para_text:
                    markdown_lines.append(para_text)
                    markdown_lines.append("")
                current_paragraph = []

            text = _clean_text(text)
            if text and ":" in text:
                markdown_lines.append(f"**{text}**")
                markdown_lines.append("")

        # Line breaks
        elif isinstance(element, Tag) and element.name == "br":
            if current_paragraph:
                para_text = " ".join(current_paragraph).strip()
                para_text = _clean_text(para_text)
                if para_text and len(para_text) > 3:
                    markdown_lines.append(para_text)
                    markdown_lines.append("")
                current_paragraph = []

        # Text content
        elif isinstance(element, str):
            text = element.strip()
            # Skip empty strings, nbsp, and column/page markers
            if (
                text
                and text not in ["&nbsp;", " "]
                and not text.startswith("Column:")
                and not text.startswith("Page:")
            ):
                text = _clean_text(text)
                if text:
                    current_paragraph.append(text)

    # Flush any remaining paragraph
    if current_paragraph:
        para_text = " ".join(current_paragraph).strip()
        para_text = _clean_text(para_text)
        if para_text:
            markdown_lines.append(para_text)
            markdown_lines.append("")

    # Get clean text
    raw_text = body.get_text(separator=" ", strip=True)
    raw_text = _clean_text(raw_text)

    # Clean up markdown
    cleaned_lines = _remove_excessive_blanks(markdown_lines)

    return {"metadata": metadata, "markdown": "\n".join(cleaned_lines), "raw_text": raw_text}


def _convert_new_format(soup: BeautifulSoup) -> Dict[str, Any]:
    """Convert modern semantic HTML Hansard format (2013 onwards)"""
    metadata: Dict[str, str] = {}
    markdown_lines = []

    # Extract metadata from h6 (time) if present
    time_tag = soup.find("h6")
    if time_tag:
        metadata["time"] = time_tag.get_text(strip=True)

    # Find all paragraphs
    paragraphs = soup.find_all("p")

    # Add header
    markdown_lines.append("# Budget Speech")
    markdown_lines.append("")

    if time_tag:
        markdown_lines.append(f"**Time:** {metadata['time']}")
        markdown_lines.append("")

    markdown_lines.append("---")
    markdown_lines.append("")

    for p in paragraphs:
        # Extract speaker information from <strong> tags
        strong_tag = p.find("strong")
        if strong_tag:
            speaker = strong_tag.get_text(strip=True)
            # Remove the strong tag to get the rest of the content
            strong_tag.extract()
            content = p.get_text(strip=True)
            content = _clean_text(content)

            if speaker:
                markdown_lines.append(f"**{speaker}**")
                markdown_lines.append("")
            if content:
                markdown_lines.append(content)
                markdown_lines.append("")
        else:
            # Regular paragraph
            content = p.get_text(strip=True)
            content = _clean_text(content)
            if content:
                markdown_lines.append(content)
                markdown_lines.append("")

    # Extract clean text
    raw_text = soup.get_text(separator=" ", strip=True)
    raw_text = _clean_text(raw_text)

    # Clean up markdown
    cleaned_lines = _remove_excessive_blanks(markdown_lines)

    return {"metadata": metadata, "markdown": "\n".join(cleaned_lines), "raw_text": raw_text}


def _convert_generic_format(soup: BeautifulSoup) -> Dict[str, Any]:
    """Fallback for unknown formats"""
    raw_text = soup.get_text(separator=" ", strip=True)
    raw_text = _clean_text(raw_text)

    markdown_text = soup.get_text(separator="\n\n", strip=True)
    markdown_text = _clean_text(markdown_text)

    return {"metadata": {}, "markdown": markdown_text, "raw_text": raw_text}


def _remove_excessive_blanks(lines):
    """Remove excessive blank lines while preserving structure"""
    cleaned_lines = []
    prev_blank = False
    for line in lines:
        is_blank = line.strip() == ""
        if is_blank and prev_blank:
            continue
        cleaned_lines.append(line)
        prev_blank = is_blank
    return cleaned_lines


# Quick test function
def extract_speech_text_only(html_content: str) -> str:
    """
    Simple extraction of just the speech text without any formatting.
    Useful when you just want the raw content for analysis.
    """
    result = convert_hansard_to_markdown(html_content)
    return str(result["raw_text"])
