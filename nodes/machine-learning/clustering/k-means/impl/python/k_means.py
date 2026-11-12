# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-means/. The authors are listed in prov/MRP5YA.jsonl.

"""Lloyd's algorithm for the k-means problem.

Points and centers are tuples of numbers. With fractions.Fraction coordinates all the
arithmetic is exact. The function does not choose the initial centers: pass them in
(for example k distinct data points chosen at random, or the k-means++ seeding).
"""

import random
from typing import Optional, Sequence

Point = tuple


def sq_dist(x: Sequence, y: Sequence):
    return sum((a - b) * (a - b) for a, b in zip(x, y))


def centroid(cluster: Sequence[Point]) -> Point:
    n = len(cluster)
    return tuple(sum(p[t] for p in cluster) / n for t in range(len(cluster[0])))


def assignment_cost(points: Sequence[Point], centers: Sequence[Point], labels: Sequence[int]):
    """The cost of a labeling with the given centers (not necessarily the nearest ones)."""
    return sum(sq_dist(x, centers[j]) for x, j in zip(points, labels))


def lloyd(
    points: Sequence[Point],
    centers: Sequence[Point],
    max_iter: Optional[int] = None,
):
    """Run Lloyd's algorithm from the given initial centers.

    Returns (centers, labels, history), where history[t] is the cost after the update
    step of iteration t + 1. A point keeps its current center when that center is one of
    its nearest centers; this tie rule makes the cost fall strictly in each iteration
    that changes a label, so the loop always ends. An empty cluster keeps its center.
    """
    centers = [tuple(c) for c in centers]
    k = len(centers)
    labels: Optional[list[int]] = None  # @line L1
    history = []
    while max_iter is None or len(history) < max_iter:  # @line L2
        changed = False  # @line L3
        new = []
        for i, x in enumerate(points):  # @line L4
            dists = [sq_dist(x, c) for c in centers]
            j = min(range(k), key=dists.__getitem__)  # @line L5
            if labels is not None and dists[labels[i]] == dists[j]:
                j = labels[i]
            if labels is None or j != labels[i]:  # @line L6
                changed = True
            new.append(j)
        if not changed:  # @line L7
            break
        labels = new
        for j in range(k):  # @line L8
            members = [x for x, a in zip(points, labels) if a == j]  # @line L9
            if members:
                centers[j] = centroid(members)  # @line L10
        history.append(assignment_cost(points, centers, labels))
    return centers, labels, history


def random_init(points: Sequence[Point], k: int, rng: random.Random) -> list[Point]:
    """Forgy initialization: k distinct data points chosen uniformly at random."""
    return [points[i] for i in rng.sample(range(len(points)), k)]
