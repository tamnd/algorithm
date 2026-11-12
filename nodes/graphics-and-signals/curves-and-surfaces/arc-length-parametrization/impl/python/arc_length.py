# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arc-length-parametrization/. The authors are listed in prov/ZB4VYJ.jsonl.

"""Arc length of a parametric curve and its inverse, the arc-length parameter.

The arc length s(t) = integral from a to t of |C'(x)| dx is computed by adaptive
Gauss-Legendre quadrature: an interval is accepted when the rule on the whole
interval and the sum of the rule on its two halves differ by at most the local
tolerance, and split otherwise, with the tolerance halved. This is an error
estimate, not a proven bound. The inverse t(s) is found by Newton's method on
s(t) - s = 0, whose derivative is the speed, with a bisection step whenever
Newton leaves the bracket. The curve must be regular (nonzero speed) for the
inverse to be unique; zero speed at isolated points is handled by the bracket.
"""

import bisect
import math
from typing import Callable, List, Sequence, Tuple

Vec = Tuple[float, ...]


def _legendre(n: int, x: float) -> Tuple[float, float]:
    """The values P_n(x) and P_n'(x) by the three-term recurrence (|x| < 1)."""
    p0, p1 = 1.0, x
    for k in range(2, n + 1):
        p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
    return p1, n * (x * p1 - p0) / (x * x - 1)


def legendre_rule(n: int) -> Tuple[List[float], List[float]]:
    """Nodes and weights of the n-point Gauss-Legendre rule on [-1, 1], nodes increasing."""
    nodes, weights = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p, dp = _legendre(n, x)
            dx = p / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        p, dp = _legendre(n, x)
        nodes.append(x)
        weights.append(2 / ((1 - x * x) * dp * dp))
    return nodes[::-1], weights[::-1]


_RULE = legendre_rule(5)


def gauss(f: Callable[[float], float], a: float, b: float, rule=_RULE) -> float:
    """The Gauss-Legendre approximation of the integral of f over [a, b]."""
    xs, ws = rule
    mid, half = (a + b) / 2, (b - a) / 2
    return half * sum(w * f(mid + half * x) for x, w in zip(xs, ws))


def speed_of(deriv: Callable[[float], Vec]) -> Callable[[float], float]:
    """The speed |C'(t)| from the derivative of the curve."""
    return lambda t: math.sqrt(sum(c * c for c in deriv(t)))


def length_table(speed, a: float, b: float, tol: float = 1e-10, max_depth: int = 40):
    """Breakpoints t_0 = a < ... < t_K = b and cumulative lengths s_k = s(t_k).

    The pieces are the halves of the intervals that the adaptive rule accepts.
    """
    ts, ss = [a], [0.0]

    def walk(lo, hi, whole, eps, depth):
        mid = (lo + hi) / 2
        left = gauss(speed, lo, mid)
        right = gauss(speed, mid, hi)
        if abs(left + right - whole) <= eps or depth >= max_depth:
            ts.append(mid)
            ss.append(ss[-1] + left)
            ts.append(hi)
            ss.append(ss[-1] + right)
            return
        walk(lo, mid, left, eps / 2, depth + 1)
        walk(mid, hi, right, eps / 2, depth + 1)

    walk(a, b, gauss(speed, a, b), tol, 0)
    return ts, ss


def arc_length(speed, a: float, b: float, tol: float = 1e-10) -> float:
    """The length of the curve between the parameters a and b."""
    return length_table(speed, a, b, tol)[1][-1]


def param_at_length(speed, ts: Sequence[float], ss: Sequence[float], s: float,
                    tol: float = 1e-13) -> float:
    """The parameter t with s(t) = s, using a table from length_table."""
    if s <= 0:
        return ts[0]
    if s >= ss[-1]:
        return ts[-1]
    k = bisect.bisect_right(ss, s) - 1
    lo, hi, s_lo = ts[k], ts[k + 1], ss[k]
    t = lo + (hi - lo) * (s - s_lo) / (ss[k + 1] - s_lo)
    for _ in range(100):
        st = s_lo + gauss(speed, lo, t)  # s(t), from the known value at lo
        g = st - s
        if g == 0:
            return t
        if g > 0:
            hi = t
        else:
            lo, s_lo = t, st
        v = speed(t)
        nt = t - g / v if v > 0 else lo
        if not lo < nt < hi:
            nt = (lo + hi) / 2  # the bisection safeguard
        if abs(nt - t) <= tol * max(1.0, abs(t)):
            return nt
        t = nt
    return t


def uniform_samples(curve, deriv, a: float, b: float, count: int, tol: float = 1e-10):
    """Parameters and points that split the curve into count pieces of equal arc length."""
    speed = speed_of(deriv)
    ts, ss = length_table(speed, a, b, tol)
    total = ss[-1]
    params = [param_at_length(speed, ts, ss, total * k / count) for k in range(count + 1)]
    return params, [curve(t) for t in params]
