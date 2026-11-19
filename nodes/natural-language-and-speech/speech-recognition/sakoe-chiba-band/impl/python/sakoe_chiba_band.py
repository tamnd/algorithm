# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sakoe-chiba-band/. The authors are listed in prov/HMGHCC.jsonl.

"""DTW restricted to a Sakoe-Chiba band.

x = x_1 ... x_n and y = y_1 ... y_m. A warping path from (1, 1) to (n, m) uses
the steps (1, 0), (0, 1) and (1, 1). The band of width r keeps only the cells
with |i - j| <= r, so a path in the band exists if and only if |n - m| <= r.
The recurrence is the symmetric1 pattern of the dynamic-time-warping page:

    D[i][j] = d(x_i, y_j) + min(D[i-1][j-1], D[i-1][j], D[i][j-1]),

with D[0][0] = 0 and every other cell outside the band at infinity. Only the
cells of the band are stored, so time and memory are O(n r) for r >= 1.
"""

import math
from typing import Callable, Dict, Sequence, Tuple

INF = math.inf


def abs_dist(a, b) -> float:
    return abs(a - b)


def band_dtw(x: Sequence, y: Sequence, r: int, dist: Callable = abs_dist):
    """Return (cost, path, cells): the best cost in the band, a best path, and the number of cells filled.

    Ties in the traceback go to the diagonal, then (i - 1, j), then (i, j - 1).
    Raise ValueError if no warping path fits in the band (|n - m| > r).
    """
    n, m = len(x), len(y)
    if n == 0 or m == 0 or r < 0:
        raise ValueError("need non-empty sequences and r >= 0")
    if abs(n - m) > r:  # @line L1
        raise ValueError("no warping path fits in the band: |n - m| > r")
    D: Dict[Tuple[int, int], float] = {(0, 0): 0.0}  # @line L2
    back: Dict[Tuple[int, int], Tuple[int, int]] = {}
    for i in range(1, n + 1):  # @line L3
        for j in range(max(1, i - r), min(m, i + r) + 1):  # @line L4
            best, arg = D.get((i - 1, j - 1), INF), (i - 1, j - 1)  # @line L5
            for cell in ((i - 1, j), (i, j - 1)):
                v = D.get(cell, INF)
                if v < best:
                    best, arg = v, cell
            D[(i, j)] = dist(x[i - 1], y[j - 1]) + best
            back[(i, j)] = arg
    path = [(n, m)]
    while path[-1] != (1, 1):
        path.append(back[path[-1]])
    path.reverse()
    return D[(n, m)], path, len(D) - 1  # @line L6


def full_dtw(x: Sequence, y: Sequence, dist: Callable = abs_dist) -> float:
    """The unconstrained symmetric1 DTW cost, O(n m), for comparison."""
    n, m = len(x), len(y)
    D = [[INF] * (m + 1) for _ in range(n + 1)]
    D[0][0] = 0.0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i][j] = dist(x[i - 1], y[j - 1]) + min(D[i - 1][j - 1], D[i - 1][j], D[i][j - 1])
    return D[n][m]
