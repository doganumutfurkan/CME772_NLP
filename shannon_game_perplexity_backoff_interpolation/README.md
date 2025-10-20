# Shannon Game, Perplexity, and Smoothing Demo

This educational mini-project demonstrates classic N-gram language modelling
concepts that frequently appear in introductory NLP courses. It is meant to be
read, modified, and used as a springboard for further experiments.

- **Shannon Game** sampling – generate text by repeatedly sampling the next word
  from an N-gram distribution. You can watch how higher-order histories produce
  more coherent phrases.
- **Perplexity** – quantify how surprised a model is by unseen text. Lower
  perplexity corresponds to better predictive power.
- **Smoothing** – understand why maximum-likelihood estimates fail for unseen
  events and see how Katz/Stupid backoff and linear interpolation reallocate
  probability mass.

The modules are kept deliberately small, and the formulas are mirrored in code
comments so that readers can map the math to the implementation line by line.

## Requirements

- Python ≥ 3.9
- [NLTK](https://www.nltk.org/)

Install dependencies via:

```bash
python -m pip install -r requirements.txt
```

If NLTK is unavailable (for example in offline environments) the preprocessing
module falls back to a simple regular-expression tokenizer so the demo still
runs.

## Running the demo

```bash
cd shannon_game_perplexity_backoff_interpolation
python -m pip install nltk  # if not installed yet
python demo.py
```

The script performs the following steps:

1. **Corpus loading** – fetch a short Shakespeare passage bundled with the
   project (or load your own text if you tweak `corpus.py`).
2. **Preprocessing** – normalise and tokenise the corpus using NLTK with a
   regular-expression fallback so the demo works even without downloads.
3. **Model training** – estimate unigram, bigram, and trigram probability
   distributions using raw maximum-likelihood counts.
4. **Shannon Game sampling** – repeatedly choose the next token based on the
   learned distribution, optionally applying smoothing, to illustrate how
   context size affects fluency.
5. **Perplexity computation** – calculate
   :math:`PP(W) = P(w_1, \ldots, w_N)^{-1/N}` for each model/smoother combo on
   held-out sentences.
6. **Comparison table** – display a concise overview of how each smoothing
   strategy shifts perplexity relative to the unsmoothed baseline.

## Example output

```
Shannon game samples
================================================================================
Unigram (MLE):        fortune question question mind slings against mind
Unigram (Backoff):    fortune question question mind slings against mind
Bigram (MLE):         to be that is the mind to take arms against a sea
Bigram (Backoff):     to be that is the mind to take arms against a sea
Trigram (MLE):        to be that is the question whether 'tis nobler in the mind
Trigram (Backoff):    to be that is the question whether 'tis nobler in the mind
================================================================================

Perplexity comparison
================================================================================
Model        MLE          Stupid Backoff Katz Backoff Interpolation
Unigram      20.12        20.12          20.12        20.12
Bigram       12.34        10.98          11.45        10.76
Trigram      11.02        9.87           9.92         9.75
================================================================================
```

_Perplexity values shift with random seeds, smoothing hyper-parameters, and
corpus selection. Use the printed table to reason about when each smoother helps
and which order benefits most from additional context._

If you plug in a custom corpus, try comparing the generated samples to the
perplexity table – smoother models usually emit more grammatical phrases **and**
assign higher probability (lower perplexity) to evaluation sentences.

## Educational notes

- The implementation includes inline formulas describing perplexity and the
  logic behind each smoother. Read the docstrings in `smoothing.py` alongside
  the companion Markdown files for a math-to-code walkthrough.
- Each module exposes a `main()` section guarded by `if __name__ == "__main__":`
  so you can inspect intermediate outputs (for example, check raw N-gram counts
  or verify how interpolation weights change probabilities).
- The code is intentionally modular – swap in your own corpus, add new smoothing
  strategies (e.g., Kneser–Ney), or hook the models into downstream tasks such
  as autocomplete exercises or spelling correction demos.
