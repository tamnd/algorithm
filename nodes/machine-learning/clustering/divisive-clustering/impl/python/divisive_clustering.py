# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/divisive-clustering/. The authors are listed in prov/9ERGNS.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, float, Fraction]
Split = tuple[tuple[int, ...], tuple[int, ...], Number]


def diameter(dist: Sequence[Sequence[Number]], c: Sequence[int]) -> Number:
    """The largest dissimilarity between two points of c (0 for one point)."""
    return max((dist[i][j] for i in c for j in c), default=0)


def splinter(dist: Sequence[Sequence[Number]], c: list[int]) -> tuple[list[int], list[int]]:
    """Split the cluster c (two or more points) into a splinter group and the rest.

    The point with the largest mean dissimilarity to the others starts the
    splinter group. Then, while the rest has two or more points, the point of the
    rest whose mean dissimilarity to the rest minus its mean dissimilarity to
    the splinter group is largest moves, if that difference is positive.
    Ties go to the smaller index. Cost: O(m^2) for m points, with running sums.
    """
    m = len(c)
    to_rest = {i: sum(dist[i][j] for j in c) for i in c}
    to_s = {i: 0 for i in c}
    first = max(c, key=lambda i: (Fraction(to_rest[i]) / (m - 1), -i))  # @line L8
    s, r = [first], [i for i in c if i != first]  # @line L9
    for i in c:
        to_rest[i] -= dist[i][first]
        to_s[i] += dist[i][first]
    while len(r) >= 2:  # @line L10

        def gain(i: int) -> Number:
            return Fraction(to_rest[i]) / (len(r) - 1) - Fraction(to_s[i]) / len(s)  # @line L11

        best = max(r, key=lambda i: (gain(i), -i))  # @line L12
        if gain(best) <= 0:  # @line L13
            break
        r.remove(best)  # @line L14
        s.append(best)
        for i in c:
            to_rest[i] -= dist[i][best]
            to_s[i] += dist[i][best]
    return sorted(s), sorted(r)  # @line L15


def divisive_clustering(dist: Sequence[Sequence[Number]]) -> list[Split]:
    """DIANA (Kaufman and Rousseeuw): top-down hierarchy of an n x n dissimilarity matrix.

    Repeatedly splits the cluster with the largest diameter by the splinter
    rule, until each cluster has one point. Returns the n - 1 splits (S, R, h) in
    the order made: S is the splinter group, R the rest and h the diameter of
    the split cluster. Cost: O(n^3) time and Theta(n^2) memory for the matrix.
    """
    n = len(dist)
    clusters = [list(range(n))] if n > 0 else []  # @line L1
    splits: list[Split] = []
    while any(len(c) > 1 for c in clusters):  # @line L2
        big = [t for t in range(len(clusters)) if len(clusters[t]) > 1]
        k = max(big, key=lambda t: (diameter(dist, clusters[t]), -t))  # @line L3
        c = clusters.pop(k)
        s, r = splinter(dist, c)  # @line L4
        clusters += [s, r]  # @line L5
        splits.append((tuple(s), tuple(r), diameter(dist, c)))  # @line L6
    return splits  # @line L7


def splits_to_merges(n: int, splits: list[Split]) -> list[tuple[int, int, Number, int]]:
    """The same hierarchy as merges (a, b, h, size), bottom up: the splits in reverse order."""
    ids: dict[frozenset[int], int] = {frozenset([i]): i for i in range(n)}
    out: list[tuple[int, int, Number, int]] = []
    for s, r, h in reversed(splits):
        a, b = sorted((ids[frozenset(s)], ids[frozenset(r)]))
        out.append((a, b, h, len(s) + len(r)))
        ids[frozenset(s) | frozenset(r)] = n + len(out) - 1
    return out
