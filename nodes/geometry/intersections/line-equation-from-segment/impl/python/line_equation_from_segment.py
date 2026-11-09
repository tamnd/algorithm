# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/line-equation-from-segment/. The authors are listed in prov/1VCZP5.jsonl.
"""The canonical integer equation A*x + B*y + C = 0 of the line through two points."""

from fractions import Fraction
from math import gcd

Point = tuple[int, int]
Line = tuple[int, int, int]


def line_through(p: Point, q: Point) -> Line:
    """The line through the distinct integer points p and q, in canonical form.

    The result has gcd(|A|, |B|, |C|) = 1 and A > 0, or A = 0 and B > 0, so two
    pairs of points give the same triple exactly when they span the same line."""
    if p == q:  # @line L1
        raise ValueError("the two points must be distinct")
    a, b = p[1] - q[1], q[0] - p[0]  # @line L2
    c = -(a * p[0] + b * p[1])  # @line L3
    g = gcd(gcd(abs(a), abs(b)), abs(c))  # @line L4
    a, b, c = a // g, b // g, c // g
    if a < 0 or (a == 0 and b < 0):  # @line L5
        a, b, c = -a, -b, -c
    return a, b, c  # @line L6


def oriented_line_through(p: Point, q: Point) -> Line:
    """The line through p and q, not normalized, with A*x + B*y + C > 0 left of p -> q."""
    if p == q:
        raise ValueError("the two points must be distinct")
    a, b = p[1] - q[1], q[0] - p[0]
    return a, b, -(a * p[0] + b * p[1])


def side(line: Line, r: tuple) -> int:
    """The sign of A*x + B*y + C at r: +1, 0 or -1."""
    a, b, c = line
    v = a * r[0] + b * r[1] + c
    return (v > 0) - (v < 0)


def line_through_rational(p: tuple, q: tuple) -> Line:
    """The canonical integer line through two distinct points with Fraction coordinates."""
    p = tuple(Fraction(t) for t in p)
    q = tuple(Fraction(t) for t in q)
    if p == q:
        raise ValueError("the two points must be distinct")
    a, b = p[1] - q[1], q[0] - p[0]
    c = -(a * p[0] + b * p[1])
    den = 1
    for t in (a, b, c):
        den = den * t.denominator // gcd(den, t.denominator)
    return line_through_from_coeffs(int(a * den), int(b * den), int(c * den))


def line_through_from_coeffs(a: int, b: int, c: int) -> Line:
    """Bring an integer triple with (a, b) != (0, 0) to the canonical form."""
    if a == 0 and b == 0:
        raise ValueError("(a, b) must not be (0, 0)")
    g = gcd(gcd(abs(a), abs(b)), abs(c))
    a, b, c = a // g, b // g, c // g
    if a < 0 or (a == 0 and b < 0):
        a, b, c = -a, -b, -c
    return a, b, c

