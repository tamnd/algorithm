# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/x-means/. The authors are listed in prov/X2J8SA.jsonl.

"""X-means (Pelleg and Moore, 2000): k-means that chooses k by the Bayesian
information criterion (BIC).

The model of a clustering is a mixture of spherical Gaussians with a common variance
sigma^2 = SSE / (d (R - K)), mixing weights R_j / R and hard assignments. Its log
likelihood is
    l = sum_j R_j log(R_j / R) - (R d / 2) log(2 pi sigma^2) - SSE / (2 sigma^2)
and its number of free parameters is p = (K - 1) + K d + 1. BIC = l - (p / 2) log R.
Implementations differ in these details; this one is internally consistent.

Points are tuples of floats.
"""

import math
import random
from typing import Sequence

Point = tuple


def sq_dist(x: Sequence, y: Sequence) -> float:
    return sum((a - b) * (a - b) for a, b in zip(x, y))


def mean(ps: Sequence[Point]) -> Point:
    return tuple(sum(p[t] for p in ps) / len(ps) for t in range(len(ps[0])))


def lloyd(points: Sequence[Point], centers: Sequence[Point], max_iter: int = 300):
    """Lloyd's algorithm with the keep-current tie rule. Returns (centers, labels)."""
    centers = [tuple(c) for c in centers]
    k = len(centers)
    labels = None
    for _ in range(max_iter):
        new = []
        for i, x in enumerate(points):
            d = [sq_dist(x, c) for c in centers]
            j = min(range(k), key=d.__getitem__)
            if labels is not None and d[labels[i]] == d[j]:
                j = labels[i]
            new.append(j)
        if new == labels:
            break
        labels = new
        for j in range(k):
            m = [x for x, a in zip(points, labels) if a == j]
            if m:
                centers[j] = mean(m)
    return centers, labels


def bic(points: Sequence[Point], centers: Sequence[Point], labels: Sequence[int]) -> float:
    """The BIC of a hard clustering under the spherical Gaussian model above."""
    R, d, K = len(points), len(points[0]), len(centers)
    sse = sum(sq_dist(x, centers[a]) for x, a in zip(points, labels))
    if R <= K:
        return -math.inf
    var = sse / (d * (R - K))
    if var == 0:
        return math.inf
    sizes = [0] * K
    for a in labels:
        sizes[a] += 1
    loglik = sum(r * math.log(r / R) for r in sizes if r)
    loglik -= R * d / 2 * math.log(2 * math.pi * var) + sse / (2 * var)
    p = (K - 1) + K * d + 1
    return loglik - p / 2 * math.log(R)


def split_children(members: Sequence[Point], c: Point, rng: random.Random):
    """Two children at c +- r u, u a random unit vector, r the RMS radius of the cluster."""
    d = len(c)
    u = [rng.gauss(0, 1) for _ in range(d)]
    norm = math.sqrt(sum(v * v for v in u)) or 1.0
    r = math.sqrt(sum(sq_dist(x, c) for x in members) / len(members))
    return [tuple(ci + r * v / norm for ci, v in zip(c, u)), tuple(ci - r * v / norm for ci, v in zip(c, u))]


def x_means(points: Sequence[Point], k_min: int, k_max: int, rng: random.Random):
    """Return (centers, labels, score) of the clustering with the best BIC seen."""
    centers = [points[i] for i in rng.sample(range(len(points)), k_min)]
    best = None
    while True:
        centers, labels = lloyd(points, centers)  # @line L1
        score = bic(points, centers, labels)  # @line L2
        if best is None or score > best[2]:
            best = (centers, labels, score)
        if len(centers) >= k_max:  # @line L3
            break
        gains = []  # (BIC gain, j, children)
        for j, c in enumerate(centers):  # @line L4
            members = [x for x, a in zip(points, labels) if a == j]
            if len(members) < 3 or len(set(members)) < 2:
                continue
            kids, kid_labels = lloyd(members, split_children(members, c, rng))  # @line L5
            if len(set(kid_labels)) < 2:
                continue
            parent = bic(members, [c], [0] * len(members))  # @line L6
            child = bic(members, kids, kid_labels)
            if child > parent:  # @line L7
                gains.append((child - parent, j, kids))
        if not gains:  # @line L8
            break
        gains.sort(key=lambda g: -g[0])
        gains = gains[: k_max - len(centers)]  # respect k_max
        split = {j: kids for _, j, kids in gains}
        new = []
        for j, c in enumerate(centers):  # @line L9
            new.extend(split.get(j, [c]))
        centers = new
    return best
