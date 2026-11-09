# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/segment-intersection-point/. The authors are listed in prov/DG9ZZA.jsonl.

from fractions import Fraction
from typing import Union

Num = Union[int, Fraction]
Point = tuple[Num, Num]
FPoint = tuple[Fraction, Fraction]


def orient(p: Point, q: Point, r: Point) -> int:
    """Return the sign of the cross product (q - p) x (r - p).

    +1 means p, q, r turn left (counterclockwise), 0 means collinear, -1 means a right turn.
    Exact for int and Fraction coordinates.
    """
    v = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (v > 0) - (v < 0)


def in_box(p: Point, q: Point, r: Point) -> bool:
    """Return True when r lies in the closed bounding box of p and q."""
    return min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= r[1] <= max(p[1], q[1])


def _fp(p: Point) -> FPoint:
    return (Fraction(p[0]), Fraction(p[1]))


def segment_intersection(a: Point, b: Point, c: Point, d: Point) -> tuple[FPoint, ...]:
    """Intersect the closed segments ab and cd exactly.

    Return () when they do not meet, (p,) when they meet in the single point p, and (p, q) with
    p < q in lexicographic order when they overlap in the segment pq. A segment may have equal end
    points (it is then a single point). Coordinates must be int or Fraction; the result uses
    Fraction. Cost: O(1) arithmetic operations.
    """
    d1 = orient(c, d, a)  # @line L1
    d2 = orient(c, d, b)
    d3 = orient(a, b, c)
    d4 = orient(a, b, d)
    if d1 * d2 < 0 and d3 * d4 < 0:  # @line L2
        # proper crossing: solve a + t (b - a) on the line cd
        ex, ey = b[0] - a[0], b[1] - a[1]
        fx, fy = d[0] - c[0], d[1] - c[1]
        t = Fraction((c[0] - a[0]) * fy - (c[1] - a[1]) * fx, ex * fy - ey * fx)  # @line L3
        return ((a[0] + t * ex, a[1] + t * ey),)  # @line L4
    if d1 == 0 and d2 == 0 and d3 == 0 and d4 == 0:  # @line L5
        lo = max(min(_fp(a), _fp(b)), min(_fp(c), _fp(d)))  # @line L6
        hi = min(max(_fp(a), _fp(b)), max(_fp(c), _fp(d)))
        if lo > hi:  # @line L7
            return ()
        if lo == hi:  # @line L8
            return (lo,)
        return (lo, hi)  # @line L9
    if d1 == 0 and in_box(c, d, a):  # @line L10
        return (_fp(a),)
    if d2 == 0 and in_box(c, d, b):  # @line L11
        return (_fp(b),)
    if d3 == 0 and in_box(a, b, c):  # @line L12
        return (_fp(c),)
    if d4 == 0 and in_box(a, b, d):  # @line L13
        return (_fp(d),)
    return ()  # @line L14


def segments_intersect(a: Point, b: Point, c: Point, d: Point) -> bool:
    """Return True when the closed segments ab and cd have a common point."""
    return len(segment_intersection(a, b, c, d)) > 0
