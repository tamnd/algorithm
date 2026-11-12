# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/agglomerative-clustering/. The authors are listed in prov/G398XN.jsonl.

import heapq
from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, float, Fraction]
Merge = tuple[int, int, Number, int]

LINKAGES = ("single", "complete", "average", "weighted", "centroid", "median", "ward")
HALF = Fraction(1, 2)


def lance_williams(
    linkage: str, d_ki: Number, d_kj: Number, d_ij: Number, n_i: int, n_j: int, n_k: int
) -> Number:
    """Return the dissimilarity of cluster k to the union of clusters i and j.

    The value is a_i d_ki + a_j d_kj + b d_ij + g |d_ki - d_kj| with the
    coefficients of Lance and Williams (1967) for the named linkage. For
    "centroid", "median" and "ward" the input values must be squared
    Euclidean distances. Cost: O(1) arithmetic operations.
    """
    s = n_i + n_j
    if linkage == "single":
        a_i, a_j, b, g = HALF, HALF, Fraction(0), -HALF
    elif linkage == "complete":
        a_i, a_j, b, g = HALF, HALF, Fraction(0), HALF
    elif linkage == "average":
        a_i, a_j, b, g = Fraction(n_i, s), Fraction(n_j, s), Fraction(0), Fraction(0)
    elif linkage == "weighted":
        a_i, a_j, b, g = HALF, HALF, Fraction(0), Fraction(0)
    elif linkage == "centroid":
        a_i, a_j, b, g = Fraction(n_i, s), Fraction(n_j, s), Fraction(-n_i * n_j, s * s), Fraction(0)
    elif linkage == "median":
        a_i, a_j, b, g = HALF, HALF, Fraction(-1, 4), Fraction(0)
    elif linkage == "ward":
        t = s + n_k
        a_i, a_j, b, g = Fraction(n_i + n_k, t), Fraction(n_j + n_k, t), Fraction(-n_k, t), Fraction(0)
    else:
        raise ValueError(f"unknown linkage {linkage!r}")
    return a_i * d_ki + a_j * d_kj + b * d_ij + g * abs(d_ki - d_kj)


def agglomerative_clustering(dist: Sequence[Sequence[Number]], linkage: str) -> list[Merge]:
    """Run greedy bottom-up clustering on an n x n dissimilarity matrix.

    Returns the n - 1 merges (a, b, h, size) in order. Leaves are 0 .. n-1 and
    the cluster made by merge t is n + t; a < b, h is the merge height and size
    is the number of points in the new cluster. Of several closest pairs, the
    pair (i, j) of slots that comes first in lexicographic order is merged.
    Cost: Theta(n^3) time and Theta(n^2) memory.
    """
    n = len(dist)
    if linkage not in LINKAGES:
        raise ValueError(f"unknown linkage {linkage!r}")
    d = [list(row) for row in dist]
    active = list(range(n))  # @line L1
    size = [1] * n
    ident = list(range(n))
    merges: list[Merge] = []  # @line L2
    while len(active) > 1:  # @line L3
        best = None
        for x in range(len(active)):  # @line L4
            for y in range(x + 1, len(active)):
                i, j = active[x], active[y]
                if best is None or d[i][j] < best[0]:
                    best = (d[i][j], i, j)
        assert best is not None
        h, i, j = best  # @line L5
        for k in active:  # @line L6
            if k != i and k != j:
                v = lance_williams(linkage, d[k][i], d[k][j], d[i][j], size[i], size[j], size[k])  # @line L7
                d[i][k] = d[k][i] = v
        a, b = sorted((ident[i], ident[j]))
        merges.append((a, b, h, size[i] + size[j]))  # @line L8
        size[i] += size[j]  # @line L9
        ident[i] = n + len(merges) - 1
        active.remove(j)
    return merges  # @line L10


def agglomerative_clustering_heap(dist: Sequence[Sequence[Number]], linkage: str) -> list[Merge]:
    """The same merges as agglomerative_clustering, with a binary heap of pairs.

    Stale heap entries are skipped by a version number per slot (lazy deletion).
    Cost: O(n^2 log n) time and Theta(n^2) memory.
    """
    n = len(dist)
    if linkage not in LINKAGES:
        raise ValueError(f"unknown linkage {linkage!r}")
    d = [list(row) for row in dist]
    alive = [True] * n
    version = [0] * n
    size = [1] * n
    ident = list(range(n))
    heap = [(d[i][j], i, j, 0, 0) for i in range(n) for j in range(i + 1, n)]
    heapq.heapify(heap)
    merges: list[Merge] = []
    while len(merges) < n - 1:
        h, i, j, vi, vj = heapq.heappop(heap)
        if not (alive[i] and alive[j] and version[i] == vi and version[j] == vj):
            continue
        for k in range(n):
            if alive[k] and k != i and k != j:
                d[i][k] = d[k][i] = lance_williams(linkage, d[k][i], d[k][j], d[i][j], size[i], size[j], size[k])
        a, b = sorted((ident[i], ident[j]))
        merges.append((a, b, h, size[i] + size[j]))
        size[i] += size[j]
        ident[i] = n + len(merges) - 1
        alive[j] = False
        version[i] += 1
        for k in range(n):
            if alive[k] and k != i:
                p, q = min(i, k), max(i, k)
                heapq.heappush(heap, (d[p][q], p, q, version[p], version[q]))
    return merges


def merges_to_sets(n: int, merges: list[Merge]) -> list[tuple[frozenset[int], frozenset[int], Number]]:
    """Turn merges with cluster ids into (A, B, h) with the point sets A and B."""
    sets = [frozenset([i]) for i in range(n)]
    out = []
    for a, b, h, _ in merges:
        out.append((sets[a], sets[b], h))
        sets.append(sets[a] | sets[b])
    return out
