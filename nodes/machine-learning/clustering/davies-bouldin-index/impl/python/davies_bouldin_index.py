# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/davies-bouldin-index/. The authors are listed in prov/7PAEH8.jsonl.
"""The Davies-Bouldin index (1979) for points in R^d.

S_i = ( (1/n_i) sum_{x in C_i} ||x - c_i||_2^q )^(1/q)    the scatter of cluster i
M_ij = ||c_i - c_j||_p                                    the separation of clusters i and j
R_ij = (S_i + S_j) / M_ij
DB = (1/k) sum_i max_{j != i} R_ij                        lower is better
The defaults q = 1 and p = 2 give the common form: the mean Euclidean distance
to the centroid, and the Euclidean distance between centroids.
"""

from math import dist, inf
from typing import Hashable, Sequence


def _centroid(rows: list) -> list:
    m = len(rows)
    return [sum(r[t] for r in rows) / m for t in range(len(rows[0]))]


def _minkowski(u: Sequence[float], v: Sequence[float], p: float) -> float:
    if p == 2:
        return dist(u, v)
    return sum(abs(a - b) ** p for a, b in zip(u, v)) ** (1 / p)


def scatters_and_centroids(points, labels, q: float = 1):
    groups: dict = {}
    for x, c in zip(points, labels):
        groups.setdefault(c, []).append(list(x))
    keys = list(groups)
    cents = [_centroid(groups[c]) for c in keys]
    scat = []
    for c, m in zip(keys, cents):
        rows = groups[c]
        scat.append((sum(dist(x, m) ** q for x in rows) / len(rows)) ** (1 / q))
    return keys, scat, cents


def davies_bouldin(points: Sequence[Sequence[float]], labels: Sequence[Hashable],
                   q: float = 1, p: float = 2) -> float:
    """Return DB. Needs k >= 2. Two equal centroids give R_ij = inf, so DB = inf.

    Cost: O(n d) for the centroids and scatters, then O(k^2 d) for the pairs.
    """
    keys, scat, cents = scatters_and_centroids(points, labels, q)
    k = len(keys)
    if k < 2:
        raise ValueError("DB needs at least 2 clusters")
    total = 0.0
    for i in range(k):
        worst = 0.0
        for j in range(k):
            if j == i:
                continue
            m = _minkowski(cents[i], cents[j], p)
            r = inf if m == 0 else (scat[i] + scat[j]) / m
            worst = max(worst, r)
        total += worst
    return total / k
