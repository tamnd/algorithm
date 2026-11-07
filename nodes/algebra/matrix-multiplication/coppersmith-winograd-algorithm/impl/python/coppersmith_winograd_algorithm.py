# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coppersmith-winograd-algorithm/. The authors are listed in prov/YF5DJV.jsonl.

"""The basic construction of Coppersmith and Winograd.

The Coppersmith-Winograd tensor for q >= 0 lives in R^(q+2) (x) R^(q+2) (x) R^(q+2):

    T_q = sum_{i=1..q} (x0 yi zi + xi y0 zi + xi yi z0) + x0 y0 z_{q+1} + x0 y_{q+1} z0 + x_{q+1} y0 z0.

As a bilinear map phi(x, y) with output index k (the index of z):

    phi_0 = sum_i xi yi + x0 y_{q+1} + x_{q+1} y0,  phi_i = x0 yi + xi y0,  phi_{q+1} = x0 y0.

The main function computes phi with q + 2 products of polynomials in a
central indeterminate eps, the approximate algorithm of border rank q + 2
and error degree 3, and reads off the coefficient of eps^3. This is the
small tensor at the start of the laser method; the matrix multiplication
algorithm built from it is galactic and is not implemented here.
"""

import math
from fractions import Fraction
from typing import Optional

Poly = list[int]  # coefficients of 1, eps, eps^2, ...


def _add(a: Poly, b: Poly) -> Poly:
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]


def _scale(c: int, a: Poly) -> Poly:
    return [c * v for v in a]


def _shift(k: int, a: Poly) -> Poly:
    return [0] * k + a


def _mul(a: Poly, b: Poly) -> Poly:
    out = [0] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        if u:
            for j, v in enumerate(b):
                out[i + j] += u * v
    return out


def _coef(a: Poly, k: int) -> int:
    return a[k] if k < len(a) else 0


def _check(x: list[int], y: list[int], q: int) -> None:
    if q < 0:
        raise ValueError("q must be nonnegative")
    if len(x) != q + 2 or len(y) != q + 2:
        raise ValueError("x and y must have length q + 2")


def coppersmith_winograd_algorithm(
    x: list[int], y: list[int], q: int, mod: Optional[int] = None
) -> list[int]:
    """Return phi(x, y) for the CW tensor T_q, computed with q + 2 products in R[eps].

    Precondition: len(x) == len(y) == q + 2 and q >= 0. The entries may be
    in any ring; only x-times-y products are formed, so commutativity of the
    entries is not used. Cost: q + 2 products of polynomials of degree at
    most 3 in eps and O(q) additions of such polynomials.
    """
    _check(x, y, q)
    x0, y0 = x[0], y[0]
    prods: list[Poly] = [[]]  # 1-based
    for i in range(1, q + 1):  # @line L1
        prods.append(_mul([x0, x[i]], [y0, y[i]]))
    big_x = sum(x[1 : q + 1])  # @line L2
    big_y = sum(y[1 : q + 1])
    prods.append(_mul([x0, 0, big_x], [y0, 0, big_y]))  # @line L3
    prods.append(_mul([x0, 0, 0, x[q + 1]], [y0, 0, 0, y[q + 1]]))  # @line L4
    p_sum: Poly = [0]
    for i in range(1, q + 1):
        p_sum = _add(p_sum, prods[i])
    c0 = _add(_add(_shift(1, p_sum), _scale(-1, prods[q + 1])), _mul([1, -q], prods[q + 2]))  # @line L5
    cs = [c0]
    for i in range(1, q + 1):  # @line L6
        cs.append(_shift(2, _add(prods[i], _scale(-1, prods[q + 1]))))
    cs.append(_shift(3, prods[q + 2]))  # @line L7
    out = [_coef(c, 3) for c in cs]  # @line L8
    if mod is not None:
        out = [v % mod for v in out]
    return out


def count_products(q: int) -> int:
    """Number of products in R[eps] made by the main function: q + 2."""
    if q < 0:
        raise ValueError("q must be nonnegative")
    return q + 2


