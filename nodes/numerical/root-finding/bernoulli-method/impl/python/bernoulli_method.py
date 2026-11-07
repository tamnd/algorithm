# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bernoulli-method/. The authors are listed in prov/QQR2VY.jsonl.

"""Bernoulli's method: the dominant root of a polynomial as the limit of
y_(k+1) / y_k, where y_k solves the linear recurrence with p as its
characteristic polynomial.

Coefficients are real and listed highest degree first: a[0] x^n + ... + a[n].
The start is the power sums s_0, ..., s_(n-1) of the roots, from Newton's
identities, so that y_k = s_k = sum of the k-th powers of the roots.
"""

import math
from dataclasses import dataclass, field
from typing import List, Sequence


@dataclass
class BernoulliResult:
    root: float
    iterations: int  # recurrence steps
    status: str  # "converged", "max-iter"
    ratios: List[float] = field(default_factory=list)


def power_sums(a: Sequence[float], count: int) -> List[float]:
    """s_0, ..., s_(count-1): Newton's identities for k < n, the recurrence after."""
    n = len(a) - 1
    s = [float(n)]
    for k in range(1, count):
        if k < n:
            acc = sum(a[j] * s[k - j] for j in range(1, k)) + k * a[k]
        else:
            acc = sum(a[j] * s[k - j] for j in range(1, n + 1))
        s.append(-acc / a[0])
    return s


def _check(coeffs: Sequence[float]) -> List[float]:
    a = [float(x) for x in coeffs]
    if not all(math.isfinite(x) for x in a):
        raise ValueError("coefficients must be finite")
    while a and a[0] == 0:
        a.pop(0)
    if len(a) < 2:
        raise ValueError("need a polynomial of degree at least 1")
    return a


def bernoulli(coeffs: Sequence[float], tol: float = 1e-12, max_iter: int = 10000) -> BernoulliResult:
    """Dominant root of the polynomial, assuming one root of largest modulus.

    Stops with "converged" when two consecutive ratios differ by at most
    tol (1 + |ratio|), and with "max-iter" otherwise. The window of the
    last n terms is rescaled every step, so it never overflows.
    """
    a = _check(coeffs)
    n = len(a) - 1
    y = power_sums(a, n)  # @line L1
    ratios = []
    prev = None
    for k in range(1, max_iter + 1):  # @line L2
        nxt = -sum(a[j] * y[-j] for j in range(1, n + 1)) / a[0]  # @line L3
        last = y[-1]
        y.append(nxt)
        y.pop(0)
        scale = max(abs(t) for t in y)  # @line L4
        if scale == 0:
            return BernoulliResult(0.0, k, "converged", ratios)  # all roots are 0
        y = [t / scale for t in y]
        if last == 0:  # @line L5
            prev = None
            continue
        rho = nxt / last  # @line L6
        ratios.append(rho)
        if prev is not None and abs(rho - prev) <= tol * (1 + abs(rho)):  # @line L7
            return BernoulliResult(rho, k, "converged", ratios)
        prev = rho
    return BernoulliResult(prev if prev is not None else math.nan, max_iter, "max-iter", ratios)  # @line L8


def bernoulli_pair(coeffs: Sequence[float], tol: float = 1e-12, max_iter: int = 10000):
    """Dominant complex pair: fit y_(k+1) = S y_k - P y_(k-1) to four
    consecutive terms and return (S, P, iterations, status); the pair is
    the roots of x^2 - S x + P."""
    a = _check(coeffs)
    n = len(a) - 1
    if n < 2:
        raise ValueError("need degree at least 2")
    w = max(n, 4)
    y = power_sums(a, w)
    prev = None
    for k in range(1, max_iter + 1):
        nxt = -sum(a[j] * y[-j] for j in range(1, n + 1)) / a[0]
        y.append(nxt)
        y.pop(0)
        scale = max(abs(t) for t in y)
        if scale == 0:
            return 0.0, 0.0, k, "converged"
        y = [t / scale for t in y]
        y0, y1, y2, y3 = y[-4:]
        det = y1 * y1 - y0 * y2
        if det == 0:
            prev = None
            continue
        S = (y1 * y2 - y0 * y3) / det
        P = (y2 * y2 - y1 * y3) / det
        if prev is not None and abs(S - prev[0]) + abs(P - prev[1]) <= tol * (1 + abs(S) + abs(P)):
            return S, P, k, "converged"
        prev = (S, P)
    S, P = prev if prev is not None else (math.nan, math.nan)
    return S, P, max_iter, "max-iter"
