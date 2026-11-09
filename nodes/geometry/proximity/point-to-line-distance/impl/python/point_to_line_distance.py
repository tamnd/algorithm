# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-to-line-distance/. The authors are listed in prov/SVW2VD.jsonl.

import math
from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]


def point_to_line_distance_squared(p: Point, a: Point, b: Point) -> tuple[Fraction, tuple[Fraction, Fraction]]:
    """Return (squared distance, foot) from p to the line through a and b.

    Precondition: a != b, coordinates are int or Fraction. The result is exact.
    Cost: O(1) arithmetic operations.
    """
    if a == b:  # @line L1
        raise ValueError("the two points do not define a line")
    ux, uy = b[0] - a[0], b[1] - a[1]  # @line L2
    wx, wy = p[0] - a[0], p[1] - a[1]  # @line L3
    c = ux * wy - uy * wx  # @line L4
    uu = ux * ux + uy * uy
    t = Fraction(wx * ux + wy * uy) / uu  # @line L5
    foot = (a[0] + t * ux, a[1] + t * uy)  # @line L6
    return Fraction(c * c) / uu, foot  # @line L7


def signed_area2(p: Point, a: Point, b: Point) -> Number:
    """Return (b - a) x (p - a): positive when p is left of the directed line a -> b."""
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


def point_to_line_distance_squared_nd(p: Sequence[Number], a: Sequence[Number], b: Sequence[Number]) -> Fraction:
    """Squared distance from p to the line through a != b in any dimension: |w|^2 - (w.u)^2 / |u|^2.

    Cost: O(d) arithmetic operations for dimension d.
    """
    if len(p) != len(a) or len(a) != len(b):
        raise ValueError("points of different dimensions")
    u = [bi - ai for ai, bi in zip(a, b)]
    w = [pi - ai for ai, pi in zip(a, p)]
    uu = sum(x * x for x in u)
    if uu == 0:
        raise ValueError("the two points do not define a line")
    wu = sum(x * y for x, y in zip(w, u))
    ww = sum(x * x for x in w)
    return Fraction(ww) - Fraction(wu * wu) / uu


def point_to_line_distance(p: Point, a: Point, b: Point) -> float:
    """The distance as a float, for display only. Compare squared distances instead."""
    return math.sqrt(point_to_line_distance_squared(p, a, b)[0])
