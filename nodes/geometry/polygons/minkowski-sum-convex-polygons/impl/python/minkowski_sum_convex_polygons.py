# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minkowski-sum-convex-polygons/. The authors are listed in prov/BG3ZFX.jsonl.

from fractions import Fraction
from typing import Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]


def cross(a: Point, b: Point) -> Number:
    return a[0] * b[1] - a[1] * b[0]


def half(d: Point) -> int:
    """0 if the angle of the nonzero vector d is in [0, pi), 1 if it is in [pi, 2 pi)."""
    return 0 if d[1] > 0 or (d[1] == 0 and d[0] > 0) else 1


def angle_le(a: Point, b: Point) -> bool:
    """True when the angle of a in [0, 2 pi) is at most the angle of b (both nonzero)."""
    ha, hb = half(a), half(b)
    if ha != hb:
        return ha < hb
    return cross(a, b) >= 0


def same_direction(a: Point, b: Point) -> bool:
    return half(a) == half(b) and cross(a, b) == 0


def lowest_first(poly: list[Point]) -> list[Point]:
    k = min(range(len(poly)), key=lambda i: (poly[i][1], poly[i][0]))
    return poly[k:] + poly[:k]


def edge_vectors(poly: list[Point]) -> list[Point]:
    n = len(poly)
    out = []
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        d = (b[0] - a[0], b[1] - a[1])
        if d != (0, 0):
            out.append(d)
    return out


def minkowski_sum_convex_polygons(p: list[Point], q: list[Point]) -> list[Point]:
    """Minkowski sum of two convex polygons by merging their edge vectors by angle.

    Each input is a nonempty list of vertices of a convex polygon in counterclockwise order. It may
    have collinear or repeated consecutive vertices, and it may be degenerate: one point, or a
    segment given by its endpoints. The result is the sum as a strictly convex polygon in
    counterclockwise order starting at its lowest vertex (least y, then least x); it has one vertex
    if the sum is a point and two if it is a segment. Coordinates must be int or Fraction.
    Cost: O(n + m) time and space.
    """
    if not p or not q:
        raise ValueError("both polygons must have at least one vertex")
    p, q = lowest_first(p), lowest_first(q)  # @line L1
    e, f = edge_vectors(p), edge_vectors(q)  # @line L2
    d: list[Point] = []
    i = j = 0  # @line L3
    while i < len(e) or j < len(f):  # @line L4
        if j == len(f) or (i < len(e) and angle_le(e[i], f[j])):  # @line L5
            v = e[i]
            i += 1
        else:  # @line L6
            v = f[j]
            j += 1
        if d and same_direction(d[-1], v):  # @line L7
            d[-1] = (d[-1][0] + v[0], d[-1][1] + v[1])
        else:
            d.append(v)
    r = [(p[0][0] + q[0][0], p[0][1] + q[0][1])]  # @line L8
    for v in d[:-1]:
        r.append((r[-1][0] + v[0], r[-1][1] + v[1]))
    return r  # @line L9
