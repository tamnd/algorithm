# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chaikin-corner-cutting/. The authors are listed in prov/A2HW9B.jsonl.

"""Chaikin corner cutting.

A point is a tuple of numbers of any dimension. Each round replaces every
edge PQ of the polygon by the two points 3/4 P + 1/4 Q and 1/4 P + 3/4 Q.
The polygons converge to the uniform quadratic B-spline curve with the
input points as control points. Integer or Fraction input gives exact
Fraction output.
"""

from fractions import Fraction
from typing import Sequence

Point = tuple

Q1 = Fraction(1, 4)
Q3 = Fraction(3, 4)


def _cut(a: Point, b: Point) -> tuple[Point, Point]:
    """Return the two points at 1/4 and 3/4 of the segment ab."""
    near = tuple(Q3 * x + Q1 * y for x, y in zip(a, b))
    far = tuple(Q1 * x + Q3 * y for x, y in zip(a, b))
    return near, far


def chaikin(points: Sequence[Point], rounds: int, closed: bool = True) -> list[Point]:
    """Apply `rounds` rounds of corner cutting and return the new polygon.

    For a closed polygon of m points the result has m * 2^rounds points,
    and point 2i of a round is 3/4 P_i + 1/4 P_(i+1). For an open polyline
    of n >= 2 points each round maps n points to 2(n - 1); the end points
    are not kept. Precondition: rounds >= 0. Cost: O(m 2^rounds d)
    operations and space for the closed case.
    """
    if rounds < 0:
        raise ValueError("rounds must be at least 0")
    p = [tuple(q) for q in points]
    for _ in range(rounds):  # @line L1
        m = len(p)
        if m < 2:
            return p
        q = []  # @line L2
        edges = m if closed else m - 1
        for i in range(edges):  # @line L3
            a, b = p[i], p[(i + 1) % m]  # @line L4
            near, far = _cut(a, b)  # @line L5
            q.append(near)  # @line L5
            q.append(far)  # @line L5
        p = q  # @line L6
    return p  # @line L7


def chaikin_keep_ends(points: Sequence[Point], rounds: int) -> list[Point]:
    """Open corner cutting that keeps the two end points.

    Each round outputs P_0, then the cut points of all edges, then P_(n-1),
    but the first and the last edge get only their inner cut point. The
    end points stay fixed, and the first and the last edge keep their
    direction. Precondition: rounds >= 0. Cost as for chaikin.
    """
    p = [tuple(q) for q in points]
    for _ in range(rounds):
        n = len(p)
        if n < 3:
            return p
        q = [p[0]]
        for i in range(n - 1):
            near, far = _cut(p[i], p[i + 1])
            if i > 0:
                q.append(near)
            if i < n - 2:
                q.append(far)
        q.append(p[-1])
        p = q
    return p


def second_difference_max(points: Sequence[Point], closed: bool = True):
    """Return the largest squared length of P_(i-1) - 2 P_i + P_(i+1).

    The distance between the polygon and its quadratic B-spline curve is at
    most the square root of this value divided by 8. Cost: O(m d).
    """
    m = len(points)
    idx = range(m) if closed else range(1, m - 1)
    best = 0
    for i in idx:
        a, b, c = points[(i - 1) % m], points[i], points[(i + 1) % m]
        v = [x - 2 * y + z for x, y, z in zip(a, b, c)]
        best = max(best, sum(t * t for t in v))
    return best
