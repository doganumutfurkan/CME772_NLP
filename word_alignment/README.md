# Word Alignment & Edit Distance Module

This folder contains tools designed to reproduce the edit distance tables manually filled during lectures and to visualize the process. The visuals present both the Dynamic Programming (DP) matrix and the backtrace steps, following the classroom-style explanation from the top-right to the bottom-left.

## File Summary

* **`edit_distance_tools.py`** – Data classes for computing edit distance, helper functions for generating the DP matrix and backtrace, and high-level interfaces for producing visual outputs.
* **`loop_similarity_demo.py`** – Example script demonstrating the loop-based explanation, manual table, and library validation sequentially.
* **`__init__.py`** – Contains shortcut imports for the classes and functions exposed by the module.
* **`study.md`** – A study guide explaining the edit distance concept, related code, and examples step by step.
* **`çalışma_notları.md`** – Türkçe açıklamalar içeren ders notları.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # For Windows: .venv\\Scripts\\activate
pip install -r requirements.txt  # If there is no requirements file, install individually:
pip install matplotlib numpy textdistance
```

> `textdistance` is optional. If the library is not available, the script continues using an internal fallback implementation.

## How to Run the Demo

```bash
python -m word_alignment.loop_similarity_demo
```

The script opens Matplotlib windows in the following order:

1. **DP Heatmap** – Cell values, direction information, and backtrace path are highlighted from top-right to bottom-left.
2. **Manual Table** – Similar to classroom examples, words align to the lower-left corner, and each step explanation appears in the table.
3. **Library Comparison** – Displays the manual result side by side with the output from the `textdistance` library.

The script will not terminate until all figures are closed, allowing you to pause and take notes.

## Customization

* Create new tables by passing different words and costs to the `compute_edit_distance` function:

  ```python
  from word_alignment.edit_distance_tools import compute_edit_distance

  result = compute_edit_distance("flaw", "lawn", substitution_cost=1)
  ```
* Save generated figures to a file:

  ```python
  from word_alignment.edit_distance_tools import plot_manual_table

  fig = plot_manual_table(result, show=False)
  fig.savefig("manual_table.png", dpi=200)
  ```
* The `loop_similarity_demo.demonstrate_loop_similarity` function can be called with your own words to recreate the same sequence for new examples.

## Related Documents

* [study.md](./study.md): Concept summary, code flow, and example solutions.
