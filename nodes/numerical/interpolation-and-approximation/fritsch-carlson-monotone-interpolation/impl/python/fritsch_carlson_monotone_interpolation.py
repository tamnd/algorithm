# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fritsch-carlson-monotone-interpolation/. The authors are listed in prov/YBFHVG.jsonl.
"""Fritsch-Carlson monotone piecewise cubic Hermite interpolation."""
import bisect
import math


def _end_slope(h0, h1, d0, d1):
    """One-sided three-point slope at an end, made shape preserving (as in Moler's pchip)."""
    s = ((2 * h0 + h1) * d0 - h0 * d1) / (h0 + h1)
    if s * d0 <= 0:
        return 0.0
    if d0 * d1 < 0 and abs(s) > 3 * abs(d0):
        return 3 * d0
    return s


def monotone_slopes(x, y):
    """Slopes d[k] at the sorted, distinct nodes x for the Fritsch-Carlson interpolant."""
    n = len(x) - 1
    if n == 0:
        return [0.0]
    h = [x[k + 1] - x[k] for k in range(n)]  # @line L1
    delta = [(y[k + 1] - y[k]) / h[k] for k in range(n)]
    if n == 1:  # @line L2
        return [delta[0], delta[0]]
    d = [0.0] * (n + 1)
    for k in range(1, n):
        if delta[k - 1] * delta[k] > 0:
            # three-point (parabola) slope, a convex combination of the two secants
            d[k] = (h[k] * delta[k - 1] + h[k - 1] * delta[k]) / (h[k - 1] + h[k])
    d[0] = _end_slope(h[0], h[1], delta[0], delta[1])
    d[n] = _end_slope(h[n - 1], h[n - 2], delta[n - 1], delta[n - 2])
    for k in range(n):  # @line L3
        if delta[k] == 0:
            d[k] = d[k + 1] = 0.0
            continue
        r = math.hypot(d[k], d[k + 1])  # @line L4
        if r > 3 * abs(delta[k]):
            tau = 3 * abs(delta[k]) / r
            d[k] *= tau
            d[k + 1] *= tau
    return d


def _prepare(xs, ys):
    if len(xs) != len(ys) or not xs:
        raise ValueError("need equal, nonzero numbers of abscissas and values")
    pairs = sorted(zip(xs, ys))
    x = [float(p[0]) for p in pairs]
    y = [float(p[1]) for p in pairs]
    for k in range(len(x) - 1):
        if x[k] == x[k + 1]:
            raise ValueError("repeated abscissa")
    return x, y


class MonotoneCubic:
    """s(t) for data (xs, ys); nodes may be given in any order but must be distinct."""

    def __init__(self, xs, ys):
        self.x, self.y = _prepare(xs, ys)
        self.d = monotone_slopes(self.x, self.y)

    def __call__(self, t):
        x, y, d = self.x, self.y, self.d
        n = len(x) - 1
        if n == 0:
            return y[0]
        k = bisect.bisect_right(x, t) - 1  # @line L5
        k = min(max(k, 0), n - 1)
        h = x[k + 1] - x[k]
        u = (t - x[k]) / h
        if u == 0.0:
            return y[k]
        if u == 1.0:
            return y[k + 1]
        v = 1.0 - u
        # cubic Hermite form: y_k v^2(1+2u) + y_{k+1} u^2(1+2v) + h d_k u v^2 - h d_{k+1} u^2 v
        return (y[k] * v * v * (1 + 2 * u) + y[k + 1] * u * u * (1 + 2 * v)  # @line L6
                + h * (d[k] * u * v * v - d[k + 1] * u * u * v))
