# Singapore Budget Speeches

Extract and convert Singapore budget speeches from Hansard to structured data.

## Modules

- **extractor**: Scrapes budget speeches from Hansard website
- **processor**: Converts markdown files to sentence-level CSV/Parquet datasets

## Usage

### Extract speeches
```bash
poetry run python extractor/main.py
```

### Process speeches to dataset
```bash
poetry run python processor/main.py
```

## Installation

```bash
poetry install
```
