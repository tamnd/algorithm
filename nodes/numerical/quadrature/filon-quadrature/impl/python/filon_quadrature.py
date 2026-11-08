# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/filon-quadrature/. The authors are listed in prov/1BJZ9V.jsonl.

"""Filon-Simpson quadrature for the integrals of f(x) cos(w x) and f(x) sin(w x) over [a, b].

The interval is cut into m (even) panels of width h = (b - a) / m. On each pair of
panels f is replaced by its quadratic interpolant, and the product of that quadratic
with cos(w x) and sin(w x) is integrated exactly. With theta = w h this gives

    integral f cos(w x) ~ h [alpha (f_m sin(w b) - f_0 sin(w a)) + beta C_even + gamma C_odd],
    integral f sin(w x) ~ h [-alpha (f_m cos(w b) - f_0 cos(w a)) + beta S_even + gamma S_odd],

with the classical coefficients alpha, beta, gamma of theta. The closed forms lose
digits to cancellation for small theta, so there they are replaced by Taylor series
whose coefficients are computed exactly with Fractions. At w = 0 the rule is the
composite Simpson rule; for any w it is exact when f is a quadratic.
"""

import math
from fractions import Fraction
from functools import lru_cache
from typing import Callable, Dict, List, Tuple

SERIES_LIMIT = 1.0  # use the series for |theta| <= 1
TERMS = 16  # powers up to theta^31; at |theta| <= 1 the first omitted terms are below 1e-28


