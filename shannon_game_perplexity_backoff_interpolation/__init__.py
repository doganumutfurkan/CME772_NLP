"""Educational N-gram language modeling toolkit."""

from .ngram_model import NGramModel
from .smoothing import (
    KatzBackoffSmoother,
    StupidBackoffSmoother,
    InterpolationSmoother,
    NoSmoothing,
)
from .sampling import shannon_game
from .perplexity import perplexity

__all__ = [
    "NGramModel",
    "KatzBackoffSmoother",
    "StupidBackoffSmoother",
    "InterpolationSmoother",
    "NoSmoothing",
    "shannon_game",
    "perplexity",
]


if __name__ == "__main__":
    from .demo import main as demo_main

    demo_main()
