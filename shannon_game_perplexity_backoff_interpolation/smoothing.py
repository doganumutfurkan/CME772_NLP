"""Smoothing strategies for count-based N-gram models."""

from __future__ import annotations

from typing import Sequence

from .ngram_model import NGramModel, Smoother


class NoSmoothing(Smoother):
    """Return the maximum-likelihood estimate without smoothing."""

    def probability(self, word: str, history: Sequence[str], model: NGramModel) -> float:
        return model.mle_probability(word, history)


class StupidBackoffSmoother(Smoother):
    """Implements the simple ("stupid") backoff heuristic."""

    def __init__(self, alpha: float = 0.4) -> None:
        if not 0.0 < alpha <= 1.0:
            raise ValueError("alpha must be between 0 and 1")
        self.alpha = alpha

    def probability(self, word: str, history: Sequence[str], model: NGramModel) -> float:
        history = model._truncate_history(history)
        count = model.next_word_counts.get(history, None)
        if count and count.get(word, 0) > 0:
            context_total = model.context_counts.get(history, 0)
            if context_total == 0:
                return 1.0 / model.vocab.size
            return count[word] / context_total
        if model.lower_order is not None:
            lower_history = history[1:] if history else tuple()
            return self.alpha * model.lower_order.probability(word, lower_history, self)
        return 1.0 / model.vocab.size


class KatzBackoffSmoother(Smoother):
    """Implements Katz backoff with a fixed discount ``d``.

    The algorithm discounts seen N-grams and redistributes the probability mass
    over unseen events using lower-order models.
    """

    def __init__(self, discount: float = 0.5) -> None:
        if not 0.0 < discount < 1.0:
            raise ValueError("discount must be in (0, 1)")
        self.discount = discount

    def probability(self, word: str, history: Sequence[str], model: NGramModel) -> float:
        history = model._truncate_history(history)
        count = model.next_word_counts.get(history, None)
        context_total = model.context_counts.get(history, 0)
        if count and count.get(word, 0) > 0 and context_total > 0:
            return (count[word] - self.discount) / context_total
        if model.lower_order is None:
            return 1.0 / model.vocab.size
        alpha = self._alpha(history, model)
        lower_history = history[1:] if history else tuple()
        lower_prob = model.lower_order.probability(word, lower_history, self)
        return alpha * lower_prob

    def _alpha(self, history: Sequence[str], model: NGramModel) -> float:
        context_total = model.context_counts.get(history, 0)
        if context_total == 0 or model.lower_order is None:
            return 1.0
        seen_counts = model.next_word_counts.get(history, {})
        discounted_sum = 0.0
        for value in seen_counts.values():
            if value > 0:
                discounted_sum += (value - self.discount) / context_total
        leftover = max(1.0 - discounted_sum, 0.0)
        if leftover == 0.0:
            return 0.0
        lower_total = 0.0
        for token in model.vocab.to_list():
            if token == "<s>" and history:
                continue
            if seen_counts.get(token, 0) == 0:
                lower_history = history[1:] if history else tuple()
                lower_total += model.lower_order.probability(token, lower_history, self)
        if lower_total == 0.0:
            return 0.0
        return leftover / lower_total


class InterpolationSmoother(Smoother):
    """Linear interpolation over all lower-order models."""

    def __init__(self, lambdas: Sequence[float]):
        if not lambdas:
            raise ValueError("lambdas must not be empty")
        if any(weight < 0 for weight in lambdas):
            raise ValueError("lambdas must be non-negative")
        self.lambdas = tuple(lambdas)

    def probability(self, word: str, history: Sequence[str], model: NGramModel) -> float:
        if len(self.lambdas) != model.n:
            raise ValueError("number of lambdas must match model order")
        total_weight = sum(self.lambdas)
        if total_weight == 0:
            raise ValueError("at least one lambda must be positive")
        weights = [weight / total_weight for weight in self.lambdas]
        probability_sum = 0.0
        for order in range(model.n, 0, -1):
            sub_model = model.get_model_for_order(order)
            sub_history = history[-(order - 1) :] if order > 1 else tuple()
            probability_sum += weights[order - 1] * sub_model.mle_probability(word, sub_history)
        return probability_sum


if __name__ == "__main__":  # pragma: no cover - manual smoke test
    from .ngram_model import NGramModel

    toy_sentences = [["the", "cat"], ["the", "dog"]]
    model = NGramModel(3, toy_sentences)
    smoother = InterpolationSmoother([0.2, 0.3, 0.5])
    print("Interpolation prob:", smoother.probability("cat", ("the", "black"), model))
