# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optics/. The authors are listed in prov/P3H623.jsonl.

"""OPTICS (Ankerst, Breunig, Kriegel and Sander 1999) with brute force range queries.

The eps-neighborhood of a point holds the point itself. UNDEFINED distances are
math.inf. The seed list is a binary heap with lazy deletion: a decrease of a
reachability pushes a new entry, and stale entries are skipped. Ties in the
reachability go to the smaller index.
"""

import heapq
import math

INF = math.inf
NOISE = -1


def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def neighbors(points, i, eps, dist=euclidean):
    """Pairs (distance, j) for all j within eps of point i, i itself included."""
    p = points[i]
    out = []
    for j, q in enumerate(points):
        dij = dist(p, q)
        if dij <= eps:
            out.append((dij, j))
    return out


def core_distance(nbrs, min_pts):
    """Distance to the min_pts-th nearest point (the point itself counts), or INF."""
    if len(nbrs) < min_pts:
        return INF
    return sorted(d for d, _ in nbrs)[min_pts - 1]


def optics(points, eps, min_pts, dist=euclidean):
    """Return (order, reach, core): the cluster order and, for each point index,
    its reachability distance and its core distance (INF means UNDEFINED)."""
    n = len(points)
    processed = [False] * n
    reach = [INF] * n
    core = [INF] * n
    order = []

    def update(nbrs, center, heap):  # OrderSeeds::update
        c = core[center]
        for d, o in nbrs:
            if not processed[o]:
                new_r = max(c, d)  # @line L13
                if new_r < reach[o]:  # @line L14
                    reach[o] = new_r
                    heapq.heappush(heap, (new_r, o))

    for i in range(n):  # @line L1
        if processed[i]:  # @line L2
            continue
        heap = []
        nbrs = neighbors(points, i, eps, dist)  # @line L3
        processed[i] = True  # @line L4
        core[i] = core_distance(nbrs, min_pts)
        order.append(i)  # @line L5
        if core[i] < INF:  # @line L6
            update(nbrs, i, heap)  # @line L7
        while heap:  # @line L8
            r, q = heapq.heappop(heap)  # @line L9
            if processed[q] or r != reach[q]:
                continue  # a stale entry
            nq = neighbors(points, q, eps, dist)  # @line L10
            processed[q] = True
            core[q] = core_distance(nq, min_pts)
            order.append(q)  # @line L11
            if core[q] < INF:
                update(nq, q, heap)  # @line L12
    return order, reach, core


def extract_dbscan(order, reach, core, eps_prime):
    """ExtractDBSCAN-Clustering (Figure 8 of the paper), for eps_prime <= eps.

    Returns labels by point index: -1 for noise, clusters 0, 1, 2, ...
    """
    labels = [NOISE] * len(order)
    cluster = NOISE  # @line L15
    for p in order:  # @line L16
        if reach[p] > eps_prime:  # @line L17
            if core[p] <= eps_prime:  # @line L18
                cluster += 1  # @line L19
                labels[p] = cluster
            else:
                labels[p] = NOISE  # @line L20
        else:
            labels[p] = cluster  # @line L21
    return labels


def assign_missed_border_points(points, labels, core, eps_prime, dist=euclidean):
    """Optional post-processing: give each noise point that lies within eps_prime
    of a core point (at eps_prime) the label of the first such core point."""
    out = list(labels)
    for i, lab in enumerate(labels):
        if lab != NOISE:
            continue
        for j in range(len(points)):
            if core[j] <= eps_prime and dist(points[i], points[j]) <= eps_prime:
                out[i] = labels[j]
                break
    return out
