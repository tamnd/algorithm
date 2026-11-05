# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-containment-sort/. The authors are listed in prov/8YB754.jsonl.
"""Interval containment by sorting.

For each interval, find an interval of the family that contains it, or report
that it is maximal. Intervals are pairs (l, r) with l <= r, all of one type
(closed, half-open or open); the containment test l' <= l and r <= r' is the
same for every type. End points may be any comparable keys, so mixed types can
be encoded as (x, 0) or (x, 1) keys.
"""

from typing import Any, Optional, Sequence, Tuple

Interval = Tuple[Any, Any]


def interval_containment_sort(intervals: Sequence[Interval]) -> list[Optional[int]]:
    """Return parent[k]: the index of an interval that contains interval k, or None.

    The intervals with parent None are exactly one copy of each maximal interval
    (an interval no other interval properly contains). Among equal copies, the
    copy with the smallest index is kept as maximal.
    """
    n = len(intervals)
    # Sort by left end ascending, then right end descending, then index.
    # Two stable sorts; reverse=True keeps equal keys in their old order.
    order = list(range(n))  # @line L1
    order.sort(key=lambda k: intervals[k][1], reverse=True)
    order.sort(key=lambda k: intervals[k][0])
    parent: list[Optional[int]] = [None] * n  # @line L2
    best: Optional[int] = None
    for k in order:  # @line L3
        if best is not None and intervals[k][1] <= intervals[best][1]:  # @line L4
            parent[k] = best  # @line L5
        else:
            best = k  # @line L6
    return parent  # @line L7


def has_nested_pair(intervals: Sequence[Interval]) -> bool:
    """Decide whether some interval contains another one (different index)."""
    return any(p is not None for p in interval_containment_sort(intervals))
