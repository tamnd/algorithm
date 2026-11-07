# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chandrupatla-method/. The authors are listed in prov/WGGEP1.jsonl.

"""Chandrupatla's method: inverse quadratic interpolation in a bracket, accepted by a test on two ratios."""

import math
from dataclasses import dataclass, field
from typing import Callable, List

U4 = 2 * 2.0 ** -52  # 4u, with u = 2^-53


@dataclass
class ChandrupatlaResult:
    root: float
    a: float
    b: float
    iterations: int
    evaluations: int
    converged: bool
    steps: List[str] = field(default_factory=list)  # "iqi" or "bisect", the rule that chose each point
    iterates: List[float] = field(default_factory=list)


def _check(v: float) -> None:
    if math.isnan(v) or math.isinf(v):
        raise ArithmeticError("f is not finite")


def chandrupatla(f: Callable[[float], float], x0: float, x1: float, tol: float = 1e-12, max_iter: int = 10000) -> ChandrupatlaResult:
    """Find a root of f between x0 and x1 by Chandrupatla's method.

    Precondition: f continuous with f(x0) f(x1) <= 0. A root lies between a
    (the newest point) and b at every step. The returned point has
    |x - x*| <= tol + 8 u |x| (u = 2^-53) on convergence. Cost: one
    evaluation of f in each step plus two at the start; for tol > 0 at most
    ceil(2 |x1 - x0| / tol) steps. Raises ValueError without a sign change
    and ArithmeticError on NaN or inf.
    """
    b, a = x0, x1  # @line L1
    fa, fb = f(a), f(b)
    evals = 2
    _check(fa)
    _check(fb)
    if fa == 0:
        return ChandrupatlaResult(a, a, a, 0, evals, True)
    if fb == 0:
        return ChandrupatlaResult(b, b, b, 0, evals, True)
    if (fa > 0) == (fb > 0):
        raise ValueError("f(x0) and f(x1) must have opposite signs")
    c, fc = a, fa
    t = 0.5
    kind = "bisect"
    steps: List[str] = []
    iterates: List[float] = []
    for k in range(1, max_iter + 1):  # @line L2
        xm, fm = (a, fa) if abs(fa) < abs(fb) else (b, fb)  # @line L3
        tl = (U4 * abs(xm) + tol / 2) / abs(b - a)
        if fm == 0 or tl >= 0.5:
            return ChandrupatlaResult(xm, min(a, b), max(a, b), k - 1, evals, True, steps, iterates)
        t = min(1 - tl, max(tl, t))  # @line L4
        x = a + t * (b - a)  # @line L5
        fx = f(x)
        evals += 1
        _check(fx)
        steps.append(kind)
        iterates.append(x)
        if (fx > 0) == (fa > 0):  # @line L6
            c, fc = a, fa
        else:
            c, fc, b, fb = b, fb, a, fa
        a, fa = x, fx  # @line L7
        if fa == 0:
            return ChandrupatlaResult(a, a, a, k, evals, True, steps, iterates)
        xi = (a - b) / (c - b)  # @line L8
        phi = (fa - fb) / (fc - fb)
        if phi * phi < xi and (1 - phi) * (1 - phi) < 1 - xi:  # @line L9
            t = fa / (fb - fa) * fc / (fb - fc) + (c - a) / (b - a) * fa / (fc - fa) * fb / (fc - fb)
            kind = "iqi"
        else:
            t, kind = 0.5, "bisect"  # @line L10
    return ChandrupatlaResult(a, min(a, b), max(a, b), max_iter, evals, False, steps, iterates)  # @line L11
