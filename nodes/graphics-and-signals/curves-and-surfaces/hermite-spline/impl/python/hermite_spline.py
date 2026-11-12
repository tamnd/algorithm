# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hermite-spline/. The authors are listed in prov/V6BWHE.jsonl.

"""Cubic Hermite spline curves in the plane or in space.

A point is a tuple of numbers. Use fractions.Fraction coordinates and knots for
exact results. The spline has knots t[0] < ... < t[n], points P[i] and tangents
D[i]; D[i] is the derivative dC/dt at t[i], in the global parameter t. On
[t[i], t[i+1]] the curve is the cubic Hermite segment with local parameter
u = (t - t[i]) / h, h = t[i+1] - t[i], and end tangents h D[i] and h D[i+1].
Cost: O(d) per point for d coordinates, after an O(log n) search for the span.
"""

from bisect import bisect_right
from typing import List, Sequence, Tuple

Point = Tuple


def hermite_basis(u):
    """The four cubic Hermite basis values (H0, H1, H2, H3) at u.

    C(u) = H0 p0 + H1 m0 + H2 m1 + H3 p1 is the segment with C(0) = p0,
    C(1) = p1, C'(0) = m0 and C'(1) = m1.
    """
    u2 = u * u
    u3 = u2 * u
    return (2 * u3 - 3 * u2 + 1, u3 - 2 * u2 + u, u3 - u2, -2 * u3 + 3 * u2)


def segment_coefficients(p0: Point, m0: Point, p1: Point, m1: Point) -> List[Point]:
    """Power basis coefficients [a, b, c, d] of the segment a + b u + c u^2 + d u^3."""
    a = tuple(p0)
    b = tuple(m0)
    c = tuple(3 * (y - x) - 2 * s - e for x, y, s, e in zip(p0, p1, m0, m1))
    d = tuple(-2 * (y - x) + s + e for x, y, s, e in zip(p0, p1, m0, m1))
    return [a, b, c, d]


def hermite_segment(p0: Point, m0: Point, p1: Point, m1: Point, u, order: int = 0) -> Point:
    """The derivative of the given order (0 to 3) of the Hermite segment at u."""
    coeffs = segment_coefficients(p0, m0, p1, m1)
    out = [0] * len(p0)
    for j in range(order, 4):
        f = 1
        for q in range(j - order + 1, j + 1):
            f *= q
        w = f * u ** (j - order)
        out = [o + w * cj for o, cj in zip(out, coeffs[j])]
    return tuple(out)


def hermite_to_bezier(p0: Point, m0: Point, p1: Point, m1: Point) -> List[Point]:
    """The cubic Bezier control points of the same segment: p0, p0 + m0/3, p1 - m1/3, p1."""
    b1 = tuple(x + s / 3 for x, s in zip(p0, m0))
    b2 = tuple(y - e / 3 for y, e in zip(p1, m1))
    return [tuple(p0), b1, b2, tuple(p1)]


def find_span(knots: Sequence, t) -> int:
    """The index i with knots[i] <= t < knots[i+1], clamped to 0 .. n - 1."""
    n = len(knots) - 1
    i = bisect_right(knots, t) - 1
    return min(max(i, 0), n - 1)


def hermite_spline(knots: Sequence, points: Sequence[Point], tangents: Sequence[Point], t, order: int = 0) -> Point:
    """Evaluate the Hermite spline (or its derivative in t of the given order) at t.

    Precondition: len(knots) == len(points) == len(tangents) >= 2 and the knots
    increase strictly. At an inner knot the segment on the right is used.
    """
    if not (len(knots) == len(points) == len(tangents) >= 2):
        raise ValueError("need matching knots, points and tangents, at least two of each")
    if any(b <= a for a, b in zip(knots, knots[1:])):
        raise ValueError("knots must increase strictly")
    i = find_span(knots, t)
    h = knots[i + 1] - knots[i]
    u = (t - knots[i]) / h
    m0 = tuple(h * x for x in tangents[i])
    m1 = tuple(h * x for x in tangents[i + 1])
    v = hermite_segment(points[i], m0, points[i + 1], m1, u, order)
    return tuple(x / h ** order for x in v)


def segment_one_sided(knots, points, tangents, i: int, side: str, order: int) -> Point:
    """The derivative of the given order of segment i at its left end ("left") or right end ("right"), in t."""
    h = knots[i + 1] - knots[i]
    m0 = tuple(h * x for x in tangents[i])
    m1 = tuple(h * x for x in tangents[i + 1])
    u = 0 if side == "left" else 1
    v = hermite_segment(points[i], m0, points[i + 1], m1, u, order)
    return tuple(x / h ** order for x in v)
