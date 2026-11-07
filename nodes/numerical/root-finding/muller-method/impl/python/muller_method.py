# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/muller-method/. The authors are listed in prov/1KDQ2S.jsonl.

"""Muller's method: step to the root of the parabola through the last three points."""

import cmath
import math
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class MullerResult:
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


def _sqrt(z: Any) -> Any:
    if isinstance(z, complex) or z < 0:
        return cmath.sqrt(z)
    return math.sqrt(z)


def muller(f: Callable[[Any], Any], x0: Any, x1: Any, x2: Any,
           tol_abs: float = 0.0, tol_rel: float = 2.0 ** -50,
           max_iter: int = 100) -> MullerResult:
    """Run Muller's method from three distinct starting points.

    The iterates stay real while the parabolas have real roots and become
    complex otherwise, so f must accept complex arguments in general.
    Precondition: tol_abs >= 0, tol_rel >= 0, max_iter >= 1. Cost: three
    evaluations of f to start and one per pass after that.
    """
    xs = [x0, x1, x2]
    fs = []
    ev = 0
    for x in xs:  # @line L1
        fx = f(x)
        ev += 1
        if fx == 0:
            return MullerResult(x, "root", 0, ev)
        if not _finite(fx):
            return MullerResult(x, "failure", 0, ev)
        fs.append(fx)
    x0, x1, x2 = xs
    f0, f1, f2 = fs
    for k in range(1, max_iter + 1):  # @line L2
        h1, h2 = x1 - x0, x2 - x1  # @line L3
        if h1 == 0 or h2 == 0 or h1 + h2 == 0:
            return MullerResult(x2, "failure", k, ev)
        d1, d2 = (f1 - f0) / h1, (f2 - f1) / h2  # @line L4
        d = (d2 - d1) / (h1 + h2)
        b = d2 + h2 * d  # @line L5
        s = _sqrt(b * b - 4 * f2 * d)  # @line L6
        e = b + s if abs(b + s) >= abs(b - s) else b - s  # @line L7
        if e == 0 or not _finite(e):  # @line L8
            return MullerResult(x2, "failure", k, ev)
        h = -2 * f2 / e  # @line L9
        x3 = x2 + h
        if not _finite(x3):
            return MullerResult(x2, "failure", k, ev)
        f3 = f(x3)  # @line L10
        ev += 1
        if f3 == 0:
            return MullerResult(x3, "root", k, ev)
        if not _finite(f3):
            return MullerResult(x3, "failure", k, ev)
        if abs(h) <= tol_abs + tol_rel * abs(x3):  # @line L11
            return MullerResult(x3, "converged", k, ev)
        x0, x1, x2 = x1, x2, x3  # @line L12
        f0, f1, f2 = f1, f2, f3
    return MullerResult(x2, "kmax reached", max_iter, ev)  # @line L13
