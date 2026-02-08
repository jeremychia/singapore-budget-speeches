"""
Main processor for batch processing speeches (one parquet per year)
"""

import logging
from parser import SpeechParser
from pathlib import Path
from typing import List, Optional

import pandas as pd
from writer import (
    load_all_years,
    prepare_dataframe_for_year,
    print_summary,
    write_year_to_parquet,
)

logger = logging.getLogger(__name__)


def process_speeches(
    markdown_dir: str = "output_markdown",
    output_dir: str = "output_processor",
    years: Optional[List[int]] = None,
    force: bool = False,
) -> pd.DataFrame:
    """
    Process budget speech markdown files, writing one parquet per year

    Args:
        markdown_dir: Directory containing markdown files
        output_dir: Directory for parquet output files
        years: List of specific years to process. If None, process all available files.
        force: If True, overwrite existing parquet files. If False, skip existing files.

    Returns:
        pandas DataFrame with all processed sentences (combined view)
    """
    markdown_path = Path(markdown_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Get all markdown files
    all_files = sorted(markdown_path.glob("*.md"))

    # Filter by years if specified
    if years is not None:
        year_set = set(years)
        files = [f for f in all_files if f.stem.isdigit() and int(f.stem) in year_set]
        logger.info(f"Filtering to {len(files)} file(s) for years: {sorted(years)}")
    else:
        files = all_files

    logger.info("Budget Speech Processor")
    logger.info("=" * 60)
    logger.info(f"Markdown directory: {markdown_path}")
    logger.info(f"Output directory: {output_path}")
    logger.info(f"Found {len(files)} files to process")
    logger.info("=" * 60)
    logger.info("Processing files...")

    # Initialize parser
    parser = SpeechParser()

    # Process each file
    processed = 0
    skipped = 0
    errors = 0

    for i, file_path in enumerate(files, 1):
        try:
            year = int(file_path.stem)
            output_file = output_path / f"{year}.parquet"

            # Check if file already exists
            if output_file.exists() and not force:
                logger.info(
                    f"{i:2d}/{len(files)}: {file_path.name} - File already exists, skipping (use --force to overwrite)"
                )
                skipped += 1
                continue

            logger.info(f"{i:2d}/{len(files)}: {file_path.name}...")

            # Parse the markdown file
            sentences = parser.parse_file(file_path)
            original_count = len(sentences)

            # Deduplicate within this year
            df_year = pd.DataFrame(sentences)
            df_year_deduped = df_year.drop_duplicates(subset=["sentence_text"], keep="first")
            sentences_deduped = df_year_deduped.to_dict("records")

            duplicates_in_year = original_count - len(sentences_deduped)

            # Prepare DataFrame for this year
            df_final = prepare_dataframe_for_year(sentences_deduped, year)

            # Write to parquet
            output_path_written = write_year_to_parquet(df_final, year, output_dir)

            if duplicates_in_year > 0:
                logger.info(
                    f"✓ Saved to {output_path_written.name} "
                    f"({original_count} → {len(sentences_deduped)} sentences, "
                    f"{duplicates_in_year} duplicates removed)"
                )
            else:
                logger.info(
                    f"✓ Saved to {output_path_written.name} ({len(sentences_deduped)} sentences)"
                )

            processed += 1

        except ValueError:
            logger.error(f"✗ {file_path.name} is not a valid year filename")
            errors += 1
        except Exception as e:
            logger.error(f"✗ Error processing {file_path.name}: {e}")
            errors += 1

    logger.info("=" * 60)
    logger.info(f"Done! Processed: {processed}, Skipped: {skipped}, Errors: {errors}")

    # Load and return combined view
    if processed > 0 or skipped > 0:
        logger.info("\nLoading combined view of all years...")
        combined_df = load_all_years(output_dir)
        print_summary(combined_df)
        return combined_df
    else:
        return pd.DataFrame()


# Keep backward compatibility with old function name
def process_all_speeches(
    markdown_dir: str = "output_markdown",
    output_csv: str = "output_processor/budget_speeches.csv",  # Ignored, kept for compatibility
    output_parquet: str = "output_processor/budget_speeches.parquet",  # Ignored, kept for compatibility
    years: Optional[List[int]] = None,
) -> pd.DataFrame:
    """
    Backward compatibility wrapper. Now writes one parquet per year.

    Args:
        markdown_dir: Directory containing markdown files
        output_csv: IGNORED - kept for backward compatibility
        output_parquet: IGNORED - kept for backward compatibility
        years: List of specific years to process

    Returns:
        pandas DataFrame with all processed sentences
    """
    # Extract output_dir from the old parquet path if provided
    output_dir = Path(output_parquet).parent if output_parquet else "output_processor"

    return process_speeches(
        markdown_dir=markdown_dir,
        output_dir=str(output_dir),
        years=years,
        force=False,
    )
