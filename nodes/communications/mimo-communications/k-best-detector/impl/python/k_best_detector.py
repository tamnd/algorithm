# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-best-detector/. The authors are listed in prov/3ZQXDE.jsonl.

"""The K-best detector: a breadth-first tree search with K survivors per level.

The model is y = H x + w with H an m by n complex matrix of full column rank
(m >= n) and x a vector of n points of a constellation S of size M. With the
upper triangular R and the vector yb of triangularize(), the ML metric is
||y - H x||^2 = ||yb - R x||^2 + c, with c independent of x. The last row of
R involves only x_(n-1), the row before it x_(n-2) and x_(n-1), and so on, so
the metric is a sum of nonnegative terms, one per tree level, and a partial
vector (x_i, ..., x_(n-1)) has a partial metric that can only grow. The search
goes from level n - 1 down to level 0, extends each survivor by all M points,
and keeps the K extensions with the smallest partial metrics.
"""

import cbb


def triangularize(y: list[complex], h: list[list[complex]]) -> tuple[list[list[complex]], list[complex], float]:
    """(R, yb, c) with R upper triangular, R^H R = H^H H, and ||y - H x||^2 = ||yb - R x||^2 + c."""
    if len(h) < len(h[0]):
        raise ValueError("the K-best detector here needs m >= n")
    hh = cbb.herm(h)
    try:
        low = cbb.cholesky(cbb.matmul(hh, h))
    except ValueError:
        raise ValueError("H must have full column rank") from None
    b = cbb.matvec(hh, y)
    n = len(b)
    yb = [0j] * n
    for i in range(n):  # forward substitution: L yb = H^H y
        yb[i] = (b[i] - sum(low[i][c] * yb[c] for c in range(i))) / low[i][i]
    r = cbb.herm(low)
    return r, yb, cbb.norm2(y) - cbb.norm2(yb)


def k_best(
    y: list[complex], h: list[list[complex]], points: list[complex], k: int
) -> list[tuple[float, list[int]]]:
    """The K survivors at the bottom of the tree, as (metric, indices), best first.

    The metric is the full ||y - H x||^2. Ties keep the earlier candidate,
    with the candidates of each level ordered by survivor and then by point index.
    """
    if k < 1:
        raise ValueError("K must be at least 1")
    r, yb, c = triangularize(y, h)  # @line L1
    n = len(yb)
    survivors = [(0.0, [])]  # @line L2  (partial metric, indices of x_i, ..., x_(n-1))
    for i in range(n - 1, -1, -1):  # @line L3
        cand = []
        for metric, tail in survivors:  # @line L4
            xs = [points[j] for j in tail]
            u = yb[i] - sum(r[i][i + 1 + t] * xs[t] for t in range(len(xs)))
            for j, p in enumerate(points):  # @line L5
                cand.append((metric + abs(u - r[i][i] * p) ** 2, [j] + tail))
        cand.sort(key=lambda e: e[0])  # stable: ties keep the generation order
        survivors = cand[:k]  # @line L6
    return [(metric + c, idx) for metric, idx in survivors]  # @line L7


def k_best_detect(y: list[complex], h: list[list[complex]], points: list[complex], k: int) -> list[int]:
    """The point indices of the best survivor of the K-best search."""
    return k_best(y, h, points, k)[0][1]
