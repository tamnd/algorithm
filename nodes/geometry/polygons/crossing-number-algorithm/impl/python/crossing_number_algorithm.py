# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crossing-number-algorithm/. The authors are listed in prov/6ADJ3H.jsonl.

from fractions import Fraction
from typing import Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]

INSIDE = 1
BOUNDARY = 0
OUTSIDE = -1


def orient(p: Point, q: Point, r: Point) -> Number:
    """Twice the signed area of the triangle pqr: positive for a left turn, zero when collinear."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def on_segment(a: Point, b: Point, q: Point) -> bool:
    """True when q lies on the closed segment ab (a == b is allowed)."""
    if orient(a, b, q) != 0:
        return False
    return (q[0] - a[0]) * (q[0] - b[0]) + (q[1] - a[1]) * (q[1] - b[1]) <= 0


def crossing_number_algorithm(polygon: list[Point], q: Point) -> int:
    """Classify q against the closed polygon by the even-odd rule.

    Returns BOUNDARY (0) when q is on an edge or a vertex, else INSIDE (1) when a ray from q to
    the right crosses the boundary an odd number of times, else OUTSIDE (-1). The polygon is a
    list of vertices in either order; it may be non-simple, and then the answer is the even-odd
    rule. A vertex with the same y as q counts as lying below the ray (the half-open rule), which
    handles a ray through a vertex and horizontal edges. Coordinates must be int or Fraction so
    that all signs are exact. Cost: Theta(n) time, O(1) extra space.
    """
    n = len(polygon)
    c = 0  # @line L1
    for i in range(n):  # @line L2
        a, b = polygon[i], polygon[(i + 1) % n]  # @line L3
        if on_segment(a, b, q):  # @line L4
            return BOUNDARY
        if (a[1] > q[1]) != (b[1] > q[1]):  # @line L5
            s = orient(a, b, q)  # @line L6
            if (s > 0) == (b[1] > a[1]):  # @line L7
                c = 1 - c
    return INSIDE if c == 1 else OUTSIDE  # @line L8
