# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/statistical-outlier-removal/. The authors are listed in prov/RBGT7A.jsonl.
"""Statistical outlier removal for a 3D point cloud.

For each point, take the mean distance to its k nearest neighbors (the point
itself excluded). Over the whole cloud, take the mean mu and the sample
standard deviation sigma of these mean distances. Keep the points whose mean
distance is at most mu + alpha sigma.

The neighbor search here is a brute force scan, O(n^2 log k) in total, which
is enough for the small clouds of the tests. A k-d tree gives the same
neighbor distances faster in low dimension.
"""

from __future__ import annotations

import heapq
import math
from typing import List, Sequence, Tuple


def knn_distances(points: Sequence[Sequence[float]], i: int, k: int) -> List[float]:
    """The k smallest distances from point i to the other points, ascending.

    The multiset of the k smallest distances does not depend on how ties
    between equal distances are broken."""
    p = points[i]
    return heapq.nsmallest(k, (math.dist(p, q) for j, q in enumerate(points) if j != i))


def mean_knn_distances(points: Sequence[Sequence[float]], k: int) -> List[float]:
    """d_i, the mean distance of each point to its k nearest neighbors."""
    n = len(points)
    if not 1 <= k <= n - 1:
        raise ValueError("need 1 <= k <= n - 1")
    d: List[float] = []
    for i in range(n):  # @line L1
        nbr = knn_distances(points, i, k)  # @line L2
        d.append(sum(nbr) / k)  # @line L3
    return d


def statistical_outlier_removal(points: Sequence[Sequence[float]], k: int,
                                alpha: float) -> Tuple[List[int], float]:
    """Return (the indices of the kept points in input order, the threshold).

    Preconditions: n >= 2 points and 1 <= k <= n - 1."""
    n = len(points)
    if n < 2:
        raise ValueError("need at least 2 points")
    d = mean_knn_distances(points, k)
    mu = sum(d) / n  # @line L4
    sigma = math.sqrt(sum((x - mu) ** 2 for x in d) / (n - 1))  # @line L5
    threshold = mu + alpha * sigma  # @line L6
    kept = [i for i in range(n) if d[i] <= threshold]  # @line L7
    return kept, threshold
