# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pencil-cut-machining/. The authors are listed in prov/K6TS7H.jsonl.

"""Pencil-cut tracing: the path of a ball end mill that touches two surfaces at once.

Each surface is given by a function g(x) = (signed distance of x from the
surface, positive on the free side) - r and its gradient. A ball of radius r
with center x touches surface i exactly when g_i(x) = 0, so the pencil curve
of ball centers is the intersection of the two offset surfaces g_1 = 0 and
g_2 = 0. It is traced by a predictor along the tangent grad g_1 x grad g_2
and a Newton corrector that moves to the nearest point with g_1 = g_2 = 0
(the minimum norm step of the 2 x 3 linear system).

The code works with floats or with Fractions. With Fractions and planes the
corrector is exact; pass normalize=False to step along the raw tangent, so
that no square root is taken.
"""

import math


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def correct(g1, dg1, g2, dg2, x, tol=1e-12, max_iter=20):
    """Newton steps to a point with g1 = g2 = 0, each the minimum norm solution
    of the linearized system."""
    for _ in range(max_iter):
        v1, v2 = g1(x), g2(x)
        if abs(v1) <= tol and abs(v2) <= tol:
            return x
        a, b = dg1(x), dg2(x)
        aa, ab, bb = dot(a, a), dot(a, b), dot(b, b)
        det = aa * bb - ab * ab
        if det == 0:
            raise ValueError("the two surfaces are tangent here; the pencil curve is not defined")
        # solve [[aa, ab], [ab, bb]] (l1, l2) = (v1, v2), then x <- x - l1 a - l2 b
        l1 = (bb * v1 - ab * v2) / det
        l2 = (aa * v2 - ab * v1) / det
        x = tuple(x[i] - l1 * a[i] - l2 * b[i] for i in range(3))
    if abs(g1(x)) <= tol and abs(g2(x)) <= tol:
        return x
    raise ValueError("the corrector did not converge")


def pencil_trace(g1, dg1, g2, dg2, x0, h, m, tol=1e-12, normalize=True):
    """Trace m steps of length h of the pencil curve of ball centers from near x0."""
    x = correct(g1, dg1, g2, dg2, x0, tol)  # @line L1
    path = [x]  # @line L2
    prev = None
    for _ in range(m):  # @line L3
        t = cross(dg1(x), dg2(x))  # @line L4
        if prev is not None and dot(t, prev) < 0:
            t = (-t[0], -t[1], -t[2])
        prev = t
        if normalize:
            n = math.sqrt(dot(t, t))
            if n == 0:
                raise ValueError("the two surfaces are tangent here; the pencil curve is not defined")
            t = (t[0] / n, t[1] / n, t[2] / n)
        y = (x[0] + h * t[0], x[1] + h * t[1], x[2] + h * t[2])  # @line L5
        x = correct(g1, dg1, g2, dg2, y, tol)  # @line L6
        path.append(x)  # @line L7
    return path  # @line L8


def contacts(x, r, dg1, dg2, unit=True):
    """The two contact points x - r n_i, with n_i the unit normals (the gradients of
    signed distances are unit vectors already when unit is True)."""
    out = []
    for dg in (dg1, dg2):
        n = dg(x)
        if not unit:
            s = math.sqrt(dot(n, n))
            n = (n[0] / s, n[1] / s, n[2] / s)
        out.append((x[0] - r * n[0], x[1] - r * n[1], x[2] - r * n[2]))
    return out


def plane(n, d, r):
    """The offset function and gradient of the plane n . x = d, with unit normal n
    pointing to the free side, for a ball of radius r."""
    def g(x):
        return dot(n, x) - d - r

    def dg(x):
        return n

    return g, dg
