# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/halley-method/. The authors are listed in prov/4V4H83.jsonl.

"""Halley's method: x <- x - 2 f f' / (2 f'^2 - f f''), cubically convergent at simple roots."""

import math
from dataclasses import dataclass, field
from typing import Callable, List


@dataclass
class HalleyResult:
    root: float
    iterations: int
    evaluations: int  # evaluations of f; f' and f'' are evaluated the same number of times
    status: str  # "converged", "exact", "stalled", "zero-denominator", "max-iter"
    iterates: List[float] = field(default_factory=list)

    @property
    def converged(self) -> bool:
        return self.status in ("converged", "exact")


def halley(f: Callable[[float], float], df: Callable[[float], float], d2f: Callable[[float], float],
           x0: float, tol: float = 1e-14, max_iter: int = 100) -> HalleyResult:
    """Run Halley's method from x0.

    Stops with "converged" when the step is at most tol (1 + |x|), with
    "exact" when f(x) = 0, with "stalled" when the step is 0 although
    f(x) != 0 (this happens when f'(x) = 0), with "zero-denominator" when
    2 f'^2 - f f'' = 0, and with "max-iter" after max_iter steps. Each step
    evaluates f, f' and f'' once. Raises ArithmeticError on NaN or inf.
    """
    x = float(x0)
    iterates = [x]
    evals = 0
    for k in range(1, max_iter + 1):  # @line L1
        fx, d1, d2 = f(x), df(x), d2f(x)  # @line L2
        evals += 1
        if not all(math.isfinite(v) for v in (fx, d1, d2)):
            raise ArithmeticError("non-finite value of f or a derivative")
        if fx == 0:  # @line L3
            return HalleyResult(x, k - 1, evals, "exact", iterates)
        den = 2 * d1 * d1 - fx * d2  # @line L4
        if den == 0:
            return HalleyResult(x, k - 1, evals, "zero-denominator", iterates)
        step = 2 * fx * d1 / den  # @line L5
        if step == 0:
            return HalleyResult(x, k - 1, evals, "stalled", iterates)
        x = x - step  # @line L6
        if not math.isfinite(x):
            raise ArithmeticError("non-finite iterate")
        iterates.append(x)
        if abs(step) <= tol * (1 + abs(x)):  # @line L7
            return HalleyResult(x, k, evals, "converged", iterates)
    return HalleyResult(x, max_iter, evals, "max-iter", iterates)  # @line L8
