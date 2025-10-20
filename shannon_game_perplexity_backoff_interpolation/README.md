# Shannon Game, Perplexity, and Smoothing Demo

This educational mini-project demonstrates classic N-gram language modelling
concepts that frequently appear in introductory NLP courses:

- **Shannon Game** sampling – generating text by rolling the probabilistic dice of
  an N-gram model.
- **Perplexity** – measuring how surprised a model is by held-out data.
- **Smoothing** – comparing maximum-likelihood estimates with Katz and Stupid
  backoff as well as linear interpolation.

The project is intentionally lightweight so that students can read through the
implementation, experiment with parameters, and extend the toolkit for their own
assignments.

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

1. Load a short Shakespeare quote that serves as the toy corpus.
2. Preprocess the text using NLTK sentence and word tokenisers.
3. Train unigram, bigram, and trigram models.
4. Generate Shannon Game samples with and without smoothing.
5. Compute perplexity values for each model and smoothing strategy.
6. Print a comparison table summarising perplexity differences.

## Example output

```
Shannon game samples
================================================================================
Unigram (MLE):        fortune question question mind slings against mind
Unigram (Backoff):    fortune question question mind slings against mind
Bigram (MLE):         to be that is the mind to take arms against a sea
Bigram (Backoff):    to be that is the mind to take arms against a sea
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

_Perplexity numbers will differ depending on the random seed, the smoothing
hyper-parameters, and the corpus size, but the table highlights how smoothing
usually improves predictive performance._

## Educational notes

- The implementation includes inline formulas describing perplexity and the
  logic behind each smoother.
- Each module exposes a `main()` section guarded by
  `if __name__ == "__main__":` so you can run them individually while
  experimenting.
- The code is intentionally modular – feel free to swap in your own corpus, add
  new smoothing strategies, or hook the models into downstream tasks.
