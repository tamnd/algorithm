# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ward-method/. The authors are listed in prov/G4DBR6.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, float, Fraction]
Merge = tuple[int, int, Number, int]


def merge_cost(n_i: int, c_i: Sequence[Number], n_j: int, c_j: Sequence[Number]) -> Number:
    """Increase of the within-cluster sum of squares when two clusters merge:
    n_i n_j / (n_i + n_j) times the squared distance of their centroids."""
    return Fraction(n_i * n_j, n_i + n_j) * sum((a - b) ** 2 for a, b in zip(c_i, c_j))


def ward_method(points: Sequence[Sequence[Number]]) -> list[Merge]:
    """Ward's minimum variance hierarchy of n points in R^d.

    At each step merges the two clusters whose union increases the total
    within-cluster sum of squares the least. Returns the merges (a, b, h, size)
    where h is that increase; leaves are 0 .. n-1, merge t makes cluster n + t,
    a < b. Of several best pairs the first in lexicographic order of slots wins.
    Cost: Theta(n^3 d) time and Theta(n d) memory.
    """
    n = len(points)
    cent = [[Fraction(x) if isinstance(x, int) else x for x in p] for p in points]  # @line L1
    size = [1] * n
    ident = list(range(n))
    active = list(range(n))
    merges: list[Merge] = []
    while len(active) > 1:  # @line L2
        best = None
        for x in range(len(active)):  # @line L3
            for y in range(x + 1, len(active)):
                i, j = active[x], active[y]
                c = merge_cost(size[i], cent[i], size[j], cent[j])  # @line L4
                if best is None or c < best[0]:
                    best = (c, i, j)
        assert best is not None
        h, i, j = best
        s = size[i] + size[j]
        cent[i] = [(size[i] * a + size[j] * b) / s for a, b in zip(cent[i], cent[j])]  # @line L5
        a_id, b_id = sorted((ident[i], ident[j]))
        merges.append((a_id, b_id, h, s))  # @line L6
        size[i] = s  # @line L7
        ident[i] = n + len(merges) - 1
        active.remove(j)
    return merges  # @line L8


def sum_of_squares(points: Sequence[Sequence[Number]], members: Sequence[int]) -> Number:
    """Within-cluster sum of squared distances of the given points to their centroid."""
    if not members:
        return 0
    d = len(points[0])
    c = [Fraction(sum(Fraction(points[i][t]) for i in members), len(members)) for t in range(d)]
    return sum((Fraction(points[i][t]) - c[t]) ** 2 for i in members for t in range(d))
