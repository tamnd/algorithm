# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sweep-union-length/. The authors are listed in prov/BJ70R6.jsonl.

from typing import TypeVar

T = TypeVar("T", int, float)


def sweep_union_length(intervals: list[tuple[T, T]], k: int = 1) -> T:
    """Return the total length of the points covered by at least k intervals.

    Each interval is a pair (l, r) with l <= r. Open, closed and half-open
    intervals give the same length, so the type of the end points is not
    needed. With k = 1 this is the length of the union. Time O(n log n),
    extra space O(n) for the 2n events.
    """
    events: list[tuple[T, int]] = []  # @line L1
    for lo, hi in intervals:  # @line L2
        events.append((lo, +1))
        events.append((hi, -1))
    events.sort(key=lambda e: (e[0], -e[1]))  # @line L3
    total: T = 0  # @line L4
    count = 0
    prev: T = 0
    for x, d in events:  # @line L5
        if count >= k:  # @line L6
            total += x - prev
        count += d  # @line L7
        prev = x  # @line L8
    return total  # @line L9
