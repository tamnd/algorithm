# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sweep-maximum-overlap/. The authors are listed in prov/KC8DHG.jsonl.

from typing import Optional, TypeVar

T = TypeVar("T", int, float)


def sweep_maximum_overlap(
    intervals: list[tuple[T, T]], closed: bool = True
) -> tuple[int, Optional[T]]:
    """Return (d, x): the largest number d of intervals that share a point, and a place x.

    Each interval is a pair (l, r). With closed=True the intervals are closed
    [l, r] with l <= r, so intervals that touch at one point overlap there, and
    x is a point of depth d. With closed=False they are half-open [l, r) with
    l < r (or open (l, r)), touching intervals do not overlap, and the depth d
    is reached at x for half-open intervals and just to the right of x for
    open ones. For no intervals the result is (0, None).
    Time O(n log n), extra space O(n).
    """
    events: list[tuple[T, int]] = []  # @line L1
    for lo, hi in intervals:  # @line L2
        events.append((lo, +1))
        events.append((hi, -1))
    # closed: starts before ends at a tie; half-open and open: ends first
    events.sort(key=lambda e: (e[0], -e[1] if closed else e[1]))  # @line L3
    count = 0  # @line L4
    best = 0
    at: Optional[T] = None
    for x, d in events:  # @line L5
        count += d  # @line L6
        if count > best:  # @line L7
            best, at = count, x
    return best, at  # @line L8
