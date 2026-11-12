# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-center-hardness/. The authors are listed in prov/MEYRRB.jsonl.

"""Farthest-first traversal for the two k-center clustering objectives
(largest radius, largest diameter), exact solvers for tiny inputs, and the
two gap reductions of the hardness theorem."""

from itertools import combinations


def farthest_first(n, k, d, first=0):
    """Farthest-first traversal on points 0..n-1 with metric d(i, j).

    Returns (centers, labels): labels[i] is the index in centers of the
    nearest center of point i (ties to the earlier center).
    """
    centers = [first]
    near = [d(i, first) for i in range(n)]
    while len(centers) < k:
        c = max(range(n), key=lambda v: (near[v], -v))
        if near[c] == 0:
            break
        centers.append(c)
        for i in range(n):
            near[i] = min(near[i], d(i, c))
    labels = []
    for i in range(n):
        best = min(range(len(centers)), key=lambda j: (d(i, centers[j]), j))
        labels.append(best)
    return centers, labels


def radius(n, centers, d):
    return max(min(d(i, c) for c in centers) for i in range(n))


def max_diameter(n, labels, d):
    """Largest distance between two points with the same label."""
    best = 0
    for i, j in combinations(range(n), 2):
        if labels[i] == labels[j]:
            best = max(best, d(i, j))
    return best


def opt_radius(n, k, d):
    """Least radius over all sets of min(k, n) data points as centers."""
    return min(radius(n, cs, d) for cs in combinations(range(n), min(k, n)))


def set_partitions(n, k):
    """Each partition of 0..n-1 into at most k blocks, once, as a label list
    (restricted growth strings, built with an explicit stack)."""
    stack = [[0]] if n else [[]]
    while stack:
        lab = stack.pop()
        if len(lab) == n:
            yield lab
            continue
        top = max(lab) + 1
        for g in range(min(top + 1, k)):
            stack.append(lab + [g])


def opt_diameter(n, k, d):
    """Least largest diameter over all partitions into at most k clusters."""
    return min(max_diameter(n, lab, d) for lab in set_partitions(n, k))


def graph_metric(n, edges):
    """Distance 0 on the diagonal, 1 on an edge and 2 otherwise."""
    E = {frozenset(e) for e in edges}

    def d(i, j):
        if i == j:
            return 0
        return 1 if frozenset((i, j)) in E else 2

    return d


def domination_number(n, edges):
    adj = [{i} for i in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    for s in range(1, n + 1):
        for D in combinations(range(n), s):
            if set().union(*(adj[v] for v in D)) == set(range(n)):
                return s
    return n


def clique_cover_number(n, edges):
    """Least number of cliques that partition the vertices."""
    E = {frozenset(e) for e in edges}
    for s in range(1, n + 1):
        for lab in set_partitions(n, s):
            if all(frozenset((i, j)) in E for i, j in combinations(range(n), 2) if lab[i] == lab[j]):
                return s
    return n
