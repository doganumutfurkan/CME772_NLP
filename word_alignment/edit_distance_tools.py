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

    print("Edit Distance Table:")
    for row in dp:
        print(row)
    print(f"\nFinal Distance between '{str1}' and '{str2}' = {dp[m][n]}")
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

    # Initialization
    for i in range(1, m+1):
        dp[i, 0] = i
        arrows[i, 0] = "↑"
    for j in range(1, n+1):
        dp[0, j] = j
        arrows[0, j] = "←"

    # DP filling
    for i in range(1, m+1):
        for j in range(1, n+1):
            if str1[i-1] == str2[j-1]:
                dp[i, j] = dp[i-1, j-1]
                arrows[i, j] = "↖"
            else:
                deletion = dp[i-1, j] + 1
                insertion = dp[i, j-1] + 1
                substitution = dp[i-1, j-1] + 2
                min_cost = min(deletion, insertion, substitution)
                dp[i, j] = min_cost
                if min_cost == substitution:
                    arrows[i, j] = "↖"
                elif min_cost == deletion:
                    arrows[i, j] = "↑"
                else:
                    arrows[i, j] = "←"

    # Backtrace + operations
    i, j = m, n
    path, operations = [], []
    while i > 0 or j > 0:
        path.append((i, j))
        if i > 0 and j > 0 and str1[i-1] == str2[j-1]:
            operations.append(("match", str1[i-1], str2[j-1]))
            i -= 1; j -= 1
        elif i > 0 and j > 0 and dp[i,j] == dp[i-1,j-1] + 2:
            operations.append(("sub", str1[i-1], str2[j-1]))
            i -= 1; j -= 1
        elif i > 0 and dp[i,j] == dp[i-1,j] + 1:
            operations.append(("del", str1[i-1], "_"))
            i -= 1
        elif j > 0 and dp[i,j] == dp[i,j-1] + 1:
            operations.append(("ins", "_", str2[j-1]))
            j -= 1
        else:
            break
    path.append((0, 0))
    path = path[::-1]
    operations = operations[::-1]

    # --- Visualization ---
    fig, ax = plt.subplots(figsize=(1.7*(n+2), 1.4*(m+2)))
    im = ax.imshow(dp, cmap=plt.cm.Blues, origin="upper")

    # Arrows + colored labels
    for i in range(m+1):
        for j in range(n+1):
            arrow = arrows[i,j]
            cost = dp[i,j]
            if arrow == "↖": arrow_color = "green"
            elif arrow == "↑": arrow_color = "red"
            elif arrow == "←": arrow_color = "purple"
            else: arrow_color = "gray"
            label = f"{cost}\n{arrow}"
            ax.text(j, i, label, ha='center', va='center',
                    color=arrow_color, fontsize=9, fontweight='bold')

    # Backtrace (★)
    for (i, j) in path:
        if i>0 and j>0:
            s1, s2 = str1[i-1], str2[j-1]
            if s1 == s2:
                label, color = f"★{s1}", "limegreen"
            elif dp[i,j] == dp[i-1,j-1] + 2:
                label, color = f"★{s1}→{s2}", "orangered"
            elif dp[i,j] == dp[i-1,j] + 1:
                label, color = f"★{s1}", "darkorange"
            else:
                label, color = f"★→{s2}", "mediumorchid"
            ax.text(j, i, label, ha='center', va='center',
                    color=color, fontsize=10, fontweight='bold')

    ax.set_xticks(np.arange(n+1))
    ax.set_yticks(np.arange(m+1))
    ax.set_xticklabels(["_"] + list(str2))
    ax.set_yticklabels(["_"] + list(str1))
    ax.set_xlabel("Target (str2)", fontsize=11)
    ax.set_ylabel("Source (str1)", fontsize=11)
    ax.set_title("Edit Distance Heatmap with Colored Arrows & Character Backtrace", fontsize=13)
    plt.colorbar(im, ax=ax, label="Cost Value")
    plt.tight_layout()
    plt.show()

    # Print alignment operations
    print("Alignment Operations:")
    print(f"{'Op':10} {'From':10} {'To':10}")
    print("-"*30)
    total_cost = 0
    for op, a, b in operations:
        cost = 0 if op=="match" else 2 if op=="sub" else 1
        total_cost += cost
        print(f"{op:10} {a:10} {b:10} (cost={cost})")
    print(f"\n✅ Final Edit Distance = {dp[m,n]} (Total Cost = {total_cost})")

    return dp[m,n]


# ==========================================================
# 3️⃣ Example Runner
# ==========================================================
if __name__ == "__main__":
    print("Manual Test:")
    edit_distance_manual("kitten", "sitting")

    print("\nVisual Test:")
    edit_distance_visual_pro("kitten", "sitting")
