#!/usr/bin/env python3
"""
Export CSV data to JSON for web visualisation
Generates lightweight summary JSONs and detailed shards for progressive loading
"""

import json
from pathlib import Path

import pandas as pd

# Paths
ANALYSIS_DIR = Path(__file__).parent
DATA_DIR = ANALYSIS_DIR.parent / "docs" / "data"
SUMMARY_DIR = DATA_DIR / "summary"
DETAILED_DIR = DATA_DIR / "detailed"
SEARCH_DIR = DATA_DIR / "search-index"


def ensure_directories():
    """Create output directories if they don't exist"""
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)
    DETAILED_DIR.mkdir(parents=True, exist_ok=True)
    (SEARCH_DIR / "decades").mkdir(parents=True, exist_ok=True)
    (SEARCH_DIR / "topics").mkdir(parents=True, exist_ok=True)
    print("✓ Created directory structure")


def export_ministries_overview():
    """Export ministry statistics as lightweight JSON"""
    print("\n📊 Exporting ministries overview...")

    # Load CSVs
    by_year = pd.read_csv(ANALYSIS_DIR / "ministry_by_year.csv")

    # Create overview JSON
    overview = {"by_year": {}, "by_ministry": {}, "insights": []}

    # Get ministry columns (all except 'year')
    ministry_cols = [col for col in by_year.columns if col != "year"]

    # Format ministry names (convert snake_case to Title Case)
    def format_ministry_name(name):
        return name.replace("_", " ").title()

    # Process by_year data
    for _, row in by_year.iterrows():
        year = str(int(row["year"]))
        overview["by_year"][year] = {}

        for ministry in ministry_cols:
            formatted_name = format_ministry_name(ministry)
            # Convert percentage to absolute count (approximate based on percentages)
            overview["by_year"][year][formatted_name] = round(float(row[ministry]), 2)

    # Calculate ministry totals and stats
    for ministry in ministry_cols:
        formatted_name = format_ministry_name(ministry)
        values = by_year[ministry].values

        total = float(values.sum())
        avg = float(values.mean())
        peak_idx = values.argmax()
        peak_year = int(by_year.iloc[peak_idx]["year"])

        overview["by_ministry"][formatted_name] = {
            "total": round(total, 2),
            "average_per_year": round(avg, 2),
            "peak_year": peak_year,
            "percentage": round((total / by_year[ministry_cols].sum().sum()) * 100, 2),
        }

    # Sort by total
    overview["by_ministry"] = dict(
        sorted(overview["by_ministry"].items(), key=lambda x: x[1]["total"], reverse=True)
    )

    # Add insights (exclude "General" when finding top ministry)
    top_ministry = next(
        (item for item in overview["by_ministry"].items() if item[0] != "General"), None
    )
    if top_ministry:
        top_insight = {
            "title": "Most Discussed Ministry",
            "description": (
                f"{top_ministry[0]} was the most discussed specific policy area, "
                f"representing {top_ministry[1]['percentage']}% of all policy discussions."
            ),
        }
    else:
        top_insight = {
            "title": "Policy Diversity",
            "description": (
                "Budget speeches cover a wide range of policy areas across all ministries."
            ),
        }

    overview["insights"] = [
        top_insight,
        {
            "title": "Policy Evolution",
            "description": (
                "Defence dominated early years (1960s-70s) during nation-building. "
                "Social Services surged in 2000s-2010s as Singapore matured. "
                "Environment emerged strongly in 2020s."
            ),
        },
        {
            "title": "Crisis Response",
            "description": (
                "Economic topics spiked during 1985 recession, 1997 Asian Financial Crisis, "
                "2008 Global Financial Crisis, and 2020 COVID-19 pandemic."
            ),
        },
    ]

    # Write to file
    output_path = SUMMARY_DIR / "ministries_overview.json"
    with open(output_path, "w") as f:
        json.dump(overview, f, indent=2)

    size_kb = output_path.stat().st_size / 1024
    print(f"  ✓ Exported ministries_overview.json ({size_kb:.1f} KB)")


