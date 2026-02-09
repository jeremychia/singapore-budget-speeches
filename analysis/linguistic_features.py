#!/usr/bin/env python3
"""
Linguistic Feature Analysis for Singapore Budget Speeches

Extracts advanced NLP metrics:
1. Vocabulary Richness (Type-Token Ratio, MTLD)
2. Temporal Orientation (Forward vs Backward looking)
3. Certainty Index (Hedging vs Confident language)
4. Passive Voice Ratio
"""

import re
from pathlib import Path

import pandas as pd
import spacy
from lexicalrichness import LexicalRichness

# Paths
ANALYSIS_DIR = Path(__file__).parent
PROCESSOR_DIR = ANALYSIS_DIR.parent / "output_processor"

# Load spaCy model
print("Loading spaCy model...")
nlp = spacy.load("en_core_web_sm")

# ============================================
# WORD LISTS FOR LINGUISTIC ANALYSIS
# ============================================

# Forward-looking language (future orientation)
FORWARD_MARKERS = [
    r"\bwill\b",
    r"\bshall\b",
    r"\bgoing to\b",
    r"\baim to\b",
    r"\bplan to\b",
    r"\bintend\b",
    r"\bfuture\b",
    r"\bupcoming\b",
    r"\bnext year\b",
    r"\bahead\b",
    r"\bseek to\b",
    r"\bexpect to\b",
    r"\bhope to\b",
    r"\bwant to\b",
    r"\bnew\b",
    r"\bpropose\b",
    r"\bproposed\b",
    r"\bintroduce\b",
    r"\blaunch\b",
    r"\bimplement\b",
    r"\binitiative\b",
    r"\bstrategy\b",
    r"\bvision\b",
    r"\bgoal\b",
    r"\btarget\b",
    r"\bambition\b",
]

# Backward-looking language (past orientation)
BACKWARD_MARKERS = [
    r"\bwas\b",
    r"\bwere\b",
    r"\bhad\b",
    r"\blast year\b",
    r"\bpreviously\b",
    r"\bin the past\b",
    r"\bhistorically\b",
    r"\bsince\b",
    r"\bachieved\b",
    r"\baccomplished\b",
    r"\bcompleted\b",
    r"\bestablished\b",
    r"\bbuilt\b",
    r"\bdeveloped\b",
    r"\bprogress\b",
    r"\bprogressed\b",
    r"\bimproved\b",
    r"\bgrew\b",
    r"\bincreased\b",
    r"\breduced\b",
    r"\brecord\b",
    r"\bhistory\b",
    r"\blegacy\b",
    r"\bfoundation\b",
]

# Hedging language (uncertainty)
HEDGE_MARKERS = [
    r"\bmay\b",
    r"\bmight\b",
    r"\bcould\b",
    r"\bperhaps\b",
    r"\bpossibly\b",
    r"\bprobably\b",
    r"\blikely\b",
    r"\bunlikely\b",
    r"\bapproximately\b",
    r"\baround\b",
    r"\babout\b",
    r"\bestimate\b",
    r"\bexpect\b",
    r"\bbelieve\b",
    r"\bseem\b",
    r"\bseems\b",
    r"\bappear\b",
    r"\bappears\b",
    r"\bsuggest\b",
    r"\bsuggests\b",
    r"\btend to\b",
    r"\bgenerally\b",
    r"\bsomewhat\b",
    r"\brelatively\b",
    r"\bpartially\b",
]

# Certainty language (confidence)
CERTAINTY_MARKERS = [
    r"\bwill\b",
    r"\bshall\b",
    r"\bmust\b",
    r"\bcertainly\b",
    r"\bdefinitely\b",
    r"\babsolutely\b",
    r"\bclearly\b",
    r"\bundoubtedly\b",
    r"\bsurely\b",
    r"\bcertain\b",
    r"\bconfident\b",
    r"\bcommit\b",
    r"\bcommitted\b",
    r"\bcommitment\b",
    r"\bensure\b",
    r"\bguarantee\b",
    r"\bdetermined\b",
    r"\bresolved\b",
    r"\bfirmly\b",
    r"\bstrongly\b",
    r"\bdecisive\b",
    r"\bcrucial\b",
    r"\bessential\b",
    r"\bvital\b",
    r"\bcritical\b",
]


def count_pattern_matches(text: str, patterns: list[str]) -> int:
    """Count total matches for a list of regex patterns."""
    text_lower = text.lower()
    total = 0
    for pattern in patterns:
        total += len(re.findall(pattern, text_lower))
    return total


def calculate_vocabulary_richness(text: str) -> dict:
    """
    Calculate vocabulary richness metrics using lexicalrichness library.

    Returns:
        - ttr: Type-Token Ratio (unique words / total words)
        - mtld: Measure of Textual Lexical Diversity (more robust for varying lengths)
    """
    try:
        lex = LexicalRichness(text)
        return {
            "ttr": round(lex.ttr, 4) if lex.words > 0 else 0,
            "mtld": round(lex.mtld(threshold=0.72), 2) if lex.words > 50 else None,
            "unique_words": lex.wordlist.__len__() if hasattr(lex, "wordlist") else 0,
            "total_words": lex.words,
        }
    except Exception:
        return {"ttr": 0, "mtld": None, "unique_words": 0, "total_words": 0}


