# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/de-casteljau-algorithm/. The authors are listed in prov/MPYB8D.jsonl.

"""The de Casteljau algorithm for Bezier curves.

A control point is a tuple of numbers of any dimension. Use
fractions.Fraction coordinates and a Fraction parameter for exact results;
floats also work. Each level of the triangle replaces neighbouring points by
the point that divides their segment in the ratio t : (1 - t).
"""

from typing import Sequence

Point = tuple


def _lerp(p: Point, q: Point, t) -> Point:
    """Return (1 - t) p + t q, coordinate by coordinate."""
    s = 1 - t
    return tuple(s * a + t * b for a, b in zip(p, q))


def de_casteljau(points: Sequence[Point], t) -> tuple[Point, list[Point], list[Point]]:
    """Evaluate the Bezier curve of `points` at `t` and split it there.

    Return (B(t), left, right). `left` holds the control points of the part
    of the curve for parameters 0 to t, and `right` those of the part for t
    to 1, both reparametrized to [0, 1]. The degree is len(points) - 1.
    """
    n = len(points) - 1
    if n < 0:
        raise ValueError("a Bezier curve needs at least one control point")
    b = [tuple(p) for p in points]  # @line L1
    left = [b[0]] + [None] * n  # @line L2
    right = [None] * n + [b[n]]  # @line L2
    for r in range(1, n + 1):  # @line L3
        for i in range(n - r + 1):  # @line L4
            b[i] = _lerp(b[i], b[i + 1], t)  # @line L5
        left[r] = b[0]  # @line L6
        right[n - r] = b[n - r]  # @line L6
    return b[0], left, right  # @line L7


def evaluate(points: Sequence[Point], t) -> Point:
    """Return the point B(t) of the Bezier curve with these control points."""
    return de_casteljau(points, t)[0]


def subdivide(points: Sequence[Point], t) -> tuple[list[Point], list[Point]]:
    """Return the control polygons of the two parts of the curve split at t."""
    _, left, right = de_casteljau(points, t)
    return left, right


def evaluate_with_derivative(points: Sequence[Point], t) -> tuple[Point, Point]:
    """Return (B(t), B'(t)).

    The derivative is n times the difference of the two points of level
    n - 1 of the triangle.
    """
    n = len(points) - 1
    if n == 0:
        return tuple(points[0]), tuple(0 * a for a in points[0])
    b = [tuple(p) for p in points]
    for r in range(1, n):
        for i in range(n - r + 1):
            b[i] = _lerp(b[i], b[i + 1], t)
    deriv = tuple(n * (q - p) for p, q in zip(b[0], b[1]))
    return _lerp(b[0], b[1], t), deriv


def rational_de_casteljau(points: Sequence[Point], weights: Sequence, t) -> Point:
    """Evaluate a rational Bezier curve by de Casteljau in homogeneous form.

    Each control point P_i with weight w_i becomes (w_i P_i, w_i). The
    algorithm runs on these points, and the result is divided by its last
    coordinate. The weights should be positive.
    """
    if len(points) != len(weights):
        raise ValueError("one weight is needed for each control point")
    homog = [tuple(w * a for a in p) + (w,) for p, w in zip(points, weights)]
    h = evaluate(homog, t)
    w = h[-1]
    if w == 0:
        raise ZeroDivisionError("the weight sum is zero at this parameter")
    return tuple(a / w for a in h[:-1])
