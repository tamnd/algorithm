# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/friends-of-friends-algorithm/. The authors are listed in prov/HXVJ9V.jsonl.
"""Friends-of-friends groups of points.

Two points are friends when their distance is at most the linking length b.
A group is a connected component of the friendship graph. Points are put in a
hash grid of cells of side b, so each friend of a point lies in the same cell
or in one of the 3^dim - 1 neighboring cells, and the components are built
with a disjoint-set forest (union by size, path halving).

Positions are tuples of any dimension. Expected time O(N + P) for P pairs at
distance at most about 2 b, when the grid lookups are O(1).
"""

import math
from itertools import product
from typing import Sequence

Vec = Sequence[float]


def _find(parent: list[int], i: int) -> int:
    while parent[i] != i:  # @line L9
        parent[i] = parent[parent[i]]
        i = parent[i]
    return i


def _union(parent: list[int], size: list[int], i: int, j: int) -> None:
    ri, rj = _find(parent, i), _find(parent, j)
    if ri == rj:
        return
    if size[ri] < size[rj]:  # @line L10
        ri, rj = rj, ri
    parent[rj] = ri
    size[ri] += size[rj]


def friends_of_friends(x: Sequence[Vec], b: float, min_size: int = 1) -> list[list[int]]:
    """Groups of point indices, each sorted, ordered by their smallest index."""
    if b <= 0:
        raise ValueError("the linking length must be positive")
    n = len(x)
    if n == 0:
        return []
    dim = len(x[0])
    grid: dict[tuple[int, ...], list[int]] = {}
    for i, p in enumerate(x):  # @line L1
        grid.setdefault(tuple(math.floor(c / b) for c in p), []).append(i)
    parent = list(range(n))  # @line L2
    size = [1] * n
    b2 = b * b
    offsets = list(product((-1, 0, 1), repeat=dim))
    for i, p in enumerate(x):  # @line L3
        cell = tuple(math.floor(c / b) for c in p)
        for off in offsets:  # @line L4
            for j in grid.get(tuple(c + o for c, o in zip(cell, off)), ()):  # @line L5
                if j > i and sum((p[k] - x[j][k]) ** 2 for k in range(dim)) <= b2:  # @line L6
                    _union(parent, size, i, j)
    groups: dict[int, list[int]] = {}
    for i in range(n):  # @line L7
        groups.setdefault(_find(parent, i), []).append(i)
    return sorted((g for g in groups.values() if len(g) >= min_size), key=lambda g: g[0])  # @line L8
