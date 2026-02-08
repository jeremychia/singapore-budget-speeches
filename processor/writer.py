"""
Writers for output formats (Parquet per year)
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)


def prepare_dataframe_for_year(sentences: List[Dict], year: int) -> pd.DataFrame:
    """
    Convert list of sentence dicts for a single year to pandas DataFrame

    Args:
        sentences: List of sentence dictionaries for one year
        year: The year being processed

    Returns:
        pandas DataFrame with sentences for that year
    """
    df = pd.DataFrame(sentences)

    if df.empty:
        return df

    # Sort by sentence_order
    df = df.sort_values(["sentence_order"]).reset_index(drop=True)

    # Re-assign sentence_order to be consecutive (0, 1, 2, ...)
    df["sentence_order"] = range(len(df))

    # Add sentence_id as first column (format: {year}_{sentence_order})
    df.insert(0, "sentence_id", [f"{year}_{i}" for i in range(len(df))])

    return df


def write_year_to_parquet(
    df: pd.DataFrame, year: int, output_dir: str = "output_processor"
) -> Path:
    """
    Write DataFrame for a single year to Parquet

    Args:
        df: DataFrame to write
        year: Year being processed
        output_dir: Output directory path

    Returns:
        Path to written file
    """
    dir_path = Path(output_dir)
    dir_path.mkdir(parents=True, exist_ok=True)

    file_path = dir_path / f"{year}.parquet"
    df.to_parquet(file_path, index=False)
    return file_path


def load_all_years(output_dir: str = "output_processor") -> pd.DataFrame:
    """
    Load all year parquet files and combine them

    Args:
        output_dir: Directory containing year parquet files

    Returns:
        Combined DataFrame with all years
    """
    dir_path = Path(output_dir)
    parquet_files = sorted(dir_path.glob("*.parquet"))

    if not parquet_files:
        logger.warning(f"No parquet files found in {output_dir}")
        return pd.DataFrame()

    dfs = []
    for file_path in parquet_files:
        try:
            df = pd.read_parquet(file_path)
            dfs.append(df)
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")

    if not dfs:
        return pd.DataFrame()

    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df = combined_df.sort_values(["year", "sentence_order"]).reset_index(drop=True)

    return combined_df


def print_summary(df: pd.DataFrame, year: Optional[int] = None):
    """
    Print summary statistics of the dataset

    Args:
        df: DataFrame to summarize
        year: If provided, indicates this is a single year summary
    """
    if df.empty:
        logger.info("No data to summarize")
        return

    logger.info(f"\n{'='*60}")
    if year:
        logger.info(f"Summary for Year {year}")
    else:
        logger.info("Dataset Summary")
    logger.info("=" * 60)
    logger.info(f"Total sentences: {len(df):,}")
    logger.info(f"Total words: {df['word_count'].sum():,}")
    logger.info(f"Avg words per sentence: {df['word_count'].mean():.1f}")

    if year:
        logger.info(f"Year: {year}")
    else:
        logger.info(f"Years covered: {df['year'].min()} - {df['year'].max()}")

    logger.info(f"DataFrame shape: {df.shape}")
    logger.info(f"\nColumns: {list(df.columns)}")
