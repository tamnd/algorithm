# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/natural-cubic-spline/. The authors are listed in prov/T0NMNV.jsonl.

"""Natural cubic spline curves through points in the plane or in space.

Given knots t[0] < ... < t[n] and points P[0..n], find the tangents D[0..n] of
the C2 Hermite spline with C''(t[0]) = C''(t[n]) = 0. The tangents solve one
tridiagonal system per coordinate (the same matrix for every coordinate),
solved here by the Thomas algorithm. The matrix is strictly diagonally
dominant, so no pivoting is needed. Use fractions.Fraction for exact results.
Cost: O(n d) time and O(n d) space for d coordinates.
"""

import math
from bisect import bisect_right
from fractions import Fraction
from typing import List, Sequence, Tuple

Point = Tuple


def tangent_system(knots: Sequence, points: Sequence[Point]):
    """The tridiagonal system (sub, diag, sup, rhs) for the tangents; rhs has one tuple per row."""
    n = len(points) - 1
    knots = [Fraction(k) if isinstance(k, int) else k for k in knots]
    h = [knots[i + 1] - knots[i] for i in range(n)]
    delta = [tuple((y - x) / h[i] for x, y in zip(points[i], points[i + 1])) for i in range(n)]
    one = h[0] / h[0]  # 1 in the number type of the knots
    sub, diag, sup, rhs = [0] * (n + 1), [0] * (n + 1), [0] * (n + 1), [None] * (n + 1)
    diag[0], sup[0] = 2 * one, one
    rhs[0] = tuple(3 * x for x in delta[0])
    for i in range(1, n):
        sub[i] = 1 / h[i - 1]
        sup[i] = 1 / h[i]
        diag[i] = 2 * (sub[i] + sup[i])
        rhs[i] = tuple(3 * (a * sub[i] + b * sup[i]) for a, b in zip(delta[i - 1], delta[i]))
    sub[n], diag[n] = one, 2 * one
    rhs[n] = tuple(3 * x for x in delta[n - 1])
    return sub, diag, sup, rhs


def thomas(sub, diag, sup, rhs):
    """Solve a tridiagonal system with vector right-hand sides, without pivoting."""
    n = len(diag)
    c = [0] * n
    d = [None] * n
    c[0] = sup[0] / diag[0]
    d[0] = tuple(x / diag[0] for x in rhs[0])
    for i in range(1, n):
        m = diag[i] - sub[i] * c[i - 1]
        c[i] = sup[i] / m if i < n - 1 else 0
        d[i] = tuple((r - sub[i] * p) / m for r, p in zip(rhs[i], d[i - 1]))
    x = [None] * n
    x[n - 1] = d[n - 1]
    for i in range(n - 2, -1, -1):
        x[i] = tuple(a - c[i] * b for a, b in zip(d[i], x[i + 1]))
    return x


def natural_tangents(knots: Sequence, points: Sequence[Point]) -> List[Point]:
    """The tangents dC/dt of the natural cubic spline at the knots.

    Precondition: len(knots) == len(points) >= 2 and the knots increase strictly.
    """
    if len(knots) != len(points) or len(points) < 2:
        raise ValueError("need one knot per point and at least two points")
    if any(b <= a for a, b in zip(knots, knots[1:])):
        raise ValueError("knots must increase strictly")
    return thomas(*tangent_system(knots, points))


def chord_length_knots(points: Sequence[Point]) -> List[float]:
    """Knots with t[i+1] - t[i] = |P[i+1] - P[i]| (floats)."""
    ts = [0.0]
    for a, b in zip(points, points[1:]):
        ts.append(ts[-1] + math.sqrt(sum((y - x) ** 2 for x, y in zip(a, b))))
    return ts


def segment_coefficients(knots, points, tangents, i: int) -> List[Point]:
    """Coefficients [a, b, c, e] of segment i as a + b s + c s^2 + e s^3, s = t - t[i]."""
    h = knots[i + 1] - knots[i]
    p0, p1, d0, d1 = points[i], points[i + 1], tangents[i], tangents[i + 1]
    c = tuple((3 * (y - x) / h - 2 * s - e) / h for x, y, s, e in zip(p0, p1, d0, d1))
    e = tuple((-2 * (y - x) / h + s + q) / (h * h) for x, y, s, q in zip(p0, p1, d0, d1))
    return [tuple(p0), tuple(d0), c, e]


def evaluate(knots, points, tangents, t, order: int = 0) -> Point:
    """The spline (or its derivative of the given order, 0 to 3) at t."""
    n = len(knots) - 1
    i = min(max(bisect_right(knots, t) - 1, 0), n - 1)
    co = segment_coefficients(knots, points, tangents, i)
    s = t - knots[i]
    out = [0] * len(points[0])
    for j in range(order, 4):
        f = 1
        for q in range(j - order + 1, j + 1):
            f *= q
        w = f * s ** (j - order)
        out = [o + w * x for o, x in zip(out, co[j])]
    return tuple(out)


def bending_energy(knots, points, tangents) -> object:
    """The integral of |C''(t)|^2 over [t[0], t[n]], exact for exact inputs."""
    total = 0
    for i in range(len(knots) - 1):
        h = knots[i + 1] - knots[i]
        co = segment_coefficients(knots, points, tangents, i)
        a = tuple(2 * x for x in co[2])
        b = tuple(2 * x + 6 * y * h for x, y in zip(co[2], co[3]))
        total += h * sum(x * x + x * y + y * y for x, y in zip(a, b)) / 3
    return total
