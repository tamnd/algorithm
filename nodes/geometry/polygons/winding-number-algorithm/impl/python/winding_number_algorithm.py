# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/winding-number-algorithm/. The authors are listed in prov/CSD45Q.jsonl.

from fractions import Fraction
from typing import Optional, Sequence, Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]


def orient(p: Point, q: Point, r: Point) -> Number:
    """Twice the signed area of pqr: positive for a left turn. Exact for int and Fraction."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def on_segment(q: Point, a: Point, b: Point) -> bool:
    """True when q lies on the closed segment ab."""
    return (
        orient(a, b, q) == 0
        and min(a[0], b[0]) <= q[0] <= max(a[0], b[0])
        and min(a[1], b[1]) <= q[1] <= max(a[1], b[1])
    )


def winding_number(poly: Sequence[Point], q: Point) -> Optional[int]:
    """The winding number of the closed polygon poly around the point q.

    poly lists the vertices; the closing edge is implied. The polygon may be self-intersecting,
    have repeated or collinear vertices and horizontal edges. The result is None when q lies on
    the boundary, else an integer: 0 means outside, and for a simple polygon it is +1 inside a
    counterclockwise polygon and -1 inside a clockwise one. Time O(n), extra space O(1).
    """
    n = len(poly)
    w = 0  # @line L1
    for i in range(n):  # @line L2
        a, b = poly[i], poly[(i + 1) % n]  # @line L3
        if on_segment(q, a, b):  # @line L4
            return None
        if a[1] <= q[1] < b[1]:  # @line L5: an upward edge that crosses the ray
            if orient(a, b, q) > 0:
                w += 1
        elif b[1] <= q[1] < a[1]:  # @line L6: a downward edge that crosses the ray
            if orient(a, b, q) < 0:
                w -= 1
    return w  # @line L7


def winding_number_algorithm(poly: Sequence[Point], q: Point, rule: str = "nonzero") -> Optional[bool]:
    """Point in polygon by the winding number: True inside, False outside, None on the boundary.

    rule is "nonzero" (inside when the winding number is not 0) or "evenodd" (inside when it is odd).
    """
    w = winding_number(poly, q)
    if w is None:
        return None
    if rule == "nonzero":
        return w != 0
    if rule == "evenodd":
        return w % 2 == 1
    raise ValueError("rule must be 'nonzero' or 'evenodd'")
