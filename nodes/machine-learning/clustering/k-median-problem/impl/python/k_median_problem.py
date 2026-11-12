# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-median-problem/. The authors are listed in prov/D8T8TZ.jsonl.

"""The k-median objective, an exact brute force solver, and the exact
dynamic program for points on a line."""

from fractions import Fraction
from itertools import combinations, product


def kmedian_cost(points, centers, dist, weights=None):
    """Sum over the points of (weight times) the distance to the nearest center."""
    if weights is None:
        weights = [1] * len(points)
    return sum(w * min(dist(p, c) for c in centers) for p, w in zip(points, weights))


def brute_force_discrete(points, k, dist, candidates=None):
    """Exact discrete k-median: try every set of k candidates.

    candidates defaults to the points themselves. Returns (cost, centers).
    Exponential time; use it only for tiny inputs.
    """
    cand = list(points) if candidates is None else list(candidates)
    k = min(k, len(cand))
    best = None
    for cs in combinations(cand, k):
        c = kmedian_cost(points, cs, dist)
        if best is None or c < best[0]:
            best = (c, list(cs))
    return best


def line_kmedian(xs, k):
    """Exact k-median of numbers on a line, by dynamic programming.

    The clusters of an optimal solution are runs of the sorted values, and
    a median of a run is an optimal center for it. F[c][j] is the least cost
    of the first j sorted values with c runs. Returns (cost, centers).
    Time O(k n^2) after sorting, with prefix sums for the run cost.
    """
    a = sorted(xs)
    n = len(a)
    if n == 0:
        return 0, []
    k = max(1, min(k, n))
    pre = [0] * (n + 1)
    for i, v in enumerate(a):
        pre[i + 1] = pre[i] + v

    def run(i, j):
        # cost of a[i..j-1] around its lower median a[m]
        m = (i + j - 1) // 2
        left = a[m] * (m - i) - (pre[m] - pre[i])
        right = (pre[j] - pre[m + 1]) - a[m] * (j - m - 1)
        return left + right

    F = [[None] * (n + 1) for _ in range(k + 1)]
    arg = [[0] * (n + 1) for _ in range(k + 1)]
    F[0][0] = 0
    for c in range(1, k + 1):
        for j in range(c, n + 1):
            best, bi = None, 0
            for i in range(c - 1, j):
                if F[c - 1][i] is None:
                    continue
                v = F[c - 1][i] + run(i, j)
                if best is None or v < best:
                    best, bi = v, i
            F[c][j], arg[c][j] = best, bi
    centers, j = [], n
    for c in range(k, 0, -1):
        i = arg[c][j]
        centers.append(a[(i + j - 1) // 2])
        j = i
    return F[k][n], sorted(centers)


def l1_cluster_cost(points):
    """Least L1 cost of one cluster in the plane: the center is the coordinate-wise median."""
    cost = Fraction(0)
    for axis in (0, 1):
        vals = sorted(p[axis] for p in points)
        med = Fraction(vals[(len(vals) - 1) // 2])
        cost += sum(abs(v - med) for v in vals)
    return cost


def l1_continuous_brute(points, k):
    """Exact continuous k-median in the plane under the L1 distance.

    Centers may be any points of the plane. For a fixed cluster the
    coordinate-wise median is an optimal center, so it is enough to try
    every labelling with at most k labels. Exponential time.
    """
    n = len(points)
    best = None
    for labels in product(range(min(k, n)), repeat=n):
        groups = [[points[i] for i in range(n) if labels[i] == g] for g in range(k)]
        c = sum(l1_cluster_cost(g) for g in groups if g)
        if best is None or c < best:
            best = c
    return best
