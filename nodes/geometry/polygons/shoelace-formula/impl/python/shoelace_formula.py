# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shoelace-formula/. The authors are listed in prov/1ARC5T.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]


def twice_signed_area(poly: Sequence[Point]) -> Number:
    """Twice the signed area of the closed polygon poly, by the shoelace formula.

    poly lists the vertices v[0], ..., v[n - 1]; the edge from v[n - 1] back to v[0] is implied.
    The result is positive for a counterclockwise simple polygon and negative for a clockwise one.
    For any closed polygon it is twice the integral of the winding number. With int or Fraction
    coordinates the result is exact. Time O(n), extra space O(1).
    """
    n = len(poly)
    if n < 3:  # @line L1
        return 0
    s: Number = 0  # @line L2
    for i in range(n):  # @line L3
        j = i + 1 if i + 1 < n else 0  # @line L4
        s += poly[i][0] * poly[j][1] - poly[j][0] * poly[i][1]  # @line L5
    return s


def shoelace_formula(poly: Sequence[Point]) -> Fraction:
    """The signed area of poly as an exact Fraction: half of twice_signed_area."""
    return Fraction(twice_signed_area(poly)) / 2  # @line L6


def polygon_area(poly: Sequence[Point]) -> Fraction:
    """The area of a simple polygon given in either orientation."""
    return abs(shoelace_formula(poly))


def twice_signed_area_shifted(poly: Sequence[Point]) -> Number:
    """The same value as twice_signed_area, computed relative to v[0].

    Each term is the cross product of v[i] - v[0] and v[i + 1] - v[0], so the intermediate
    values stay small when the polygon is far from the origin. This matters for floats and
    for fixed-width integers; for Python int and Fraction it gives the same exact result.
    """
    n = len(poly)
    if n < 3:
        return 0
    x0, y0 = poly[0]
    s: Number = 0
    for i in range(1, n - 1):
        ax, ay = poly[i][0] - x0, poly[i][1] - y0
        bx, by = poly[i + 1][0] - x0, poly[i + 1][1] - y0
        s += ax * by - bx * ay
    return s
