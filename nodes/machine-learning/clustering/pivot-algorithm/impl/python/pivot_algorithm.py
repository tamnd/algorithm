# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pivot-algorithm/. The authors are listed in prov/85NC9H.jsonl.

"""KwikCluster, the pivot algorithm of Ailon, Charikar and Newman (2005, 2008).

The input is a complete graph on vertices 0..n-1 in which each pair is labeled
+ (similar) or - (dissimilar), given as a symmetric boolean matrix `plus`
(plus[u][v] is True for a + pair; the diagonal is ignored). The output is a
partition into clusters. Picking the pivots uniformly at random gives an
expected cost of at most 3 times the optimum number of disagreements.
"""

from fractions import Fraction
from itertools import combinations, permutations
from typing import List, Sequence


def kwik_cluster(plus: Sequence[Sequence[bool]], rng) -> List[List[int]]:
    """The randomized pivot algorithm. rng is a random.Random."""
    n = len(plus)
    remaining = list(range(n))  # @line L1
    clusters = []
    while remaining:  # @line L2
        p = remaining[rng.randrange(len(remaining))]  # @line L3
        cluster = [p] + [v for v in remaining if v != p and plus[p][v]]  # @line L4
        clusters.append(sorted(cluster))  # @line L5
        members = set(cluster)
        remaining = [v for v in remaining if v not in members]  # @line L6
    return clusters


def kwik_cluster_order(plus: Sequence[Sequence[bool]], order: Sequence[int]) -> List[List[int]]:
    """The same algorithm with the pivots taken as the first remaining vertex of `order`.
    A uniformly random order gives exactly the distribution of kwik_cluster."""
    n = len(plus)
    removed = [False] * n
    clusters = []
    for p in order:
        if removed[p]:
            continue
        cluster = [p] + [v for v in range(n) if not removed[v] and v != p and plus[p][v]]
        for v in cluster:
            removed[v] = True
        clusters.append(sorted(cluster))
    return clusters


def disagreements(plus: Sequence[Sequence[bool]], clusters: Sequence[Sequence[int]]) -> int:
    """+ pairs split between clusters plus - pairs inside a cluster."""
    n = len(plus)
    label = [0] * n
    for c, members in enumerate(clusters):
        for v in members:
            label[v] = c
    return sum(1 for u, v in combinations(range(n), 2)
               if plus[u][v] != (label[u] == label[v]))


def set_partitions(n: int):
    """All partitions of range(n), by restricted growth strings, without recursion."""
    if n == 0:
        yield []
        return
    a = [0] * n
    while True:
        k = max(a) + 1
        yield [[v for v in range(n) if a[v] == c] for c in range(k)]
        i = n - 1
        while i > 0 and a[i] == max(a[:i]) + 1:
            i -= 1
        if i == 0:
            return
        a[i] += 1
        for j in range(i + 1, n):
            a[j] = 0


def optimum(plus: Sequence[Sequence[bool]]):
    """The exact minimum number of disagreements, by brute force over all partitions."""
    return min(((disagreements(plus, P), P) for P in set_partitions(len(plus))),
               key=lambda t: t[0])


def bad_triangles(plus: Sequence[Sequence[bool]]):
    """Triples with exactly two + pairs. Each clustering has a mistake in each of them."""
    n = len(plus)
    return [t for t in combinations(range(n), 3)
            if plus[t[0]][t[1]] + plus[t[0]][t[2]] + plus[t[1]][t[2]] == 2]


def hit_triangles(plus: Sequence[Sequence[bool]], order: Sequence[int]):
    """Bad triangles that are still whole when one of their vertices becomes a pivot."""
    n = len(plus)
    removed = [False] * n
    hit = []
    bad = bad_triangles(plus)
    for p in order:
        if removed[p]:
            continue
        for t in bad:
            if p in t and not any(removed[v] for v in t):
                hit.append(t)
        removed[p] = True
        for v in range(n):
            if plus[p][v]:
                removed[v] = True
    return hit


def expected_cost(plus: Sequence[Sequence[bool]]) -> Fraction:
    """The exact expected number of disagreements of KwikCluster, as the average over all n! orders."""
    n = len(plus)
    total, count = 0, 0
    for order in permutations(range(n)):
        total += disagreements(plus, kwik_cluster_order(plus, order))
        count += 1
    return Fraction(total, count)