def _trig_series(c: int, kind: str, deg: int) -> Dict[int, Fraction]:
    """Taylor coefficients of sin(c t) or cos(c t) up to degree deg."""
    out = {}
    for k in range(deg + 1):
        if (kind == "sin") == (k % 2 == 1):
            sign = -1 if (k // 2) % 2 else 1
            out[k] = Fraction(sign * c ** k, math.factorial(k))
    return out


@lru_cache(maxsize=None)
def series_coefficients() -> Tuple[List[Fraction], List[Fraction], List[Fraction]]:
    """Exact Taylor coefficients of alpha, beta, gamma in powers of theta (index = power)."""
    deg = 2 * TERMS + 4
    s2, c2 = _trig_series(2, "sin", deg), _trig_series(2, "cos", deg)
    s1, c1 = _trig_series(1, "sin", deg), _trig_series(1, "cos", deg)
    # numerators as polynomials in theta, using sin cos = sin(2t)/2, sin^2 = (1 - cos 2t)/2, cos^2 = (1 + cos 2t)/2
    na: Dict[int, Fraction] = {2: Fraction(1)}
    for k, v in s2.items():  # + theta sin(2t)/2
        na[k + 1] = na.get(k + 1, Fraction(0)) + v / 2
    for k, v in c2.items():  # - 2 sin^2 = -1 + cos 2t
        na[k] = na.get(k, Fraction(0)) + v
    na[0] = na.get(0, Fraction(0)) - 1
    nb: Dict[int, Fraction] = {}
    for k, v in c2.items():  # theta (1 + cos^2) = theta (3/2 + cos(2t)/2)
        nb[k + 1] = nb.get(k + 1, Fraction(0)) + v / 2
    nb[1] = nb.get(1, Fraction(0)) + Fraction(3, 2)
    for k, v in s2.items():  # - 2 sin cos = - sin 2t
        nb[k] = nb.get(k, Fraction(0)) - v
    ng: Dict[int, Fraction] = dict(s1)  # sin t - t cos t
    for k, v in c1.items():
        ng[k + 1] = ng.get(k + 1, Fraction(0)) - v

    def divide(num, scale):
        assert all(num.get(k, 0) == 0 for k in range(3)), "series must start at theta^3"
        return [scale * num.get(k + 3, Fraction(0)) for k in range(2 * TERMS)]
    return divide(na, 1), divide(nb, 2), divide(ng, 4)


def filon_coefficients(theta: float) -> Tuple[float, float, float]:
    """(alpha, beta, gamma) at theta; Taylor series for |theta| <= 1, closed forms otherwise."""
    if abs(theta) <= SERIES_LIMIT:
        ca, cb, cg = series_coefficients()
        def ev(c):
            return math.fsum(float(ck) * theta ** k for k, ck in enumerate(c) if ck)
        return ev(ca), ev(cb), ev(cg)
    s, c = math.sin(theta), math.cos(theta)
    t3 = theta ** 3
    alpha = (theta * theta + theta * s * c - 2.0 * s * s) / t3
    beta = 2.0 * (theta * (1.0 + c * c) - 2.0 * s * c) / t3
    gamma = 4.0 * (s - theta * c) / t3
    return alpha, beta, gamma


def filon(f: Callable[[float], float], a: float, b: float, omega: float, m: int = 64) -> Tuple[float, float]:
    """(integral of f cos(omega x), integral of f sin(omega x)) over [a, b] by Filon-Simpson.

    m is the even number of panels; m + 1 evaluations of f. Both integrals share the values.
    """
    # @line L1
    if m < 2 or m % 2:
        raise ValueError("need an even m >= 2")
    if a == b:
        return 0.0, 0.0
    # @line L2
    fx = [f(x) for x in _nodes(a, b, m)]  # h = (b - a) / m
    return _combine(fx, a, b, omega)


def _nodes(a: float, b: float, m: int) -> List[float]:
    h = (b - a) / m
    return [a + i * h for i in range(m)] + [b]


def _combine(fx: List[float], a: float, b: float, omega: float) -> Tuple[float, float]:
    """The Filon-Simpson sums for the values fx at the m + 1 equispaced nodes of [a, b]."""
    m = len(fx) - 1
    h = (b - a) / m
    xs = _nodes(a, b, m)
    # @line L3
    alpha, beta, gamma = filon_coefficients(omega * h)
    # @line L4
    cos_v = [math.cos(omega * x) for x in xs]
    sin_v = [math.sin(omega * x) for x in xs]
    c_even = math.fsum([fx[i] * cos_v[i] for i in range(0, m + 1, 2)] + [-0.5 * fx[0] * cos_v[0], -0.5 * fx[m] * cos_v[m]])
    s_even = math.fsum([fx[i] * sin_v[i] for i in range(0, m + 1, 2)] + [-0.5 * fx[0] * sin_v[0], -0.5 * fx[m] * sin_v[m]])
    c_odd = math.fsum(fx[i] * cos_v[i] for i in range(1, m, 2))
    s_odd = math.fsum(fx[i] * sin_v[i] for i in range(1, m, 2))
    # @line L5
    ic = h * math.fsum([alpha * (fx[m] * sin_v[m] - fx[0] * sin_v[0]), beta * c_even, gamma * c_odd])
    is_ = h * math.fsum([-alpha * (fx[m] * cos_v[m] - fx[0] * cos_v[0]), beta * s_even, gamma * s_odd])
    return ic, is_


def integrate(f: Callable[[float], float], a: float, b: float, omega: float,
              tol: float = 1e-10, max_m: int = 2 ** 16) -> Tuple[float, float, float, int, str]:
    """Doubling driver: m = 2, 4, 8, ... reusing every value of f.

    Returns (cos integral, sin integral, estimate, evaluations, status). The estimate is
    |change in C| + |change in S| between the last two m; status is "ok" when it is at most
    tol, and "limit" when m would exceed max_m. The stopping test is a heuristic.
    """
    if a == b:
        return 0.0, 0.0, 0.0, 0, "ok"
    m = 2
    fx = [f(x) for x in _nodes(a, b, m)]
    evals = m + 1
    c, s = _combine(fx, a, b, omega)
    est = float("inf")
    while 2 * m <= max_m:
        m2 = 2 * m
        xs2 = _nodes(a, b, m2)
        new = [f(xs2[i]) for i in range(1, m2, 2)]
        evals += len(new)
        fx2 = [0.0] * (m2 + 1)
        fx2[0::2] = fx
        fx2[1::2] = new
        c2, s2 = _combine(fx2, a, b, omega)
        est = abs(c2 - c) + abs(s2 - s)
        fx, m, c, s = fx2, m2, c2, s2
        if est <= tol:
            return c, s, est, evals, "ok"
    return c, s, est, evals, "limit"


def exact_monomial(k: int, a: float, b: float, omega: float) -> complex:
    """Integral of x^k e^(i omega x) over [a, b] by repeated integration by parts (omega != 0)."""
    io = 1j * omega
    total = 0j
    for x, sign in ((b, 1), (a, -1)):
        # x^k e^(iwx) sum_j (-1)^j k!/(k-j)! x^(-j) / (iw)^(j+1)
        e = complex(math.cos(omega * x), math.sin(omega * x))
        s = 0j
        for j in range(k + 1):
            s += (-1) ** j * math.factorial(k) / math.factorial(k - j) * x ** (k - j) / io ** (j + 1)
        total += sign * e * s
    return total
