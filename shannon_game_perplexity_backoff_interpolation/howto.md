# How to work with the Shannon Game & Perplexity demo

This guide walks through every file in the repository, explains how the pieces
fit together, and recaps the language-modelling concepts the code illustrates.
Treat it as both a quick-start manual and a set of lecture notes you can extend.

## Project files

- `corpus.py` – utilities to load the bundled Shakespeare excerpt or read a
  custom text file. Use this when you want to plug in your own corpus.
- `demo.py` – the main driver. It performs preprocessing, trains each N-gram
  order, applies smoothing strategies, generates Shannon samples, and prints a
  perplexity comparison table.
- `ngram_model.py` – houses the generic count-based `NGramModel` class and its
  helpers for computing conditional probabilities.
- `perplexity.py` – defines the `perplexity(model, sentences, smoother)` helper
  with inline comments showing how the probability of a sequence is turned into
  the final :math:`PP(W)` score.
- `preprocessing.py` – normalisation plus sentence/word tokenisation. It tries
  NLTK first and falls back to a simple regex tokenizer if the NLTK data package
  is unavailable.
- `sampling.py` – implements the Shannon Game generator. Given a history, it
  samples the next token according to model probabilities (optionally smoothed).
- `smoothing.py` – contains the smoothing families: `NoSmoothing`,
  `StupidBackoffSmoother`, `KatzBackoffSmoother`, and `InterpolationSmoother`.
  Docstrings cross-reference the equations included later in this document.
- `requirements.txt` – lists Python dependencies so you can quickly reproduce the
  environment.

Each module includes a minimal `if __name__ == "__main__":` block so you can run
files individually for ad-hoc inspection (e.g., printing raw counts or sampling
from a single smoother).

## Running the demo

1. Install the dependency (NLTK) and the repository itself:

   ```bash
   python -m pip install -r requirements.txt
   ```

2. Execute the demo script from the project directory:

   ```bash
   python demo.py
   ```

3. Optional tweaks:
   - Pass the `--corpus` flag to `demo.py` to provide your own text file.
   - Modify the interpolation weights or backoff discounts near the top of
     `demo.py` and rerun to see how the perplexity table reacts.

The script prints example sentences produced by each model and a table comparing
perplexity under different smoothing strategies. Use these outputs to reason
about which settings produce the most fluent text versus the best predictive
scores.

## Concept snippets

### Shannon Game

The Shannon Game repeatedly samples the next token from the model's conditional
probabilities. Intuitively it is like asking the model to play a game of "guess
what word comes next" using a weighted die.

```python
from shannon_game_perplexity_backoff_interpolation.sampling import shannon_game

for word in shannon_game(model, max_tokens=12, smoother=smoother):
    print(word, end=" ")
```

Higher-order models (bigrams, trigrams) make use of longer histories so the
output typically feels more coherent than unigram sampling.

### Perplexity

Perplexity measures how surprised a model is by a sequence. For tokens
:math:`w_1, \ldots, w_N` we implement the textbook formula in `perplexity.py`:

```text
PP(W) = P(w_1, \ldots, w_N)^{-1/N}
```

The probability term expands into a product of conditional probabilities:
:math:`P(w_1, \ldots, w_N) = \prod_{i=1}^{N} P(w_i \mid h_i)` where :math:`h_i`
represents the relevant history (previous one or two tokens for bigrams and
trigrams). Lower perplexity means the model assigned higher probability to the
sequence, indicating better predictive ability.

### Backoff smoothing

Backoff strategies revert to lower-order models when an N-gram has zero counts.
Stupid Backoff, used in the demo, scales the lower-order probability by a fixed
factor :math:`\alpha`:

```text
P_{SB}(w|h) =
  \begin{cases}
    \frac{c(hw)}{c(h)} & c(hw) > 0 \\
    \alpha P_{SB}(w|h') & \text{otherwise}
  \end{cases}
```

Katz Backoff improves on this by discounting observed counts by :math:`d` and
redistributing the leftover mass through :math:`\alpha(h)`.

### Linear interpolation

Interpolation blends multiple N-gram orders using weights :math:`\lambda_i` that
sum to one:

```text
P_{interp}(w|h) = \sum_{i=1}^{n} \lambda_i P_i(w|h_{i-1})
```

By adjusting the weights in `demo.py` you can emphasise higher- or lower-order
contexts and observe how the Shannon samples and perplexity scores react.

---

Experiment freely: swap in a different corpus, add sentence boundary tokens, or
augment the evaluation metrics. The modular layout is designed to make such
extensions straightforward.
