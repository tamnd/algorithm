# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/circle-line-intersection/. The authors are listed in prov/SGBK99.jsonl.
"""Exact intersection of a circle and a line.

The circle has an integer center c and an integer radius r >= 0; the line is
A*x + B*y + C = 0 with integers and (A, B) != (0, 0). A point of the answer is
returned as a QuadPoint: base + coef * sqrt(rad), with Fraction coordinates in
base and coef and an integer rad >= 0. When rad is a perfect square the point
is rational, and `rational()` gives it exactly.
"""

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt, sqrt


@dataclass(frozen=True)
class QuadPoint:
    base: tuple[Fraction, Fraction]
    coef: tuple[Fraction, Fraction]
    rad: int

    def rational(self):
        """The exact point if sqrt(rad) is an integer, else None."""
        s = isqrt(self.rad)
        if s * s != self.rad:
            return None
        return (self.base[0] + s * self.coef[0], self.base[1] + s * self.coef[1])

    def to_float(self) -> tuple[float, float]:
        s = sqrt(self.rad)
        return (float(self.base[0]) + s * float(self.coef[0]),
                float(self.base[1]) + s * float(self.coef[1]))


def circle_line_intersection(c: tuple[int, int], r: int, a: int, b: int, cc: int) -> list[QuadPoint]:
    """The 0, 1 or 2 points where the line a*x + b*y + cc = 0 meets the circle (c, r)."""
    if a == 0 and b == 0:  # @line L1
        raise ValueError("the line needs (a, b) != (0, 0)")
    if r < 0:
        raise ValueError("the radius must not be negative")
    n = a * a + b * b  # @line L2
    e = a * c[0] + b * c[1] + cc
    foot = (c[0] - Fraction(e * a, n), c[1] - Fraction(e * b, n))  # @line L3
    d = r * r * n - e * e  # @line L4
    zero = (Fraction(0), Fraction(0))
    if d < 0:  # @line L5
        return []
    if d == 0:  # @line L6
        return [QuadPoint(foot, zero, 0)]
    u = (Fraction(-b, n), Fraction(a, n))  # @line L7
    return [QuadPoint(foot, u, d), QuadPoint(foot, (-u[0], -u[1]), d)]


def intersection_count(c: tuple[int, int], r: int, a: int, b: int, cc: int) -> int:
    """Only the number of common points: the sign of r^2 (a^2 + b^2) - (a c_x + b c_y + cc)^2."""
    d = r * r * (a * a + b * b) - (a * c[0] + b * c[1] + cc) ** 2
    return 0 if d < 0 else (1 if d == 0 else 2)
