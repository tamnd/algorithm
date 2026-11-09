# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-in-convex-polygon/. The authors are listed in prov/KB6KXW.jsonl.

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


def point_in_convex_polygon(polygon: list[Point], q: Point) -> int:
    """Classify q against a strictly convex polygon by binary search over the fan from polygon[0].

    The polygon must be strictly convex (no three consecutive vertices collinear) and given in
    counterclockwise order, with n >= 3 vertices. Returns INSIDE (1), BOUNDARY (0) or OUTSIDE (-1).
    Coordinates must be int or Fraction so that all signs are exact. Cost: O(log n) time, O(1)
    extra space; the input is not checked, since checking would cost Theta(n).
    """
    n = len(polygon)
    if n < 3:
        raise ValueError("a convex polygon needs at least 3 vertices")
    v0 = polygon[0]
    a = orient(v0, polygon[1], q)
    b = orient(v0, polygon[n - 1], q)
    if a < 0 or b > 0:  # @line L1
        return OUTSIDE
    lo, hi = 1, n - 1  # @line L2
    while hi - lo > 1:  # @line L3
        mid = (lo + hi) // 2  # @line L4
        if orient(v0, polygon[mid], q) >= 0:  # @line L5
            lo = mid
        else:
            hi = mid
    s = orient(polygon[lo], polygon[hi], q)  # @line L6
    if s < 0:  # @line L7
        return OUTSIDE
    if s == 0 or (lo == 1 and a == 0) or (hi == n - 1 and b == 0):  # @line L8
        return BOUNDARY
    return INSIDE  # @line L9
