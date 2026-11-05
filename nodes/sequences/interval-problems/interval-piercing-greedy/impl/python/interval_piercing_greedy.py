# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-piercing-greedy/. The authors are listed in prov/V30M7R.jsonl.
"""Greedy piercing of intervals by the earliest right end.

kind is "closed" ([l, r], l <= r), "half-open" ([l, r), l < r) or "open"
((l, r), l < r). For closed intervals the points are right ends. For the other
types the greedy point is "just left of r"; the function returns a concrete
point of that group: max l for half-open, and the midpoint of max l and r for
open intervals.
"""

from typing import Sequence, Tuple

Interval = Tuple[float, float]


def interval_piercing_greedy(intervals: Sequence[Interval], kind: str = "closed") -> list[float]:
    """Return a smallest list of points such that every interval contains one."""
    if kind not in ("closed", "half-open", "open"):
        raise ValueError("kind must be closed, half-open or open")
    order = sorted(range(len(intervals)), key=lambda k: intervals[k][1])  # @line L1
    points: list[float] = []  # @line L2
    p = None  # the right end that opened the current group
    max_l = None  # the largest left end in the current group
    for k in order:  # @line L3
        l, r = intervals[k]
        pierced = p is not None and (l <= p if kind == "closed" else l < p)  # @line L4
        if not pierced:
            p, max_l = r, l  # @line L5
            points.append(_point(p, max_l, kind))  # @line L6
        else:
            # The group point must also lie in this interval: move it right
            # of l if needed (only for half-open and open intervals).
            max_l = max(max_l, l)
            points[-1] = _point(p, max_l, kind)
    return points  # @line L7


def _point(p, max_l, kind):
    if kind == "closed":
        return p
    if kind == "half-open":
        return max_l
    return (max_l + p) / 2
