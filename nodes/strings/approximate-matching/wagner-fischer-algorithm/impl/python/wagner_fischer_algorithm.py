# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wagner-fischer-algorithm/. The authors are listed in prov/ZX8DFX.jsonl.

"""Levenshtein distance by the Wagner-Fischer dynamic program.

The edit model is unit cost: insertion, deletion and substitution each cost 1,
and there are no transpositions. Indices are 0-based.
"""


def edit_table(x: str, y: str) -> list[list[int]]:
    """Return the table D with D[i][j] = distance of x[:i] and y[:j].

    Precondition: none. Cost: Theta(len(x) * len(y)) time and space.
    """
    m, n = len(x), len(y)
    d = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):  # @line L1
        d[i][0] = i
    for j in range(n + 1):  # @line L2
        d[0][j] = j
    for i in range(1, m + 1):  # @line L3
        for j in range(1, n + 1):  # @line L4
            c = 0 if x[i - 1] == y[j - 1] else 1  # @line L5
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + c)  # @line L6
    return d


def edit_distance(x: str, y: str) -> int:
    """Return the Levenshtein distance of x and y.

    Keeps two rows over the shorter string. Cost: Theta(len(x) * len(y))
    time and O(min(len(x), len(y))) extra space.
    """
    if len(y) > len(x):
        x, y = y, x
    n = len(y)
    prev = list(range(n + 1))
    for i in range(1, len(x) + 1):
        cur = [i] + [0] * n
        xi = x[i - 1]
        for j in range(1, n + 1):
            c = 0 if xi == y[j - 1] else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + c)
        prev = cur
    return prev[n]  # @line L7


def alignment(x: str, y: str) -> list[tuple[str, str]]:
    """Return an optimal alignment of x and y as a list of columns (a, b).

    A column ("a", "b") is a match when a == b and a substitution when a != b,
    ("a", "") is a deletion and ("", "b") is an insertion. The number of
    columns with a != b is the distance. Cost: Theta(len(x) * len(y)).
    """
    d = edit_table(x, y)
    i, j = len(x), len(y)  # @line L8
    cols: list[tuple[str, str]] = []
    while i > 0 or j > 0:  # @line L9
        if i > 0 and j > 0 and d[i][j] == d[i - 1][j - 1] + (x[i - 1] != y[j - 1]):  # @line L10
            cols.append((x[i - 1], y[j - 1]))
            i, j = i - 1, j - 1
        elif i > 0 and d[i][j] == d[i - 1][j] + 1:  # @line L11
            cols.append((x[i - 1], ""))
            i -= 1
        else:  # @line L12
            cols.append(("", y[j - 1]))
            j -= 1
    cols.reverse()
    return cols  # @line L13
