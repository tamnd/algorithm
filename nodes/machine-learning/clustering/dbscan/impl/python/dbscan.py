# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dbscan/. The authors are listed in prov/MFMXQM.jsonl.

"""DBSCAN (Ester, Kriegel, Sander and Xu 1996) with brute force range queries.

The eps-neighborhood of a point holds the point itself, so a point is a core
point when at least min_pts points (itself included) lie within distance eps.
Labels: -1 is noise, and the clusters are numbered 0, 1, 2, ... in the order
in which the scan of the input finds their first core point.
"""

import math
from collections import deque

NOISE = -1
UNDEFINED = -2


def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def range_query(points, i, eps, dist=euclidean):
    """All indices j with dist(points[i], points[j]) <= eps, i itself included."""
    p = points[i]
    return [j for j, q in enumerate(points) if dist(p, q) <= eps]


def dbscan(points, eps, min_pts, dist=euclidean):
    """Return (labels, is_core) for the input points.

    Each point gets at most one range query and enters the queue at most once.
    """
    n = len(points)
    label = [UNDEFINED] * n  # @line L1
    is_core = [False] * n
    cluster = -1

    def claim(j, queue):
        if label[j] == NOISE:  # @line L14
            label[j] = cluster  # a border point: it was noise until now
        elif label[j] == UNDEFINED:  # @line L15
            label[j] = cluster
            queue.append(j)

    for i in range(n):  # @line L2
        if label[i] != UNDEFINED:  # @line L3
            continue
        nbrs = range_query(points, i, eps, dist)  # @line L4
        if len(nbrs) < min_pts:  # @line L5
            label[i] = NOISE  # may become a border point later
            continue
        cluster += 1  # @line L6
        label[i] = cluster
        is_core[i] = True
        queue = deque()
        for j in nbrs:  # @line L7
            claim(j, queue)
        while queue:  # @line L8
            q = queue.popleft()  # @line L9
            nq = range_query(points, q, eps, dist)  # @line L10
            if len(nq) >= min_pts:  # @line L11
                is_core[q] = True
                for j in nq:  # @line L12
                    claim(j, queue)
    return label, is_core  # @line L13
