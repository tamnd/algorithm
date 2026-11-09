# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/half-plane-intersection-deque/. The authors are listed in prov/EFZJWK.jsonl.

from collections import deque
from fractions import Fraction
from functools import cmp_to_key
from typing import Optional, Union

Num = Union[int, Fraction]
Point = tuple[Num, Num]
# A half-plane is (p, d): the closed set of points x with cross(d, x - p) >= 0, left of the line
# through p in direction d. The direction d must not be the zero vector.
HalfPlane = tuple[Point, Point]


def cross(u: Point, v: Point) -> Num:
    return u[0] * v[1] - u[1] * v[0]


def _half(d: Point) -> int:
    return 0 if d[1] > 0 or (d[1] == 0 and d[0] > 0) else 1


def _angle_cmp(g: HalfPlane, h: HalfPlane) -> int:
    """Compare the directions of g and h by angle in [0, 2 pi); exact."""
    a, b = _half(g[1]), _half(h[1])
    if a != b:
        return a - b
    c = cross(g[1], h[1])
    return -1 if c > 0 else (1 if c < 0 else 0)


def strictly_inside(h: HalfPlane, x: Point) -> bool:
    (px, py), d = h
    return cross(d, (x[0] - px, x[1] - py)) > 0


def meet(g: HalfPlane, h: HalfPlane) -> Optional[tuple[Fraction, Fraction]]:
    """The common point of the boundary lines of g and h, or None when they are parallel."""
    (p, d), (q, e) = g, h
    den = cross(d, e)
    if den == 0:
        return None
    t = Fraction(cross((q[0] - p[0], q[1] - p[1]), e), den)
    return (p[0] + t * d[0], p[1] + t * d[1])


def half_plane_intersection(planes: list[HalfPlane]) -> list[tuple[Fraction, Fraction]]:
    """Return the vertices, in counterclockwise order, of the intersection of the closed half-planes.

    Precondition: the intersection is bounded or empty (add the four sides of a large box if
    needed). The result has no repeated and no collinear vertices. If the intersection is empty,
    a single point or a segment (zero area), the result is []. Coordinates must be int or
    Fraction; the vertices are exact Fractions.
    Cost: O(n log n) for the sort and O(n) for the deque passes.
    """
    hs = sorted(planes, key=cmp_to_key(_angle_cmp))  # @line L1
    uniq: list[HalfPlane] = []
    for h in hs:
        if uniq and _angle_cmp(uniq[-1], h) == 0:
            # same direction: keep the half-plane whose line is further to the left
            if strictly_inside(uniq[-1], h[0]):
                uniq[-1] = h
        else:
            uniq.append(h)
    dq: deque[HalfPlane] = deque()  # @line L2
    for h in uniq:  # @line L3
        while len(dq) >= 2 and not strictly_inside(h, meet(dq[-2], dq[-1])):  # @line L4
            dq.pop()
        while len(dq) >= 2 and not strictly_inside(h, meet(dq[0], dq[1])):  # @line L5
            dq.popleft()
        if dq and cross(dq[-1][1], h[1]) <= 0:  # @line L6
            return []
        dq.append(h)  # @line L7
    while len(dq) >= 3:  # @line L8
        if not strictly_inside(dq[0], meet(dq[-2], dq[-1])):
            dq.pop()
        elif not strictly_inside(dq[-1], meet(dq[0], dq[1])):  # @line L9
            dq.popleft()
        else:
            break
    if len(dq) < 3 or cross(dq[-1][1], dq[0][1]) <= 0:  # @line L10
        return []
    hs = list(dq)
    return [meet(hs[i], hs[(i + 1) % len(hs)]) for i in range(len(hs))]  # type: ignore[misc]  # @line L11
