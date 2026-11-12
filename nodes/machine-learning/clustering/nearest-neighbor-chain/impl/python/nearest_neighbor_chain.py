# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nearest-neighbor-chain/. The authors are listed in prov/5P8XRG.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, float, Fraction]
Merge = tuple[int, int, Number, int]

REDUCIBLE = ("single", "complete", "average", "weighted", "ward")


def update(linkage: str, d_ki: Number, d_kj: Number, d_ij: Number, n_i: int, n_j: int, n_k: int) -> Number:
    """Lance-Williams update of d(k, i u j) for the reducible linkages.

    For "ward" the values must be squared Euclidean distances (the merge
    height is then twice the increase of the within-cluster sum of squares).
    """
    if linkage == "single":
        return min(d_ki, d_kj)
    if linkage == "complete":
        return max(d_ki, d_kj)
    if linkage == "average":
        return Fraction(n_i, n_i + n_j) * d_ki + Fraction(n_j, n_i + n_j) * d_kj
    if linkage == "weighted":
        return Fraction(1, 2) * (d_ki + d_kj)
    t = n_i + n_j + n_k
    return Fraction(n_i + n_k, t) * d_ki + Fraction(n_j + n_k, t) * d_kj - Fraction(n_k, t) * d_ij


def nearest_neighbor_chain(dist: Sequence[Sequence[Number]], linkage: str) -> list[Merge]:
    """The agglomerative hierarchy of a reducible linkage by the NN-chain method.

    Follows nearest neighbors from an arbitrary cluster until two clusters are
    reciprocal nearest neighbors, merges them, and goes on from the rest of the
    chain. Returns the merges (a, b, h, size) sorted by height, with leaves
    0 .. n-1 and merge t making cluster n + t, a < b. With no ties among the
    linkage values it equals the greedy hierarchy.
    Cost: Theta(n^2) time and Theta(n^2) memory for the matrix.
    """
    if linkage not in REDUCIBLE:
        raise ValueError(f"linkage {linkage!r} is not reducible")
    n = len(dist)
    d = [list(row) for row in dist]
    active = set(range(n))  # @line L1
    size = [1] * n
    members = {i: [i] for i in range(n)}
    found: list[tuple[Number, list[int], list[int]]] = []
    chain: list[int] = []  # @line L2
    while len(active) > 1:  # @line L3
        if not chain:  # @line L4
            chain.append(min(active))
        a = chain[-1]  # @line L5
        prev = chain[-2] if len(chain) >= 2 else -1
        b, bd = prev, (d[a][prev] if prev >= 0 else None)  # @line L6
        for c in range(n):  # O(n) scan in index order, so ties go to the smaller index
            if c in active and c != a and (bd is None or d[a][c] < bd):
                b, bd = c, d[a][c]
        if b == prev:  # @line L7
            chain.pop()  # @line L8
            chain.pop()
            i, j = min(a, b), max(a, b)
            found.append((bd, members[i], members[j]))  # @line L9
            for k in active:  # @line L10
                if k != i and k != j:
                    d[i][k] = d[k][i] = update(linkage, d[k][i], d[k][j], d[i][j], size[i], size[j], size[k])
            size[i] += size[j]  # @line L11
            members[i] = members[i] + members[j]
            active.remove(j)
        else:
            chain.append(b)  # @line L12
    return _relabel(n, found)  # @line L13


def _relabel(n: int, found: list[tuple[Number, list[int], list[int]]]) -> list[Merge]:
    """Sort the merges by height (stable) and give them cluster ids with union-find."""
    parent = list(range(n))
    cluster = list(range(n))
    size = [1] * n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    out: list[Merge] = []
    for h, left, right in sorted(found, key=lambda t: t[0]):
        ru, rv = find(left[0]), find(right[0])
        a, b = sorted((cluster[ru], cluster[rv]))
        parent[rv] = ru
        size[ru] += size[rv]
        out.append((a, b, h, size[ru]))
        cluster[ru] = n + len(out) - 1
    return out
