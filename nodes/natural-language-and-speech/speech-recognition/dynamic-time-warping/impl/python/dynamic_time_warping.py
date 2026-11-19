# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-time-warping/. The authors are listed in prov/JJFMC2.jsonl.

"""Dynamic time warping (DTW) of two sequences.

x = x_1 ... x_n and y = y_1 ... y_m are sequences of numbers or of vectors, and
d(a, b) >= 0 is a local distance. A warping path is a list of cells (i, j),
1-based, from (1, 1) to (n, m), where each step is (1, 0), (0, 1) or (1, 1).

A step pattern gives the weight of each step as a multiple of d at the cell the
step enters. The three patterns here are

    name         diagonal (i-1, j-1)   vertical (i-1, j)   horizontal (i, j-1)   divide by
    symmetric1   1                     1                   1                     1
    symmetric2   2                     1                   1                     n + m
    asymmetric   1                     1                   0                     n

symmetric2 weights each step by its delta i + delta j, and asymmetric by its
delta i, as in Sakoe and Chiba 1978. The first cell (1, 1) is entered by a
diagonal step from the sentinel cell (0, 0), with D[0][0] = 0 and D[i][0] =
D[0][j] = infinity, so the same recurrence covers all three patterns. Then the
sum of the step weights is n + m for symmetric2 and n for asymmetric on every
path, which is why those totals are the normalizers.

Tie rule of the traceback: the diagonal step first, then the vertical step,
then the horizontal step.
"""

import math
from typing import Callable, List, Sequence, Tuple

INF = math.inf

STEP_PATTERNS = {
    "symmetric1": (1, 1, 1),
    "symmetric2": (2, 1, 1),
    "asymmetric": (1, 1, 0),
}


def abs_dist(a, b) -> float:
    """|a - b| for numbers."""
    return abs(a - b)


def sq_euclidean(a, b) -> float:
    """Squared Euclidean distance of two vectors of the same length."""
    return math.fsum((u - v) ** 2 for u, v in zip(a, b))


def dtw(x: Sequence, y: Sequence, dist: Callable = abs_dist, step: str = "symmetric1"):
    """Return (D, path): the cost D[n][m] of a best warping path, and that path.

    The cost is not normalized; see dtw_distance. Cost: O(n m) calls of dist,
    O(n m) time and O(n m) memory for the table and the back pointers.
    """
    n, m = len(x), len(y)
    if n == 0 or m == 0:
        raise ValueError("both sequences must be non-empty")
    wd, wv, wh = STEP_PATTERNS[step]
    D = [[INF] * (m + 1) for _ in range(n + 1)]
    back = [[(0, 0)] * (m + 1) for _ in range(n + 1)]
    D[0][0] = 0.0  # @line L1
    for i in range(1, n + 1):  # @line L2
        for j in range(1, m + 1):  # @line L3
            c = dist(x[i - 1], y[j - 1])  # @line L4
            best, arg = D[i - 1][j - 1] + wd * c, (i - 1, j - 1)  # @line L5
            v = D[i - 1][j] + wv * c
            if v < best:
                best, arg = v, (i - 1, j)
            h = D[i][j - 1] + wh * c
            if h < best:
                best, arg = h, (i, j - 1)
            D[i][j], back[i][j] = best, arg  # @line L6
    path = [(n, m)]  # @line L7
    while path[-1] != (1, 1):  # @line L8
        i, j = path[-1]
        path.append(back[i][j])
    path.reverse()
    return D[n][m], path  # @line L9


def normalizer(n: int, m: int, step: str) -> int:
    """The sum of the step weights of every path: 1, n + m or n."""
    return {"symmetric1": 1, "symmetric2": n + m, "asymmetric": n}[step]


def dtw_distance(x: Sequence, y: Sequence, dist: Callable = abs_dist, step: str = "symmetric1") -> float:
    """Return D[n][m] divided by the normalizer of the step pattern."""
    cost, _ = dtw(x, y, dist, step)
    return cost / normalizer(len(x), len(y), step)


def path_cost(x: Sequence, y: Sequence, path: Sequence[Tuple[int, int]], dist: Callable = abs_dist, step: str = "symmetric1"):
    """Return the weighted cost of a warping path under a step pattern."""
    wd, wv, wh = STEP_PATTERNS[step]
    total = 0.0
    prev = (0, 0)
    for i, j in path:
        di, dj = i - prev[0], j - prev[1]
        w = wd if (di, dj) == (1, 1) else wv if (di, dj) == (1, 0) else wh
        total += w * dist(x[i - 1], y[j - 1])
        prev = (i, j)
    return total


def is_warping_path(path: Sequence[Tuple[int, int]], n: int, m: int) -> bool:
    """True if the path goes from (1, 1) to (n, m) with steps (1, 0), (0, 1) or (1, 1)."""
    if not path or path[0] != (1, 1) or path[-1] != (n, m):
        return False
    return all((b[0] - a[0], b[1] - a[1]) in ((1, 0), (0, 1), (1, 1)) for a, b in zip(path, path[1:]))
