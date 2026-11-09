# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polygon-simplicity-test/. The authors are listed in prov/HSYKXN.jsonl.

from bisect import bisect_left, bisect_right
from fractions import Fraction
from typing import Optional, Sequence, Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]
Violation = tuple[str, int, int]


def orient(p: Point, q: Point, r: Point) -> int:
    """Sign of (q - p) x (r - p): +1 left turn, 0 collinear, -1 right turn."""
    v = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (v > 0) - (v < 0)


def _in_box(p: Point, q: Point, r: Point) -> bool:
    return min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= r[1] <= max(p[1], q[1])


def segments_intersect(a: Point, b: Point, c: Point, d: Point) -> bool:
    """Exact test whether the closed segments ab and cd have a common point."""
    d1, d2, d3, d4 = orient(c, d, a), orient(c, d, b), orient(a, b, c), orient(a, b, d)
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True
    return (
        (d1 == 0 and _in_box(c, d, a))
        or (d2 == 0 and _in_box(c, d, b))
        or (d3 == 0 and _in_box(a, b, c))
        or (d4 == 0 and _in_box(a, b, d))
    )


def find_violation(poly: Sequence[Point]) -> Optional[Violation]:
    """Return None if the closed polygon is simple, else a witness.

    Edge i joins poly[i] and poly[i + 1] (indices mod n). The polygon is simple when n >= 3,
    adjacent edges meet only in their shared vertex, and other edges do not meet. Witnesses:
    ("too few vertices", -1, -1); ("repeated vertex", i, j) with poly[i] == poly[j];
    ("fold", i, j) for adjacent edges i, j that overlap; ("meet", i, j) for two non-adjacent
    edges that share a point. Coordinates must be int or Fraction. Time O(n log n) comparisons
    and orientation tests; the status is a Python list, so an insert also moves O(n) references.
    """
    n = len(poly)
    if n < 3:  # @line L1
        return ("too few vertices", -1, -1)
    first: dict[Point, int] = {}
    for i, p in enumerate(poly):  # @line L2
        if p in first:
            return ("repeated vertex", first[p], i)
        first[p] = i
    for i in range(n):  # @line L3
        a, b, c = poly[i - 1], poly[i], poly[(i + 1) % n]
        if orient(a, b, c) == 0 and (a[0] - b[0]) * (c[0] - b[0]) + (a[1] - b[1]) * (c[1] - b[1]) > 0:
            return ("fold", (i - 1) % n, i)

    seg = [(min(poly[i], poly[(i + 1) % n]), max(poly[i], poly[(i + 1) % n])) for i in range(n)]

    def adjacent(i: int, j: int) -> bool:
        return (i - j) % n in (1, n - 1)

    def check(s: int, t: int) -> Optional[Violation]:
        if adjacent(s, t) or not segments_intersect(*seg[s], *seg[t]):
            return None
        return ("meet", min(s, t), max(s, t))

    status: list[int] = []
    for v in sorted(range(n), key=lambda k: poly[k]):  # @line L4
        p = poly[v]
        here = ((v - 1) % n, v)

        # side(t) is -1, 0, +1 when p is above, on, below the line of t; it does not decrease
        # along the status, so two binary searches find the edges through p.
        def side(t: int) -> int:
            return -orient(seg[t][0], seg[t][1], p)

        i = bisect_left(status, 0, key=side)  # @line L5
        j = bisect_right(status, 0, key=side)
        for k in range(i, j):  # @line L6
            t = status[k]
            if t not in here:
                e = here[0] if not adjacent(t, here[0]) else here[1]
                return ("meet", min(t, e), max(t, e))
        del status[i:j]  # @line L7
        starting = [e for e in here if seg[e][0] == p]  # @line L8
        if len(starting) == 2:
            e1, e2 = starting
            r1, r2 = seg[e1][1], seg[e2][1]
            if orient(p, r1, r2) < 0:
                starting = [e2, e1]
        status[i:i] = starting
        c = len(starting)
        pairs = [(i - 1, i)] if c == 0 else [(i - 1, i), (i + c - 1, i + c)]
        for x, y in pairs:  # @line L9
            if 0 <= x and y < len(status):
                found = check(status[x], status[y])
                if found:
                    return found
    return None  # @line L10


def is_simple(poly: Sequence[Point]) -> bool:
    return find_violation(poly) is None
