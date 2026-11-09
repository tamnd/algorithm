# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shamos-hoey-algorithm/. The authors are listed in prov/5XWJY8.jsonl.

from bisect import bisect_left, bisect_right
from fractions import Fraction
from typing import Optional, Union

Num = Union[int, Fraction]
Point = tuple[Num, Num]
Segment = tuple[Point, Point]


def orient(p: Point, q: Point, r: Point) -> int:
    """Sign of (q - p) x (r - p): +1 left turn, 0 collinear, -1 right turn. Exact for int and Fraction."""
    v = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (v > 0) - (v < 0)


def _in_box(p: Point, q: Point, r: Point) -> bool:
    return min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= r[1] <= max(p[1], q[1])


def segments_intersect(s: Segment, t: Segment) -> bool:
    """Exact test whether the closed segments s and t have a common point (all degenerate cases)."""
    a, b = s
    c, d = t
    d1, d2, d3, d4 = orient(c, d, a), orient(c, d, b), orient(a, b, c), orient(a, b, d)
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True
    return (
        (d1 == 0 and _in_box(c, d, a))
        or (d2 == 0 and _in_box(c, d, b))
        or (d3 == 0 and _in_box(a, b, c))
        or (d4 == 0 and _in_box(a, b, d))
    )


def shamos_hoey(segments: list[Segment]) -> Optional[tuple[int, int]]:
    """Return a pair (i, j), i < j, of indices of two closed segments that intersect, or None.

    Segments may be vertical, may have length zero, may share end points or overlap; coordinates
    must be int or Fraction so that every test is exact. The sweep goes over the end points in
    lexicographic order and stops at the first intersection it finds.
    Cost: O(n log n) comparisons and orientation tests. The status is a Python list, so one insert
    or delete also moves O(n) references; a balanced search tree removes that term.
    """
    seg = [(min(a, b), max(a, b)) for a, b in segments]  # @line L1
    at: dict[Point, list[int]] = {}
    for i, (l, r) in enumerate(seg):
        at.setdefault(l, []).append(i)
        if r != l:
            at.setdefault(r, []).append(i)
    status: list[int] = []  # @line L2

    def found(i: int, j: int) -> tuple[int, int]:
        return (min(i, j), max(i, j))

    for p in sorted(at):  # @line L3
        here = at[p]  # @line L4
        if len(here) >= 2:  # @line L5
            return found(here[0], here[1])
        s = here[0]  # @line L6
        # side(t) = -orient(t.l, t.r, p) is -1, 0, +1 when p is above, on, below the line of t;
        # it does not decrease along the status, so two binary searches find the zero block.
        def side(t: int) -> int:
            return -orient(seg[t][0], seg[t][1], p)

        i = bisect_left(status, 0, key=side)  # @line L7
        j = bisect_right(status, 0, key=side)
        for k in range(i, j):  # @line L8
            if status[k] != s:
                return found(s, status[k])
        l, r = seg[s]
        if l == r:  # @line L9
            continue
        if p == l:  # @line L10
            status.insert(i, s)
            for k in (i - 1, i + 1):
                if 0 <= k < len(status) and segments_intersect(seg[s], seg[status[k]]):
                    return found(s, status[k])
        else:  # @line L11
            assert j == i + 1 and status[i] == s
            del status[i]
            if 0 < i < len(status) and segments_intersect(seg[status[i - 1]], seg[status[i]]):
                return found(status[i - 1], status[i])
    return None  # @line L12
