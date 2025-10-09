# Edit Distance Study Guide

This guide explains how the code in the `word_alignment` module works and introduces the basics of the edit distance concept through examples. All visuals follow the classroom convention of tracing the backtrace path from the top-right to the bottom-left.

## 1. Module Components

### 1.1 `compute_edit_distance`

* Calculates the weighted edit distance between two words.
* Returns the DP matrix, selected arrows (↖, ↑, ←), and the cells visited during backtrace.
* Default costs: insertion = 1, deletion = 1, substitution = 2.

### 1.2 `plot_manual_table`

* Generates a table layout that mimics the paper-style matrix used in lectures.
* Words are placed relative to the bottom-left corner; the top-right cell is the target point.
* Uses expanded boxes to prevent label overlap.

### 1.3 `plot_visual_walkthrough`

* Presents the heatmap, direction arrows, and operation summary within the same narrative.
* The backtrace path is emphasized using cell borders and connecting lines.

### 1.4 `compute_library_distance`

* Uses the `textdistance` package for verification when available.
* If unavailable, falls back to the internal Levenshtein implementation.

### 1.5 `loop_similarity_demo.demonstrate_loop_similarity`

* Executes all of the above steps with a single command.
* Adds an extra figure illustrating the nested loop pseudo-code and resulting scores.

## 2. Weighted Edit Distance Steps

The value of each cell is always the minimum of three possible moves:

1. **↖ Diagonal (Match / Substitution)**

   * No additional cost if characters match.
   * Adds `substitution_cost` if they differ.
2. **↑ Up (Deletion)** – Removes a character from the source word.
3. **← Left (Insertion)** – Adds a character to the target word.

The first row and column represent the cost of transforming an empty string into the other word (`i * deletion_cost`, `j * insertion_cost`). The backtrace always starts from the top-right cell and ends in the bottom-left corner.

## 3. Example 1 – "kitten" → "sitting"

This example uses the default words from the demo script.

```python
from word_alignment.edit_distance_tools import compute_edit_distance

result = compute_edit_distance("kitten", "sitting")
print(result.distance)  # 5
print(result.similarity_score)  # 0.29...
```

### 3.1 Key Cells

| Cell (i, j) | Characters | Selected Move  | Explanation                                             |
| ----------- | ---------- | -------------- | ------------------------------------------------------- |
| (1, 1)      | `k` vs `s` | ↖ Substitution | `k → s` cost 2, cheaper than other options.             |
| (3, 4)      | `t` vs `t` | ↖ Match        | Characters are the same, no cost added.                 |
| (6, 7)      | `n` vs `g` | ↑ Deletion     | `n` does not appear in target, deletion minimizes cost. |

### 3.2 Backtrace Story

1. **Start:** Top-right cell `(6, 7)` → total cost `5`.
2. **Deletion:** Character `n` removed (↑ move).
3. **Substitution:** `e → i` performed (↖ move, cost 2).
4. **Insertion:** Extra `g` in target added (← move).
5. **Matches:** Remaining `itt` sequence progresses diagonally (↖) without errors.
6. **End:** Arrives at bottom-left corner `(0, 0)`.

Calling `plot_visual_walkthrough(result)` highlights these steps using borders and lines, while `plot_manual_table(result)` rebuilds the table with extended columns.

## 4. Example 2 – Manual Practice with Short Words

Follow these steps to calculate the transformation of "ad" → "sad" manually:

1. Fill the first row and column:

   * `dp[0][0] = 0`
   * `dp[0][1] = 1` (insert s)
   * `dp[0][2] = 2` (insert s + a)
   * `dp[1][0] = 1` (delete a)
   * `dp[2][0] = 2` (delete a + d)
2. Compute each cell within nested loops:

```python
str1, str2 = "ad", "sad"
# dp table initialized with row 0 and column 0 values.
for i in range(1, len(str1) + 1):
    for j in range(1, len(str2) + 1):
        cost_sub = dp[i-1][j-1] + (0 if str1[i-1] == str2[j-1] else 2)
        cost_del = dp[i-1][j] + 1
        cost_ins = dp[i][j-1] + 1
        dp[i][j] = min(cost_sub, cost_del, cost_ins)
```

3. The top-right cell `(2, 3)` value is `2`; backtrace steps:

   * `d` matches `d` (↖).
   * `a` matches `a` (↖).
   * `s` added at the start (←).

This short example helps understand the behavior in longer word pairs.

## 5. Code Execution Tips

* To save figures generated during demos:

  ```python
  from word_alignment.edit_distance_tools import compute_edit_distance, plot_manual_table

  result = compute_edit_distance("flaw", "lawn")
  fig = plot_manual_table(result, show=False)
  fig.savefig("flaw_vs_lawn_manual.png", dpi=200)
  ```
* To test with different weights, pass parameters:

  ```python
  compute_edit_distance("kitten", "sitting", substitution_cost=1)
  ```

## 6. Use Cases in NLP

* **Spell Correction:** Converts user input into the closest word in a dictionary.
* **Automatic Grading:** Compares student answers against reference solutions.
* **Machine Translation Evaluation:** Measures difference between translation output and gold standard.
* **Speech Recognition / OCR:** Evaluates model accuracy using edit distance.

## 7. Study Strategies

1. Start by filling short word tables manually on paper.
2. Add short notes explaining why each move was selected.
3. Compare your hand calculations with the module's visuals.
4. Verify results side-by-side with `compute_library_distance` outputs.
5. Practice drawing diagrams from top-right → bottom-left, following the lecture’s convention.

Good luck and happy studying!
