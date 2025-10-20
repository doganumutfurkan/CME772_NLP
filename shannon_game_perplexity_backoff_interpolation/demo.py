"""Demonstration script for Shannon game sampling and smoothing."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence

if __package__ is None or __package__ == "":  # pragma: no cover - runtime convenience
    import sys

    PACKAGE_ROOT = Path(__file__).resolve().parent
    sys.path.insert(0, str(PACKAGE_ROOT.parent))
    from shannon_game_perplexity_backoff_interpolation.corpus import load_default_corpus
    from shannon_game_perplexity_backoff_interpolation.ngram_model import NGramModel
    from shannon_game_perplexity_backoff_interpolation.perplexity import perplexity
    from shannon_game_perplexity_backoff_interpolation.preprocessing import prepare_corpus
    from shannon_game_perplexity_backoff_interpolation.sampling import shannon_game
    from shannon_game_perplexity_backoff_interpolation.smoothing import (
        InterpolationSmoother,
        KatzBackoffSmoother,
        NoSmoothing,
        StupidBackoffSmoother,
    )
else:  # pragma: no cover - import path resolved by Python
    from .corpus import load_default_corpus
    from .ngram_model import NGramModel
    from .perplexity import perplexity
    from .preprocessing import prepare_corpus
    from .sampling import shannon_game
    from .smoothing import (
        InterpolationSmoother,
        KatzBackoffSmoother,
        NoSmoothing,
        StupidBackoffSmoother,
    )


@dataclass
class ModelBundle:
    """Convenience container pairing a model and its name."""

    name: str
    model: NGramModel


def build_models(sentences: Sequence[Sequence[str]]) -> List[ModelBundle]:
    """Train unigram, bigram, and trigram models."""

    return [
        ModelBundle("Unigram", NGramModel(1, sentences)),
        ModelBundle("Bigram", NGramModel(2, sentences)),
        ModelBundle("Trigram", NGramModel(3, sentences)),
    ]


def compute_perplexities(
    models: Sequence[ModelBundle],
    sentences: Sequence[Sequence[str]],
) -> Dict[str, Dict[str, float]]:
    """Compute perplexity scores for models with different smoothers."""

    results: Dict[str, Dict[str, float]] = {}
    smoother_factories = {
        "MLE": lambda _model: NoSmoothing(),
        "Stupid Backoff": lambda _model: StupidBackoffSmoother(alpha=0.4),
        "Katz Backoff": lambda _model: KatzBackoffSmoother(discount=0.5),
        "Interpolation": lambda model: InterpolationSmoother([0.2, 0.3, 0.5][: model.n]),
    }
    for bundle in models:
        per_model: Dict[str, float] = {}
        for name, factory in smoother_factories.items():
            smoother = factory(bundle.model)
            try:
                score = perplexity(bundle.model, sentences, smoother)
            except ValueError:
                score = float("nan")
            per_model[name] = score
        results[bundle.name] = per_model
    return results


def print_perplexity_table(results: Dict[str, Dict[str, float]]) -> None:
    """Print a formatted perplexity comparison table."""

    headers = ["Model"] + list(next(iter(results.values())).keys())
    column_widths = [max(len(header), 12) for header in headers]
    row_format = " ".join(f"{{:<{width}}}" for width in column_widths)
    print("\nPerplexity comparison")
    print("=" * 80)
    print(row_format.format(*headers))
    for model_name, scores in results.items():
        row = [model_name]
        row.extend(f"{value:>10.2f}" if value != float("inf") else "       inf" for value in scores.values())
        print(row_format.format(*row))
    print("=" * 80)


def demonstrate_shannon(models: Sequence[ModelBundle]) -> None:
    """Generate Shannon game samples for each model."""

    print("\nShannon game samples")
    print("=" * 80)
    for bundle in models:
        sample_plain = shannon_game(bundle.model, seed=42)
        sample_smoothed = shannon_game(bundle.model, smoother=StupidBackoffSmoother(), seed=42)
        print(f"{bundle.name} (MLE):        {sample_plain}")
        print(f"{bundle.name} (Backoff):    {sample_smoothed}")
    print("=" * 80)


def main() -> None:
    """Run the full demonstration pipeline."""

    raw_text = load_default_corpus()
    sentences = prepare_corpus(raw_text)
    models = build_models(sentences)
    demonstrate_shannon(models)
    results = compute_perplexities(models, sentences)
    print_perplexity_table(results)


if __name__ == "__main__":
    main()
