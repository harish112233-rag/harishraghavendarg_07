"""
BookIQ — NLP Preprocessing & Summarization Engine
Uses NLTK + sumy (extractive) with transformers as optional upgrade.
Fully offline, no API key needed.
"""

import re
import os
import json
import math
import nltk
import string
from collections import Counter

# ── NLTK data download (silent) ───────────────────────────────────────────────
def ensure_nltk():
    packages = ["punkt", "punkt_tab", "stopwords", "averaged_perceptron_tagger"]
    for pkg in packages:
        try:
            nltk.data.find(f"tokenizers/{pkg}" if "punkt" in pkg else f"corpora/{pkg}")
        except LookupError:
            nltk.download(pkg, quiet=True)

ensure_nltk()

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords


# ═══════════════════════════════════════════════════════════════════════════════
#  TEXT CLEANING
# ═══════════════════════════════════════════════════════════════════════════════

def clean_text(text: str) -> str:
    """Remove noise while keeping sentence structure intact."""
    # Normalize unicode dashes and quotes
    text = text.replace("\u2014", " — ").replace("\u2013", " - ")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    # Remove excessive whitespace
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    # Remove page numbers (e.g. "Page 12" or standalone numbers on a line)
    text = re.sub(r"(?m)^\s*Page\s+\d+\s*$", "", text)
    text = re.sub(r"(?m)^\s*\d+\s*$", "", text)
    return text.strip()


def detect_language(text: str) -> str:
    """Lightweight English check based on common word frequency."""
    english_markers = {"the", "and", "of", "to", "a", "in", "is", "it", "you", "that"}
    words = set(text.lower().split()[:200])
    overlap = len(words & english_markers)
    return "English" if overlap >= 3 else "Unknown"


# ═══════════════════════════════════════════════════════════════════════════════
#  CHUNKING
# ═══════════════════════════════════════════════════════════════════════════════

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 80) -> list[str]:
    """
    Split text into overlapping word-boundary chunks.
    chunk_size: target words per chunk
    overlap   : words shared between adjacent chunks
    """
    words = text.split()
    if len(words) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end == len(words):
            break
        start += chunk_size - overlap

    return chunks


# ═══════════════════════════════════════════════════════════════════════════════
#  EXTRACTIVE SUMMARISATION  (TF-IDF sentence scoring)
# ═══════════════════════════════════════════════════════════════════════════════

def _score_sentences(sentences: list[str], stop_words: set) -> dict[str, float]:
    """Score each sentence using TF-IDF-style word frequency."""
    # Word frequency across whole text
    word_freq: Counter = Counter()
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word.isalpha() and word not in stop_words:
                word_freq[word] += 1

    if not word_freq:
        return {s: 0.0 for s in sentences}

    max_freq = max(word_freq.values())
    word_freq = {w: f / max_freq for w, f in word_freq.items()}

    scores = {}
    for sent in sentences:
        score = sum(
            word_freq.get(w.lower(), 0.0)
            for w in word_tokenize(sent)
            if w.isalpha() and w.lower() not in stop_words
        )
        scores[sent] = score

    return scores


def extractive_summary(
    text: str,
    num_sentences: int = 5,
    style: str = "paragraph",
) -> str:
    """
    Pure extractive summary: pick top-scored sentences in original order.
    style: 'paragraph' | 'bullets'
    """
    stop_words = set(stopwords.words("english"))
    sentences = sent_tokenize(text)

    # Remove very short sentences
    sentences = [s for s in sentences if len(s.split()) > 6]

    if len(sentences) <= num_sentences:
        result = sentences
    else:
        scores = _score_sentences(sentences, stop_words)
        top = sorted(scores, key=scores.get, reverse=True)[:num_sentences]
        # Re-order by original position
        result = [s for s in sentences if s in top]

    if style == "bullets":
        return "\n".join(f"• {s.strip()}" for s in result)
    return " ".join(result)


# ═══════════════════════════════════════════════════════════════════════════════
#  KEYWORD & KEY IDEA EXTRACTION
# ═══════════════════════════════════════════════════════════════════════════════

def extract_keywords(text: str, top_n: int = 10) -> list[str]:
    """Return top_n meaningful keywords by TF score."""
    stop_words = set(stopwords.words("english"))
    words = [
        w.lower() for w in word_tokenize(text)
        if w.isalpha() and len(w) > 3 and w.lower() not in stop_words
    ]
    freq = Counter(words)
    return [word for word, _ in freq.most_common(top_n)]