def calculate_temporal_orientation(text: str) -> dict:
    """
    Calculate forward vs backward looking language ratio.

    Returns:
        - forward_count: Number of forward-looking markers
        - backward_count: Number of backward-looking markers
        - temporal_ratio: forward / (forward + backward), higher = more forward-looking
    """
    forward = count_pattern_matches(text, FORWARD_MARKERS)
    backward = count_pattern_matches(text, BACKWARD_MARKERS)
    total = forward + backward

    return {
        "forward_count": forward,
        "backward_count": backward,
        "temporal_ratio": round(forward / total, 4) if total > 0 else 0.5,
    }


def calculate_certainty_index(text: str) -> dict:
    """
    Calculate certainty vs hedging language ratio.

    Returns:
        - hedge_count: Number of hedging markers
        - certainty_count: Number of certainty markers
        - certainty_ratio: certainty / (certainty + hedge), higher = more confident
    """
    hedge = count_pattern_matches(text, HEDGE_MARKERS)
    certainty = count_pattern_matches(text, CERTAINTY_MARKERS)
    total = hedge + certainty

    return {
        "hedge_count": hedge,
        "certainty_count": certainty,
        "certainty_ratio": round(certainty / total, 4) if total > 0 else 0.5,
    }


def calculate_passive_voice_ratio(text: str) -> dict:
    """
    Calculate passive voice ratio using spaCy dependency parsing.

    Looks for passive subjects (nsubjpass) which indicate passive constructions.

    Returns:
        - passive_count: Number of passive voice constructions
        - active_count: Number of active subjects
        - passive_ratio: passive / (passive + active), higher = more passive
    """
    doc = nlp(text)

    passive_count = 0
    active_count = 0

    for token in doc:
        # Passive subject (e.g., "The bill was passed")
        if token.dep_ == "nsubjpass":
            passive_count += 1
        # Active subject (e.g., "We passed the bill")
        elif token.dep_ == "nsubj" and token.head.pos_ == "VERB":
            active_count += 1

    total = passive_count + active_count

    return {
        "passive_count": passive_count,
        "active_count": active_count,
        "passive_ratio": round(passive_count / total, 4) if total > 0 else 0,
    }


def analyze_speech(year: int) -> dict:
    """Analyze a single speech and return all linguistic metrics."""
    filepath = PROCESSOR_DIR / f"{year}.parquet"

    if not filepath.exists():
        print(f"  ⚠ File not found: {filepath}")
        return None

    df = pd.read_parquet(filepath)

    # Combine all sentences into full text
    full_text = " ".join(df["sentence_text"].tolist())
    total_sentences = len(df)
    total_words = df["word_count"].sum()

    # Calculate all metrics
    vocab = calculate_vocabulary_richness(full_text)
    temporal = calculate_temporal_orientation(full_text)
    certainty = calculate_certainty_index(full_text)
    passive = calculate_passive_voice_ratio(full_text)

    return {
        "year": year,
        "total_sentences": total_sentences,
        "total_words": int(total_words),
        # Vocabulary richness
        "ttr": vocab["ttr"],
        "mtld": vocab["mtld"],
        "unique_words": vocab["unique_words"],
        # Temporal orientation
        "forward_count": temporal["forward_count"],
        "backward_count": temporal["backward_count"],
        "temporal_ratio": temporal["temporal_ratio"],
        # Certainty index
        "hedge_count": certainty["hedge_count"],
        "certainty_count": certainty["certainty_count"],
        "certainty_ratio": certainty["certainty_ratio"],
        # Passive voice
        "passive_count": passive["passive_count"],
        "active_count": passive["active_count"],
        "passive_ratio": passive["passive_ratio"],
    }


def main():
    """Run linguistic analysis on all budget speeches."""
    print("=" * 60)
    print("🔤 LINGUISTIC FEATURE ANALYSIS")
    print("=" * 60)

    results = []
    years = range(1960, 2026)

    for year in years:
        print(f"  Analyzing {year}...", end=" ")
        result = analyze_speech(year)
        if result:
            results.append(result)
            print(
                f"TTR={result['ttr']:.3f}, "
                f"Temporal={result['temporal_ratio']:.2f}, "
                f"Certainty={result['certainty_ratio']:.2f}, "
                f"Passive={result['passive_ratio']:.2f}"
            )

    # Create DataFrame and save
    df = pd.DataFrame(results)
    output_path = ANALYSIS_DIR / "linguistic_features.csv"
    df.to_csv(output_path, index=False)

    print("\n" + "=" * 60)
    print(f"✅ Saved to {output_path}")
    print("=" * 60)

    # Print summary statistics
    print("\n📊 Summary Statistics:")
    print(f"  Vocabulary Richness (TTR): {df['ttr'].mean():.3f} avg (range: {df['ttr'].min():.3f} - {df['ttr'].max():.3f})")
    print(f"  Temporal Orientation: {df['temporal_ratio'].mean():.2f} avg (0=past, 1=future)")
    print(f"  Certainty Index: {df['certainty_ratio'].mean():.2f} avg (0=hedging, 1=certain)")
    print(f"  Passive Voice Ratio: {df['passive_ratio'].mean():.2f} avg")

    return df


if __name__ == "__main__":
    main()
