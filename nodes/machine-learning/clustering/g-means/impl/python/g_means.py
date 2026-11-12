# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/g-means/. The authors are listed in prov/3WDD1J.jsonl.

"""G-means (Hamerly and Elkan, 2003): k-means that grows k until the points of each
cluster look Gaussian along the direction of a trial split.

For each cluster: put two children at c +- m with m = s sqrt(2 lambda / pi), where s is
the main principal direction and lambda its eigenvalue; run 2-means on the points of
the cluster; project the points on v = c1 - c2; standardize; and apply the
Anderson-Darling test with Stephens' correction A*^2 = A^2 (1 + 4/n - 25/n^2). If
A*^2 exceeds the critical value, replace the center by the two children. The default
critical value 1.8692 is the one of the paper, for alpha = 0.0001.

Points are tuples of floats.
"""

import math
import random
from typing import Sequence

Point = tuple
CRITICAL_0001 = 1.8692


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


def normal_cdf(z: float) -> float:
    return 0.5 * math.erfc(-z / math.sqrt(2.0))


def anderson_darling(values: Sequence[float]) -> float:
    """A*^2 for normality with estimated mean and variance (Stephens' correction)."""
    n = len(values)
    mu = sum(values) / n
    var = sum((v - mu) ** 2 for v in values) / (n - 1)
    sd = math.sqrt(var)
    eps = 1e-300
    z = sorted(normal_cdf((v - mu) / sd) for v in values)
    s = 0.0
    for i in range(1, n + 1):
        s += (2 * i - 1) * (math.log(max(z[i - 1], eps)) + math.log(max(1.0 - z[n - i], eps)))
    a2 = -n - s / n
    return a2 * (1 + 4 / n - 25 / (n * n))


def principal_direction(points: Sequence[Point], rng: random.Random, iters: int = 100):
    """Main eigenvector and eigenvalue of the sample covariance, by power iteration."""
    d = len(points[0])
    c = mean(points)
    n = len(points)
    cov = [[sum((p[a] - c[a]) * (p[b] - c[b]) for p in points) / n for b in range(d)] for a in range(d)]
    v = [rng.gauss(0, 1) for _ in range(d)]
    lam = 0.0
    for _ in range(iters):
        w = [sum(cov[a][b] * v[b] for b in range(d)) for a in range(d)]
        norm = math.sqrt(sum(x * x for x in w))
        if norm == 0:
            return [0.0] * d, 0.0
        v = [x / norm for x in w]
        lam = norm
    return v, lam


def check_cluster(members: Sequence[Point], c: Point, rng: random.Random, critical: float):
    """Return (split?, children). split is True when the projection is not Gaussian."""
    s, lam = principal_direction(members, rng)  # @line L4
    m = [x * math.sqrt(2 * lam / math.pi) for x in s]
    kids, labels = lloyd(members, [tuple(a + b for a, b in zip(c, m)), tuple(a - b for a, b in zip(c, m))])  # @line L5
    v = [a - b for a, b in zip(kids[0], kids[1])]
    vv = sum(x * x for x in v)
    if vv == 0:
        return False, kids
    proj = [sum(a * b for a, b in zip(x, v)) / vv for x in members]  # @line L6
    if max(proj) - min(proj) == 0:
        return False, kids
    return anderson_darling(proj) > critical, kids  # @line L7


def g_means(points: Sequence[Point], rng: random.Random, critical: float = CRITICAL_0001, k_max: int = 100, min_size: int = 8):
    """Return (centers, labels). Starts from one center, the mean of all points."""
    centers = [mean(points)]  # @line L1
    while True:
        centers, labels = lloyd(points, centers)  # @line L2
        new, split_any = [], False
        for j, c in enumerate(centers):  # @line L3
            members = [x for x, a in zip(points, labels) if a == j]
            if len(members) < min_size or len(new) + (len(centers) - j) >= k_max:
                new.append(c)
                continue
            split, kids = check_cluster(members, c, rng, critical)
            if split:  # @line L8
                new.extend(kids)
                split_any = True
            else:
                new.append(c)
        if not split_any:  # @line L9
            return centers, labels
        centers = new
