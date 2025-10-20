"""Shannon game style sampling for N-gram models."""

from __future__ import annotations

import random
from typing import List

from .ngram_model import END_TOKEN, START_TOKEN, NGramModel
from .smoothing import Smoother


def shannon_game(
    model: NGramModel,
    max_length: int = 20,
    smoother: Smoother | None = None,
    seed: int | None = None,
) -> str:
    """Generate a sentence using the Shannon game.

    Parameters
    ----------
    model:
        The trained :class:`~shannon_game_perplexity_backoff_interpolation.ngram_model.NGramModel`.
    max_length:
        Maximum number of tokens to sample (excluding padding tokens).
    smoother:
        Optional smoothing strategy to use during sampling.
    seed:
        Optional random seed for reproducibility.
    """

    if seed is not None:
        random.seed(seed)

    history: List[str] = [START_TOKEN] * (model.n - 1)
    generated: List[str] = []

    for _ in range(max_length):
        distribution = model.distribution(history, smoother)
        tokens = list(distribution.keys())
        probabilities = list(distribution.values())
        next_token = random.choices(tokens, weights=probabilities, k=1)[0]
        if next_token == END_TOKEN:
            break
        generated.append(next_token)
        if model.n > 1:
            history = (history + [next_token])[-(model.n - 1) :]
    return " ".join(generated)


if __name__ == "__main__":
    from .preprocessing import prepare_corpus

    toy_text = "To be, or not to be, that is the question."
    sentences = prepare_corpus(toy_text)
    model = NGramModel(2, sentences)
    print(shannon_game(model, seed=13))
