"""Core N-gram language model data structures.

This module implements count-based N-gram models that are re-used by the
smoothing strategies defined in :mod:`smoothing`. The goal is to keep the code
simple and well documented so it can be used for educational purposes.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, List, MutableMapping, Sequence, Tuple


START_TOKEN = "<s>"
END_TOKEN = "</s>"
UNKNOWN_TOKEN = "<UNK>"


def pad_sentence(sentence: Sequence[str], n: int) -> List[str]:
    """Pad a tokenised sentence with start and end markers.

    Parameters
    ----------
    sentence:
        A sequence of already tokenised words.
    n:
        The order of the N-gram model. ``n-1`` start tokens will be added.

    Returns
    -------
    list[str]
        A new list containing padding markers.
    """

    padded: List[str] = [START_TOKEN] * (n - 1)
    padded.extend(sentence)
    padded.append(END_TOKEN)
    return padded


@dataclass
class Vocabulary:
    """Simple helper class to keep track of seen tokens."""

    words: Counter

    @classmethod
    def build(cls, tokens: Iterable[str]) -> "Vocabulary":
        counter = Counter(tokens)
        counter[UNKNOWN_TOKEN] += 1  # ensure unknown token exists
        return cls(counter)

    def __contains__(self, item: str) -> bool:
        return item in self.words

    def add(self, item: str) -> None:
        self.words[item] += 1

    def to_list(self) -> List[str]:
        return list(self.words.keys())

    @property
    def size(self) -> int:
        return len(self.words)


class NGramModel:
    """Count-based N-gram language model with optional lower-order backoff.

    The model stores counts of N-grams and their contexts. Higher-order models
    recursively build lower-order models to make smoothing strategies easier to
    implement.
    """

    def __init__(self, n: int, sentences: Sequence[Sequence[str]]):
        if n < 1:
            raise ValueError("n must be >= 1")
        self.n = n
        self.sentences = [list(sentence) for sentence in sentences]
        self.vocab = Vocabulary.build(token for sentence in self.sentences for token in sentence)
        self.vocab.add(START_TOKEN)
        self.vocab.add(END_TOKEN)

        self.ngram_counts: Counter[Tuple[str, ...]] = Counter()
        self.context_counts: Counter[Tuple[str, ...]] = Counter()
        self.next_word_counts: MutableMapping[Tuple[str, ...], Counter[str]] = defaultdict(Counter)

        self._build_counts()

        self.lower_order: NGramModel | None = None
        if n > 1:
            self.lower_order = NGramModel(n - 1, sentences)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _build_counts(self) -> None:
        for sentence in self.sentences:
            padded = pad_sentence(sentence, self.n)
            for i in range(self.n - 1, len(padded)):
                history = tuple(padded[i - self.n + 1 : i]) if self.n > 1 else tuple()
                ngram = (*history, padded[i]) if history else (padded[i],)
                self.ngram_counts[ngram] += 1
                if history:
                    self.context_counts[history] += 1
                    self.next_word_counts[history][ngram[-1]] += 1
                else:
                    self.context_counts[tuple()] = sum(self.ngram_counts.values())

    def _truncate_history(self, history: Sequence[str]) -> Tuple[str, ...]:
        if self.n == 1:
            return tuple()
        truncated = tuple(history[-(self.n - 1) :])
        if len(truncated) < self.n - 1:
            padding = (START_TOKEN,) * (self.n - 1 - len(truncated))
            return padding + truncated
        return truncated

    def _normalise_word(self, word: str) -> str:
        if word in self.vocab:
            return word
        return UNKNOWN_TOKEN

    def get_model_for_order(self, order: int) -> "NGramModel":
        if order < 1 or order > self.n:
            raise ValueError("order must be between 1 and n")
        if order == self.n:
            return self
        if self.lower_order is None:
            raise ValueError("lower order model not available")
        return self.lower_order.get_model_for_order(order)

    # ------------------------------------------------------------------
    # Probability helpers
    # ------------------------------------------------------------------
    def mle_probability(self, word: str, history: Sequence[str]) -> float:
        """Return the maximum-likelihood estimate for the given context."""

        history_tuple = self._truncate_history(history)
        word = self._normalise_word(word)
        if self.n == 1:
            total = sum(self.ngram_counts.values())
            count = self.ngram_counts[(word,)]
            if total == 0:
                return 1.0 / self.vocab.size
            return count / total

        context_total = self.context_counts.get(history_tuple, 0)
        if context_total == 0:
            return 1.0 / self.vocab.size
        count = self.next_word_counts.get(history_tuple, Counter()).get(word, 0)
        return count / context_total

    def probability(
        self,
        word: str,
        history: Sequence[str],
        smoother: "Smoother | None" = None,
    ) -> float:
        from .smoothing import NoSmoothing

        strategy: Smoother = smoother or NoSmoothing()
        return strategy.probability(word, tuple(history), self)

    # ------------------------------------------------------------------
    # Sampling helpers
    # ------------------------------------------------------------------
    def distribution(self, history: Sequence[str], smoother: "Smoother | None" = None) -> Dict[str, float]:
        history_tuple = self._truncate_history(history)
        probs = {
            word: self.probability(word, history_tuple, smoother)
            for word in self.vocab.to_list()
            if word != START_TOKEN
        }
        total = sum(probs.values())
        if total == 0.0:
            uniform = 1.0 / len(probs)
            return {word: uniform for word in probs}
        return {word: prob / total for word, prob in probs.items()}

    # ------------------------------------------------------------------
    # Utilities for external evaluation
    # ------------------------------------------------------------------
    def sentence_log_probability(
        self,
        sentence: Sequence[str],
        smoother: "Smoother | None" = None,
    ) -> float:
        import math

        padded = pad_sentence(sentence, self.n)
        total_log_prob = 0.0
        for i in range(self.n - 1, len(padded)):
            history = tuple(padded[i - self.n + 1 : i]) if self.n > 1 else tuple()
            word = padded[i]
            prob = self.probability(word, history, smoother)
            if prob <= 0.0:
                return float("-inf")
            total_log_prob += math.log(prob)
        return total_log_prob


class Smoother:
    """Protocol-like base class for smoothing strategies."""

    def probability(self, word: str, history: Sequence[str], model: NGramModel) -> float:
        raise NotImplementedError


if __name__ == "__main__":
    toy_sentences = [["the", "cat"], ["the", "dog"]]
    model = NGramModel(2, toy_sentences)
    print("Sample probability", model.probability("cat", ("the",)))
