# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/consensus-clustering/. The authors are listed in prov/B4JZZB.jsonl.
"""Consensus clustering as a median partition under the Mirkin distance.

A clustering of n items is a list of n labels. The distance between two
clusterings is the number of unordered pairs that one of them joins and the
other splits (the Mirkin distance, divided by 2). The median partition
minimizes the sum of the distances to the m input clusterings. It reduces to
weighted correlation clustering with the co-association weights.

The algorithm is the one of Ailon, Charikar and Newman: run the pivot rule
on the majority weights, compare the result with the best input clustering,
and return the better one. Its expected ratio is 11/7.
"""

from fractions import Fraction
from itertools import combinations


def canonical(labels):
    """Relabel so that labels appear as 0, 1, 2, ... in the order of the items."""
    seen = {}
    return [seen.setdefault(x, len(seen)) for x in labels]


def clusters_to_labels(clusters, n):
    labels = [-1] * n
    for c, members in enumerate(clusters):
        for v in members:
            labels[v] = c
    return labels


def co_association(labelings):
    """W[u][v] is the fraction of input clusterings that put u and v together."""
    m = len(labelings)
    n = len(labelings[0])
    W = [[Fraction(1)] * n for _ in range(n)]
    for u, v in combinations(range(n), 2):
        together = sum(1 for lab in labelings if lab[u] == lab[v])  # @line L2
        W[u][v] = W[v][u] = Fraction(together, m)
    return W


def _pairs(k):
    return k * (k - 1) // 2


def mirkin_distance(a, b):
    """The number of unordered pairs on which clusterings a and b disagree, in O(n)."""
    size_a, size_b, both = {}, {}, {}
    for x, y in zip(a, b):
        size_a[x] = size_a.get(x, 0) + 1
        size_b[y] = size_b.get(y, 0) + 1
        both[(x, y)] = both.get((x, y), 0) + 1
    joined_a = sum(_pairs(k) for k in size_a.values())
    joined_b = sum(_pairs(k) for k in size_b.values())
    joined_both = sum(_pairs(k) for k in both.values())
    return joined_a + joined_b - 2 * joined_both


def mirkin_distance_naive(a, b):
    """The same distance by a scan over all pairs, in O(n^2)."""
    n = len(a)
    return sum(1 for u, v in combinations(range(n), 2) if (a[u] == a[v]) != (b[u] == b[v]))


def total_distance(labels, labelings):
    return sum(mirkin_distance(labels, lab) for lab in labelings)


def weighted_cost(labels, W):
    """Correlation clustering cost: w+ for each split pair, w- = 1 - w+ for each joined pair."""
    n = len(labels)
    cost = Fraction(0)
    for u, v in combinations(range(n), 2):
        cost += (1 - W[u][v]) if labels[u] == labels[v] else W[u][v]
    return cost


def majority_pivot_order(W, order):
    """The pivot rule on the majority graph, with pivots taken in the given order."""
    n = len(W)
    in_rest = [True] * n
    clusters = []
    for p in order:
        if not in_rest[p]:
            continue
        cluster = [p] + [v for v in range(n) if v != p and in_rest[v] and 2 * W[p][v] > 1]
        for v in cluster:
            in_rest[v] = False
        clusters.append(sorted(cluster))
    return clusters_to_labels(clusters, n)


def majority_pivot(W, rng):
    """Lines L3 to L7: random pivots, each takes its majority neighbors."""
    n = len(W)
    rest = list(range(n))                                    # @line L3
    in_rest = [True] * n
    clusters = []
    while rest:                                              # @line L4
        p = rest[rng.randrange(len(rest))]                   # @line L5
        cluster = [p] + [v for v in rest if v != p and 2 * W[p][v] > 1]  # @line L6
        for v in cluster:                                    # @line L7
            in_rest[v] = False
        rest = [v for v in rest if in_rest[v]]
        clusters.append(sorted(cluster))
    return clusters_to_labels(clusters, n)


def best_input(labelings):
    """The input clustering with the least total distance to all inputs."""
    return min(labelings, key=lambda lab: total_distance(lab, labelings))


def consensus(labelings, rng):
    """The combined algorithm of Ailon, Charikar and Newman (expected ratio 11/7)."""
    if not labelings or not labelings[0]:
        raise ValueError("need at least one clustering of at least one item")
    n = len(labelings[0])
    if any(len(lab) != n for lab in labelings):
        raise ValueError("all clusterings must label the same items")
    W = co_association(labelings)                            # @line L1
    Q = majority_pivot(W, rng)
    B = best_input(labelings)                                # @line L8
    if total_distance(Q, labelings) <= total_distance(B, labelings):  # @line L9
        return canonical(Q)
    return canonical(B)


def set_partitions(n):
    """All set partitions of range(n) as restricted growth strings, without recursion."""
    if n == 0:
        yield []
        return
    a = [0] * n
    b = [0] * n  # b[i] = 1 + max(a[0..i-1])
    for i in range(1, n):
        b[i] = 1
    while True:
        yield list(a)
        i = n - 1
        while i > 0 and a[i] == b[i]:
            i -= 1
        if i == 0:
            return
        a[i] += 1
        for j in range(i + 1, n):
            a[j] = 0
            b[j] = max(b[j - 1], a[j - 1] + 1)


def median_partition(labelings):
    """Brute force: the least total distance and all partitions that reach it."""
    n = len(labelings[0])
    best, argbest = None, []
    for labels in set_partitions(n):
        d = total_distance(labels, labelings)
        if best is None or d < best:
            best, argbest = d, [labels]
        elif d == best:
            argbest.append(labels)
    return best, argbest