def extract_key_ideas(text: str, n: int = 5) -> list[str]:
    """Extract n key idea sentences — highest density sentences, one per chunk."""
    stop_words = set(stopwords.words("english"))
    sentences = sent_tokenize(text)
    sentences = [s for s in sentences if len(s.split()) > 8]
    if not sentences:
        return []
    scores = _score_sentences(sentences, stop_words)
    sorted_sents = sorted(scores, key=scores.get, reverse=True)

    # Deduplicate: skip sentences too similar to already-chosen ones
    ideas = []
    chosen_words: set = set()
    for sent in sorted_sents:
        words = set(word_tokenize(sent.lower()))
        overlap = len(words & chosen_words) / max(len(words), 1)
        if overlap < 0.45:
            ideas.append(sent.strip())
            chosen_words |= words
        if len(ideas) >= n:
            break

    return ideas


# ═══════════════════════════════════════════════════════════════════════════════
#  CHUNK-LEVEL THEN DOCUMENT-LEVEL SUMMARISATION
# ═══════════════════════════════════════════════════════════════════════════════

def summarise_document(
    text: str,
    length: str = "medium",   # short | medium | detailed
    style: str = "paragraph", # paragraph | bullets
    chunk_size: int = 800,
    overlap: int = 80,
) -> dict:
    """
    Full pipeline:
      clean → chunk → extractive summary per chunk → combine → final summary
    Returns dict with all artefacts.
    """
    length_map = {"short": 3, "medium": 5, "detailed": 8}
    final_sents = {"short": 4, "medium": 7, "detailed": 12}
    sent_per_chunk = length_map.get(length, 5)

    cleaned = clean_text(text)
    language = detect_language(cleaned)
    chunks = chunk_text(cleaned, chunk_size=chunk_size, overlap=overlap)

    # Per-chunk summaries
    chunk_summaries = []
    for chunk in chunks:
        cs = extractive_summary(chunk, num_sentences=sent_per_chunk, style="paragraph")
        chunk_summaries.append(cs)

    combined = " ".join(chunk_summaries)

    # Final summary from combined chunk summaries
    final = extractive_summary(
        combined,
        num_sentences=final_sents.get(length, 7),
        style=style,
    )

    keywords = extract_keywords(cleaned)
    key_ideas = extract_key_ideas(cleaned, n=5)

    word_count_original = len(cleaned.split())
    word_count_summary  = len(final.split())
    compression = round((1 - word_count_summary / max(word_count_original, 1)) * 100, 1)

    return {
        "summary":        final,
        "key_ideas":      key_ideas,
        "keywords":       keywords,
        "chunks":         chunks,
        "chunk_summaries": chunk_summaries,
        "language":       language,
        "stats": {
            "original_words":  word_count_original,
            "summary_words":   word_count_summary,
            "compression_pct": compression,
            "num_chunks":      len(chunks),
            "num_sentences":   len(sent_tokenize(cleaned)),
        },
    }


# ── ROUGE-1 evaluation ────────────────────────────────────────────────────────

def rouge1_score(hypothesis: str, reference: str) -> dict:
    """Compute ROUGE-1 precision, recall, and F1."""
    stop = set(stopwords.words("english"))
    hyp  = [w.lower() for w in word_tokenize(hypothesis) if w.isalpha() and w.lower() not in stop]
    ref  = [w.lower() for w in word_tokenize(reference)  if w.isalpha() and w.lower() not in stop]

    if not hyp or not ref:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    hyp_c = Counter(hyp)
    ref_c = Counter(ref)
    overlap = sum((hyp_c & ref_c).values())

    precision = overlap / len(hyp)
    recall    = overlap / len(ref)
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    return {
        "precision": round(precision, 4),
        "recall":    round(recall,    4),
        "f1":        round(f1,        4),
    }


# ── CLI test ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys, pathlib

    sample = pathlib.Path("../sample_books/sherlock_holmes.txt")
    if len(sys.argv) > 1:
        sample = pathlib.Path(sys.argv[1])

    text = sample.read_text(encoding="utf-8")
    print(f"Input: {len(text.split())} words\n")

    result = summarise_document(text, length="medium", style="paragraph")

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(result["summary"])

    print("\nKEY IDEAS")
    for i, idea in enumerate(result["key_ideas"], 1):
        print(f"  {i}. {idea}")

    print("\nKEYWORDS:", ", ".join(result["keywords"]))
    print("\nSTATS:", json.dumps(result["stats"], indent=2))
