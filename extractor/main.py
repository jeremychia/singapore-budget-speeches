import logging
from pathlib import Path
from typing import Any, Dict

from speech_links import budget_speech_links
from utils_hansard import convert_hansard_to_markdown  # type: ignore[attr-defined]
from utils_link import extract_report_id, fetch_hansard, get_hansard_content

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Create output directory in project root (one level up from extractor/)
project_root = Path(__file__).parent.parent
output_dir = project_root / "output"
output_dir.mkdir(exist_ok=True)

# Iterate through all years
for year, data in budget_speech_links.items():
    logger.info(f"Processing year {year}...")

    # Extract report_id from hansard URL
    hansard_url = data.get("hansard", "")
    report_id = extract_report_id(hansard_url)

    if not report_id:
        logger.warning(f"No report ID found for {year}, skipping...")
        continue

    try:
        # Fetch and convert
        api_response = fetch_hansard(report_id)
        speech_html = get_hansard_content(api_response)

        if not speech_html:
            logger.warning(f"No HTML content for {year}, skipping...")
            continue

        # Convert HTML to markdown
        output: Dict[str, Any] = convert_hansard_to_markdown(speech_html)
        markdown_content = output.get("markdown", "")

        # Save to file
        output_file = output_dir / f"{year}.md"
        output_file.write_text(markdown_content, encoding="utf-8")
        logger.info(f"Saved to {output_file}")

    except Exception as e:
        logger.error(f"Error processing {year}: {e}")

logger.info("Done!")
