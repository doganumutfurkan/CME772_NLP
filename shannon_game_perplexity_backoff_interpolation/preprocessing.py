"""Utilities for preparing a toy corpus for N-gram modelling."""

from __future__ import annotations

import re
from typing import Iterable, List, Sequence

try:  # pragma: no cover - import may fail in restricted environments
    import nltk
except ImportError:  # pragma: no cover - fallback
    nltk = None


def normalise_whitespace(text: str) -> str:
    """Collapse consecutive whitespace to single spaces."""

    return re.sub(r"\s+", " ", text.strip())


def sentence_tokenise(text: str) -> List[str]:
    """Split text into sentences using NLTK's Punkt segmenter."""
    if nltk is None:
        # Simple regex-based sentence split as a fallback
        return [segment.strip() for segment in re.split(r"(?<=[.!?])\s+", text) if segment]
    nltk.download("punkt", quiet=True)
    return nltk.sent_tokenize(text)


def word_tokenise(sentence: str) -> List[str]:
    """Tokenise a sentence into words using NLTK."""
    if nltk is None:
        return re.findall(r"\b[\w']+\b|[^\w\s]", sentence)
    nltk.download("punkt", quiet=True)
    return nltk.word_tokenize(sentence)


def prepare_corpus(text: str) -> List[List[str]]:
    """Convert raw text into a list of token lists.

    The function lowercases the text, performs sentence segmentation, and
    tokenises each sentence.
    """

    cleaned = normalise_whitespace(text.lower())
    sentences = sentence_tokenise(cleaned)
    return [word_tokenise(sentence) for sentence in sentences]


def flatten(sentences: Iterable[Sequence[str]]) -> List[str]:
    """Flatten nested token lists for convenience."""

    return [token for sentence in sentences for token in sentence]


if __name__ == "__main__":
    SAMPLE_TEXT = "To be, or not to be, that is the question."
    tokenised = prepare_corpus(SAMPLE_TEXT)
    print(tokenised)
