# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/euclidean-k-median/. The authors are listed in prov/3ZK1AD.jsonl.

"""Exact solvers for small cases of Euclidean k-median: brute force over candidate centres, and the dynamic program
for points on a line. Weiszfeld's iteration gives an approximate 1-median in the plane."""

from itertools import accumulate, combinations
from math import dist
from typing import Optional, Sequence

Point = tuple[float, ...]


def cost(points: Sequence[Point], centres: Sequence[Point]) -> float:
    """The sum over the points of the distance to the nearest centre."""
    return sum(min(dist(p, c) for c in centres) for p in points)


def discrete_k_median(points: Sequence[Point], k: int,
                      candidates: Optional[Sequence[Point]] = None) -> tuple[float, tuple[Point, ...]]:
    """The best k centres among the candidates (the input points by default), by trying all sets."""
    cand = list(points if candidates is None else candidates)
    best = (float("inf"), ())
    for centres in combinations(cand, min(k, len(cand))):
        best = min(best, (cost(points, centres), centres))
    return best


def line_k_median(xs: Sequence[float], k: int) -> tuple[float, list[float]]:
    """Exact k-median of points on a line in O(k n^2) time.

    In an optimal solution the clusters are runs of the sorted points, and the best centre of a run is its median."""
    x = sorted(xs)
    n = len(x)
    pre = [0.0] + list(accumulate(x))

    def run_cost(i: int, j: int) -> float:  # the points x[i..j-1] served by their median x[(i + j - 1) // 2]
        m = (i + j - 1) // 2
        return (x[m] * (m - i) - (pre[m] - pre[i])) + ((pre[j] - pre[m + 1]) - x[m] * (j - m - 1))

    inf = float("inf")
    k = min(k, n)
    best = [[inf] * (n + 1) for _ in range(k + 1)]
    cut = [[0] * (n + 1) for _ in range(k + 1)]
    best[0][0] = 0.0
    for c in range(1, k + 1):
        for j in range(1, n + 1):
            for i in range(c - 1, j):
                v = best[c - 1][i] + run_cost(i, j)
                if v < best[c][j]:
                    best[c][j], cut[c][j] = v, i
    centres, j = [], n
    for c in range(k, 0, -1):
        i = cut[c][j]
        centres.append(x[(i + j - 1) // 2])
        j = i
    return best[k][n], centres[::-1]


def weiszfeld(points: Sequence[Point], rounds: int = 200) -> Point:
    """An approximate geometric median (the 1-median) by Weiszfeld's iteration from the centroid."""
    d = len(points[0])
    y = tuple(sum(p[t] for p in points) / len(points) for t in range(d))
    for _ in range(rounds):
        num, den = [0.0] * d, 0.0
        for p in points:
            r = dist(p, y)
            if r < 1e-12:
                return y
            for t in range(d):
                num[t] += p[t] / r
            den += 1 / r
        y = tuple(v / den for v in num)
    return y
