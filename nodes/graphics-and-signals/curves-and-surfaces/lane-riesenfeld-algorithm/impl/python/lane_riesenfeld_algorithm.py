# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lane-riesenfeld-algorithm/. The authors are listed in prov/DS8H6B.jsonl.

"""The Lane-Riesenfeld algorithm for uniform B-spline curves.

A point is a tuple of numbers of any dimension. One round doubles every
control point and then replaces each point by the midpoint of it and its
successor, d times. The result is the control polygon of the same uniform
B-spline curve of degree d on knots of half the spacing. Integer or
Fraction input gives exact Fraction output.
"""

from fractions import Fraction
from math import comb
from typing import Sequence

Point = tuple

HALF = Fraction(1, 2)


def _mid(a: Point, b: Point) -> Point:
    return tuple(HALF * (x + y) for x, y in zip(a, b))


def lane_riesenfeld(points: Sequence[Point], degree: int, rounds: int, closed: bool = True) -> list[Point]:
    """Refine a uniform B-spline control polygon of the given degree.

    Precondition: degree >= 0 and rounds >= 0. For a closed polygon of m
    points the result has m * 2^rounds points, and after one round point j
    is the refined control point whose first knot is (j + degree) / 2. For
    an open polyline each round maps n points to 2n - degree points.
    Cost: O(degree * m * 2^rounds * dim) operations.
    """
    if degree < 0 or rounds < 0:
        raise ValueError("degree and rounds must be at least 0")
    p = [tuple(q) for q in points]
    for _ in range(rounds):  # @line L1
        if not p:
            return p
        q = [p[j // 2] for j in range(2 * len(p))]  # @line L2
        for _ in range(degree):  # @line L3
            m = len(q)  # @line L4
            if closed:  # @line L4
                q = [_mid(q[j], q[(j + 1) % m]) for j in range(m)]  # @line L4
            else:  # @line L4
                q = [_mid(q[j], q[j + 1]) for j in range(m - 1)]  # @line L4
        p = q  # @line L5
    return p  # @line L6


def refine_by_mask(points: Sequence[Point], degree: int) -> list[Point]:
    """One closed round by the direct formula, for comparison.

    Point j is 2^(-degree) times the sum over i of C(degree + 1, 2i - j + 1)
    times P_i, with indices modulo m. Cost: O(degree * m * dim).
    """
    m = len(points)
    out = []
    for j in range(2 * m):
        acc = [Fraction(0)] * len(points[0])
        for i in range(j // 2 - degree - 1, j // 2 + degree + 2):
            c = 2 * i - j + 1
            if 0 <= c <= degree + 1:
                w = Fraction(comb(degree + 1, c), 2**degree)
                acc = [a + w * x for a, x in zip(acc, points[i % m])]
        out.append(tuple(acc))
    return out
