# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bisection-method/. The authors are listed in prov/QXCMB9.jsonl.

"""The bisection method: halve a sign-changing bracket until it is short enough."""

import math
from dataclasses import dataclass
from typing import Callable


@dataclass
class BisectionResult:
    """The returned point, the final bracket and the work done."""

    root: float
    a: float
    b: float
    iterations: int
    evaluations: int
    converged: bool


def _sign(v: float) -> int:
    return 1 if v > 0 else -1


def bisection(f: Callable[[float], float], a: float, b: float, tol: float = 1e-12,
              max_iter: int = 3000) -> BisectionResult:
    """Find x with |x - x*| <= tol for a root x* of a continuous f in [a, b].

    Precondition: a < b are finite, f is continuous on [a, b] and f(a), f(b)
    have opposite signs (or one of them is 0), tol >= 0. Raises ValueError when
    there is no sign change or f returns NaN. converged is False only when
    max_iter passes end first. Cost: at most ceil(log2((b - a)/(2 tol))) + 2
    evaluations of f when tol > 0, O(1) extra space.
    """
    if not a < b:
        raise ValueError("need a < b")
    fa, fb = f(a), f(b)  # @line L1
    evals = 2
    if fa == 0:  # @line L2
        return BisectionResult(a, a, a, 0, evals, True)
    if fb == 0:
        return BisectionResult(b, b, b, 0, evals, True)
    if math.isnan(fa) or math.isnan(fb) or _sign(fa) == _sign(fb):  # @line L3
        raise ValueError("f(a) and f(b) must have opposite signs")
    for k in range(1, max_iter + 1):  # @line L4
        c = a + (b - a) / 2  # @line L5
        if c <= a or c >= b:  # @line L6
            return BisectionResult(c, a, b, k - 1, evals, True)
        fc = f(c)  # @line L7
        evals += 1
        if fc == 0:  # @line L8
            return BisectionResult(c, c, c, k, evals, True)
        if math.isnan(fc):
            raise ValueError("f returned NaN at %r" % c)
        if _sign(fc) == _sign(fa):  # @line L9
            a, fa = c, fc
        else:  # @line L10
            b, fb = c, fc
        if b - a <= 2 * tol:  # @line L11
            return BisectionResult(a + (b - a) / 2, a, b, k, evals, True)
    return BisectionResult(a + (b - a) / 2, a, b, max_iter, evals, False)  # @line L12
