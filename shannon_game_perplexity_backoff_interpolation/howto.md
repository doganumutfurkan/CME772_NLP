# How to work with the Shannon Game & Perplexity demo

This document explains each file in the project, how to run the demonstration
script, and provides short refreshers on the key concepts.

## Project files

- `corpus.py` – exposes helper functions to load the built-in Shakespeare quote
  or read text from disk.
- `demo.py` – orchestrates preprocessing, model training, Shannon sampling, and
  perplexity evaluation.
- `ngram_model.py` – implements the count-based N-gram models shared by all
  smoothers.
- `perplexity.py` – contains the `perplexity(model, sentences, smoother)`
  function.
- `preprocessing.py` – text normalisation plus sentence/word tokenisation with
  NLTK (and a regex-based fallback if NLTK is unavailable).
- `sampling.py` – provides the Shannon Game generator that repeatedly samples
  the next word given a history.
- `smoothing.py` – defines the `NoSmoothing`, `StupidBackoffSmoother`,
  `KatzBackoffSmoother`, and `InterpolationSmoother` strategies.
- `requirements.txt` – lists the required Python dependency (NLTK).

Each module includes a small `if __name__ == "__main__":` block for quick
experiments.

## Running the demo

```bash
python -m pip install -r requirements.txt
python demo.py
```

## Concept snippets

### Shannon Game

The Shannon Game samples each new word using the learned probability
distribution. In code:

```python
history = ("to", "be")
next_word = model.distribution(history)["that"]
```

### Perplexity

Perplexity measures how surprised a model is by a sequence. For tokens
:math:`w_1, \ldots, w_N`, the formula implemented in `perplexity.py` is:

```text
PP(W) = P(w_1, \ldots, w_N)^{-1/N}
```

### Backoff smoothing

Backoff strategies fall back to lower-order models when an N-gram has zero
counts. The Stupid Backoff probability for word :math:`w` given history
:math:`h` is:

```text
P_{SB}(w|h) =
  \begin{cases}
    \frac{c(hw)}{c(h)} & \text{if } c(hw) > 0 \\
    \alpha P_{SB}(w|h') & \text{otherwise}
  \end{cases}
```

### Katz backoff

Katz backoff discounts seen counts by a constant :math:`d` and redistributes the
remaining mass:

```text
P_{K}(w|h) =
  \begin{cases}
    \frac{c(hw) - d}{c(h)} & c(hw) > 0 \\
    \alpha(h) P_{K}(w|h') & \text{otherwise}
  \end{cases}
```

### Linear interpolation

Interpolation mixes different N-gram orders with weights :math:`\lambda_i`:

```text
P_{interp}(w|h) = \sum_{i=1}^{n} \lambda_i P_i(w|h_{i-1})
```

Experiment with the weights in `demo.py` to see how the distribution changes.
