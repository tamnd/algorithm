# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/single-linkage-clustering/. The authors are listed in prov/NRPC50.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, float, Fraction]
Merge = tuple[int, int, Number, int]


def single_linkage_clustering(dist: Sequence[Sequence[Number]]) -> list[Merge]:
    """Single-linkage hierarchy of an n x n dissimilarity matrix.

    Builds a minimum spanning tree with Prim's algorithm on the complete graph,
    sorts its n - 1 edges and replays them with union-find. Returns the merges
    (a, b, h, size): leaves are 0 .. n-1, merge t makes cluster n + t, a < b.
    Cost: Theta(n^2) time for the tree, O(n log n) for the sort, Theta(n)
    extra memory besides the matrix.
    """
    n = len(dist)
    if n == 0:
        return []
    in_tree = [False] * n
    in_tree[0] = True  # @line L1
    best = [dist[0][v] for v in range(n)]
    origin = [0] * n
    edges: list[tuple[Number, int, int]] = []  # @line L2
    for _ in range(n - 1):  # @line L3
        k = -1
        for v in range(n):  # @line L4
            if not in_tree[v] and (k < 0 or best[v] < best[k]):
                k = v
        in_tree[k] = True  # @line L5
        edges.append((best[k], origin[k], k))
        for v in range(n):  # @line L6
            if not in_tree[v] and dist[k][v] < best[v]:
                best[v] = dist[k][v]
                origin[v] = k
    edges.sort(key=lambda e: e[0])  # @line L7
    parent = list(range(n))
    cluster = list(range(n))
    size = [1] * n
    merges: list[Merge] = []

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for w, u, v in edges:  # @line L8
        ru, rv = find(u), find(v)  # @line L9
        a, b = sorted((cluster[ru], cluster[rv]))
        if size[ru] < size[rv]:
            ru, rv = rv, ru
        parent[rv] = ru
        size[ru] += size[rv]
        merges.append((a, b, w, size[ru]))
        cluster[ru] = n + len(merges) - 1
    return merges  # @line L10


def cut_into_k(n: int, merges: list[Merge], k: int) -> list[int]:
    """Labels of the k clusters left after the first n - k merges (1 <= k <= n).

    Clusters are numbered 0, 1, ... in the order of their smallest point.
    """
    member = [[i] for i in range(n)]
    for a, b, _, _ in merges[: n - k]:
        member.append(member[a] + member[b])
        member[a], member[b] = [], []
    labels = [0] * n
    for c, pts in enumerate(sorted((m for m in member if m), key=min)):
        for p in pts:
            labels[p] = c
    return labels


def spacing(dist: Sequence[Sequence[Number]], labels: list[int]) -> Number:
    """The least dissimilarity between two points with different labels."""
    n = len(dist)
    return min(dist[i][j] for i in range(n) for j in range(i + 1, n) if labels[i] != labels[j])
