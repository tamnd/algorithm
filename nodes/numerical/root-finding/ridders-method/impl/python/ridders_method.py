# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ridders-method/. The authors are listed in prov/AGQH37.jsonl.

"""Ridders' method: a bracketing method with an exponential correction at the midpoint."""

import math
from dataclasses import dataclass, field
from typing import Any, Callable, List


@dataclass
class RiddersResult:
    """The returned point, why the loop ended, the final bracket, and the work done."""

    root: Any
    reason: str  # "root", "bracket", "converged", "no sign change", "failure" or "kmax reached"
    iterations: int
    evaluations: int
    a: Any
    b: Any
    trial: List[Any] = field(default_factory=list)  # the Ridders points x

    @property
    def converged(self) -> bool:
        return self.reason in ("root", "bracket", "converged")


def _finite(v: Any) -> bool:
    return math.isfinite(float(v))


def _sign(v: Any) -> int:
    return (v > 0) - (v < 0)


def ridders(f: Callable[[Any], Any], a: Any, b: Any, tol: float = 0.0,
            max_iter: int = 200) -> RiddersResult:
    """Find a root of f in the bracket [a, b] with f(a) f(b) < 0.

    Works for float values. With tol = 0 the loop runs until the bracket
    cannot shrink in floating point, or until two successive Ridders points
    agree to within tol. Precondition: a < b, tol >= 0,
    max_iter >= 1. Cost: two evaluations to start and two per pass; the
    bracket at least halves in each pass.
    """
    fa, fb = f(a), f(b)  # @line L1
    ev = 2
    if not (_finite(fa) and _finite(fb)):
        return RiddersResult(a, "failure", 0, ev, a, b)
    if fa == 0:
        return RiddersResult(a, "root", 0, ev, a, a)
    if fb == 0:
        return RiddersResult(b, "root", 0, ev, b, b)
    if _sign(fa) == _sign(fb):
        return RiddersResult(a, "no sign change", 0, ev, a, b)
    trial: List[Any] = []
    x_prev = None
    for k in range(1, max_iter + 1):  # @line L2
        m = a + (b - a) / 2  # @line L3
        if not a < m < b:
            return RiddersResult(m, "bracket", k - 1, ev, a, b, trial)
        fm = f(m)
        ev += 1
        if fm == 0:
            return RiddersResult(m, "root", k, ev, m, m, trial)
        if not _finite(fm):
            return RiddersResult(m, "failure", k, ev, a, b, trial)
        t = max(abs(fa), abs(fb), abs(fm))  # @line L4
        s = t * math.sqrt((fm / t) ** 2 - (fa / t) * (fb / t))
        x = m + (m - a) * _sign(fa - fb) * (fm / s)  # @line L5
        x = min(max(x, a), b)
        fx = f(x)  # @line L6
        ev += 1
        trial.append(x)
        if fx == 0:
            return RiddersResult(x, "root", k, ev, x, x, trial)
        if not _finite(fx):
            return RiddersResult(x, "failure", k, ev, a, b, trial)
        if _sign(fm) != _sign(fx):  # @line L7
            if m < x:
                a, fa, b, fb = m, fm, x, fx
            else:
                a, fa, b, fb = x, fx, m, fm
        elif _sign(fa) != _sign(fx):
            b, fb = x, fx
        else:
            a, fa = x, fx
        if b - a <= 2 * tol:  # @line L8
            return RiddersResult(a + (b - a) / 2, "bracket", k, ev, a, b, trial)
        if x_prev is not None and abs(x - x_prev) <= tol:  # @line L9
            return RiddersResult(x, "converged", k, ev, a, b, trial)
        x_prev = x  # @line L10
    return RiddersResult(a + (b - a) / 2, "kmax reached", max_iter, ev, a, b, trial)  # @line L11
