# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/samarati-algorithm/. The authors are listed in prov/FM4D27.jsonl.
"""Samarati's binary search over the heights of a full-domain generalization lattice.

A table is a list of rows. Each row is a tuple of d quasi-identifier values.
A hierarchy for attribute a is a list of dicts: hierarchy[a][l] maps each raw
value of attribute a to its value at level l, and hierarchy[a][0] is the
identity. A generalization vector v gives one level v[a] per attribute.
"""

from collections import Counter
from itertools import product
from typing import Hashable, Optional, Sequence

Row = tuple[Hashable, ...]
Hierarchy = Sequence[Sequence[dict[Hashable, Hashable]]]
Vector = tuple[int, ...]


def generalize(table: Sequence[Row], hierarchy: Hierarchy, v: Vector) -> list[Row]:
    """Return the table with each value of attribute a replaced by its value at level v[a]."""
    return [tuple(hierarchy[a][v[a]][row[a]] for a in range(len(v))) for row in table]


def suppressed_count(table: Sequence[Row], hierarchy: Hierarchy, v: Vector, k: int) -> int:
    """Return the number of rows that are in a group of fewer than k equal rows at vector v."""
    gen = generalize(table, hierarchy, v)
    counts = Counter(gen)  # @line L12
    return sum(c for c in counts.values() if c < k)  # @line L13


def satisfies(table: Sequence[Row], hierarchy: Hierarchy, v: Vector, k: int, max_sup: int) -> bool:
    """True when the table generalized by v is k-anonymous after removing at most max_sup rows."""
    return suppressed_count(table, hierarchy, v, k) <= max_sup  # @line L14


def vectors_at_height(heights: Sequence[int], h: int) -> list[Vector]:
    """All vectors v with 0 <= v[a] <= heights[a] and sum(v) == h, in lexicographic order."""
    return [v for v in product(*(range(t + 1) for t in heights)) if sum(v) == h]


def samarati(table: Sequence[Row], hierarchy: Hierarchy, k: int, max_sup: int) -> Optional[Vector]:
    """Return a generalization vector of minimal height that satisfies k-anonymity with at most
    max_sup suppressed rows, or None when even the top vector does not satisfy it.

    Among the satisfying vectors of minimal height, the result is the first one in
    lexicographic order. Such a vector is k-minimal: no satisfying vector lies strictly below it.

    Precondition: k >= 1, max_sup >= 0, each hierarchy[a] has at least one level, and
    each hierarchy is a tree (each level coarsens the one below), so that the number
    of suppressed rows can only fall when a level goes up.
    Cost: at most ceil(log2(h + 1)) + 1 rounds, where h is the height of the top vector.
    Each round tests at most g vectors, where g is the number of vectors of the lattice,
    and each test takes O(n d) expected time for n rows and d attributes.
    """
    heights = [len(levels) - 1 for levels in hierarchy]
    top: Vector = tuple(heights)
    if not satisfies(table, hierarchy, top, k, max_sup):  # @line L1
        return None
    low, high = 0, sum(heights)  # @line L2
    sol: Vector = top  # @line L3
    while low < high:  # @line L4
        try_h = (low + high) // 2  # @line L5
        found: Optional[Vector] = None  # @line L6
        for v in vectors_at_height(heights, try_h):  # @line L7
            if satisfies(table, hierarchy, v, k, max_sup):  # @line L8
                found = v
                break
        if found is not None:  # @line L9
            sol, high = found, try_h
        else:  # @line L10
            low = try_h + 1
    return sol  # @line L11
