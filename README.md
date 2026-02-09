# Singapore Budget Speeches (1960-2025)

> **Interactive exploration of 65 years of Singapore's fiscal policy through 40,000+ sentences from budget speeches**

A comprehensive data analysis project that extracts, processes, and visualizes Singapore's budget speeches from 1960 to 2025, revealing how policy priorities evolved across seven Finance Ministers and major historical milestones.

---

## 📊 At a Glance

- **40,123 sentences** from 66 budget speeches
- **7 Finance Ministers** from Goh Keng Swee to Lawrence Wong
- **15 Ministry classifications** (Defence, Finance, Education, Health, etc.)
- **Linguistic analysis** tracking readability and complexity evolution
- **Crisis response patterns** analyzing 4 major economic crises
- **Interactive website** (coming soon) for exploring the data

---

## 🚀 Quick Start

```bash
# Clone and install
git clone https://github.com/parleh-mate/singapore-budget-speeches.git
cd singapore-budget-speeches
poetry install

# Download spaCy model
python -m spacy download en_core_web_sm

# Extract speeches from Hansard
poetry run python extractor/main.py

# Process to structured datasets
poetry run python processor/main.py

# Explore analysis notebooks
poetry run jupyter notebook
```

---

## 📁 Project Components

Each folder has its own detailed README:

| Folder | Purpose | Documentation |
|--------|---------|---------------|
| **[extractor/](extractor/)** | Web scraping from Parliament Hansard | [📖 Extractor README](extractor/README.md) |
| **[processor/](processor/)** | Markdown → structured data pipeline | [📖 Processor README](processor/README.md) |
| **[analysis/](analysis/)** | Jupyter notebooks & key findings | [📖 Analysis README](analysis/README.md) |
| **[output_markdown/](output_markdown/)** | Raw speeches (66 markdown files) | [📖 Output README](output_markdown/README.md) |
| **[output_processor/](output_processor/)** | Processed Parquet datasets | [📖 Data README](output_processor/README.md) |
| **[docs/](docs/)** | Interactive website (coming soon) | [📖 Website README](docs/README.md) |

---

## 🔍 Key Findings (Summary)

### Singapore's Policy Evolution

| Era | Timeframe | Characteristics |
|-----|-----------|-----------------|
| **Survival & Security** | 1960s-1970s | Defence 19.8%, industrialization, nation-building |
| **Economic Transformation** | 1980s-1990s | Finance 17.4%, services economy, crisis responses |
| **Inclusive Growth** | 2000s-2010s | Manpower 9.2%, healthcare, social safety nets |
| **Sustainable Future** | 2020s | Environment 4.1%, digital, climate action |

**📊 Full findings and charts**: See [analysis/README.md](analysis/README.md)

### Minister Comparison

| Minister | Years | Top Focus | Style Descriptor |
|----------|-------|-----------|------------------|
| Goh Keng Swee | 1959-1984 | Defence (25.2%) | The Architect |
| Richard Hu | 1985-2001 | Finance (19.3%) | The Prudent Steward |
| Tharman Shanmugaratnam | 2007-2015 | Manpower (9.2%) | The Social Reformer |
| Heng Swee Keat | 2015-2021 | Manpower (9.8%) | The Inclusivity Champion |
| Lawrence Wong | 2021-2025 | Sustainability (4.1%) | The Sustainability Advocate |

---

## 📊 Available Datasets

### Analysis Outputs (`analysis/` folder)
- `ministry_by_year.csv` - Ministry distribution by year
- `ministry_by_minister.csv` - Minister policy focus
- `yearly_speech_statistics.csv` - Readability & complexity
- `minister_speech_statistics.csv` - Speech characteristics
- [+ 4 more files](analysis/README.md#datasets)

### Raw Sentence Data (`output_processor/` folder)
- One Parquet file per year (1960-2025)
- Total: **40,123 sentences** with metadata

**📖 Full dataset documentation**: See [output_processor/README.md](output_processor/README.md)

---

## 🔬 Methodology

| Step | Description | Details |
|------|-------------|---------|
| **1. Extraction** | Scrape from Parliament Hansard | [extractor/README.md](extractor/README.md) |
| **2. Processing** | Sentence tokenization with spaCy | [processor/README.md](processor/README.md) |
| **3. Classification** | 15 ministry categories (82.7% accuracy) | [analysis/README.md](analysis/README.md#methodology) |
| **4. Analysis** | Linguistic metrics, crisis patterns | [analysis/README.md](analysis/README.md) |

---

## 🌐 Interactive Website (Coming Soon)

Progressive disclosure design with three reading paths:
- **Storyteller** (5 min): Key insights and narrative
- **Explorer** (15 min): Interactive visualizations
- **Researcher** (30+ min): Full data access

**Preview**: `https://jeremychia.github.io/singapore-budget-speeches/` (deployment pending)
**Design docs**: [WEBSITE_STRATEGY.md](WEBSITE_STRATEGY.md)

---

## 🛠️ Development

### Requirements
- Python 3.9+
- Poetry for dependencies
- spaCy 3.0+ with English model

### Project Structure
```
singapore-budget-speeches/
├── extractor/          # Web scraping (BeautifulSoup)
├── processor/          # Data pipeline (spaCy, pandas)
├── analysis/           # Jupyter notebooks
├── output_markdown/    # Raw speeches (66 files)
├── output_processor/   # Parquet datasets
├── docs/              # Website (GitHub Pages)
└── WEBSITE_STRATEGY.md # Design documentation
```

### Adding New Speeches

1. Update `extractor/speech_links.py` with new speech metadata
2. Run extraction: `poetry run python extractor/main.py`
3. Process data: `poetry run python processor/main.py`
4. Re-run analysis notebooks

**📖 Detailed guide**: See [extractor/README.md](extractor/README.md#adding-new-speeches)

---

## 📈 Quick Usage Examples

```python
import pandas as pd

# Load sentence data
df = pd.read_parquet('output_processor/2020.parquet')

# Search for keywords
healthcare = df[df['sentence_text'].str.contains('healthcare', case=False)]

# Load ministry trends
ministry_trends = pd.read_csv('analysis/ministry_by_year.csv', index_col=0)
ministry_trends['defence'].plot(title='Defence Prominence Over Time')
```

**📖 More examples**: See [analysis/README.md](analysis/README.md#usage-examples)

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional NLP analysis (sentiment, topic modeling)
- Website features and visualizations
- Data quality improvements
- Documentation and tutorials

**Process**: Fork → Feature branch → Pull request
**Issues**: Use GitHub Issues for bugs and feature requests

---

## 📄 License & Credits

**License**: MIT License - see [LICENSE](LICENSE)
**Data Source**: Singapore Parliament Official Reports (Hansard) - public government data
**Author**: Jeremy Chia

---

## 📚 Documentation Index

- **[Extractor Documentation](extractor/README.md)** - Web scraping process
- **[Processor Documentation](processor/README.md)** - Data pipeline details
- **[Analysis Documentation](analysis/README.md)** - Findings and methodology
- **[Output Data Documentation](output_processor/README.md)** - Dataset schemas
- **[Website Strategy](WEBSITE_STRATEGY.md)** - Interactive site design

---

**Last Updated**: February 2026
**Coverage**: 1960-2025 (66 speeches, 40,123 sentences)
