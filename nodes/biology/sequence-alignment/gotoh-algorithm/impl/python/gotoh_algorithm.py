# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gotoh-algorithm/. The authors are listed in prov/GKC398.jsonl.

from typing import Callable

NEG = float("-inf")
Score = Callable[[str, str], int]


def gotoh_algorithm(x: str, y: str, s: Score, d: int, e: int) -> tuple[int, str, str]:
    """Return (score, row1, row2): an optimal global alignment of x and y.

    The score is the sum of s(a, b) over the aligned pairs minus g(L) = d + (L - 1) e
    for each gap of length L. A gap is a maximal run of columns with a space in the
    same row. The method needs d >= e, so that one long gap never costs more than
    two shorter gaps of the same total length.
    """
    if d < e:
        raise ValueError("the recurrence needs d >= e")
    m, n = len(x), len(y)
    M = [[NEG] * (n + 1) for _ in range(m + 1)]
    X = [[NEG] * (n + 1) for _ in range(m + 1)]
    Y = [[NEG] * (n + 1) for _ in range(m + 1)]
    H = [[NEG] * (n + 1) for _ in range(m + 1)]
    M[0][0] = H[0][0] = 0  # @line L1
    for i in range(m + 1):  # @line L2
        for j in range(n + 1):  # @line L3
            if i == 0 and j == 0:  # @line L4
                continue
            if i > 0 and j > 0:
                M[i][j] = H[i - 1][j - 1] + s(x[i - 1], y[j - 1])  # @line L5
            if i > 0:
                X[i][j] = max(H[i - 1][j] - d, X[i - 1][j] - e)  # @line L6
            if j > 0:
                Y[i][j] = max(H[i][j - 1] - d, Y[i][j - 1] - e)  # @line L7
            H[i][j] = max(M[i][j], X[i][j], Y[i][j])  # @line L8

    # Traceback. The state names the matrix that the current value comes from.
    i, j, state = m, n, "H"  # @line L9
    top: list[str] = []
    bottom: list[str] = []
    while i > 0 or j > 0:  # @line L10
        if state == "H":  # @line L11
            if M[i][j] == H[i][j]:
                state = "M"
            elif X[i][j] == H[i][j]:
                state = "X"
            else:
                state = "Y"
        if state == "M":  # @line L12
            top.append(x[i - 1])
            bottom.append(y[j - 1])
            i, j, state = i - 1, j - 1, "H"
        elif state == "X":  # @line L13
            top.append(x[i - 1])
            bottom.append("-")
            state = "X" if X[i][j] == X[i - 1][j] - e else "H"  # @line L14
            i -= 1
        else:  # @line L15
            top.append("-")
            bottom.append(y[j - 1])
            state = "Y" if Y[i][j] == Y[i][j - 1] - e else "H"
            j -= 1
    return int(H[m][n]), "".join(reversed(top)), "".join(reversed(bottom))  # @line L16


def affine_score(row1: str, row2: str, s: Score, d: int, e: int) -> int:
    """Score a given alignment (two rows of equal length, '-' for a space)."""
    total, prev = 0, None
    for a, b in zip(row1, row2):
        if a == "-" and b == "-":
            raise ValueError("a column with two spaces")
        kind = "X" if b == "-" else "Y" if a == "-" else "M"
        if kind == "M":
            total += s(a, b)
        else:
            total -= e if kind == prev else d
        prev = kind
    return total
