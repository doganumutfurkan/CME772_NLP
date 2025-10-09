"""
edit_distance_tools.py
----------------------

A teaching-oriented module for Edit Distance (Levenshtein) calculations.
Includes both a manual loop-based implementation and a visualized version
with colored arrows, backtrace path, and character transformations.

Course: NLP - Edit Distance Assignment
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import Patch


# ==========================================================
# 1️⃣ Manual Edit Distance (for-loop version)
# ==========================================================
def edit_distance_manual(str1: str, str2: str) -> int:
    """
    Compute edit distance using dynamic programming with manual loops.
    Costs: insertion=1, deletion=1, substitution=2
    """
    m, n = len(str1), len(str2)
    dp = [[0 for _ in range(n+1)] for _ in range(m+1)]

    for i in range(m+1):
        dp[i][0] = i
    for j in range(n+1):
        dp[0][j] = j

    for i in range(1, m+1):
        for j in range(1, n+1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                deletion = dp[i-1][j] + 1
                insertion = dp[i][j-1] + 1
                substitution = dp[i-1][j-1] + 2
                dp[i][j] = min(deletion, insertion, substitution)

    fig, ax = plt.subplots(figsize=(1.4*(n+2), 1.0*(m+2)))
    ax.axis("off")

    table_data = [[dp[i][j] for j in range(n+1)] for i in range(m+1)]
    row_labels = ["_"] + list(str1)
    col_labels = ["_"] + list(str2)

    table = ax.table(cellText=table_data,
                     rowLabels=row_labels,
                     colLabels=col_labels,
                     cellLoc='center',
                     loc='center')
    table.scale(1, 1.3)
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    ax.set_title(
        f"Manual Edit Distance Dynamic Programming Table\nDistance('{str1}', '{str2}') = {dp[m][n]}",
        fontsize=12,
        pad=20,
    )
    plt.tight_layout()
    plt.show()
    return dp[m][n]


# ==========================================================
# 2️⃣ Visual Enhanced Version (colored arrows + path)
# ==========================================================
def edit_distance_visual_pro(str1: str, str2: str) -> int:
    """
    Visualize edit distance as a heatmap with:
    - colored arrows (↖, ↑, ←)
    - backtrace path (★)
    - character transformations and costs
    """
    m, n = len(str1), len(str2)
    dp = np.zeros((m+1, n+1), dtype=int)
    arrows = np.full((m+1, n+1), "", dtype=object)
    moves = np.full((m+1, n+1), "", dtype=object)

    # Initialization
    moves[0, 0] = "start"
    for i in range(1, m+1):
        dp[i, 0] = i
        arrows[i, 0] = "↑"
        moves[i, 0] = "del"
    for j in range(1, n+1):
        dp[0, j] = j
        arrows[0, j] = "←"
        moves[0, j] = "ins"

    # DP filling
    for i in range(1, m+1):
        for j in range(1, n+1):
            if str1[i-1] == str2[j-1]:
                dp[i, j] = dp[i-1, j-1]
                arrows[i, j] = "↖"
                moves[i, j] = "match"
            else:
                deletion = dp[i-1, j] + 1
                insertion = dp[i, j-1] + 1
                substitution = dp[i-1, j-1] + 2
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

    # Backtrace + operations
    i, j = m, n
    path = [(i, j)]
    operations = []
    arrow_for_op = {"match": "↖", "sub": "↖", "del": "↑", "ins": "←"}

    while i > 0 or j > 0:
        current_cell = (i, j)

        if i > 0 and j > 0 and str1[i-1] == str2[j-1]:
            next_cell = (i - 1, j - 1)
            operations.append(
                {
                    "op": "match",
                    "from_char": str1[i - 1],
                    "to_char": str2[j - 1],
                    "cost": 0,
                    "arrow": arrow_for_op["match"],
                    "from_cell": next_cell,
                    "to_cell": current_cell,
                }
            )
        elif i > 0 and j > 0 and dp[i, j] == dp[i - 1, j - 1] + 2:
            next_cell = (i - 1, j - 1)
            operations.append(
                {
                    "op": "sub",
                    "from_char": str1[i - 1],
                    "to_char": str2[j - 1],
                    "cost": 2,
                    "arrow": arrow_for_op["sub"],
                    "from_cell": next_cell,
                    "to_cell": current_cell,
                }
            )
        elif i > 0 and dp[i, j] == dp[i - 1, j] + 1:
            next_cell = (i - 1, j)
            operations.append(
                {
                    "op": "del",
                    "from_char": str1[i - 1],
                    "to_char": "_",
                    "cost": 1,
                    "arrow": arrow_for_op["del"],
                    "from_cell": next_cell,
                    "to_cell": current_cell,
                }
            )
        elif j > 0 and dp[i, j] == dp[i, j - 1] + 1:
            next_cell = (i, j - 1)
            operations.append(
                {
                    "op": "ins",
                    "from_char": "_",
                    "to_char": str2[j - 1],
                    "cost": 1,
                    "arrow": arrow_for_op["ins"],
                    "from_cell": next_cell,
                    "to_cell": current_cell,
                }
            )
        else:
            break

        i, j = next_cell
        path.append((i, j))

    if path[-1] != (0, 0):
        path.append((0, 0))

    # --- Visualization ---
    fig = plt.figure(figsize=(1.8*(n+2), 1.9*(m+3)))
    outer_gs = fig.add_gridspec(2, 1, height_ratios=[3.2, 1.5], hspace=0.55)
    top_gs = outer_gs[0].subgridspec(1, 2, width_ratios=[3.3, 1.2], wspace=0.35)

    ax = fig.add_subplot(top_gs[0, 0])
    im = ax.imshow(dp, cmap=plt.cm.Blues, origin="upper")

    # Arrows + colored labels
    text_bbox = dict(boxstyle="round,pad=0.25", facecolor="white", alpha=0.85, edgecolor="none")
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
            move_kind = moves[i, j]
            color = move_colors.get(move_kind, "#34495e")
            arrow = arrows[i, j]
            label = f"{cost}\n{arrow}" if arrow else f"{cost}"
            ax.text(
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

    # Backtrace highlight
    highlight_palette = {
        "match": "#27ae60",
        "sub": "#d35400",
        "del": "#f1c40f",
        "ins": "#9b59b6",
    }

    for (cell_i, cell_j), op in zip(path[:-1], operations):
        edge_color = highlight_palette.get(op["op"], "#2980b9")
        ax.add_patch(
            Rectangle(
                (cell_j - 0.5, cell_i - 0.5),
                1,
                1,
                fill=False,
                edgecolor=edge_color,
                linewidth=2.5,
                zorder=4,
            )
        )

    path_cols = [j for (_, j) in path]
    path_rows = [i for (i, _) in path]
    ax.plot(
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

    # Annotate start/end for clarity
    start_row, start_col = path_rows[0], path_cols[0]
    end_row, end_col = path_rows[-1], path_cols[-1]
    ax.scatter([start_col], [start_row], color="#d35400", s=90, marker="*", zorder=6)
    ax.scatter([end_col], [end_row], color="#2ecc71", s=70, marker="s", zorder=6)
    ax.text(
        start_col - 0.2,
        start_row - 0.25,
        "Start (m,n)",
        color="#d35400",
        fontsize=10,
        weight="bold",
        ha="right",
        va="top",
    )
    ax.text(
        end_col + 0.35,
        end_row + 0.3,
        "Finish (0,0)",
        color="#27ae60",
        fontsize=10,
        weight="bold",
        ha="left",
        va="bottom",
    )

    ax.set_xticks(np.arange(n+1))
    ax.set_yticks(np.arange(m+1))
    ax.set_xticklabels(["_"] + list(str2))
    ax.set_yticklabels(["_"] + list(str1))
    ax.set_xlabel("Target (str2)", fontsize=11)
    ax.set_ylabel("Source (str1)", fontsize=11)
    ax.set_title("Edit Distance Heatmap with Colored Arrows & Character Backtrace", fontsize=13)
    plt.colorbar(im, ax=ax, label="Cost Value")

    # Legend and cheat sheet
    legend_elements = [
        Patch(facecolor=move_colors["match"], edgecolor="none", label="↖ Match / Keep (cost 0)"),
        Patch(facecolor=move_colors["sub"], edgecolor="none", label="↖ Substitution (cost 2)"),
        Patch(facecolor=move_colors["del"], edgecolor="none", label="↑ Deletion (cost 1)"),
        Patch(facecolor=move_colors["ins"], edgecolor="none", label="← Insertion (cost 1)"),
    ]
    ax.legend(
        handles=legend_elements,
        loc="upper left",
        bbox_to_anchor=(0, 1.02),
        frameon=True,
        framealpha=0.9,
        title="Arrow Legend",
        fontsize=9,
        title_fontsize=10,
        ncol=2,
    )

    ax_notes = fig.add_subplot(top_gs[0, 1])
    ax_notes.axis("off")
    notes_lines = [
        "How to read the table:",
        "• Rows = source string (str1) characters including '_' for start.",
        "• Columns = target string (str2) characters including '_' for start.",
        "• Costs: insertion = 1, deletion = 1, substitution = 2, match = 0.",
        "• Initialization fills the first row/column with incremental costs.",
        "• Choose the minimum of ← insertion, ↑ deletion, ↖ substitution/match.",
        "• Backtrace starts at the bottom-right cell (final cost) and follows the arrows",
        "  until reaching the top-left start cell.",
        "• Left (←) = insert into str1, Down (↑) = delete from str1,",
        "  Diagonal (↖) = match/substitute characters.",
        "• Nested loops compute every cell: outer loop over str1, inner loop over str2.",
    ]
    y_cursor = 1.0
    ax_notes.text(
        0,
        y_cursor,
        "\n".join(notes_lines),
        fontsize=11,
        va="top",
        transform=ax_notes.transAxes,
    )

    y_cursor -= 0.05 * len(notes_lines) + 0.05
    ax_notes.text(
        0,
        y_cursor,
        "Backtrace Steps (bottom-right to top-left):",
        fontsize=11.5,
        fontweight="bold",
        va="top",
        transform=ax_notes.transAxes,
    )

    step_lines = []
    for idx, op in enumerate(operations, start=1):
        start_cell = op["to_cell"]
        end_cell = op["from_cell"]
        start_label = f"({start_cell[0]}, {start_cell[1]})"
        end_label = f"({end_cell[0]}, {end_cell[1]})"
        if op["op"] == "match":
            desc = f"Match '{op['from_char']}' = '{op['to_char']}'"
        elif op["op"] == "sub":
            desc = f"Substitute '{op['from_char']}' → '{op['to_char']}'"
        elif op["op"] == "del":
            desc = f"Delete '{op['from_char']}' from str1"
        else:
            desc = f"Insert '{op['to_char']}' into str1"
        step_lines.append(
            f"{idx}. {desc} ({op['arrow']} {start_label} → {end_label}, cost {op['cost']})"
        )

    if step_lines:
        for line in step_lines:
            y_cursor -= 0.06
            ax_notes.text(
                0,
                y_cursor,
                line,
                fontsize=10.5,
                va="top",
                transform=ax_notes.transAxes,
            )
    else:
        y_cursor -= 0.06
        ax_notes.text(
            0,
            y_cursor,
            "Strings already identical — no edits needed.",
            fontsize=10.5,
            va="top",
            transform=ax_notes.transAxes,
        )

    # Alignment summary table
    ax_table = fig.add_subplot(outer_gs[1, 0])
    ax_table.axis("off")
    total_cost = 0
    table_rows = []
    for idx, op in enumerate(operations, start=1):
        total_cost += op["cost"]
        action = {
            "match": f"Keep '{op['from_char']}'",
            "sub": f"Sub '{op['from_char']}'→'{op['to_char']}'",
            "del": f"Del '{op['from_char']}'",
            "ins": f"Ins '{op['to_char']}'",
        }[op["op"]]
        coord_text = f"{op['to_cell']} → {op['from_cell']}"
        table_rows.append([idx, action, op["arrow"], coord_text, op["cost"]])

    if table_rows:
        table = ax_table.table(
            cellText=table_rows,
            colLabels=["Step", "Action", "Move", "Cells (from → to)", "Cost"],
            cellLoc="center",
            loc="center",
        )
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.05, 1.35)

    summary_text = f"Final Edit Distance = {dp[m, n]} (Total Cost = {total_cost})"
    ax_table.text(0.5, 0.96, "Alignment Operations Overview", ha="center", va="top", fontsize=12.5, fontweight="bold")
    ax_table.text(0.5, 0.08, summary_text, ha="center", va="bottom", fontsize=11.5)

    plt.tight_layout()
    plt.show()

    return dp[m,n]


# ==========================================================
# 3️⃣ Example Runner
# ==========================================================
if __name__ == "__main__":
    edit_distance_manual("kitten", "sitting")
    edit_distance_visual_pro("kitten", "sitting")
