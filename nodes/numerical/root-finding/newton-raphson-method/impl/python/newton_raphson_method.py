# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-raphson-method/. The authors are listed in prov/WV8WGC.jsonl.

"""Newton's method: step to the zero of the tangent line, x - f(x)/f'(x)."""

import cmath
import math
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class NewtonResult:
    """The returned point, why the loop ended, and the work done."""

    root: Any
    reason: str  # "root", "converged", "failure" or "kmax reached"
    iterations: int
    f_evals: int
    df_evals: int

    @property
    def converged(self) -> bool:
        return self.reason in ("root", "converged")


def _finite(v: Any) -> bool:
    if isinstance(v, complex):
        return cmath.isfinite(v)
    return math.isfinite(float(v))


def newton(f: Callable[[Any], Any], df: Callable[[Any], Any], x0: Any,
           tol_abs: float = 0.0, tol_rel: float = 2.0 ** -51,
           max_iter: int = 100) -> NewtonResult:
    """Run Newton's method on f from x0.

    Works for float, complex and fractions.Fraction values. Precondition:
    tol_abs >= 0, tol_rel >= 0, not both zero, max_iter >= 1. Convergence is
    guaranteed only near a simple root of a C^2 function. Cost: one call of f
    and one of df per pass, at most max_iter passes, O(1) extra space.
    """
    x = x0  # @line L1
    fe = de = 0
    for k in range(1, max_iter + 1):  # @line L2
        fx = f(x)  # @line L3
        fe += 1
        if fx == 0:  # @line L4
            return NewtonResult(x, "root", k, fe, de)
        d = df(x)  # @line L5
        de += 1
        if d == 0 or not _finite(fx) or not _finite(d):  # @line L6
            return NewtonResult(x, "failure", k, fe, de)
        s = -fx / d  # @line L7
        x_new = x + s  # @line L8
        if not _finite(x_new):  # @line L9
            return NewtonResult(x, "failure", k, fe, de)
        if abs(s) <= tol_abs + tol_rel * abs(x_new):  # @line L10
            return NewtonResult(x_new, "converged", k, fe, de)
        x = x_new  # @line L11
    return NewtonResult(x, "kmax reached", max_iter, fe, de)  # @line L12
