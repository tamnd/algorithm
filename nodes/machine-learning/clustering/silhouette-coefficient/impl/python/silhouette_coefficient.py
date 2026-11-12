# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/silhouette-coefficient/. The authors are listed in prov/9J34RM.jsonl.
"""Silhouettes of Rousseeuw (1987) for any dissimilarity."""

from math import dist
from typing import Callable, Hashable, Sequence, TypeVar

P = TypeVar("P")


def silhouette_samples(points: Sequence[P], labels: Sequence[Hashable],
                       d: Callable[[P, P], float] = dist) -> list:
    """Return s(i) for each point.

    a(i): the mean dissimilarity from i to the other members of its own cluster.
    b(i): the least, over the other clusters C, of the mean dissimilarity from i to C.
    s(i) = (b(i) - a(i)) / max(a(i), b(i)), and s(i) = 0 when i is alone in its cluster.
    The input needs at least 2 clusters. Each point needs one pass over all points,
    so the cost is n(n - 1)/2 dissimilarities if d is symmetric and cached, n^2 here.
    The arithmetic follows the type of d: exact with Fractions, floats otherwise.
    """
    n = len(points)
    if n != len(labels):
        raise ValueError("points and labels must have the same length")
    size: dict = {}
    for c in labels:
        size[c] = size.get(c, 0) + 1
    if len(size) < 2:
        raise ValueError("the silhouette needs at least 2 clusters")
    out = []
    for i in range(n):
        sums: dict = {c: 0 for c in size}
        for j in range(n):
            if j != i:
                sums[labels[j]] += d(points[i], points[j])
        own = labels[i]
        if size[own] == 1:
            out.append(0)
            continue
        a = sums[own] / (size[own] - 1)
        b = min(sums[c] / size[c] for c in size if c != own)
        m = max(a, b)
        out.append(0 if m == 0 else (b - a) / m)
    return out


def mean_silhouette(points, labels, d=dist):
    """The mean of s(i) over all n points (the "silhouette score")."""
    s = silhouette_samples(points, labels, d)
    return sum(s) / len(s)


def cluster_silhouettes(points, labels, d=dist) -> dict:
    """The mean of s(i) over each cluster (the average silhouette width of a cluster)."""
    s = silhouette_samples(points, labels, d)
    acc: dict = {}
    for c, v in zip(labels, s):
        t = acc.setdefault(c, [0, 0])
        t[0] += v
        t[1] += 1
    return {c: t[0] / t[1] for c, t in acc.items()}
