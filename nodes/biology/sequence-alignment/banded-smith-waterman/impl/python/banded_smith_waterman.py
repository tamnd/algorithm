# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/banded-smith-waterman/. The authors are listed in prov/HNEF8P.jsonl.

from typing import Callable

NEG = float("-inf")
Score = Callable[[str, str], int]


def banded_smith_waterman(
    x: str, y: str, s: Score, d: int, e: int, lo: int, hi: int
) -> tuple[int, str, str, int, int]:
    """Best local alignment of x and y whose path stays in the band lo <= j - i <= hi.

    Cell (i, j) is in the band when lo <= j - i <= hi. A gap of length L costs
    d + (L - 1) e, with d >= e >= 0. Return (score, row1, row2, i, j), where (i, j)
    is the cell where the alignment ends: its part of x ends with x[i - 1] and its
    part of y ends with y[j - 1]. The empty alignment has score 0 and (i, j) = (0, 0).
    """
    if d < e or e < 0:
        raise ValueError("the recurrence needs d >= e >= 0")
    m, n = len(x), len(y)
    w = hi - lo + 1
    if w <= 0:
        return 0, "", "", 0, 0
    # Row i keeps the cells j = i + lo .. i + hi at offsets 0 .. w - 1.
    H = [[NEG] * w for _ in range(m + 1)]
    M = [[NEG] * w for _ in range(m + 1)]
    X = [[NEG] * w for _ in range(m + 1)]
    Y = [[NEG] * w for _ in range(m + 1)]

    def get(T, i, j):
        k = j - i - lo
        if i < 0 or j < 0 or k < 0 or k >= w:
            return NEG
        return T[i][k]

    best, bi, bj = 0, 0, 0  # @line L1
    for i in range(m + 1):  # @line L2
        for j in range(max(0, i + lo), min(n, i + hi) + 1):  # @line L3
            k = j - i - lo
            if i > 0 and j > 0:
                M[i][k] = get(H, i - 1, j - 1) + s(x[i - 1], y[j - 1])  # @line L4
            X[i][k] = max(get(H, i - 1, j) - d, get(X, i - 1, j) - e)  # @line L5
            Y[i][k] = max(get(H, i, j - 1) - d, get(Y, i, j - 1) - e)  # @line L6
            H[i][k] = max(0, M[i][k], X[i][k], Y[i][k])  # @line L7
            if H[i][k] > best:  # @line L8
                best, bi, bj = H[i][k], i, j

    # Traceback from the best cell until a cell whose value is the 0 of a fresh start.
    if best == 0:
        return 0, "", "", 0, 0
    i, j, state = bi, bj, "H"  # @line L9
    top: list[str] = []
    bottom: list[str] = []
    while True:  # @line L10
        if state == "H":  # @line L11
            h = get(H, i, j)
            if h == 0:
                break
            state = "M" if get(M, i, j) == h else "X" if get(X, i, j) == h else "Y"
        if state == "M":  # @line L12
            top.append(x[i - 1])
            bottom.append(y[j - 1])
            i, j, state = i - 1, j - 1, "H"
        elif state == "X":  # @line L13
            top.append(x[i - 1])
            bottom.append("-")
            state = "X" if get(X, i, j) == get(X, i - 1, j) - e else "H"
            i -= 1
        else:  # @line L14
            top.append("-")
            bottom.append(y[j - 1])
            state = "Y" if get(Y, i, j) == get(Y, i, j - 1) - e else "H"
            j -= 1
    return int(best), "".join(reversed(top)), "".join(reversed(bottom)), bi, bj  # @line L15
