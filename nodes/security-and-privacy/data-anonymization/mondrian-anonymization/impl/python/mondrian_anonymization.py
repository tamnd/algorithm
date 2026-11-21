# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mondrian-anonymization/. The authors are listed in prov/EV1MMH.jsonl.
"""Greedy strict multidimensional partitioning for k-anonymity (Mondrian), on integer attributes.

A table is a list of rows. Each row is a tuple of d integers, the quasi-identifier values.
The result is a partition of the row indices into regions. Each region is released with
the range [min, max] of each attribute over its rows.
"""

from fractions import Fraction
from typing import Optional, Sequence

Row = tuple[int, ...]


def best_cut(table: Sequence[Row], part: Sequence[int], a: int, k: int) -> Optional[int]:
    """Return the allowable cut value x on attribute a that maximizes
    min(#{t : t[a] <= x}, #{t : t[a] > x}) over the rows of part, ties to the smaller x.
    A cut is allowable when both sides have at least k rows. Return None when no cut is allowable.
    """
    values = sorted(table[i][a] for i in part)
    best: Optional[int] = None
    best_score = -1
    for j in range(len(values) - 1):
        if values[j] != values[j + 1]:
            left = j + 1
            right = len(values) - left
            if left >= k and right >= k and min(left, right) > best_score:
                best, best_score = values[j], min(left, right)
    return best


def mondrian(table: Sequence[Row], k: int) -> list[list[int]]:
    """Return the regions of the greedy Mondrian partition, each a sorted list of row indices.
    The regions are sorted by their first index.

    Every region has at least k rows, and no region has an allowable cut on any attribute,
    so each region has at most 2 d (k - 1) + m rows, where m is the largest number of
    equal rows of the table.

    Precondition: k >= 1 and len(table) >= k, or the table is empty.
    Cost: O(d r log r) time for a region of r rows. With distinct values the cuts are at
    the median and the total is O(d n log^2 n); in the worst case the recursion has
    n / k levels and the total is O(d n^2 log n). Space O(n). An explicit stack replaces recursion.
    """
    n = len(table)
    if n == 0:
        return []
    d = len(table[0])
    full_range = [max(r[a] for r in table) - min(r[a] for r in table) for a in range(d)]
    result: list[list[int]] = []  # @line L1
    stack: list[list[int]] = [list(range(n))]
    while stack:  # @line L2
        part = stack.pop()  # @line L3

        def norm_range(a: int) -> Fraction:
            if full_range[a] == 0:
                return Fraction(0)
            vals = [table[i][a] for i in part]
            return Fraction(max(vals) - min(vals), full_range[a])

        order = sorted(range(d), key=lambda a: (-norm_range(a), a))
        cut_done = False
        for a in order:  # @line L4
            x = best_cut(table, part, a, k)  # @line L5
            if x is not None:  # @line L6
                lhs = [i for i in part if table[i][a] <= x]
                rhs = [i for i in part if table[i][a] > x]
                stack.append(rhs)  # @line L7
                stack.append(lhs)
                cut_done = True
                break
        if not cut_done:
            result.append(sorted(part))  # @line L8
    result.sort()
    return result  # @line L9


def summarize(table: Sequence[Row], regions: Sequence[Sequence[int]]) -> list[tuple[tuple[int, int], ...]]:
    """Return the released box of each region: the pair (min, max) for each attribute."""
    d = len(table[0]) if table else 0
    return [tuple((min(table[i][a] for i in reg), max(table[i][a] for i in reg)) for a in range(d)) for reg in regions]