def export_ministers_overview():
    """Export minister statistics as lightweight JSON"""
    print("\n👤 Exporting ministers overview...")

    # Load CSVs
    yearly_stats = pd.read_csv(ANALYSIS_DIR / "yearly_speech_statistics.csv")
    minister_topics = pd.read_csv(ANALYSIS_DIR / "ministry_by_minister.csv")

    # Define minister periods (hardcoded for accuracy)
    minister_periods = {
        "Goh Keng Swee": "1960-1965",
        "Lim Kim San": "1967-1970",
        "Hon Sui Sen": "1971-1983",
        "Goh Chok Tong": "1982-1984",
        "Dr Richard Hu Tsu Tau": "1985-2001",
        "Dr Tony Tan Keng Yam": "2002-2004",
        "Lee Hsien Loong": "2005-2007",
        "Tharman Shanmugaratnam": "2008-2015",
        "Heng Swee Keat": "2016-2021",
        "Lawrence Wong": "2022-2025",
    }

    overview = {"ministers": [], "minister_topics": {}}

    # Process each minister from yearly stats
    minister_groups = yearly_stats.groupby("minister")

    for minister_name, group in minister_groups:
        # Calculate stats
        num_speeches = len(group)
        total_sentences = int(group["total_sentences"].sum())
        avg_sentence_length = round(float(group["avg_words_per_sentence"].mean()), 1)
        readability_score = round(float(group["readability"].mean()), 1)

        minister_data = {
            "name": minister_name,
            "years_served": minister_periods.get(minister_name, "Unknown"),
            "num_speeches": num_speeches,
            "total_sentences": total_sentences,
            "avg_sentence_length": avg_sentence_length,
            "readability_score": readability_score,
        }

        overview["ministers"].append(minister_data)

    # Process minister topics
    for _, row in minister_topics.iterrows():
        minister = row["minister"]
        overview["minister_topics"][minister] = {}

        for col in minister_topics.columns:
            if col != "minister":
                formatted_name = col.replace("_", " ").title()
                overview["minister_topics"][minister][formatted_name] = round(float(row[col]), 2)

    # Write to file
    output_path = SUMMARY_DIR / "ministers_overview.json"
    with open(output_path, "w") as f:
        json.dump(overview, f, indent=2)

    size_kb = output_path.stat().st_size / 1024
    print(f"  ✓ Exported ministers_overview.json ({size_kb:.1f} KB)")


def export_yearly_overview():
    """Export yearly statistics as lightweight JSON"""
    print("\n📅 Exporting yearly overview...")

    # Load CSVs
    df = pd.read_csv(ANALYSIS_DIR / "yearly_speech_statistics.csv")

    # Load linguistic features if available
    linguistic_path = ANALYSIS_DIR / "linguistic_features.csv"
    linguistic_df = None
    if linguistic_path.exists():
        linguistic_df = pd.read_csv(linguistic_path)
        print("  ✓ Loaded linguistic features")

    overview = {
        "by_year": {},
        "by_minister": {},
        "insights": {
            "readability_trend": (
                "Readability improved from ~40 (1960s) to ~60 (2020s). "
                "Higher scores mean easier to read."
            ),
            "sentence_length": (
                "Average sentence length decreased from 28 words (1960s) to 22 words (2020s), "
                "making speeches clearer."
            ),
            "most_readable": (
                "Recent ministers use shorter sentences and simpler language "
                "compared to earlier decades."
            ),
            "complex_topics": (
                "Economic and financial topics tend to have lower readability "
                "due to technical terminology."
            ),
        },
    }

    # Process by year
    for _, row in df.iterrows():
        year = str(int(row["year"]))
        year_data = {
            "total_sentences": int(row["total_sentences"]),
            "avg_sentence_length": round(float(row["avg_words_per_sentence"]), 1),
            "readability": round(float(row["readability"]), 1),
            "minister": row["minister"],
        }

        # Add linguistic features if available
        if linguistic_df is not None:
            ling_row = linguistic_df[linguistic_df["year"] == int(row["year"])]
            if not ling_row.empty:
                ling_row = ling_row.iloc[0]
                year_data["ttr"] = round(float(ling_row["ttr"]), 4)
                year_data["mtld"] = (
                    round(float(ling_row["mtld"]), 2) if pd.notna(ling_row["mtld"]) else None
                )
                year_data["temporal_ratio"] = round(float(ling_row["temporal_ratio"]), 4)
                year_data["certainty_ratio"] = round(float(ling_row["certainty_ratio"]), 4)
                year_data["passive_ratio"] = round(float(ling_row["passive_ratio"]), 4)

        overview["by_year"][year] = year_data

    # Group by minister
    minister_stats = (
        df.groupby("minister")
        .agg({"readability": "mean", "avg_words_per_sentence": "mean", "total_sentences": "sum"})
        .reset_index()
    )

    for _, row in minister_stats.iterrows():
        minister = row["minister"]
        overview["by_minister"][minister] = {
            "avg_readability": round(float(row["readability"]), 1),
            "avg_sentence_length": round(float(row["avg_words_per_sentence"]), 1),
            "total_sentences": int(row["total_sentences"]),
        }

    # Write to file
    output_path = SUMMARY_DIR / "yearly_overview.json"
    with open(output_path, "w") as f:
        json.dump(overview, f, indent=2)

    size_kb = output_path.stat().st_size / 1024
    print(f"  ✓ Exported yearly_overview.json ({size_kb:.1f} KB)")


