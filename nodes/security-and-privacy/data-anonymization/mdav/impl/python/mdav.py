# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mdav/. The authors are listed in prov/HMJJKR.jsonl.
"""MDAV (maximum distance to average vector), the fixed-size microaggregation heuristic.

A record is a sequence of d numbers. The distance is the Euclidean distance; the code
compares squared distances, which gives the same order. Ties go to the lowest record
index, so the result is deterministic. With int or Fraction inputs the arithmetic is exact.
"""

import heapq
from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, float, Fraction]
Record = Sequence[Number]


def _centroid(records: Sequence[Record], ids: Sequence[int]) -> list[Number]:
    d = len(records[ids[0]])
    return [sum(Fraction(records[i][a]) if isinstance(records[i][a], int) else records[i][a] for i in ids) / len(ids) for a in range(d)]


def _dist2(x: Sequence[Number], y: Sequence[Number]) -> Number:
    return sum((xa - ya) * (xa - ya) for xa, ya in zip(x, y))


def _farthest(records: Sequence[Record], ids: Sequence[int], point: Sequence[Number]) -> int:
    # The largest distance wins; on a tie the lowest index wins.
    return min(ids, key=lambda i: (-_dist2(records[i], point), i))


def _group_around(records: Sequence[Record], ids: Sequence[int], r: int, k: int) -> list[int]:
    others = [i for i in ids if i != r]
    nearest = heapq.nsmallest(k - 1, others, key=lambda i: (_dist2(records[i], records[r]), i))
    return sorted([r] + nearest)


def mdav(records: Sequence[Record], k: int) -> list[list[int]]:
    """Partition the record indices into groups by MDAV.

    Returns the groups in the order MDAV forms them, each as a sorted list of indices.
    Every group has k records, except the last, which has between k and 2k - 1.

    Precondition: 1 <= k <= n, where n = len(records), and all records have the same
    dimension d.
    Cost: at most n / (2k) + 2 rounds, each with O(n d) distance work and an
    O(n log k) selection, so O(n^2 (d + log k) / k) time and O(n) extra space.
    """
    n = len(records)
    if not 1 <= k <= n:
        raise ValueError("need 1 <= k <= number of records")
    remaining = list(range(n))  # @line L1
    groups: list[list[int]] = []
    while len(remaining) >= 3 * k:  # @line L2
        c = _centroid(records, remaining)  # @line L3
        r = _farthest(records, remaining, c)  # @line L4
        g_r = _group_around(records, remaining, r, k)  # @line L5
        groups.append(g_r)
        taken = set(g_r)
        remaining = [i for i in remaining if i not in taken]
        s = _farthest(records, remaining, records[r])  # @line L6
        g_s = _group_around(records, remaining, s, k)  # @line L7
        groups.append(g_s)
        taken = set(g_s)
        remaining = [i for i in remaining if i not in taken]
    if len(remaining) >= 2 * k:  # @line L8
        c = _centroid(records, remaining)
        r = _farthest(records, remaining, c)  # @line L9
        g_r = _group_around(records, remaining, r, k)  # @line L10
        groups.append(g_r)
        taken = set(g_r)
        remaining = [i for i in remaining if i not in taken]
    groups.append(sorted(remaining))  # @line L11
    return groups


def microaggregate(records: Sequence[Record], k: int) -> tuple[list[list[int]], list[list[Number]]]:
    """Run MDAV and replace each record by the centroid of its group.

    Returns (groups, masked), where masked[i] is the centroid of the group of record i.
    Precondition and cost as for mdav; the replacement adds O(n d).
    """
    groups = mdav(records, k)
    masked: list[list[Number]] = [[] for _ in records]
    for g in groups:  # @line L12
        c = _centroid(records, g)
        for i in g:
            masked[i] = list(c)  # @line L13
    return groups, masked  # @line L14


def sse(records: Sequence[Record], groups: Sequence[Sequence[int]]) -> Number:
    """The within-group sum of squared errors, the information loss of a partition."""
    total: Number = 0
    for g in groups:
        c = _centroid(records, g)
        total += sum(_dist2(records[i], c) for i in g)
    return total
