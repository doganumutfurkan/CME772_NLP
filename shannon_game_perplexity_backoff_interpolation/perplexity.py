"""Perplexity computations for N-gram models."""

from __future__ import annotations

import math
from typing import Sequence

from .ngram_model import NGramModel
from .smoothing import Smoother


def perplexity(
    model: NGramModel,
    sentences: Sequence[Sequence[str]],
    smoother: Smoother | None = None,
) -> float:
    """Compute the perplexity of a model on the provided sentences.

    Perplexity is defined as

    .. math:: PP(W) = P(w_1, \ldots, w_N)^{-1/N}

    where the joint probability is estimated via the N-gram model.
    """

    total_log_prob = 0.0
    total_tokens = 0
    for sentence in sentences:
        log_prob = model.sentence_log_probability(sentence, smoother)
        if log_prob == float("-inf"):
            return float("inf")
        total_log_prob += log_prob
        total_tokens += len(sentence) + 1  # include the end token
    if total_tokens == 0:
        return float("inf")
    avg_log_prob = total_log_prob / total_tokens
    return math.exp(-avg_log_prob)


if __name__ == "__main__":
    from .preprocessing import prepare_corpus

    toy_text = "To be, or not to be, that is the question."
    sentences = prepare_corpus(toy_text)
    model = NGramModel(2, sentences)
    print(perplexity(model, sentences))
