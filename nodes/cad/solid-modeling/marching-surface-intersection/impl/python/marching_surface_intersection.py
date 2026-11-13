# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/marching-surface-intersection/. The authors are listed in prov/ZVWZT1.jsonl.

"""Marching along the intersection curve of two implicit surfaces, in floating point.

A surface is the zero set of a quadric q(x) = x . A x + b . x + c, with the
gradient 2 A x + b. Planes, spheres and circular cylinders are quadrics. The
method traces one branch of the curve f = g = 0 from a start point: each step
predicts along the unit tangent, the cross product of the two gradients, and
corrects back onto both surfaces with Newton steps of least length. The step
is halved when Newton fails or the tangent turns too much. The trace stops
when the branch closes, when it leaves the box, or after max_steps steps.

Tolerances: a returned point p has |f(p)| and |g(p)| at most TOL, after the
gradients have been scaled as they are given.
"""

import math

Vec = tuple
TOL = 1e-11


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


class Quadric:
    """The surface x . A x + b . x + c = 0, with A symmetric 3 by 3."""

    def __init__(self, A, b: Vec, c: float):
        self.A = [list(map(float, row)) for row in A]
        self.b = tuple(map(float, b))
        self.c = float(c)

    def _Ax(self, x: Vec) -> Vec:
        return tuple(sum(self.A[i][j] * x[j] for j in range(3)) for i in range(3))

    def value(self, x: Vec) -> float:
        return dot(x, self._Ax(x)) + dot(self.b, x) + self.c

    def grad(self, x: Vec) -> Vec:
        return add(scale(2.0, self._Ax(x)), self.b)


def sphere(center: Vec, R: float) -> Quadric:
    I3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    return Quadric(I3, scale(-2.0, center), dot(center, center) - R * R)


def cylinder(point: Vec, axis: Vec, R: float) -> Quadric:
    u = scale(1.0 / norm(axis), axis)
    A = [[(1.0 if i == j else 0.0) - u[i] * u[j] for j in range(3)] for i in range(3)]
    Aa = tuple(sum(A[i][j] * point[j] for j in range(3)) for i in range(3))
    return Quadric(A, scale(-2.0, Aa), dot(point, Aa) - R * R)


def plane(n: Vec, d: float) -> Quadric:
    return Quadric([[0, 0, 0], [0, 0, 0], [0, 0, 0]], n, -d)


def correct(f, g, x: Vec, iters: int = 30):
    """Newton steps of least length onto f = g = 0; None when they fail."""
    for _ in range(iters):
        F1, F2 = f.value(x), g.value(x)
        if abs(F1) <= TOL and abs(F2) <= TOL:
            return x
        a, b = f.grad(x), g.grad(x)
        aa, ab, bb = dot(a, a), dot(a, b), dot(b, b)
        det = aa * bb - ab * ab
        if det <= 1e-24 * aa * bb:
            return None
        l1 = (bb * F1 - ab * F2) / det
        l2 = (aa * F2 - ab * F1) / det
        x = sub(x, add(scale(l1, a), scale(l2, b)))
        if not all(math.isfinite(v) for v in x):
            return None
    return None


def unit_tangent(f, g, p: Vec):
    t = cross(f.grad(p), g.grad(p))
    n = norm(t)
    if n == 0.0:
        return None
    return scale(1.0 / n, t)


def inside(box, p: Vec) -> bool:
    lo, hi = box
    return all(lo[i] <= p[i] <= hi[i] for i in range(3))


def march(f, g, x0: Vec, h: float, box, max_steps: int = 10000, max_turn: float = 0.2, h_min: float = 1e-7):
    """Trace one branch through the point near x0. Return (points, closed)."""
    p0 = correct(f, g, x0)  # @line L1
    if p0 is None:
        raise ValueError("the start point does not converge onto the curve")
    t0 = unit_tangent(f, g, p0)
    if t0 is None:
        raise ValueError("the start point is a singular point of the curve")
    ends = {+1: [], -1: []}  # @line L2
    for d in (+1, -1):  # @line L3
        p, t_prev, step, left = p0, scale(d, t0), h, False  # @line L4
        for _ in range(max_steps):
            t = unit_tangent(f, g, p)  # @line L5
            if t is None:
                break
            if dot(t, t_prev) < 0:
                t = scale(-1.0, t)
            q = correct(f, g, add(p, scale(step, t)))  # @line L6
            tq = None if q is None else unit_tangent(f, g, q)
            if q is None or tq is None or abs(dot(tq, t)) < math.cos(max_turn) or norm(sub(q, p)) > 2 * step:
                step /= 2  # @line L7
                if step < h_min:
                    break
                continue
            if not inside(box, q):  # @line L8
                break
            gap = norm(sub(q, p0))
            left = left or gap > 2 * h
            if left and gap <= h:  # @line L9
                return [p0] + ends[+1], True
            ends[d].append(q)  # @line L10
            p, t_prev = q, t  # @line L11
            step = min(h, 1.5 * step)
    return list(reversed(ends[-1])) + [p0] + ends[+1], False  # @line L12
