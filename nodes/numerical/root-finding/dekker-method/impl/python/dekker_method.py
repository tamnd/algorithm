# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dekker-method/. The authors are listed in prov/GD9DJV.jsonl.

"""Dekker's method: secant steps kept inside a bracket, with bisection as the fallback."""

import math
from dataclasses import dataclass, field
from typing import Callable, List


@dataclass
class DekkerResult:
    root: float
    a: float
    b: float
    iterations: int
    evaluations: int
    converged: bool
    steps: List[str] = field(default_factory=list)  # "secant", "bisect" or "min" for each step
    iterates: List[float] = field(default_factory=list)


def _check(v: float) -> None:
    if math.isnan(v) or math.isinf(v):
        raise ArithmeticError("f is not finite")


def dekker(f: Callable[[float], float], a: float, b: float, tol: float = 1e-12, max_iter: int = 10000) -> DekkerResult:
    """Find a root of f in [a, b] by Dekker's method.

    Precondition: f continuous on [a, b] with f(a) f(b) <= 0. At every step
    a root lies between the contrapoint a and the best point b. Returns b
    with |b - x*| <= tol + 8 u |b| on convergence, u = 2^-53. Cost: one evaluation of f
    in each step plus two at the start. The number of steps is at most about
    (b - a)/tol, not logarithmic (see the page). Raises ValueError if there
    is no sign change and ArithmeticError on NaN or inf.
    """
    fa, fb = f(a), f(b)  # @line L1
    evals = 2
    _check(fa)
    _check(fb)
    if fa == 0:
        return DekkerResult(a, a, a, 0, evals, True)
    if fb == 0:
        return DekkerResult(b, b, b, 0, evals, True)
    if (fa > 0) == (fb > 0):
        raise ValueError("f(a) and f(b) must have opposite signs")
    p, fp = a, fa  # the previous best point
    steps: List[str] = []
    iterates: List[float] = []
    for k in range(1, max_iter + 1):  # @line L2
        if abs(fa) < abs(fb):  # @line L3
            p, fp = b, fb
            a, fa, b, fb = b, fb, a, fa
        m = a + (b - a) / 2  # @line L4
        t = 2 * math.ulp(1.0) * abs(b) + tol / 2
        if abs(m - b) <= t:
            return DekkerResult(b, min(a, b), max(a, b), k - 1, evals, True, steps, iterates)
        kind = "secant"
        if fb != fp:  # @line L5
            s = b - fb * (b - p) / (fb - fp)
        else:
            s, kind = m, "bisect"
        if not (min(b, m) < s < max(b, m)):  # @line L6
            s, kind = m, "bisect"
        if abs(s - b) < t:  # @line L7
            s, kind = b + math.copysign(t, m - b), "min"
        p, fp = b, fb  # @line L8
        b, fb = s, f(s)
        evals += 1
        _check(fb)
        steps.append(kind)
        iterates.append(b)
        if fb == 0:
            return DekkerResult(b, b, b, k, evals, True, steps, iterates)
        if (fa > 0) == (fb > 0):  # @line L9
            a, fa = p, fp
    return DekkerResult(b, min(a, b), max(a, b), max_iter, evals, False, steps, iterates)
