# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pate/. The authors are listed in prov/7WDT5Q.jsonl.
"""Private aggregation of teacher ensembles (PATE) with the Laplace noisy max (LNMax).

The private data is split into k disjoint parts by position, and one teacher
is trained on each part. Each public query point gets the label that wins a
vote of the teachers after Laplace noise of scale 1/gamma is added to each
vote count. A student is trained on the public points and the noisy labels.

Under replace neighbors (one private example changed, at the same position),
one teacher changes, so each answer is 2 gamma-DP and Q answers are
2 gamma Q-DP by basic composition. The student is post-processing.

The teachers and the student are nearest-centroid classifiers, so that the
code needs no library. Floats and random.Random are used for the noise, so
this code shows the algorithm and is not a safe deployment.
"""

from __future__ import annotations

import math
import random
from typing import Optional, Sequence

Point = Sequence[float]
Example = tuple[Point, int]
Model = list[Optional[list[float]]]  # one centroid per class, or None for a class with no example


def split(data: Sequence[Example], k: int) -> list[list[Example]]:
    """The k disjoint parts: example i goes to part i mod k. Cost: O(n)."""
    parts: list[list[Example]] = [[] for _ in range(k)]
    for i, example in enumerate(data):
        parts[i % k].append(example)
    return parts


def train_centroids(examples: Sequence[Example], classes: int) -> Model:
    """The mean point of each class. Cost: O(n d)."""
    sums: list[Optional[list[float]]] = [None] * classes
    counts = [0] * classes
    for x, y in examples:
        if sums[y] is None:
            sums[y] = [0.0] * len(x)
        s = sums[y]
        for j, xj in enumerate(x):
            s[j] += xj
        counts[y] += 1
    return [None if s is None else [v / counts[c] for v in s] for c, s in enumerate(sums)]


def predict(model: Model, x: Point) -> int:
    """The class of the nearest centroid; ties go to the smaller class, and an empty model says 0. Cost: O(m d)."""
    best, best_d = 0, math.inf
    for c, centre in enumerate(model):
        if centre is None:
            continue
        dist = sum((a - b) ** 2 for a, b in zip(x, centre))
        if dist < best_d:
            best, best_d = c, dist
    return best


def vote_counts(teachers: Sequence[Model], x: Point, classes: int) -> list[int]:
    """The number of teachers that predict each class at x. Cost: O(k m d)."""
    counts = [0] * classes
    for t in teachers:
        counts[predict(t, x)] += 1
    return counts


def laplace(scale: float, rng: random.Random) -> float:
    """A Laplace(0, scale) draw, as the difference of two exponential draws."""
    return rng.expovariate(1 / scale) - rng.expovariate(1 / scale)


def noisy_max(counts: Sequence[int], gamma: float, rng: random.Random) -> int:
    """argmax_c (counts[c] + Lap(1/gamma)). Ties have probability 0. Cost: O(m)."""
    noisy = [n + laplace(1 / gamma, rng) for n in counts]
    return max(range(len(noisy)), key=lambda c: noisy[c])


def pate(private: Sequence[Example], public: Sequence[Point], k: int, classes: int,
         gamma: float, rng: random.Random) -> tuple[Model, list[int]]:
    """The student model and the noisy labels of the public points.

    Precondition: k >= 1, gamma > 0, labels in range(classes).
    Privacy: 2 gamma len(public)-DP under replace neighbors on the private data.
    Cost: O(n d) to train the teachers, O(k m d) per query, O(Q d) for the student.
    """
    if k < 1 or gamma <= 0:
        raise ValueError("need k >= 1 and gamma > 0")
    if any(not 0 <= y < classes for _, y in private):
        raise ValueError("labels must be in range(classes)")
    parts = split(private, k)  # @line L1
    teachers = [train_centroids(part, classes) for part in parts]  # @line L2
    labels: list[int] = []
    for x in public:  # @line L3
        counts = vote_counts(teachers, x, classes)  # @line L4
        labels.append(noisy_max(counts, gamma, rng))  # @line L5
    student = train_centroids(list(zip(public, labels)), classes)  # @line L6
    return student, labels  # @line L7


def basic_epsilon(gamma: float, queries: int) -> float:
    """The privacy of the labels by basic composition: 2 gamma per answer."""
    return 2 * gamma * queries


def _laplace_pdf(z: float, gamma: float) -> float:
    return gamma / 2 * math.exp(-gamma * abs(z))


def _laplace_cdf(z: float, gamma: float) -> float:
    return 0.5 * math.exp(gamma * z) if z < 0 else 1 - 0.5 * math.exp(-gamma * z)


def noisy_max_pmf(counts: Sequence[int], gamma: float, per_unit: int = 20) -> list[float]:
    """The probability that each class wins the noisy vote, by numerical integration.

    P(c wins) = integral of pdf(z - n_c) prod_{j != c} cdf(z - n_j) dz. The
    integrand is smooth between the counts, so composite Simpson is used on
    each piece between them, and on tails of width 30 / gamma, whose outer
    mass is below e^(-30). Each piece gets at least per_unit steps per length
    1 / gamma. Cost: O(m^2 (m + gamma max_count + 30) per_unit).
    """
    knots = sorted(set(counts))
    lo, hi = knots[0] - 30 / gamma, knots[-1] + 30 / gamma
    points = [lo] + knots + [hi]
    out = []
    for c, nc in enumerate(counts):
        def g(z: float) -> float:
            v = _laplace_pdf(z - nc, gamma)
            for j, nj in enumerate(counts):
                if j != c:
                    v *= _laplace_cdf(z - nj, gamma)
            return v

        total = 0.0
        for a, b in zip(points, points[1:]):
            if b <= a:
                continue
            pieces = 2 * max(10, math.ceil((b - a) * gamma * per_unit / 2))
            h = (b - a) / pieces
            s = g(a) + g(b)
            for i in range(1, pieces):
                s += (4 if i % 2 else 2) * g(a + i * h)
            total += s * h / 3
        out.append(total)
    return out
