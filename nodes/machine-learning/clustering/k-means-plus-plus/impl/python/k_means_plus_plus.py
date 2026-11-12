# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-means-plus-plus/. The authors are listed in prov/V3K4X6.jsonl.

"""k-means++ (D^2 seeding) followed by Lloyd's algorithm.

Points are tuples of numbers. The random generator is a parameter, so a run is
reproducible. seeding_distribution gives the exact probability of each next center
with fractions.Fraction, for tests and for small examples.
"""

import random
from fractions import Fraction
from typing import Sequence

Point = tuple


def sq_dist(x: Sequence, y: Sequence):
    return sum((a - b) * (a - b) for a, b in zip(x, y))


def centroid(cluster: Sequence[Point]) -> Point:
    n = len(cluster)
    return tuple(sum(p[t] for p in cluster) / n for t in range(len(cluster[0])))


def cost(points: Sequence[Point], centers: Sequence[Point]):
    """The k-means cost: the sum of squared distances to the nearest center."""
    return sum(min(sq_dist(x, c) for c in centers) for x in points)


def seeding_distribution(points: Sequence[Point], chosen: Sequence[int]) -> list[Fraction]:
    """The exact probability that each point is the next center, given the chosen indices.

    With no chosen center the distribution is uniform. Otherwise it is D(x)^2 / sum D^2,
    where D(x) is the distance to the nearest chosen center. If all D(x) are 0 the
    distribution is uniform over the points that are not chosen.
    """
    n = len(points)
    if not chosen:
        return [Fraction(1, n)] * n
    d2 = [Fraction(min(sq_dist(x, points[j]) for j in chosen)) for x in points]
    total = sum(d2)
    if total == 0:
        rest = [i for i in range(n) if i not in chosen]
        return [Fraction(1, len(rest)) if i in rest else Fraction(0) for i in range(n)]
    return [w / total for w in d2]


def seed(points: Sequence[Point], k: int, rng: random.Random) -> list[int]:
    """D^2 seeding. Returns the indices of the k chosen centers, in the order of choice."""
    n = len(points)
    if not 1 <= k <= n:
        raise ValueError("need 1 <= k <= n")
    first = rng.randrange(n)  # @line L1
    chosen = [first]
    d2 = [sq_dist(x, points[first]) for x in points]  # @line L2
    while len(chosen) < k:  # @line L3
        total = sum(d2)  # @line L4
        if total == 0:
            # all points coincide with chosen centers: take any point not chosen
            rest = [i for i in range(n) if i not in chosen]
            nxt = rest[rng.randrange(len(rest))]
        else:
            r = rng.random() * total  # @line L5
            acc = 0
            nxt = n - 1
            for i, w in enumerate(d2):
                acc += w
                if r < acc and w > 0:
                    nxt = i
                    break
            else:
                nxt = max(i for i in range(n) if d2[i] > 0)
        chosen.append(nxt)  # @line L6
        for i, x in enumerate(points):  # @line L7
            dx = sq_dist(x, points[nxt])
            if dx < d2[i]:
                d2[i] = dx  # @line L8
    return chosen


def lloyd(points: Sequence[Point], centers: Sequence[Point]):
    """Lloyd's algorithm with the keep-current tie rule. Returns (centers, labels)."""
    centers = [tuple(c) for c in centers]
    k = len(centers)
    labels = None
    while True:
        new = []
        for i, x in enumerate(points):
            dists = [sq_dist(x, c) for c in centers]
            j = min(range(k), key=dists.__getitem__)
            if labels is not None and dists[labels[i]] == dists[j]:
                j = labels[i]
            new.append(j)
        if new == labels:
            return centers, labels
        labels = new
        for j in range(k):
            members = [x for x, a in zip(points, labels) if a == j]
            if members:
                centers[j] = centroid(members)


def k_means_plus_plus(points: Sequence[Point], k: int, rng: random.Random):
    """Seed with D^2 sampling, then run Lloyd's algorithm. Returns (centers, labels)."""
    idx = seed(points, k, rng)
    return lloyd(points, [points[i] for i in idx])  # @line L9
