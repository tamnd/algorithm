# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brent-method/. The authors are listed in prov/E222GS.jsonl.

"""Brent's method (zeroin): inverse quadratic interpolation, secant and bisection in a bracket."""

import math
from dataclasses import dataclass, field
from typing import Callable, List

U4 = 2 * 2.0 ** -52  # 4u, with u = 2^-53 the unit roundoff of binary64


@dataclass
class BrentResult:
    root: float
    a: float
    b: float
    iterations: int
    evaluations: int
    converged: bool
    steps: List[str] = field(default_factory=list)  # "iqi", "secant" or "bisect" for each step
    iterates: List[float] = field(default_factory=list)


def _check(v: float) -> None:
    if math.isnan(v) or math.isinf(v):
        raise ArithmeticError("f is not finite")


def brent(f: Callable[[float], float], a: float, b: float, tol: float = 1e-12, max_iter: int = 10000) -> BrentResult:
    """Find a root of f in [a, b] by Brent's method.

    Precondition: f continuous on [a, b] with f(a) f(b) <= 0. A root lies
    between b and the contrapoint c at every step, and the returned b has
    |b - x*| <= tol + 8 u |b| (u = 2^-53). Cost: one evaluation of f in each
    step plus two at the start; for tol > 0 at most 2 (k + 2)^2 steps, where
    k = ceil(log2((b - a)/tol)) is the bisection count. Raises ValueError if
    there is no sign change and ArithmeticError on NaN or inf.
    """
    fa, fb = f(a), f(b)  # @line L1
    evals = 2
    _check(fa)
    _check(fb)
    if fa == 0:
        return BrentResult(a, a, a, 0, evals, True)
    if fb == 0:
        return BrentResult(b, b, b, 0, evals, True)
    if (fa > 0) == (fb > 0):
        raise ValueError("f(a) and f(b) must have opposite signs")
    c, fc = a, fa
    d = e = b - a
    steps: List[str] = []
    iterates: List[float] = []
    for k in range(1, max_iter + 1):  # @line L2
        if (fb > 0) == (fc > 0):  # @line L3
            c, fc = a, fa
            d = e = b - a
        if abs(fc) < abs(fb):  # @line L4
            a, b, c = b, c, b
            fa, fb, fc = fb, fc, fb
        t = U4 * abs(b) + tol / 2  # @line L5
        m = (c - b) / 2
        if abs(m) <= t or fb == 0:
            return BrentResult(b, min(b, c), max(b, c), k - 1, evals, True, steps, iterates)
        kind = "bisect"
        if abs(e) >= t and abs(fa) > abs(fb):  # @line L6
            s = fb / fa  # @line L7
            if a == c:
                p, q = 2 * m * s, 1 - s
                trial = "secant"
            else:
                q, r = fa / fc, fb / fc
                p = s * (2 * m * q * (q - r) - (b - a) * (r - 1))
                q = (q - 1) * (r - 1) * (s - 1)
                trial = "iqi"
            if p > 0:  # @line L8
                q = -q
            p = abs(p)
            if 2 * p < min(3 * m * q - abs(t * q), abs(e * q)):  # @line L9
                e, d = d, p / q
                kind = trial
            else:
                d = e = m
        else:
            d = e = m  # @line L10
        a, fa = b, fb  # @line L11
        b = b + d if abs(d) > t else b + math.copysign(t, m)
        fb = f(b)
        evals += 1
        _check(fb)
        steps.append(kind)
        iterates.append(b)
    lo, hi = min(b, c), max(b, c)
    return BrentResult(b, lo, hi, max_iter, evals, False, steps, iterates)
