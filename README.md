# CME772_NLP

This project collects study materials and visualization tools for the CME772 Natural Language Processing course. The focus is on interactive exploration of weighted edit distance, alignment backtraces, and the programming patterns that implement them.

## Repository structure

- `word_alignment/`
  - `edit_distance_tools.py`: Core module with dataclasses and helpers for computing weighted edit distance matrices, extracting backtraces, and rendering explanatory figures.
  - `loop_similarity_demo.py`: Example script that imports the module to walk through the character-by-character loop, display the manual dynamic-programming table, and compare the classroom solution with a library implementation.
  - `__init__.py`: Convenience exports so that notebooks or follow-up assignments can import the visualization and computation utilities with `from word_alignment import ...`.
  - `readme.md`: Module-level notes that focus on alignment-specific visuals.

## Getting started

1. **Install dependencies**
   - Python 3.9+
   - `matplotlib`
   - `numpy`
   - `textdistance` (optional; used for the verification helper, but the module falls back to an internal implementation if it is unavailable.)

2. **Run the demo**
   ```bash
   python -m word_alignment.loop_similarity_demo
   ```
   The script opens a sequence of Matplotlib figures that illustrate:
   - The dynamic-programming grid with weights and annotated backtrace path.
   - A step-by-step table that narrates each alignment move (deletion, insertion, substitution).
   - A side-by-side comparison between the manual calculation and the `textdistance` library for cross-checking the final edit distance.

## Key features

- **Classroom-oriented orientation**: Both the heatmap and manual table are oriented so the path travels from the top-right start cell to the bottom-left origin, matching the lecture walkthrough.
- **Rich annotations**: Each visualization layers legends, cell highlights, and textual summaries to reinforce why each operation was chosen.
- **Reusable computation layer**: The `EditDistanceComputation` dataclass separates the DP matrix calculation from the plotting routines, making it easy to reuse the logic in assignments or notebooks.
- **Library verification**: The optional `LibraryDistanceCheck` helper demonstrates how to validate hand-worked solutions with an established NLP package.

## Extending the materials

- Swap in different words or cost configurations by instantiating `EditDistanceConfig` with new parameters.
- Use the exported `build_alignment_figures` and `run_loop_similarity_demo` functions as templates for new lesson plans.
- Incorporate the study notes in `study` for quick reminders about the algorithm and its NLP applications.

## License

The content is provided for educational use in CME772. Adapt it freely for personal study or classroom demonstrations.
