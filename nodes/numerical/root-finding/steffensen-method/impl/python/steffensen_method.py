# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/steffensen-method/. The authors are listed in prov/ZF9XZ7.jsonl.

"""Steffensen's method: a secant step whose increment is f(x) itself."""

import math
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class SteffensenResult:
    """The returned point, why the loop ended, and the work done."""

    root: Any
    reason: str  # "root", "residual", "converged", "failure" or "kmax reached"
    iterations: int
    evaluations: int

    @property
    def converged(self) -> bool:
        return self.reason in ("root", "residual", "converged")


def _finite(v: Any) -> bool:
    return math.isfinite(float(v))


def steffensen(f: Callable[[Any], Any], x0: Any, tol_abs: float = 0.0,
               tol_rel: float = 2.0 ** -50, max_iter: int = 100) -> SteffensenResult:
    """Solve f(x) = 0 by x <- x - f(x)^2 / (f(x + f(x)) - f(x)).

    Works for float and fractions.Fraction values. Precondition: tol_abs >= 0,
    tol_rel >= 0, max_iter >= 1. Convergence is guaranteed only near a simple
    root of a C^2 function. Cost: two evaluations of f per pass.
    """
    x = x0  # @line L1
    ev = 0
    for k in range(1, max_iter + 1):  # @line L2
        fx = f(x)  # @line L3
        ev += 1
        if fx == 0:
            return SteffensenResult(x, "root", k, ev)
        if not _finite(fx):  # @line L4
            return SteffensenResult(x, "failure", k, ev)
        xh = x + fx  # @line L5
        if xh == x:
            # |f(x)| is below half an ulp of x: no slope can be formed
            return SteffensenResult(x, "residual", k, ev)
        h = xh - x
        fxh = f(xh)
        ev += 1
        if not _finite(fxh):
            return SteffensenResult(x, "failure", k, ev)
        d = (fxh - fx) / h  # @line L6
        if d == 0:
            return SteffensenResult(x, "failure", k, ev)
        s = -fx / d  # @line L7
        x_new = x + s  # @line L8
        if not _finite(x_new):  # @line L9
            return SteffensenResult(x, "failure", k, ev)
        if abs(s) <= tol_abs + tol_rel * abs(x_new):  # @line L10
            return SteffensenResult(x_new, "converged", k, ev)
        x = x_new  # @line L11
    return SteffensenResult(x, "kmax reached", max_iter, ev)  # @line L12


def steffensen_fixed_point(g: Callable[[Any], Any], x0: Any, tol_abs: float = 0.0,
                           tol_rel: float = 2.0 ** -50,
                           max_iter: int = 100) -> SteffensenResult:
    """Find a fixed point g(x) = x by Aitken's extrapolation of x, g(x), g(g(x)).

    This is steffensen applied to f(x) = g(x) - x, written with g. Cost: two
    evaluations of g per pass.
    """
    x = x0
    ev = 0
    for k in range(1, max_iter + 1):
        y = g(x)
        ev += 1
        if y == x:
            return SteffensenResult(x, "root", k, ev)
        if not _finite(y):
            return SteffensenResult(x, "failure", k, ev)
        z = g(y)
        ev += 1
        if not _finite(z):
            return SteffensenResult(x, "failure", k, ev)
        den = z - 2 * y + x
        if den == 0:
            return SteffensenResult(y, "failure", k, ev)
        s = -(y - x) ** 2 / den
        x_new = x + s
        if not _finite(x_new):
            return SteffensenResult(x, "failure", k, ev)
        if abs(s) <= tol_abs + tol_rel * abs(x_new):
            return SteffensenResult(x_new, "converged", k, ev)
        x = x_new
    return SteffensenResult(x, "kmax reached", max_iter, ev)
