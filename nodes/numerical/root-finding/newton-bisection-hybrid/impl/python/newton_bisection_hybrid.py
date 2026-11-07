# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-bisection-hybrid/. The authors are listed in prov/STTPS1.jsonl.

"""Safeguarded Newton method: Newton steps inside a bracket, bisection as the fallback."""

import math
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional


@dataclass
class SafeNewtonResult:
    """The returned point, why the loop ended, the work done and the last bracket."""

    root: Any
    reason: str  # "root", "bracket", "converged", "no bracket", "failure", "kmax reached"
    iterations: int
    f_evals: int
    df_evals: int
    a: Any
    b: Any
    steps: List[str] = field(default_factory=list)  # "newton" or "bisect", one per pass

    @property
    def converged(self) -> bool:
        return self.reason in ("root", "bracket", "converged")


def _finite(v: Any) -> bool:
    return math.isfinite(float(v))


def safe_newton(
    f: Callable[[Any], Any],
    df: Callable[[Any], Any],
    a: Any,
    b: Any,
    tol: Any = 0.0,
    max_iter: int = 200,
) -> SafeNewtonResult:
    """Find a zero of f in [a, b] with Newton steps safeguarded by bisection.

    Precondition: a < b and f(a), f(b) finite with opposite signs (otherwise
    "no bracket" is returned); df is the derivative of f. A Newton step is
    taken when it lands strictly inside the bracket and is at most half the
    previous step; otherwise the bracket is bisected. With tol > 0 the loop
    ends after at most (N + 1)^2 passes, N = ceil(log2((b - a)/tol)), in
    exact arithmetic. Cost per pass: one f and at most one df evaluation.
    """
    fa = f(a)  # @line L1
    fb = f(b)
    nf, nd = 2, 0
    steps: List[str] = []
    if fa == 0:
        return SafeNewtonResult(a, "root", 0, nf, nd, a, b, steps)
    if fb == 0:
        return SafeNewtonResult(b, "root", 0, nf, nd, a, b, steps)
    if not (_finite(fa) and _finite(fb)) or (fa > 0) == (fb > 0):  # @line L2
        return SafeNewtonResult(a, "no bracket", 0, nf, nd, a, b, steps)
    x = a + (b - a) / 2  # @line L3
    s_prev = b - a
    for k in range(1, max_iter + 1):  # @line L4
        fx = f(x)  # @line L5
        nf += 1
        if fx == 0:
            return SafeNewtonResult(x, "root", k, nf, nd, a, b, steps)
        if not _finite(fx):
            return SafeNewtonResult(x, "failure", k, nf, nd, a, b, steps)
        if (fx > 0) == (fa > 0):  # @line L6
            a, fa = x, fx
        else:
            b, fb = x, fx
        if b - a <= 2 * tol:  # @line L7
            return SafeNewtonResult(a + (b - a) / 2, "bracket", k, nf, nd, a, b, steps)
        d = df(x)  # @line L8
        nd += 1
        xn: Optional[Any] = None
        if d != 0 and _finite(d):
            xn = x - fx / d
            if not _finite(xn):
                xn = None
        if xn is None or not (a < xn < b) or abs(xn - x) > abs(s_prev) / 2:  # @line L9
            xn = a + (b - a) / 2
            steps.append("bisect")
        else:
            steps.append("newton")
        if abs(xn - x) <= tol:  # @line L10
            return SafeNewtonResult(xn, "converged", k, nf, nd, a, b, steps)
        s_prev = xn - x  # @line L11
        x = xn
    return SafeNewtonResult(x, "kmax reached", max_iter, nf, nd, a, b, steps)  # @line L12