def export_search_index():
    """Export search index with progressive loading support using parquet files"""
    print("\n🔍 Exporting search index...")

    # Use parquet files as the source (cleaner, no duplicates)
    parquet_dir = ANALYSIS_DIR.parent / "output_processor"
    all_sentences = []

    # Minister periods for attribution (from speech_links.py)
    minister_periods = {
        (1960, 1965): "Goh Keng Swee",
        (1966, 1967): "Lim Kim San",
        (1968, 1970): "Goh Keng Swee",
        (1971, 1978): "Hon Sui Sen",
        (1979, 1981): "Goh Chok Tong",
        (1982, 1985): "Dr Tony Tan Keng Yam",
        (1986, 2001): "Dr Richard Hu Tsu Tau",
        (2002, 2006): "Lee Hsien Loong",
        (2007, 2015): "Tharman Shanmugaratnam",
        (2016, 2021): "Heng Swee Keat",
        (2022, 2026): "Lawrence Wong",
    }

    def get_minister(year):
        for (start, end), name in minister_periods.items():
            if start <= year <= end:
                return name
        return "Unknown"

    # Topic keywords for classification - aligned with ministry names in ministries_overview
    topic_keywords = {
        "Defence": [
            "defence",
            "defense",
            "military",
            "armed forces",
            "army",
            "navy",
            "air force",
            "national service",
            "ns",
            "mindef",
            "saf",
            "security",
            "terrorism",
            "homeland",
        ],
        "Education": [
            "education",
            "school",
            "university",
            "polytechnic",
            "ite",
            "student",
            "teacher",
            "curriculum",
            "moe",
            "learning",
            "skillsfuture",
            "training",
            "vocational",
            "preschool",
            "tuition",
            "nus",
            "ntu",
            "smu",
            "scholarship",
        ],
        "Health": [
            "health",
            "healthcare",
            "hospital",
            "medical",
            "medicine",
            "doctor",
            "nurse",
            "moh",
            "clinic",
            "patient",
            "disease",
            "treatment",
            "medisave",
            "medishield",
            "medifund",
            "elderly care",
            "mental health",
            "vaccine",
            "pandemic",
            "covid",
        ],
        "National Development": [
            "housing",
            "hdb",
            "flat",
            "home",
            "property",
            "bto",
            "resale",
            "mortgage",
            "cpf housing",
            "public housing",
            "rental",
            "estate",
            "neighbourhood",
            "urban",
            "land use",
            "planning",
            "ura",
            "development",
        ],
        "Transport": [
            "transport",
            "mrt",
            "bus",
            "train",
            "lta",
            "road",
            "traffic",
            "vehicle",
            "car",
            "taxi",
            "cycling",
            "infrastructure",
            "airport",
            "changi",
            "port",
            "ewl",
            "nsl",
            "nel",
            "dtl",
            "ccl",
            "tel",
        ],
        "Trade Industry": [
            "economy",
            "economic",
            "gdp",
            "growth",
            "recession",
            "inflation",
            "trade",
            "export",
            "import",
            "investment",
            "business",
            "enterprise",
            "sme",
            "startup",
            "industry",
            "manufacturing",
            "services",
            "tourism",
            "employment",
            "jobs",
            "unemployment",
            "wages",
            "productivity",
            "competitiveness",
            "mti",
        ],
        "Finance": [
            "tax",
            "gst",
            "budget",
            "fiscal",
            "revenue",
            "expenditure",
            "deficit",
            "surplus",
            "reserves",
            "mas",
            "cpf",
            "savings",
            "pension",
            "retirement",
            "income tax",
            "corporate tax",
            "stamp duty",
            "iras",
        ],
        "Social Family Development": [
            "social",
            "welfare",
            "comcare",
            "assistance",
            "support",
            "low-income",
            "vulnerable",
            "disability",
            "family",
            "children",
            "youth",
            "seniors",
            "pioneer generation",
            "merdeka generation",
            "silver support",
            "workfare",
            "gst voucher",
            "cdc voucher",
            "msf",
        ],
        "Sustainability Environment": [
            "environment",
            "climate",
            "sustainability",
            "green",
            "carbon",
            "emissions",
            "renewable",
            "solar",
            "energy",
            "water",
            "newater",
            "recycling",
            "waste",
            "pollution",
            "biodiversity",
            "nature",
            "parks",
            "gardens",
            "mse",
        ],
        "Communications Information": [
            "technology",
            "digital",
            "innovation",
            "research",
            "r&d",
            "ai",
            "artificial intelligence",
            "smart nation",
            "cyber",
            "data",
            "fintech",
            "biotech",
            "infocomm",
            "ict",
            "automation",
            "robotics",
            "internet",
            "mci",
            "imda",
        ],
        "Manpower": [
            "workforce",
            "workers",
            "foreign workers",
            "levy",
            "mom",
            "labour",
            "labor",
            "skills",
            "retraining",
        ],
        "Home Affairs": [
            "police",
            "spf",
            "scdf",
            "civil defence",
            "fire",
            "emergency",
            "crime",
            "law enforcement",
            "mha",
            "immigration",
            "ica",
            "prisons",
        ],
        "Foreign Affairs": [
            "foreign",
            "diplomacy",
            "asean",
            "international",
            "bilateral",
            "embassy",
            "mfa",
            "treaty",
        ],
        "Culture Community Youth": [
            "culture",
            "arts",
            "heritage",
            "sports",
            "community",
            "mccy",
            "nac",
            "museum",
            "national day",
        ],
        "Law": [
            "legal",
            "courts",
            "judiciary",
            "minlaw",
            "attorney",
            "legislation",
        ],
    }

    def classify_topic(text):
        """Classify a sentence into a topic based on keywords"""
        text_lower = text.lower()
        topic_scores = {}

        for topic, keywords in topic_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                topic_scores[topic] = score

        if topic_scores:
            return max(topic_scores, key=topic_scores.get)
        return "General"

    # Process each parquet file
    parquet_files = sorted(parquet_dir.glob("*.parquet"))

    for filepath in parquet_files:
        year = int(filepath.stem)
        df = pd.read_parquet(filepath)

        minister = get_minister(year)
        decade = f"{(year // 10) * 10}s"

        for _, row in df.iterrows():
            sentence = row["sentence_text"].strip()

            # Skip very short fragments or placeholder text
            if len(sentence) < 20:
                continue
            if "Please refer to Hansard document" in sentence:
                continue

            # Classify the sentence topic
            topic = classify_topic(sentence)

            all_sentences.append(
                {
                    "year": year,
                    "decade": decade,
                    "minister": minister,
                    "text": sentence,
                    "idx": int(row["sentence_order"]),
                    "topic": topic,
                }
            )

    print(f"  📝 Extracted {len(all_sentences):,} sentences from {len(parquet_files)} speeches")

    # Create overview - aligned with ministries_overview.json
    overview = {
        "total_sentences": len(all_sentences),
        "years": sorted(list(set(s["year"] for s in all_sentences))),
        "decades": ["1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"],
        "topics": [
            "General",
            "Defence",
            "Finance",
            "Trade Industry",
            "Manpower",
            "Education",
            "Transport",
            "National Development",
            "Health",
            "Sustainability Environment",
            "Social Family Development",
            "Home Affairs",
            "Foreign Affairs",
            "Communications Information",
            "Culture Community Youth",
            "Law",
        ],
    }

    output_path = SEARCH_DIR / "overview.json"
    with open(output_path, "w") as f:
        json.dump(overview, f, indent=2)
    print(f"  ✓ Exported overview.json ({output_path.stat().st_size / 1024:.1f} KB)")

    # Export by decade shards
    for decade in ["1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]:
        decade_sentences = [s for s in all_sentences if s["decade"] == decade]

        shard = {"decade": decade, "count": len(decade_sentences), "sentences": decade_sentences}

        output_path = SEARCH_DIR / "decades" / f"{decade}.json"
        with open(output_path, "w") as f:
            json.dump(shard, f)

        size_kb = output_path.stat().st_size / 1024
        print(f"  ✓ Exported {decade}.json ({size_kb:.1f} KB, {len(decade_sentences):,} sentences)")

    print(f"\n  ✅ Search index complete with {len(all_sentences):,} searchable sentences")


def main():
    """Main export pipeline"""
    print("=" * 60)
    print("🚀 EXPORTING DATA FOR WEB VISUALISATION")
    print("=" * 60)

    try:
        # Create directories
        ensure_directories()

        # Export data
        export_ministries_overview()
        export_ministers_overview()
        export_yearly_overview()
        export_search_index()

        print("\n" + "=" * 60)
        print("✅ EXPORT COMPLETE!")
        print("=" * 60)
        print(f"\nOutput directory: {DATA_DIR}")
        print("\nNext steps:")
        print("  1. Test locally: cd docs && python -m http.server 8000")
        print("  2. Open browser: http://localhost:8000")
        print("  3. Commit and push to GitHub for deployment")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        raise


if __name__ == "__main__":
    main()
