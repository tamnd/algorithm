# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cure/. The authors are listed in prov/C6AZ80.jsonl.

"""CURE (Guha, Rastogi and Shim 1998): hierarchical clustering in which each
cluster is represented by c well scattered points shrunk toward its mean by a
factor alpha. The distance of two clusters is the smallest distance between
their representatives. The merging uses a heap of cluster pairs with lazy
deletion. For large data, CURE clusters a random sample, first in partitions,
removes slowly growing clusters as outliers, and labels every point by its
nearest representative.
"""

import heapq
import math


def dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


class Cluster:
    __slots__ = ("points", "mean", "rep")

    def __init__(self, points, mean, rep):
        self.points, self.mean, self.rep = points, mean, rep


def scattered_points(points, mean, c):
    """Farthest point selection: first the point farthest from the mean, then
    each time the point farthest from those already chosen. Ties go to the
    earlier point in the list."""
    chosen = []
    best_d = [math.inf] * len(points)
    for i in range(min(c, len(points))):  # @line L10
        pick, pick_d = -1, -1.0
        for j, p in enumerate(points):
            d = dist(p, mean) if i == 0 else best_d[j]
            if d > pick_d:
                pick, pick_d = j, d
        chosen.append(points[pick])
        q = points[pick]
        for j, p in enumerate(points):
            best_d[j] = min(best_d[j], dist(p, q))
        best_d[pick] = -1.0  # never chosen twice
    return chosen


def make_cluster(points, c, alpha):
    d = len(points[0])
    mean = tuple(sum(p[k] for p in points) / len(points) for k in range(d))  # @line L9
    scattered = scattered_points(points, mean, c)
    rep = [tuple(p[k] + alpha * (mean[k] - p[k]) for k in range(d)) for p in scattered]  # @line L11
    return Cluster(points, mean, rep)  # @line L12


def merge(u, v, c, alpha):
    points = u.points + v.points  # @line L8
    return make_cluster(points, c, alpha)


def cluster_dist(u, v):
    return min(dist(a, b) for a in u.rep for b in v.rep)


def hierarchical(clusters, k, c, alpha, outlier_at=None, outlier_size=0):
    """Merge the closest pair of clusters until k remain. If outlier_at is given,
    when the number of clusters first drops to outlier_at or fewer, the clusters
    with fewer than outlier_size points are removed as outliers."""
    alive = dict(enumerate(clusters))
    next_id = len(clusters)
    heap = []
    ids = sorted(alive)
    for i, a in enumerate(ids):  # @line L2
        for b in ids[i + 1:]:
            heap.append((cluster_dist(alive[a], alive[b]), a, b))
    heapq.heapify(heap)
    pruned = outlier_at is None
    while len(alive) > k and heap:  # @line L3
        if not pruned and len(alive) <= outlier_at:
            pruned = True
            for i in [i for i, u in alive.items() if len(u.points) < outlier_size]:  # @line L15
                del alive[i]
            continue
        d, a, b = heapq.heappop(heap)  # @line L4
        if a not in alive or b not in alive:
            continue  # a stale pair: lazy deletion
        w = merge(alive.pop(a), alive.pop(b), c, alpha)  # @line L5
        for x in sorted(alive):  # @line L6
            heapq.heappush(heap, (cluster_dist(alive[x], w), x, next_id))
        alive[next_id] = w
        next_id += 1
    return [alive[i] for i in sorted(alive)]  # @line L7


def label_points(data, clusters):
    """Give each point the index of the cluster with the nearest representative."""
    labels = []
    for x in data:  # @line L17
        best, arg = math.inf, -1
        for i, u in enumerate(clusters):
            for r in u.rep:
                d = dist(x, r)
                if d < best:
                    best, arg = d, i
        labels.append(arg)
    return labels


def cure(data, k, c=10, alpha=0.3, rng=None, sample_size=None, partitions=1, reduce_by=3,
         outlier_at=None, outlier_size=0):
    """Return (labels, clusters). Without a sample size and with one partition,
    this is the plain hierarchical CURE on all points."""
    if not data:
        return [], []
    sample = list(data)
    if sample_size is not None and sample_size < len(data):
        sample = rng.sample(sample, sample_size)  # @line L13
    singletons = [Cluster([p], tuple(p), [tuple(p)]) for p in sample]  # @line L1
    if partitions > 1:
        size = math.ceil(len(singletons) / partitions)
        partial = []
        for start in range(0, len(singletons), size):  # @line L14
            part = singletons[start:start + size]
            target = max(k, len(part) // reduce_by)
            partial += hierarchical(part, target, c, alpha)
        singletons = partial
    clusters = hierarchical(singletons, k, c, alpha, outlier_at, outlier_size)  # @line L16
    return label_points(data, clusters), clusters
