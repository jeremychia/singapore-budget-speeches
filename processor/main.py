"""
Main entry point for running the processor
"""

import argparse
import logging

from processor import process_speeches  # type: ignore[attr-defined]


def main():
    """Run the budget speech processor"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Process Singapore budget speech markdown files into parquet "
        "(one file per year)"
    )
    parser.add_argument(
        "--years",
        type=int,
        nargs="+",
        help="Specific years to process (e.g., --years 2025 2026). "
        "If not provided, processes all available files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force overwrite existing parquet files",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output_processor",
        help="Output directory for parquet files (default: output_processor)",
    )

    args = parser.parse_args()

    process_speeches(
        markdown_dir="output_markdown",
        output_dir=args.output_dir,
        years=args.years,
        force=args.force,
    )


if __name__ == "__main__":
    main()
