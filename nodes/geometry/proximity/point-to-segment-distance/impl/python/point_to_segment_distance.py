# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-to-segment-distance/. The authors are listed in prov/XQG3E1.jsonl.

import math
from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]


def point_to_segment_distance_squared(p: Point, a: Point, b: Point) -> tuple[Number, tuple[Number, Number]]:
    """Return (squared distance, closest point) from p to the closed segment ab.

    a == b is allowed (the segment is one point). Coordinates are int or Fraction;
    the result is exact. Cost: O(1) arithmetic operations.
    """
    ux, uy = b[0] - a[0], b[1] - a[1]  # @line L1
    wx, wy = p[0] - a[0], p[1] - a[1]  # @line L2
    s = wx * ux + wy * uy  # @line L3
    if s <= 0:  # @line L4
        return wx * wx + wy * wy, a
    d = ux * ux + uy * uy  # @line L5
    if s >= d:  # @line L6
        return (p[0] - b[0]) ** 2 + (p[1] - b[1]) ** 2, b
    c = ux * wy - uy * wx  # @line L7
    t = Fraction(s, 1) / d
    return Fraction(c * c) / d, (a[0] + t * ux, a[1] + t * uy)  # @line L8


def point_to_segment_distance_squared_nd(p: Sequence[Number], a: Sequence[Number], b: Sequence[Number]) -> Number:
    """Squared distance from p to the segment ab in any dimension. Cost: O(d)."""
    u = [y - x for x, y in zip(a, b)]
    w = [y - x for x, y in zip(a, p)]
    s = sum(x * y for x, y in zip(w, u))
    ww = sum(x * x for x in w)
    if s <= 0:
        return ww
    d = sum(x * x for x in u)
    if s >= d:
        return sum((x - y) ** 2 for x, y in zip(p, b))
    return ww - Fraction(s * s) / d


def point_to_segment_distance(p: Point, a: Point, b: Point) -> float:
    """The distance as a float, for display only. Compare squared distances instead."""
    return math.sqrt(point_to_segment_distance_squared(p, a, b)[0])
