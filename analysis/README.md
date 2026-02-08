# Budget Speeches Analysis

This folder contains Jupyter notebooks for analyzing Singapore budget speeches data.

## Contents

- `speech_analysis.ipynb` - Main analysis notebook covering:
  - Number of speeches given by each minister
  - Length of speeches over the years
  - Trends in speech characteristics
  - Comparative analysis by minister

## Setup

The required dependencies are already installed in the project:
- pandas
- matplotlib
- seaborn
- jupyter
- numpy

## Running the Analysis

1. Make sure you're in the project root directory
2. Start Jupyter:
   ```bash
   poetry run jupyter notebook
   ```
3. Navigate to `analysis/speech_analysis.ipynb`
4. Run all cells to generate the analysis

Alternatively, you can open the notebook directly in VS Code with the Jupyter extension.

## Data Source

The analysis uses parquet files from the `output_processor/` directory, which contains processed budget speeches from 1960-2025. Minister information is pulled from `extractor/speech_links.py`.

## Output Files

The notebook generates:
- `yearly_speech_statistics.csv` - Statistics aggregated by year
- `minister_speech_statistics.csv` - Statistics aggregated by minister
- Various visualizations and charts

## Key Analyses

### 1. Speeches by Minister
- Bar chart showing total number of budget speeches delivered by each minister
- Year ranges for each minister's tenure

### 2. Speech Length Over Time
- Total words per speech over the years
- Total sentences per speech
- Trend analysis showing how speech length has evolved

### 3. Speech Characteristics by Minister
- Average speech length by minister
- Average words per sentence by minister
- Comparative visualizations

### 4. Temporal Trends
- Combined view showing how different ministers' speech patterns vary
- Identification of longest and shortest speeches
- Overall statistical summaries
