# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ruled-surface/. The authors are listed in prov/TB1NXX.jsonl.

"""Ruled surfaces S(u, v) = (1 - v) a(u) + v b(u).

The directrix form is S(u, v) = a(u) + v w(u) with the ruling direction
w = b - a. Curves are functions of u that return tuples of numbers; their
derivatives are given as functions too. Every formula below uses only +, -, *
and /, so it is exact on Fraction input, except the square roots of the
Gaussian curvature, which are not needed.
"""

from typing import Callable, Tuple

Point = Tuple
Curve = Callable[[object], Point]


def sub(p: Point, q: Point) -> Point:
    return tuple(x - y for x, y in zip(p, q))


def dot(p: Point, q: Point):
    return sum(x * y for x, y in zip(p, q))


def cross(p: Point, q: Point) -> Point:
    return (p[1] * q[2] - p[2] * q[1], p[2] * q[0] - p[0] * q[2], p[0] * q[1] - p[1] * q[0])


def det3(p: Point, q: Point, r: Point):
    return dot(p, cross(q, r))


def ruled_point(a: Curve, b: Curve, u, v) -> Point:
    """The point at parameter v on the ruling segment from a(u) to b(u)."""
    pa, pb = a(u), b(u)
    return tuple((1 - v) * x + v * y for x, y in zip(pa, pb))


def ruled_partials(a: Curve, da: Curve, b: Curve, db: Curve, u, v) -> Tuple[Point, Point]:
    """S_u = (1 - v) a' + v b' and S_v = b - a."""
    su = tuple((1 - v) * x + v * y for x, y in zip(da(u), db(u)))
    return su, sub(b(u), a(u))


def developability_value(a: Curve, da: Curve, b: Curve, db: Curve, u):
    """The triple product det(a', w, w') with w = b - a.

    It is 0 at u exactly when the tangent plane is the same at every point of
    the ruling at u. A ruled surface is developable when it is 0 for every u.
    """
    w = sub(b(u), a(u))
    dw = sub(db(u), da(u))
    return det3(da(u), w, dw)


def gaussian_curvature(a: Curve, da: Curve, b: Curve, db: Curve, u, v):
    """K = -det(a', w, w')^2 / |S_u x S_v|^4 at a regular point. It is never positive."""
    su, sv = ruled_partials(a, da, b, db, u, v)  # @line L1 L2
    nn = cross(su, sv)  # @line L3
    w2 = dot(nn, nn)
    if w2 == 0:  # @line L4
        raise ValueError("the surface is singular at this point")
    d = developability_value(a, da, b, db, u)  # @line L5
    return -d * d / (w2 * w2)  # @line L6