def decomposition(q: int) -> list[tuple[list[Poly], list[Poly], list[Poly]]]:
    """The q + 2 rank-one terms u (x) v (x) w over R[eps] with sum eps^3 T_q + O(eps^4).

    Each vector is a list of q + 2 polynomials in eps. The w vectors are
    truncated to degree 3, which does not change the coefficients of
    eps^0, ..., eps^3.
    """
    if q < 0:
        raise ValueError("q must be nonnegative")
    d = q + 2

    def vec(entries: dict[int, Poly]) -> list[Poly]:
        return [entries.get(k, [0]) for k in range(d)]

    terms = []
    for i in range(1, q + 1):
        u = vec({0: [1], i: [0, 1]})
        w = vec({0: [0, 1], i: [0, 0, 1]})
        terms.append((u, u, w))
    s = vec({**{i: [0, 0, 1] for i in range(1, q + 1)}, 0: [1]})
    terms.append((s, s, [_scale(-1, p) for p in s]))
    t = vec({0: [1], q + 1: [0, 0, 0, 1]})
    terms.append((t, t, vec({0: [1, -q], q + 1: [0, 0, 0, 1]})))
    return terms


def cw_exact_by_interpolation(
    x: list[int], y: list[int], q: int, mod: Optional[int] = None
) -> list[int]:
    """Exact phi(x, y) from 7 evaluations of the approximate algorithm, 7(q + 2) scalar products.

    With the truncated w, f(eps) = eps^(-3) * (sum of the terms at eps) is a
    polynomial of degree at most 6 in eps with f(0) = phi(x, y). It is
    evaluated at eps = 1..7 and interpolated at 0. Over Z the arithmetic is
    in Q; with mod, mod must be a prime larger than 7.
    """
    _check(x, y, q)
    if mod is not None and (mod <= 7 or any(mod % p == 0 for p in range(2, int(mod**0.5) + 1))):
        raise ValueError("mod must be a prime larger than 7")
    terms = decomposition(q)
    points = list(range(1, 8))

    def ev(p: Poly, e: int) -> int:
        return sum(c * e**k for k, c in enumerate(p))

    values = []
    for e in points:
        out = [0] * (q + 2)
        for u, v, w in terms:
            m = sum(ev(u[a], e) * x[a] for a in range(q + 2)) * sum(ev(v[b], e) * y[b] for b in range(q + 2))
            for k in range(q + 2):
                out[k] += m * ev(w[k], e)
        values.append(out)
    result = []
    for k in range(q + 2):
        acc = Fraction(0)
        for t, e in enumerate(points):
            lam = Fraction(1)
            for s, f in enumerate(points):
                if s != t:
                    lam *= Fraction(-f, e - f)
            acc += lam * Fraction(values[t][k], e**3)
        if mod is None:
            assert acc.denominator == 1
            result.append(int(acc))
        else:
            result.append(acc.numerator * pow(acc.denominator, -1, mod) % mod)
    return result


def cw_approximate(x: list[float], y: list[float], q: int, eps: float) -> list[float]:
    """The approximate algorithm at a fixed eps in floating point: phi(x, y) + O(eps)."""
    _check(x, y, q)
    terms = decomposition(q)

    def ev(p: Poly) -> float:
        return sum(c * eps**k for k, c in enumerate(p))

    out = [0.0] * (q + 2)
    for u, v, w in terms:
        m = sum(ev(u[a]) * x[a] for a in range(q + 2)) * sum(ev(v[b]) * y[b] for b in range(q + 2))
        for k in range(q + 2):
            out[k] += m * ev(w[k])
    return [o / eps**3 for o in out]


def _entropy(*ps: float) -> float:
    return -sum(p * math.log2(p) for p in ps if p > 0)


def easy_bound(q: int) -> float:
    """Bound on omega from the easy CW tensor with q >= 2: log_q(4 (q + 2)^3 / 27)."""
    if q < 2:
        raise ValueError("q must be at least 2")
    return math.log(4 * (q + 2) ** 3 / 27, q)


def complete_bound(q: int, alpha: float) -> float:
    """Laser bound from the complete CW tensor and weight alpha in (0, 1/3]."""
    if q < 2 or not 0 < alpha <= 1 / 3:
        raise ValueError("need q >= 2 and 0 < alpha <= 1/3")
    h = _entropy(2 / 3 - alpha, 2 * alpha, 1 / 3 - alpha)
    return (math.log2(q + 2) - h) / (alpha * math.log2(q))


def best_complete_bound(q: int) -> tuple[float, float]:
    """Minimize complete_bound over alpha; returns (bound, alpha)."""
    lo, hi = 1e-9, 1 / 3
    for _ in range(200):  # the function is unimodal in alpha on this interval
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if complete_bound(q, m1) <= complete_bound(q, m2):
            hi = m2
        else:
            lo = m1
    a = (lo + hi) / 2
    return complete_bound(q, a), a
