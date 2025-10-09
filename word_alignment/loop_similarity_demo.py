"""Visual demonstration of the loop-based edit-distance similarity score."""

from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt

# ``loop_similarity_demo.py`` is sometimes launched directly with
# ``python loop_similarity_demo.py`` from the directory that contains it.  In
# that context ``__package__`` is ``None`` and relative imports (``from .foo``)
# fail.  To keep the teaching material resilient, fall back to importing from
# the parent directory when the module is executed as a script.
if __package__ in {None, ""}:
    PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))
    if PACKAGE_ROOT not in sys.path:
        sys.path.insert(0, PACKAGE_ROOT)

    from edit_distance_tools import (  # type: ignore[attr-defined]
        EditDistanceResult,
        compute_edit_distance,
        plot_manual_table,
        plot_visual_walkthrough,
    )
else:  # pragma: no cover - exercised when imported as part of the package
    from .edit_distance_tools import (
        EditDistanceResult,
        compute_edit_distance,
        plot_manual_table,
        plot_visual_walkthrough,
    )

if TYPE_CHECKING:
    # ``mypy``/``pyright`` should still understand the re-exported symbols.
    from .edit_distance_tools import EditDistanceResult as _EditDistanceResult

    EditDistanceResult = _EditDistanceResult


def demonstrate_loop_similarity(str1: str, str2: str) -> None:
    """Show every component of the loop-based edit-distance exercise."""

    result = compute_edit_distance(str1, str2)

    # Keep the main visuals but postpone rendering until we call ``plt.show``.
    plot_manual_table(result, show=False)
    plot_visual_walkthrough(result, show=False)
    _plot_loop_story(result, show=False)

    plt.show()


def _plot_loop_story(result: EditDistanceResult, *, show: bool) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    ax.axis("off")

    loops_text = [
        "Loop-based similarity pseudocode:",
        "for i in range(1, len(str1) + 1):",
        "    for j in range(1, len(str2) + 1):",
        "        dp[i][j] = min(↖ substitution/match, ↑ deletion, ← insertion)",
        "        # pick the operation with the smallest cumulative cost",
        "",
        f"Final Edit Distance: {result.distance}",
        f"Normalised Similarity Score: {result.similarity_score:.2f}",
        (
            "Backtrace visuals highlight the optimal path; the table retells it "
            "from the top-right corner down to the bottom-left like in class."
        ),
    ]

    ax.text(
        0.02,
        0.98,
        "\n".join(loops_text),
        fontsize=12,
        va="top",
        ha="left",
        linespacing=1.35,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#fdf2e9", edgecolor="#d35400", alpha=0.95),
    )

    if show:
        plt.show()

    return fig


if __name__ == "__main__":
    demonstrate_loop_similarity("kitten", "sitting")
