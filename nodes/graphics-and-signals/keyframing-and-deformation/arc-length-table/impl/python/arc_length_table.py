# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arc-length-table/. The authors are listed in prov/JYYH1E.jsonl.
"""Arc length table of a parametric curve, and its inverse.

The table stores the parameters u_k = a + k h, h = (b - a) / m, and the arc
lengths s_k from u_0 to u_k, computed by adaptive five-point Gauss-Legendre
quadrature of the speed |c'(u)|. A query takes a distance s* in [0, s_m],
finds the interval by binary search, interpolates linearly, and can refine
the result by Newton steps on s(u) - s*.
"""

import bisect
import math

# Five-point Gauss-Legendre nodes and weights on [-1, 1].
_GL_X = (
    0.0,
    -0.5384693101056831,
    0.5384693101056831,
    -0.9061798459386640,
    0.9061798459386640,
)
_GL_W = (
    0.5688888888888889,
    0.4786286704993665,
    0.4786286704993665,
    0.2369268850561891,
    0.2369268850561891,
)


def gauss5(f, x, y):
    """Return the five-point Gauss-Legendre estimate of the integral of f on [x, y]."""
    c = (x + y) / 2.0
    r = (y - x) / 2.0
    return r * sum(w * f(c + r * t) for t, w in zip(_GL_X, _GL_W))


def adaptive_gauss(f, x, y, eps, whole=None, depth=0):
    """Return the integral of f on [x, y] to about the absolute error eps."""
    if whole is None:
        whole = gauss5(f, x, y)  # @line L5
    mid = (x + y) / 2.0
    left = gauss5(f, x, mid)  # @line L6
    right = gauss5(f, mid, y)
    if abs(left + right - whole) <= eps or depth >= 40:  # @line L7
        return left + right
    return adaptive_gauss(f, x, mid, eps / 2.0, left, depth + 1) + adaptive_gauss(  # @line L8
        f, mid, y, eps / 2.0, right, depth + 1
    )


def speed_of(dcurve):
    """Return the function u -> |c'(u)| for a derivative function dcurve."""
    return lambda u: math.sqrt(sum(x * x for x in dcurve(u)))


class ArcLengthTable:
    """Arc length table of a curve given by its derivative c'(u) on [a, b]."""

    def __init__(self, dcurve, a, b, m, eps=1e-12):
        if m < 1 or not b > a:
            raise ValueError("need m >= 1 and b > a")
        self.speed = speed_of(dcurve)
        self.a, self.b, self.m = a, b, m
        self.h = (b - a) / m  # @line L1
        self.u = [a]
        self.s = [0.0]
        for k in range(1, m + 1):  # @line L2
            uk = a + k * self.h  # @line L3
            self.s.append(self.s[-1] + adaptive_gauss(self.speed, self.u[-1], uk, eps / m))  # @line L4
            self.u.append(uk)

    def length(self):
        """Return the total arc length s_m."""
        return self.s[-1]

    def arc_length(self, u):
        """Return s(u), from the table and one Gauss-Legendre rule on the last part."""
        k = min(max(int((u - self.a) / self.h), 0), self.m - 1)
        return self.s[k] + gauss5(self.speed, self.u[k], u)

    def param(self, s_star, newton=0):
        """Return the parameter u with s(u) = s_star, with optional Newton steps."""
        s_star = min(max(s_star, 0.0), self.s[-1])
        k = bisect.bisect_right(self.s, s_star) - 1  # @line L9
        k = min(max(k, 0), self.m - 1)
        ds = self.s[k + 1] - self.s[k]
        u = self.u[k] + (self.h * (s_star - self.s[k]) / ds if ds > 0.0 else 0.0)  # @line L10
        for _ in range(newton):
            v = self.speed(u)
            if v == 0.0:
                break
            u = u - (self.s[k] + gauss5(self.speed, self.u[k], u) - s_star) / v  # @line L11
            u = min(max(u, self.u[k]), self.u[k + 1])
        return u  # @line L12
