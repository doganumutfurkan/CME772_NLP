"""
Teaching-oriented edit distance utilities.

The module exposes a small pipeline:

1. :func:`compute_edit_distance` builds the dynamic-programming matrix and
   records the preferred move for each cell.
2. :func:`plot_manual_table` visualises the DP grid exactly as it would appear
   on paper when filling it with nested ``for`` loops.
3. :func:`plot_visual_walkthrough` renders an annotated heatmap and creates a
   roomy companion figure that lists the backtrace steps in table form.

Convenience wrappers (:func:`edit_distance_manual` and
:func:`edit_distance_visual_pro`) mirror the names that were previously used in
notebooks so that existing material keeps working while benefitting from the new
layout.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch, Rectangle

__all__ = [
    "EditOperation",
    "EditDistanceResult",
    "LibraryDistanceCheck",
    "compute_edit_distance",
    "compute_library_distance",
    "plot_manual_table",
    "plot_visual_walkthrough",
    "plot_operations_table",
    "edit_distance_manual",
    "edit_distance_visual_pro",
]


@dataclass(frozen=True)
class EditOperation:
    """Represents a single step of the edit-distance backtrace."""

    kind: str
    from_char: str
    to_char: str
    cost: int
    arrow: str
    from_cell: Tuple[int, int]
    to_cell: Tuple[int, int]

    @property
    def action_label(self) -> str:
        """Return a compact textual description for tables."""

        mapping = {
            "match": f"Keep '{self.from_char}'",
            "sub": f"Sub '{self.from_char}'→'{self.to_char}'",
            "del": f"Del '{self.from_char}'",
            "ins": f"Ins '{self.to_char}'",
        }
        return mapping.get(self.kind, self.kind)

    @property
    def description(self) -> str:
        """Return a human-readable narration for notes."""

        if self.kind == "match":
            return f"Match '{self.from_char}' = '{self.to_char}'"
        if self.kind == "sub":
            return f"Substitute '{self.from_char}' → '{self.to_char}'"
        if self.kind == "del":
            return f"Delete '{self.from_char}' from str1"
        if self.kind == "ins":
            return f"Insert '{self.to_char}' into str1"
        return self.kind


@dataclass(frozen=True)
class EditDistanceResult:
    """Container returned by :func:`compute_edit_distance`."""

    source: str
    target: str
    dp: np.ndarray
    arrows: np.ndarray
    moves: np.ndarray
    path: List[Tuple[int, int]]
    operations: List[EditOperation]
    insertion_cost: int
    deletion_cost: int
    substitution_cost: int

    @property
    def distance(self) -> int:
        return int(self.dp[-1, -1])

    @property
    def similarity_score(self) -> float:
        """Normalised similarity score in ``[0, 1]`` based on edit distance."""

        denominator = max(len(self.source), len(self.target), 1)
        return 1.0 - (self.distance / denominator)


@dataclass(frozen=True)
class LibraryDistanceCheck:
    """Summary of an external-library verification run."""

    library_name: str
    distance: int | None
    similarity_score: float | None
    detail: str
    succeeded: bool

    @property
    def formatted_distance(self) -> str:
        return "N/A" if self.distance is None else str(self.distance)

    @property
    def formatted_similarity(self) -> str:
        if self.similarity_score is None:
            return "N/A"
        return f"{self.similarity_score:.2f}"


def compute_edit_distance(
    source: str,
    target: str,
    *,
    insertion_cost: int = 1,
    deletion_cost: int = 1,
    substitution_cost: int = 2,
) -> EditDistanceResult:
    """Compute the edit distance and capture metadata for teaching visuals."""

    m, n = len(source), len(target)
    dp = np.zeros((m + 1, n + 1), dtype=int)
    arrows = np.full((m + 1, n + 1), "", dtype=object)
    moves = np.full((m + 1, n + 1), "", dtype=object)
    moves[0, 0] = "start"

    for i in range(1, m + 1):
        dp[i, 0] = i * deletion_cost
        arrows[i, 0] = "↑"
        moves[i, 0] = "del"
    for j in range(1, n + 1):
        dp[0, j] = j * insertion_cost
        arrows[0, j] = "←"
        moves[0, j] = "ins"

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if source[i - 1] == target[j - 1]:
                dp[i, j] = dp[i - 1, j - 1]
                arrows[i, j] = "↖"
                moves[i, j] = "match"
            else:
                deletion = dp[i - 1, j] + deletion_cost
                insertion = dp[i, j - 1] + insertion_cost
                substitution = dp[i - 1, j - 1] + substitution_cost
                min_cost = min(deletion, insertion, substitution)
                dp[i, j] = min_cost
                if min_cost == substitution:
                    arrows[i, j] = "↖"
                    moves[i, j] = "sub"
                elif min_cost == deletion:
                    arrows[i, j] = "↑"
                    moves[i, j] = "del"
                else:
                    arrows[i, j] = "←"
                    moves[i, j] = "ins"

    path, operations = _backtrace(
        source,
        target,
        dp,
        moves,
        insertion_cost=insertion_cost,
        deletion_cost=deletion_cost,
        substitution_cost=substitution_cost,
    )

    return EditDistanceResult(
        source=source,
        target=target,
        dp=dp,
        arrows=arrows,
        moves=moves,
        path=path,
        operations=operations,
        insertion_cost=insertion_cost,
        deletion_cost=deletion_cost,
        substitution_cost=substitution_cost,
    )


def compute_library_distance(
    source: str,
    target: str,
    *,
    insertion_cost: int = 1,
    deletion_cost: int = 1,
    substitution_cost: int = 2,
) -> LibraryDistanceCheck:
    """Run an external reference implementation when available.

    The classroom exercises rely on weighted costs (insertion/deletion = 1,
    substitution = 2).  ``textdistance`` exposes a Levenshtein variant that can
    honour those weights, so we prefer it when present.  If the dependency is not
    installed, the function falls back to a bundled weighted implementation so
    the demo can still display a comparison and highlight that the external
    library is missing.
    """

    denominator = max(len(source), len(target), 1)
    weights = (insertion_cost, deletion_cost, substitution_cost)

    try:
        import textdistance  # type: ignore[import]
    except ImportError:
        fallback_distance = _weighted_levenshtein(source, target, weights)
        similarity = 1.0 - (fallback_distance / denominator)
        return LibraryDistanceCheck(
            library_name="textdistance (fallback)",
            distance=fallback_distance,
            similarity_score=similarity,
            detail=(
                "textdistance not installed; using bundled weighted Levenshtein "
                "to illustrate the expected outcome."
            ),
            succeeded=False,
        )

    algorithm = textdistance.Levenshtein(weights=weights)
    distance = int(algorithm.distance(source, target))
    similarity = 1.0 - (distance / denominator)
    return LibraryDistanceCheck(
        library_name="textdistance.Levenshtein",
        distance=distance,
        similarity_score=similarity,
        detail="Computed with textdistance.Levenshtein using custom weights.",
        succeeded=True,
    )


def _backtrace(
    source: str,
    target: str,
    dp: np.ndarray,
    moves: np.ndarray,
    *,
    insertion_cost: int,
    deletion_cost: int,
    substitution_cost: int,
) -> Tuple[List[Tuple[int, int]], List[EditOperation]]:
    arrow_map = {"match": "↖", "sub": "↖", "del": "↑", "ins": "←"}
    i, j = len(source), len(target)
    path: List[Tuple[int, int]] = [(i, j)]
    operations: List[EditOperation] = []

    while i > 0 or j > 0:
        move = moves[i, j]
        if move == "match":
            next_i, next_j = i - 1, j - 1
            op = EditOperation(
                kind="match",
                from_char=source[i - 1],
                to_char=target[j - 1],
                cost=0,
                arrow=arrow_map["match"],
                from_cell=(next_i, next_j),
                to_cell=(i, j),
            )
        elif move == "sub":
            next_i, next_j = i - 1, j - 1
            op = EditOperation(
                kind="sub",
                from_char=source[i - 1],
                to_char=target[j - 1],
                cost=substitution_cost,
                arrow=arrow_map["sub"],
                from_cell=(next_i, next_j),
                to_cell=(i, j),
            )
        elif move == "del":
            next_i, next_j = i - 1, j
            op = EditOperation(
                kind="del",
                from_char=source[i - 1],
                to_char="_",
                cost=deletion_cost,
                arrow=arrow_map["del"],
                from_cell=(next_i, next_j),
                to_cell=(i, j),
            )
        elif move == "ins":
            next_i, next_j = i, j - 1
            op = EditOperation(
                kind="ins",
                from_char="_",
                to_char=target[j - 1],
                cost=insertion_cost,
                arrow=arrow_map["ins"],
                from_cell=(next_i, next_j),
                to_cell=(i, j),
            )
        else:
            break

        operations.append(op)
        i, j = next_i, next_j
        path.append((i, j))

    if path[-1] != (0, 0):
        path.append((0, 0))

    return path, operations


def _orient_operations_for_display(
    operations: List[EditOperation],
    source_length: int,
) -> List[EditOperation]:
    """Flip the backtrace vertically so it starts top-right like class notes."""

    arrow_map = {"↖": "↙", "↑": "↓", "←": "←"}
    oriented: List[EditOperation] = []

    for op in operations:
        oriented.append(
            replace(
                op,
                arrow=arrow_map.get(op.arrow, op.arrow),
                to_cell=(source_length - op.to_cell[0], op.to_cell[1]),
                from_cell=(source_length - op.from_cell[0], op.from_cell[1]),
            )
        )

    return oriented


def plot_manual_table(
    result: EditDistanceResult,
    *,
    figsize: Tuple[float, float] | None = None,
    show: bool = False,
):
    """Plot the raw DP grid that results from the nested-loop computation."""

    dp_list = result.dp.tolist()
    m, n = len(result.source), len(result.target)
    fig_width = 1.4 * (n + 2)
    fig_height = 1.0 * (m + 2)
    fig, ax = plt.subplots(figsize=figsize or (fig_width, fig_height))
    ax.axis("off")

    table = ax.table(
        cellText=dp_list,
        rowLabels=["_"] + list(result.source),
        colLabels=["_"] + list(result.target),
        cellLoc="center",
        loc="center",
    )
    table.scale(1.15, 1.55)
    table.auto_set_font_size(False)
    table.set_fontsize(11)

    ax.set_title(
        (
            "Manual Edit Distance Dynamic Programming Table\n"
            f"Distance('{result.source}', '{result.target}') = {result.distance}"
        ),
        fontsize=13,
        pad=20,
    )

    if show:
        plt.show()
    return fig


def plot_visual_walkthrough(
    result: EditDistanceResult,
    *,
    show: bool = False,
):
    """Render the heatmap + notes figure and a spacious operations table."""

    heatmap_fig = _create_heatmap_figure(result)
    summary_fig = plot_operations_table(result, show=False)

    if show:
        plt.show()

    return heatmap_fig, summary_fig


def _create_heatmap_figure(result: EditDistanceResult) -> plt.Figure:
    dp = result.dp
    m, n = len(result.source), len(result.target)
    fig_width = 1.55 * (n + 3)
    fig_height = 1.55 * (m + 4)
    fig = plt.figure(figsize=(fig_width, fig_height))
    gs = fig.add_gridspec(
        2,
        2,
        height_ratios=[4.6, 1.2],
        width_ratios=[3.4, 2.2],
        hspace=0.45,
        wspace=0.45,
    )

    ax_heatmap = fig.add_subplot(gs[0, 0])
    # Flip the vertical orientation so the highlighted path travels from the
    # top-right towards the bottom-left just like it is traced during class
    # exercises.  ``origin='lower'`` keeps the numeric grid intact while
    # repositioning the visual start cell in the upper corner.
    im = ax_heatmap.imshow(dp, cmap=plt.cm.Blues, origin="lower")

    text_bbox = dict(boxstyle="round,pad=0.25", facecolor="white", alpha=0.82, edgecolor="none")
    move_colors = {
        "match": "#27ae60",
        "sub": "#d35400",
        "del": "#e74c3c",
        "ins": "#8e44ad",
        "start": "#34495e",
    }

    for i in range(m + 1):
        for j in range(n + 1):
            cost = dp[i, j]
            move_kind = result.moves[i, j]
            color = move_colors.get(move_kind, "#34495e")
            arrow = result.arrows[i, j]
            label = f"{cost}\n{arrow}" if arrow else f"{cost}"
            ax_heatmap.text(
                j,
                i,
                label,
                ha="center",
                va="center",
                color=color,
                fontsize=9,
                fontweight="bold",
                bbox=text_bbox,
                zorder=3,
            )

    highlight_palette = {
        "match": "#27ae60",
        "sub": "#d35400",
        "del": "#f1c40f",
        "ins": "#9b59b6",
    }
    oriented_operations = _orient_operations_for_display(result.operations, len(result.source))

    for (cell_i, cell_j), op in zip(result.path[:-1], result.operations):
        edge_color = highlight_palette.get(op.kind, "#2980b9")
        ax_heatmap.add_patch(
            Rectangle(
                (cell_j - 0.5, cell_i - 0.5),
                1,
                1,
                fill=False,
                edgecolor=edge_color,
                linewidth=2.6,
                zorder=4,
            )
        )

    path_cols = [j for (_, j) in result.path]
    path_rows = [i for (i, _) in result.path]
    ax_heatmap.plot(
        path_cols,
        path_rows,
        color="#f39c12",
        linewidth=2,
        marker="o",
        markersize=5,
        markerfacecolor="#fdf5e6",
        markeredgecolor="#d35400",
        zorder=5,
    )

    start_row, start_col = path_rows[0], path_cols[0]
    end_row, end_col = path_rows[-1], path_cols[-1]
    ax_heatmap.scatter([start_col], [start_row], color="#d35400", s=90, marker="*", zorder=6)
    ax_heatmap.scatter([end_col], [end_row], color="#2ecc71", s=70, marker="s", zorder=6)
    ax_heatmap.text(
        start_col - 0.3,
        start_row + 0.28,
        "Start (m,n) → top-right",
        color="#d35400",
        fontsize=10,
        weight="bold",
        ha="right",
        va="bottom",
    )
    ax_heatmap.text(
        end_col + 0.35,
        end_row - 0.35,
        "Finish (0,0) → bottom-left",
        color="#27ae60",
        fontsize=10,
        weight="bold",
        ha="left",
        va="top",
    )

    ax_heatmap.set_xticks(np.arange(n + 1))
    ax_heatmap.set_yticks(np.arange(m + 1))
    ax_heatmap.set_xticklabels(["_"] + list(result.target))
    ax_heatmap.set_yticklabels(["_"] + list(result.source))
    ax_heatmap.set_xlabel("Target (str2)", fontsize=11)
    ax_heatmap.set_ylabel("Source (str1)", fontsize=11)
    ax_heatmap.set_title(
        "Edit Distance Heatmap with Highlighted Backtrace",
        fontsize=13,
        pad=14,
    )

    fig.colorbar(im, ax=ax_heatmap, fraction=0.046, pad=0.04, label="Cell Cost")

    legend_handles = [
        Patch(facecolor=move_colors["match"], edgecolor="none", label="↖ Match / Keep (cost 0)"),
        Patch(facecolor=move_colors["sub"], edgecolor="none", label="↖ Substitution (cost 2)"),
        Patch(facecolor=move_colors["del"], edgecolor="none", label="↑ Deletion (cost 1)"),
        Patch(facecolor=move_colors["ins"], edgecolor="none", label="← Insertion (cost 1)"),
    ]
    ax_legend = fig.add_subplot(gs[1, 0])
    ax_legend.axis("off")
    legend = ax_legend.legend(
        handles=legend_handles,
        loc="center",
        ncol=2,
        frameon=True,
        framealpha=0.92,
        title="Arrow Legend",
        fontsize=9,
        title_fontsize=10,
    )
    legend._legend_box.align = "left"  # type: ignore[attr-defined]

    ax_notes = fig.add_subplot(gs[:, 1])
    ax_notes.axis("off")
    notes_lines = [
        "How to read the heatmap:",
        "• Rows = characters of str1 (source) with '_' bootstrap cell.",
        "• Columns = characters of str2 (target) with '_' bootstrap cell.",
        "• Nested loops fill the grid: outer loop over str1, inner loop over str2.",
        "• At each cell choose min of ← insert, ↑ delete, ↖ substitute/match.",
        "• Costs — insert: 1, delete: 1, substitute: 2, match: 0.",
        "• Heatmap backtrace now begins at the top-right and ends bottom-left.",
        "• Table narration matches the class path (top-right → bottom-left).",
        "• Arrow direction encodes the operation that minimised the cost.",
    ]
    ax_notes.text(
        0,
        1,
        "\n".join(notes_lines),
        fontsize=11,
        va="top",
        transform=ax_notes.transAxes,
    )

    if result.operations:
        ax_notes.text(
            0,
            1 - 0.08 * len(notes_lines) - 0.05,
            "Backtrace steps (top-right → bottom-left):",
            fontsize=11.5,
            fontweight="bold",
            va="top",
            transform=ax_notes.transAxes,
        )

        y_cursor = 1 - 0.08 * len(notes_lines) - 0.12
        for idx, op in enumerate(oriented_operations, start=1):
            step_text = (
                f"{idx}. {op.description} "
                f"({op.arrow} {op.to_cell} → {op.from_cell}, cost {op.cost})"
            )
            ax_notes.text(
                0,
                y_cursor,
                step_text,
                fontsize=10.5,
                va="top",
                transform=ax_notes.transAxes,
            )
            y_cursor -= 0.065
    else:
        ax_notes.text(
            0,
            0.2,
            "Strings identical — backtrace has no edits to perform.",
            fontsize=10.5,
            va="top",
            transform=ax_notes.transAxes,
        )

    return fig


def plot_operations_table(
    result: EditDistanceResult,
    *,
    show: bool = False,
):
    """Create a roomy table that lists backtrace steps one per row."""

    num_rows = max(len(result.operations), 1)
    fig_height = 0.95 * num_rows + 2.6
    fig, ax = plt.subplots(figsize=(9.0, fig_height))
    ax.axis("off")

    header = "Alignment Operations Overview (backtrace order)"
    ax.text(0.5, 0.95, header, ha="center", va="top", fontsize=12.5, fontweight="bold")

    oriented_ops = _orient_operations_for_display(result.operations, len(result.source))

    if oriented_ops:
        table_rows = [
            [
                idx,
                op.action_label,
                op.arrow,
                f"{op.to_cell}",
                f"{op.from_cell}",
                op.cost,
            ]
            for idx, op in enumerate(oriented_ops, start=1)
        ]
        col_labels = [
            "Step",
            "Action",
            "Move",
            "Current cell",
            "Next cell",
            "Cost",
        ]
        col_widths = [0.1, 0.34, 0.1, 0.18, 0.18, 0.1]
        table = ax.table(
            cellText=table_rows,
            colLabels=col_labels,
            loc="center",
            cellLoc="center",
            colWidths=col_widths,
        )
        table.scale(1.0, 2.5)
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.auto_set_column_width(list(range(len(col_labels))))

        for (row_idx, col_idx), cell in table.get_celld().items():
            cell._text.set_fontsize(11)
            if row_idx == 0:
                cell.set_facecolor("#ecf0f1")
                cell._text.set_weight("bold")
            elif row_idx % 2 == 1:
                cell.set_facecolor("#f8f9fa")

            if col_idx == 1:
                cell._text.set_ha("left")
            else:
                cell._text.set_ha("center")

            cell._text.set_va("center")
    else:
        ax.text(
            0.5,
            0.5,
            "No edits needed — the strings already match.",
            ha="center",
            va="center",
            fontsize=11,
        )

    summary = f"Final Edit Distance = {result.distance}"
    ax.text(0.5, 0.08, summary, ha="center", va="bottom", fontsize=11.5)
    ax.text(
        0.5,
        0.02,
        "Orientation: start at top-right, move left/down to reach bottom-left.",
        ha="center",
        va="bottom",
        fontsize=10.5,
        color="#2c3e50",
    )

    if show:
        plt.show()

    return fig


def edit_distance_manual(str1: str, str2: str, *, show: bool = True) -> int:
    """Convenience wrapper that mirrors the original function signature."""

    result = compute_edit_distance(str1, str2)
    plot_manual_table(result, show=show)
    return result.distance


def edit_distance_visual_pro(str1: str, str2: str, *, show: bool = True) -> int:
    """Convenience wrapper for the enhanced visual walkthrough."""

    result = compute_edit_distance(str1, str2)
    plot_visual_walkthrough(result, show=show)
    return result.distance


def _weighted_levenshtein(
    source: str, target: str, weights: Tuple[int, int, int]
) -> int:
    """Reference implementation mirroring ``textdistance`` weighting."""

    ins_cost, del_cost, sub_cost = weights
    m, n = len(source), len(target)
    dp = np.zeros((m + 1, n + 1), dtype=int)
    for i in range(1, m + 1):
        dp[i, 0] = i * del_cost
    for j in range(1, n + 1):
        dp[0, j] = j * ins_cost

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if source[i - 1] == target[j - 1]:
                dp[i, j] = dp[i - 1, j - 1]
            else:
                deletion = dp[i - 1, j] + del_cost
                insertion = dp[i, j - 1] + ins_cost
                substitution = dp[i - 1, j - 1] + sub_cost
                dp[i, j] = min(deletion, insertion, substitution)

    return int(dp[-1, -1])
