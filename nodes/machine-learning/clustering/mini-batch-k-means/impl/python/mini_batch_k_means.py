# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mini-batch-k-means/. The authors are listed in prov/A9SG65.jsonl.

"""Mini-batch k-means (Sculley, 2010), Algorithm 1 of the paper.

Each iteration draws a batch of b points, caches the nearest center of each point of
the batch, and then moves each center toward each of its batch points with the per
center learning rate 1 / (number of points that the center has received so far).
The batch is drawn without replacement inside one iteration. The optional projection
step of the paper (for sparse centers) is not included.
"""

import random
from fractions import Fraction
from typing import Optional, Sequence

Point = tuple


def sq_dist(x: Sequence, y: Sequence):
    return sum((a - b) * (a - b) for a, b in zip(x, y))


def nearest(x: Sequence, centers: Sequence[Point]) -> int:
    return min(range(len(centers)), key=lambda j: sq_dist(x, centers[j]))


def cost(points: Sequence[Point], centers: Sequence[Point]):
    return sum(min(sq_dist(x, c) for c in centers) for x in points)


def mini_batch_k_means(
    points: Sequence[Point],
    k: int,
    b: int,
    t: int,
    rng: random.Random,
    init: Optional[Sequence[Point]] = None,
    log: Optional[list] = None,
):
    """Run t iterations with batches of size b. Returns (centers, counts).

    init gives the initial centers; by default k distinct data points are drawn.
    If log is a list, each update (center index, point) is appended to it.
    """
    n = len(points)
    if init is None:
        centers = [tuple(points[i]) for i in rng.sample(range(n), k)]  # @line L1
    else:
        centers = [tuple(c) for c in init]
    counts = [0] * k  # @line L2
    for _ in range(t):  # @line L3
        batch = [points[i] for i in rng.sample(range(n), min(b, n))]  # @line L4
        cached = [nearest(x, centers) for x in batch]  # @line L5
        for x, j in zip(batch, cached):  # @line L6
            counts[j] += 1  # @line L7
            eta = Fraction(1, counts[j])  # @line L8
            centers[j] = tuple((1 - eta) * c + eta * xi for c, xi in zip(centers[j], x))  # @line L9
            if log is not None:
                log.append((j, x))
    return centers, counts
