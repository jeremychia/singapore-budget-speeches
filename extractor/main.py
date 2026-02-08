import argparse
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

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


def extract_speeches(
    years: Optional[List[int]] = None,
    force: bool = False,
) -> None:
    """
    Extract budget speeches for specified years

    Args:
        years: List of years to process. If None, process all years.
        force: If True, overwrite existing files. If False, skip existing files.
    """
    # Create output directory in project root (one level up from extractor/)
    project_root = Path(__file__).parent.parent
    output_dir = project_root / "output_markdown"
    output_dir.mkdir(exist_ok=True)

    # Determine which years to process
    if years is None:
        years_to_process = sorted(budget_speech_links.keys())
        logger.info(f"Processing all {len(years_to_process)} years...")
    else:
        years_to_process = sorted(years)
        logger.info(f"Processing {len(years_to_process)} specific year(s): {years_to_process}")

    # Iterate through selected years
    processed = 0
    skipped = 0
    errors = 0

    for year in years_to_process:
        # Check if year exists in budget_speech_links
        if year not in budget_speech_links:
            logger.warning(f"Year {year} not found in budget_speech_links, skipping...")
            skipped += 1
            continue

        # Check if file already exists
        output_file = output_dir / f"{year}.md"
        if output_file.exists() and not force:
            logger.info(f"Year {year}: File already exists, skipping (use --force to overwrite)")
            skipped += 1
            continue

        logger.info(f"Processing year {year}...")

        data = budget_speech_links[year]

        # Extract report_id from hansard URL
        hansard_url = data.get("hansard", "")
        report_id = extract_report_id(hansard_url)

        if not report_id:
            logger.warning(f"No report ID found for {year}, skipping...")
            skipped += 1
            continue

        try:
            # Fetch and convert
            api_response = fetch_hansard(report_id)
            speech_html = get_hansard_content(api_response)

            if not speech_html:
                logger.warning(f"No HTML content for {year}, skipping...")
                skipped += 1
                continue

            # Convert HTML to markdown
            output: Dict[str, Any] = convert_hansard_to_markdown(speech_html)
            markdown_content = output.get("markdown", "")

            # Save to file
            output_file.write_text(markdown_content, encoding="utf-8")
            logger.info(f"✓ Saved to {output_file}")
            processed += 1

        except Exception as e:
            logger.error(f"✗ Error processing {year}: {e}")
            errors += 1

    logger.info("=" * 60)
    logger.info(f"Done! Processed: {processed}, Skipped: {skipped}, Errors: {errors}")


def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(description="Extract Singapore budget speeches from Hansard")
    parser.add_argument(
        "--years",
        type=int,
        nargs="+",
        help="Specific years to process (e.g., --years 2025 2026). If not provided, processes all years.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force overwrite existing files",
    )

    args = parser.parse_args()
    extract_speeches(years=args.years, force=args.force)


if __name__ == "__main__":
    main()
