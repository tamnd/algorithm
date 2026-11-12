# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bisecting-k-means/. The authors are listed in prov/4FMVJH.jsonl.

"""Bisecting k-means (Steinbach, Karypis and Kumar, 2000).

Start with one cluster. Repeat until there are k clusters: choose a cluster by the
rule ("largest" = most points, "sse" = largest sum of squared errors), split it
with 2-means (Lloyd's algorithm with k = 2) from `trials` random starts, and keep
the split with the least SSE. Clusters are lists of point indices.
"""

import random
from typing import Sequence

Point = tuple


def sq_dist(x: Sequence, y: Sequence):
    return sum((a - b) * (a - b) for a, b in zip(x, y))


def centroid(cluster: Sequence[Point]) -> Point:
    n = len(cluster)
    return tuple(sum(p[t] for p in cluster) / n for t in range(len(cluster[0])))


def sse(points: Sequence[Point], idx: Sequence[int]):
    c = centroid([points[i] for i in idx])
    return sum(sq_dist(points[i], c) for i in idx)


def two_means(points: Sequence[Point], idx: Sequence[int], rng: random.Random):
    """Lloyd's algorithm with k = 2 on the points idx, from two distinct random points.

    Returns (left, right), two non-empty lists of indices, or None if all points of
    idx coincide. Ties keep the current side, so the loop ends.
    """
    distinct = sorted({points[i] for i in idx})
    if len(distinct) < 2:
        return None
    c = [tuple(p) for p in rng.sample(distinct, 2)]
    side = None
    while True:
        new = []
        for t, i in enumerate(idx):
            d0, d1 = sq_dist(points[i], c[0]), sq_dist(points[i], c[1])
            s = 0 if d0 < d1 else 1 if d1 < d0 else (side[t] if side else 0)
            new.append(s)
        if new == side:
            break
        side = new
        for s in (0, 1):
            members = [points[i] for i, a in zip(idx, side) if a == s]
            if members:
                c[s] = centroid(members)
    left = [i for i, a in zip(idx, side) if a == 0]
    right = [i for i, a in zip(idx, side) if a == 1]
    if not left or not right:
        return None
    return left, right


def bisecting_k_means(
    points: Sequence[Point],
    k: int,
    rng: random.Random,
    rule: str = "sse",
    trials: int = 5,
):
    """Return (clusters, log). log[s] = (index of the split cluster, its SSE, total SSE after)."""
    clusters = [list(range(len(points)))]  # @line L1
    log = []
    blocked = set()  # clusters (as tuples) whose 2-means split failed: all points coincide
    while len(clusters) < k:  # @line L2
        cand = [j for j, c in enumerate(clusters) if tuple(c) not in blocked]
        if not cand:
            break
        if rule == "largest":  # @line L3
            j = max(cand, key=lambda j: (len(clusters[j]), -j))
        else:
            j = max(cand, key=lambda j: (sse(points, clusters[j]), -j))
        best = None
        for _ in range(trials):  # @line L4
            split = two_means(points, clusters[j], rng)  # @line L5
            if split is None:
                break
            cost = sse(points, split[0]) + sse(points, split[1])
            if best is None or cost < best[0]:  # @line L6
                best = (cost, split)
        if best is None:
            blocked.add(tuple(clusters[j]))
            continue
        parent_sse = sse(points, clusters[j])
        clusters[j:j + 1] = [best[1][0], best[1][1]]  # @line L7
        log.append((j, parent_sse, sum(sse(points, c) for c in clusters)))
    return clusters, log  # @line L8
