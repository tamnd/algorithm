# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hartigan-wong-algorithm/. The authors are listed in prov/RNKKMZ.jsonl.

"""Hartigan's single point move method for k-means.

This is the move rule of Hartigan and Wong (1979): a point x leaves its cluster i and
joins cluster j when n_j/(n_j+1) |x - c_j|^2 < n_i/(n_i-1) |x - c_i|^2. The code scans
the points in order and moves each point to the cluster with the least cost of adding
it. It does not keep the live sets and the quick transfer stage of the Fortran
routine AS 136; these only save time and do not change the set of stable partitions.
"""

from typing import Sequence

Point = tuple


def sq_dist(x: Sequence, y: Sequence):
    return sum((a - b) * (a - b) for a, b in zip(x, y))


def centroid(cluster: Sequence[Point]) -> Point:
    n = len(cluster)
    return tuple(sum(p[t] for p in cluster) / n for t in range(len(cluster[0])))


def partition_cost(points: Sequence[Point], labels: Sequence[int], k: int):
    """The k-means cost of a labeling, with each cluster at its mean."""
    total = 0
    for j in range(k):
        members = [x for x, a in zip(points, labels) if a == j]
        if members:
            c = centroid(members)
            total += sum(sq_dist(x, c) for x in members)
    return total


def hartigan(points: Sequence[Point], labels: Sequence[int], k: int):
    """Run Hartigan's method from the given labels (values in 0..k-1).

    Returns (labels, centers, moves). Each entry of moves is (i, p, q, delta): point i
    moved from cluster p to cluster q and the cost changed by delta < 0. An empty
    cluster has center None and size 0; its cost of adding a point is 0.
    """
    labels = list(labels)
    d = len(points[0])
    size = [0] * k  # @line L1
    sums = [[0] * d for _ in range(k)]
    for x, a in zip(points, labels):
        size[a] += 1
        for t in range(d):
            sums[a][t] += x[t]
    centers = [tuple(s / size[j] for s in sums[j]) if size[j] else None for j in range(k)]
    moves = []
    moved = True
    while moved:  # @line L2
        moved = False  # @line L3
        for i, x in enumerate(points):  # @line L4
            p = labels[i]  # @line L5
            if size[p] == 1:
                continue
            remove = size[p] * sq_dist(x, centers[p]) / (size[p] - 1)  # @line L6
            best_q, best_add = None, None
            for j in range(k):  # @line L7
                if j == p:
                    continue
                add = 0 if size[j] == 0 else size[j] * sq_dist(x, centers[j]) / (size[j] + 1)
                if best_add is None or add < best_add:
                    best_q, best_add = j, add
            if best_q is not None and best_add < remove:  # @line L8
                q = best_q
                size[p] -= 1  # @line L9
                for t in range(d):
                    sums[p][t] -= x[t]
                centers[p] = tuple(s / size[p] for s in sums[p])
                size[q] += 1  # @line L10
                for t in range(d):
                    sums[q][t] += x[t]
                centers[q] = tuple(s / size[q] for s in sums[q])
                labels[i] = q  # @line L11
                moves.append((i, p, q, best_add - remove))
                moved = True
    return labels, centers, moves  # @line L12


def nearest_labels(points: Sequence[Point], centers: Sequence[Point]) -> list[int]:
    """Labels of the nearest centers, the usual start of Hartigan's method."""
    return [min(range(len(centers)), key=lambda j: sq_dist(x, centers[j])) for x in points]
