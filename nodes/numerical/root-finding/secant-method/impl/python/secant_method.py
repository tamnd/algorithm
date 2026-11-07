# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/secant-method/. The authors are listed in prov/8VVH8M.jsonl.

"""The secant method: step to the zero of the line through the last two points."""

import cmath
import math
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class SecantResult:
    """The returned point, why the loop ended, and the work done."""

    root: Any
    reason: str  # "root", "converged", "failure" or "kmax reached"
    iterations: int
    evaluations: int

    @property
    def converged(self) -> bool:
        return self.reason in ("root", "converged")


def _finite(v: Any) -> bool:
    if isinstance(v, complex):
        return cmath.isfinite(v)
    return math.isfinite(float(v))


def secant(f: Callable[[Any], Any], x0: Any, x1: Any, tol_abs: float = 0.0,
           tol_rel: float = 2.0 ** -51, max_iter: int = 100) -> SecantResult:
    """Run the secant method on f from the two points x0 != x1.

    Works for float, complex, Decimal and Fraction values. Precondition:
    tol_abs >= 0, tol_rel >= 0, not both zero. Convergence is guaranteed only
    near a simple root of a C^2 function. Cost: at most max_iter + 2 calls of
    f, O(1) extra space.
    """
    f0 = f(x0)  # @line L1
    if f0 == 0:
        return SecantResult(x0, "root", 0, 1)
    f1 = f(x1)  # @line L2
    evals = 2
    if f1 == 0:
        return SecantResult(x1, "root", 0, evals)
    for k in range(1, max_iter + 1):  # @line L3
        if f1 == f0 or not _finite(f0) or not _finite(f1):  # @line L4
            return SecantResult(x1, "failure", k, evals)
        s = -f1 * (x1 - x0) / (f1 - f0)  # @line L5
        x2 = x1 + s  # @line L6
        if not _finite(x2):  # @line L7
            return SecantResult(x1, "failure", k, evals)
        if abs(s) <= tol_abs + tol_rel * abs(x2):  # @line L8
            return SecantResult(x2, "converged", k, evals)
        f2 = f(x2)  # @line L9
        evals += 1
        if f2 == 0:
            return SecantResult(x2, "root", k, evals)
        x0, f0, x1, f1 = x1, f1, x2, f2  # @line L10
    return SecantResult(x1, "kmax reached", max_iter, evals)  # @line L11
