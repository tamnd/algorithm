# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dunn-index/. The authors are listed in prov/PBD47N.jsonl.
"""The Dunn index (1974) for any dissimilarity.

delta(C_i, C_j) = min over x in C_i, y in C_j of d(x, y)    the gap between two clusters
diam(C) = max over x, y in C of d(x, y)                     the diameter of a cluster
D = min_{i != j} delta(C_i, C_j) / max_l diam(C_l)          higher is better
"""

from math import dist, inf
from typing import Callable, Hashable, Sequence, TypeVar

P = TypeVar("P")


def gap_and_diameter(points: Sequence[P], labels: Sequence[Hashable],
                     d: Callable[[P, P], float] = dist):
    """One pass over the n(n - 1)/2 pairs: the least gap between clusters, the largest diameter."""
    n = len(points)
    gap = inf
    diam = 0
    for i in range(n):
        for j in range(i + 1, n):
            x = d(points[i], points[j])
            if labels[i] == labels[j]:
                diam = max(diam, x)
            else:
                gap = min(gap, x)
    return gap, diam


def dunn(points, labels, d=dist):
    """Return D. Needs k >= 2. When each cluster has diameter 0, D = inf."""
    if len(set(labels)) < 2:
        raise ValueError("the Dunn index needs at least 2 clusters")
    gap, diam = gap_and_diameter(points, labels, d)
    return inf if diam == 0 else gap / diam
