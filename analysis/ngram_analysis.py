#!/usr/bin/env python3
"""
N-gram Analysis for Singapore Budget Speeches

Extracts top n-grams (phrases) for each Finance Minister to reveal
distinctive language patterns and policy emphases.
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Optional

# Add extractor to path for speech_links
sys.path.append(str(Path(__file__).parent.parent / "extractor"))

from speech_links import budget_speech_links  # noqa: E402

# Paths
ANALYSIS_DIR = Path(__file__).parent
OUTPUT_DIR = ANALYSIS_DIR.parent / "docs" / "data" / "summary"
MARKDOWN_DIR = ANALYSIS_DIR.parent / "output_markdown"

# Common stopwords and function words to filter out
STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "but",
    "in",
    "on",
    "at",
    "to",
    "for",
    "of",
    "with",
    "by",
    "from",
    "as",
    "is",
    "was",
    "are",
    "were",
    "been",
    "be",
    "have",
    "has",
    "had",
    "do",
    "does",
    "did",
    "will",
    "would",
    "could",
    "should",
    "may",
    "might",
    "must",
    "shall",
    "can",
    "need",
    "this",
    "that",
    "these",
    "those",
    "it",
    "its",
    "they",
    "them",
    "their",
    "we",
    "our",
    "us",
    "i",
    "me",
    "my",
    "you",
    "your",
    "he",
    "him",
    "his",
    "she",
    "her",
    "who",
    "which",
    "what",
    "where",
    "when",
    "how",
    "why",
    "all",
    "each",
    "every",
    "both",
    "few",
    "more",
    "most",
    "other",
    "some",
    "such",
    "no",
    "nor",
    "not",
    "only",
    "same",
    "so",
    "than",
    "too",
    "very",
    "just",
    "also",
    "now",
    "here",
    "there",
    "then",
    "if",
    "because",
    "while",
    "although",
    "though",
    "after",
    "before",
    "during",
    "until",
    "unless",
    "about",
    "into",
    "through",
    "over",
    "under",
    "again",
    "further",
    "once",
    "mr",
    "sir",
    "speaker",
    "chairman",
    "members",
    "house",
    "parliament",
    "therefore",
    "however",
    "moreover",
    "thus",
    "hence",
    "accordingly",
    "singapore",
    "singaporeans",
    "government",
    "minister",
    "ministry",
    "year",
    "years",
    "per",
    "cent",
    "percent",
    "million",
    "billion",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "first",
    "second",
    "third",
    "last",
    "next",
    "new",
    "well",
    "many",
    "much",
    "like",
    "get",
    "make",
    "made",
    "going",
    "want",
    "even",
    "still",
    "already",
    "being",
    "been",
    "being",
    "having",
    "doing",
    "done",
    "getting",
    "making",
}

# Boring phrases to filter out (common parliamentary language and minister names)
BORING_PHRASES = {
    # Parliamentary language
    "per cent",
    "last year",
    "this year",
    "next year",
    "fiscal year",
    "financial year",
    "mr speaker",
    "mr chairman",
    "budget speech",
    "hon members",
    "budget debate",
    "committee of supply",
    "supply bill",
    # Document references (hansard noise)
    "hansard document",
    "please refer",
    "refer hansard",
    "see hansard",
    "refer document",
    "document full",
    "full text",
    "text available",
    "refer to hansard",
    "refer toannex",
    "refer to annex",
    "refer annex",
    "toannex",
    "annex a",
    "annex b",
    "annex c",
    "annex d",
    "annex e",
    "document please",
    "please refer toannex",
    "s c",
    # Minister names (self-references)
    "dr goh",
    "goh keng",
    "keng swee",
    "dr goh keng",
    "goh keng swee",
    "lim kim",
    "kim san",
    "lim kim san",
    "hon sui",
    "sui sen",
    "hon sui sen",
    "goh chok",
    "chok tong",
    "goh chok tong",
    "hu tsu",
    "tsu tau",
    "hu tsu tau",
    "dr richard",
    "richard hu",
    "tony tan",
    "tan keng",
    "dr tony",
    "dr tony tan",
    "tony tan keng",
    "hsien loong",
    "lee hsien",
    "lee hsien loong",
    "tharman shanmugaratnam",
    "shanmugaratnam",
    "heng swee",
    "swee keat",
    "heng swee keat",
    "lawrence wong",
    # Other noise
    "r d",
    "d expenditure",
    "000 000",
    "000",
}


def is_boring_phrase(phrase: str) -> bool:
    """Check if phrase should be filtered out."""
    # Direct match
    if phrase in BORING_PHRASES:
        return True
    # Contains certain noise patterns
    noise_patterns = [
        "hansard",
        "annex",
        "document",
        "please refer",
        "toannex",
        "keng yam",
        "richard hu",
        "hu tsu",
        "tsu tau",
    ]
    for pattern in noise_patterns:
        if pattern in phrase:
            return True
    # Filter fiscal year references like "1971 72"
    if re.match(r"^\d{4} \d{2}$", phrase):
        return True
    # Filter single letter combos like "p a p", "p m", "s c"
    if re.match(r"^[a-z]( [a-z])+$", phrase):
        return True
    return False


def get_minister_for_year(year: int) -> Optional[str]:
    """Get the minister who delivered the budget for a given year."""
    if year in budget_speech_links:
        minister = budget_speech_links[year].get("minister")
        return str(minister) if minister else None
    return None


def load_speech_text(year: int) -> str:
    """Load and clean speech text for a given year."""
    filepath = MARKDOWN_DIR / f"{year}.md"
    if not filepath.exists():
        return ""

    with open(filepath, encoding="utf-8") as f:
        text = f.read()

    # Remove markdown headers and formatting
    text = re.sub(r"^#.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*|__", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    # Clean and normalize
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_ngrams(text: str, n: int) -> list[str]:
    """Extract n-grams from text."""
    words = text.split()
    ngrams = []

    for i in range(len(words) - n + 1):
        ngram = " ".join(words[i : i + n])
        # Filter out ngrams with stopwords at start/end
        ngram_words = ngram.split()
        if ngram_words[0] in STOPWORDS or ngram_words[-1] in STOPWORDS:
            continue
        # Filter out ngrams that are all stopwords
        if all(w in STOPWORDS for w in ngram_words):
            continue
        # Filter out boring phrases using pattern matching
        if is_boring_phrase(ngram):
            continue
        ngrams.append(ngram)

    return ngrams


def calculate_tfidf_boost(
    phrase: str,
    minister_count: int,
    minister_total: int,
    all_ministers_count: dict[str, int],
) -> float:
    """
    Calculate a TF-IDF-like score to boost distinctive phrases.
    Phrases used more by this minister relative to others get higher scores.
    """
    tf = minister_count / max(minister_total, 1)

    # Count how many ministers use this phrase
    ministers_using = sum(1 for count in all_ministers_count.values() if count > 0)
    total_ministers = len(all_ministers_count)

    # IDF-like score (higher if fewer ministers use it)
    idf = 1 + (total_ministers - ministers_using) / total_ministers

    return tf * idf * minister_count


def analyze_minister_ngrams(
    n_values: list[int] = [2, 3],
    top_k: int = 15,
) -> dict:
    """
    Analyze n-grams for each minister.

    Args:
        n_values: List of n-gram sizes to analyze (default: bigrams and trigrams)
        top_k: Number of top phrases to return per minister

    Returns:
        Dictionary with minister n-gram data
    """
    # Group speeches by minister
    minister_texts: dict[str, str] = {}
    minister_years: dict[str, list[int]] = {}

    for year in range(1960, 2026):
        minister = get_minister_for_year(year)
        if not minister:
            continue

        text = load_speech_text(year)
        if not text:
            continue

        if minister not in minister_texts:
            minister_texts[minister] = ""
            minister_years[minister] = []

        minister_texts[minister] += " " + text
        minister_years[minister].append(year)

    # Extract n-grams for each minister
    minister_ngrams: dict[str, Counter] = {}
    all_ngrams: Counter = Counter()

    for minister, text in minister_texts.items():
        ngrams: list[str] = []
        for n in n_values:
            ngrams.extend(extract_ngrams(text, n))

        minister_ngrams[minister] = Counter(ngrams)
        all_ngrams.update(ngrams)

    # Calculate scores and get top phrases per minister
    results: dict[str, object] = {
        "ministers": {},
        "metadata": {"n_values": n_values, "top_k": top_k},
    }
    ministers_dict: dict[str, object] = {}

    for minister, ngram_counts in minister_ngrams.items():
        total_ngrams = sum(ngram_counts.values())

        # Get counts from all ministers for each phrase
        scored_phrases = []
        for phrase, count in ngram_counts.items():
            if count < 3:  # Minimum frequency threshold
                continue

            # Get this phrase's count for all ministers
            all_minister_counts = {m: minister_ngrams[m].get(phrase, 0) for m in minister_ngrams}

            # Calculate distinctiveness score
            score = calculate_tfidf_boost(phrase, count, total_ngrams, all_minister_counts)

            scored_phrases.append(
                {
                    "phrase": phrase,
                    "count": count,
                    "score": round(score, 4),
                }
            )

        # Sort by score and get top k
        scored_phrases.sort(key=lambda x: x["score"], reverse=True)
        top_phrases = scored_phrases[:top_k]

        ministers_dict[minister] = {
            "years": f"{min(minister_years[minister])}-{max(minister_years[minister])}",
            "num_speeches": len(minister_years[minister]),
            "phrases": top_phrases,
        }

    results["ministers"] = ministers_dict
    return results


def export_ngrams_json():
    """Export n-gram analysis to JSON for web visualization."""
    print("📊 Analyzing minister n-grams...")

    results = analyze_minister_ngrams(n_values=[2, 3], top_k=15)

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIR / "minister_ngrams.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    size_kb = output_path.stat().st_size / 1024
    print(f"  ✓ Exported minister_ngrams.json ({size_kb:.1f} KB)")

    # Print summary
    print("\n  Top phrases by minister:")
    for minister, data in results["ministers"].items():
        top_phrase = data["phrases"][0] if data["phrases"] else {"phrase": "N/A"}
        print(f"    {minister}: \"{top_phrase['phrase']}\"")

    return results


if __name__ == "__main__":
    export_ngrams_json()
