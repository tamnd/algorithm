# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/complete-linkage-clustering/. The authors are listed in prov/6884Z8.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, float, Fraction]
Merge = tuple[int, int, Number, int]


def complete_linkage_clustering(dist: Sequence[Sequence[Number]]) -> list[Merge]:
    """Complete-linkage hierarchy of an n x n dissimilarity matrix.

    At each step merges the two clusters whose largest member distance is the
    least, and sets the distance of the new cluster to each other cluster to
    the larger of the two old distances. Returns the merges (a, b, h, size):
    leaves are 0 .. n-1, merge t makes cluster n + t, a < b. Of several closest
    pairs the first in lexicographic order of slots is merged.
    Cost: Theta(n^3) time and Theta(n^2) memory.
    """
    n = len(dist)
    d = [list(row) for row in dist]  # @line L1
    active = list(range(n))
    ident = list(range(n))
    size = [1] * n
    merges: list[Merge] = []
    while len(active) > 1:  # @line L2
        best = None
        for x in range(len(active)):  # @line L3
            for y in range(x + 1, len(active)):
                i, j = active[x], active[y]
                if best is None or d[i][j] < best[0]:
                    best = (d[i][j], i, j)
        assert best is not None
        h, i, j = best
        for k in active:  # @line L4
            if k != i and k != j:
                d[i][k] = d[k][i] = max(d[i][k], d[j][k])  # @line L5
        a, b = sorted((ident[i], ident[j]))
        merges.append((a, b, h, size[i] + size[j]))  # @line L6
        size[i] += size[j]  # @line L7
        ident[i] = n + len(merges) - 1
        active.remove(j)
    return merges  # @line L8


def cut_into_k(n: int, merges: list[Merge], k: int) -> list[int]:
    """Labels of the k clusters left after the first n - k merges, numbered by smallest point."""
    member = [[i] for i in range(n)]
    for a, b, _, _ in merges[: n - k]:
        member.append(member[a] + member[b])
        member[a], member[b] = [], []
    labels = [0] * n
    for c, pts in enumerate(sorted((m for m in member if m), key=min)):
        for p in pts:
            labels[p] = c
    return labels
