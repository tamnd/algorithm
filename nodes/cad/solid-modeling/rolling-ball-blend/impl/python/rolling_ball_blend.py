# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rolling-ball-blend/. The authors are listed in prov/DRVDD3.jsonl.

"""Constant-radius rolling-ball blend of two surfaces, in floating point.

Each surface is given by a signed distance function sd(x), which is exact
near the surface, and its gradient, the unit normal. Planes and circular
cylinders are provided. The side of the ball is chosen by a sign s = +1 or
-1 for each surface: the ball center c satisfies sd_i(c) = s_i r.

The method follows the page: the spine (the path of the ball center) is
the intersection of the two offset surfaces sd_i = s_i r, traced by steps
along the cross product of the normals with a Newton correction. At each
spine point the contact points are the feet of the center on the two
surfaces, and the cross section is the shorter circular arc between them
around the center.
"""

import math

Vec = tuple


def add(a: Vec, b: Vec) -> Vec:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a: Vec, b: Vec) -> Vec:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def scale(t: float, a: Vec) -> Vec:
    return (t * a[0], t * a[1], t * a[2])


def dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Vec, b: Vec) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def norm(a: Vec) -> float:
    return math.sqrt(dot(a, a))


def unit(a: Vec) -> Vec:
    return scale(1.0 / norm(a), a)


class Plane:
    """The plane n . x = d with the positive side along the normal n."""

    def __init__(self, n: Vec, d: float):
        length = norm(n)
        self.n = scale(1.0 / length, n)
        self.d = d / length

    def sd(self, x: Vec) -> float:
        return dot(self.n, x) - self.d

    def normal(self, x: Vec) -> Vec:
        return self.n


class Cylinder:
    """The circular cylinder of radius R around the line a + t u, positive outside."""

    def __init__(self, a: Vec, u: Vec, R: float):
        self.a = a
        self.u = unit(u)
        self.R = R

    def radial(self, x: Vec) -> Vec:
        w = sub(x, self.a)
        return sub(w, scale(dot(w, self.u), self.u))

    def sd(self, x: Vec) -> float:
        return norm(self.radial(x)) - self.R

    def normal(self, x: Vec) -> Vec:
        return unit(self.radial(x))


def foot(surface, x: Vec) -> Vec:
    """The nearest point of the surface to x, valid where sd is a true distance."""
    return sub(x, scale(surface.sd(x), surface.normal(x)))


def correct(s1, s2, r: float, sides: tuple, x: Vec, tol: float = 1e-13, iters: int = 40) -> Vec:
    """Newton iteration with the minimum-norm step onto sd1 = s1 r and sd2 = s2 r."""
    for _ in range(iters):
        f1 = s1.sd(x) - sides[0] * r
        f2 = s2.sd(x) - sides[1] * r
        if abs(f1) <= tol and abs(f2) <= tol:
            return x
        g1, g2 = s1.normal(x), s2.normal(x)
        a, b, c = dot(g1, g1), dot(g1, g2), dot(g2, g2)
        det = a * c - b * b
        if det < 1e-14:
            raise ValueError("the normals are parallel, the spine is not regular here")
        l1 = (c * f1 - b * f2) / det
        l2 = (a * f2 - b * f1) / det
        x = sub(x, add(scale(l1, g1), scale(l2, g2)))
    raise ValueError("Newton correction did not converge")


def tangent(s1, s2, c: Vec, prev):
    """The unit vector along n1 x n2 at c, with the sign of the previous tangent."""
    t = cross(s1.normal(c), s2.normal(c))
    if norm(t) < 1e-7:
        raise ValueError("the normals are parallel, the spine has no tangent here")
    t = unit(t)
    if prev is not None and dot(t, prev) < 0:
        t = scale(-1.0, t)
    return t


def shorter_arc(c: Vec, p1: Vec, p2: Vec, r: float, k: int) -> list:
    """k + 1 points of the shorter great circle arc from p1 to p2 around c."""
    a = scale(1.0 / r, sub(p1, c))
    b = scale(1.0 / r, sub(p2, c))
    theta = math.acos(max(-1.0, min(1.0, dot(a, b))))
    arc = []
    for j in range(k + 1):
        lam = j / k
        if theta < 1e-12:
            w = a
        else:
            w = add(scale(math.sin((1 - lam) * theta), a), scale(math.sin(lam * theta), b))
            w = scale(1.0 / math.sin(theta), w)
        arc.append(add(c, scale(r, w)))
    return arc


def rolling_ball_blend(s1, s2, r: float, sides: tuple, start: Vec, h: float, max_steps: int, k: int = 8):
    """Return (spine, sections, closed); each section is (p1, p2, arc points)."""
    c = correct(s1, s2, r, sides, start)  # @line L1
    spine = [c]  # @line L2
    prev, left, closed = None, False, False
    for _ in range(max_steps):  # @line L3
        t = tangent(s1, s2, c, prev)  # @line L4
        c = correct(s1, s2, r, sides, add(c, scale(h, t)))  # @line L5
        gap = norm(sub(c, spine[0]))
        left = left or gap > 2 * h
        if left and gap <= 1.5 * h:  # @line L7
            closed = True
            break
        spine.append(c)  # @line L6
        prev = t
    sections = []
    for c in spine:  # @line L8
        p1 = sub(c, scale(sides[0] * r, s1.normal(c)))  # @line L9
        p2 = sub(c, scale(sides[1] * r, s2.normal(c)))
        arc = shorter_arc(c, p1, p2, r, k)  # @line L10
        sections.append((p1, p2, arc))  # @line L11
    return spine, sections, closed  # @line L12
