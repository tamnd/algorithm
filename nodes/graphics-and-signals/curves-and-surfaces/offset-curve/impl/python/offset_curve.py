# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/offset-curve/. The authors are listed in prov/CF6X62.jsonl.

"""Offset of a plane parametric curve: C_d(t) = C(t) + d N(t).

N is the unit normal obtained by turning the unit tangent by +90 degrees, so
d > 0 offsets to the left of the direction of travel. With the signed
curvature k = (x'y'' - y'x'') / |C'|^3 the offset satisfies

    C_d'(t) = (1 - d k(t)) C'(t),   k_d = k / |1 - d k|,

so the offset is regular except where d k = 1, that is, where d equals the
signed radius of curvature; there it has a cusp, and where d k > 1 it runs
backwards. A polynomial curve has a rational offset in its own parameter
exactly when its speed is a polynomial (a Pythagorean-hodograph curve).
"""

import math
from typing import Callable, List, Sequence, Tuple

Vec = Tuple


def unit_normal(d1: Vec) -> Vec:
    s = math.hypot(d1[0], d1[1])
    return (-d1[1] / s, d1[0] / s)


def signed_curvature(d1: Vec, d2: Vec) -> float:
    return (d1[0] * d2[1] - d1[1] * d2[0]) / math.hypot(d1[0], d1[1]) ** 3


def offset_point(p: Vec, d1: Vec, d: float) -> Vec:
    n = unit_normal(d1)
    return (p[0] + d * n[0], p[1] + d * n[1])


def offset_derivative(d1: Vec, d2: Vec, d: float) -> Vec:
    """C_d'(t) = (1 - d k) C'(t)."""
    f = 1 - d * signed_curvature(d1, d2)
    return (f * d1[0], f * d1[1])


def offset_curvature(k: float, d: float) -> float:
    """The signed curvature of the offset, in its own direction of travel, where d k != 1.

    It is k / (1 - d k) where the offset runs forwards (d k < 1). Where it runs
    backwards (d k > 1) its tangent and normal are reversed, which gives k / (d k - 1).
    """
    return k / abs(1 - d * k)


def cusp_parameters(d1: Callable, d2: Callable, d: float, a: float, b: float,
                    samples: int = 1000, tol: float = 1e-14) -> List[float]:
    """Parameters in [a, b] where d k(t) = 1, found by sign changes of
    g(t) = d (x'y'' - y'x'') - |C'|^3 on a grid and bisection."""

    def g(t):
        p, q = d1(t), d2(t)
        return d * (p[0] * q[1] - p[1] * q[0]) - math.hypot(p[0], p[1]) ** 3

    roots = []
    xs = [a + (b - a) * i / samples for i in range(samples + 1)]
    gs = [g(x) for x in xs]
    for i in range(samples):
        lo, hi, glo = xs[i], xs[i + 1], gs[i]
        if glo == 0:
            roots.append(lo)
            continue
        if glo * gs[i + 1] < 0:
            while hi - lo > tol * max(1.0, abs(lo)):
                mid = (lo + hi) / 2
                gm = g(mid)
                if (gm < 0) == (glo < 0):
                    lo, glo = mid, gm
                else:
                    hi = mid
            roots.append((lo + hi) / 2)
    if gs[-1] == 0:
        roots.append(b)
    return roots


# Pythagorean-hodograph curves: polynomials as coefficient lists, lowest degree first.

def _mul(p, q):
    out = [p[0] - p[0]] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return out


def _add(p, q, sign=1):
    n = max(len(p), len(q))
    p = list(p) + [0] * (n - len(p))
    q = list(q) + [0] * (n - len(q))
    return [x + sign * y for x, y in zip(p, q)]


def _integrate(p, c0):
    return [c0] + [x / (i + 1) for i, x in enumerate(p)]


def _eval(p, t):
    acc = 0
    for c in reversed(p):
        acc = acc * t + c
    return acc


def ph_curve(u: Sequence, v: Sequence, start: Vec):
    """The PH curve with hodograph x' = u^2 - v^2, y' = 2 u v and speed sigma = u^2 + v^2.

    Returns the coefficient lists (x, y, sigma). Exact for Fraction input.
    """
    uu, vv, uv = _mul(u, u), _mul(v, v), _mul(u, v)
    dx = _add(uu, vv, -1)
    dy = [2 * c for c in uv]
    sigma = _add(uu, vv)
    return _integrate(dx, start[0]), _integrate(dy, start[1]), sigma, dx, dy


def ph_offset_point(curve, t, d):
    """The exact offset point C(t) + d N(t) of a PH curve: rational, no square root."""
    x, y, sigma, dx, dy = curve
    s = _eval(sigma, t)
    return (_eval(x, t) - d * _eval(dy, t) / s, _eval(y, t) + d * _eval(dx, t) / s)
