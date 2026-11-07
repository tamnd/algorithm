# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/illinois-method/. The authors are listed in prov/C2H8P5.jsonl.

"""The Illinois method: regula falsi with the stale function value halved."""

import math
from dataclasses import dataclass, field
from typing import Callable, List


@dataclass
class IllinoisResult:
    root: float
    a: float
    b: float
    iterations: int
    evaluations: int
    converged: bool
    iterates: List[float] = field(default_factory=list)


def illinois(f: Callable[[float], float], a: float, b: float, tol: float = 1e-12, max_iter: int = 200) -> IllinoisResult:
    """Find a root of f in [a, b] by the Illinois method.

    Precondition: f is continuous on [a, b], f(a) and f(b) are finite, and
    f(a) f(b) <= 0. The bracket [a, b] holds a root at every step. The method
    stops when the bracket is at most tol wide (or 4 ulps of its ends), when
    f is exactly zero at an iterate, or after max_iter steps. Cost: one
    evaluation of f in each step, plus two at the start. Raises ValueError
    if there is no sign change and ArithmeticError if f returns NaN or inf.
    """
    fa, fb = f(a), f(b)  # @line L1
    evals = 2
    for v in (fa, fb):
        if math.isnan(v) or math.isinf(v):
            raise ArithmeticError("f is not finite at an end of the bracket")
    if fa == 0:
        return IllinoisResult(a, a, a, 0, evals, True)
    if fb == 0:
        return IllinoisResult(b, b, b, 0, evals, True)
    if (fa > 0) == (fb > 0):
        raise ValueError("f(a) and f(b) must have opposite signs")
    iterates: List[float] = []
    x = b
    for k in range(1, max_iter + 1):  # @line L2
        lo, hi = min(a, b), max(a, b)
        if hi - lo <= max(tol, 4 * math.ulp(max(abs(lo), abs(hi)))):  # @line L3
            return IllinoisResult(x, lo, hi, k - 1, evals, True, iterates)
        x = b - fb * (b - a) / (fb - fa)  # @line L4
        if not (lo < x < hi):  # rounding put x outside: bisect instead
            x = lo + (hi - lo) / 2
        fx = f(x)  # @line L5
        evals += 1
        if math.isnan(fx) or math.isinf(fx):
            raise ArithmeticError("f is not finite at an iterate")
        iterates.append(x)
        if fx == 0:  # @line L6
            return IllinoisResult(x, x, x, k, evals, True, iterates)
        if (fx > 0) != (fb > 0):  # @line L7
            a, fa = b, fb  # @line L8
        else:
            fa = fa / 2  # @line L9
        b, fb = x, fx  # @line L10
    lo, hi = min(a, b), max(a, b)
    return IllinoisResult(x, lo, hi, max_iter, evals, False, iterates)
