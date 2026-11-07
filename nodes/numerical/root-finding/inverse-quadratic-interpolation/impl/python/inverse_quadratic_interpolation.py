# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverse-quadratic-interpolation/. The authors are listed in prov/6ZVEEE.jsonl.

"""Inverse quadratic interpolation: fit x as a quadratic in y through three points, take y = 0."""

import math
from dataclasses import dataclass, field
from typing import Callable, List


@dataclass
class IQIResult:
    root: float
    iterations: int
    evaluations: int
    status: str  # "step", "zero", "equal-values" or "max-iter"
    iterates: List[float] = field(default_factory=list)

    @property
    def converged(self) -> bool:
        return self.status in ("step", "zero")


def iqi_step(x0: float, f0: float, x1: float, f1: float, x2: float, f2: float) -> float:
    """The zero of the quadratic in y through (f0, x0), (f1, x1), (f2, x2), in Newton form.

    Precondition: f0, f1, f2 are distinct.
    """
    d21 = (x2 - x1) / (f2 - f1)
    d10 = (x1 - x0) / (f1 - f0)
    d210 = (d10 - d21) / (f0 - f2)
    return x2 - f2 * d21 + f1 * f2 * d210


def inverse_quadratic_interpolation(f: Callable[[float], float], x0: float, x1: float, x2: float,
                                    tol: float = 1e-12, max_iter: int = 100) -> IQIResult:
    """Iterate inverse quadratic interpolation from three starting points.

    Precondition: x0, x1, x2 near a simple root of f, with distinct values
    of f. Local method: no bracket and no guarantee from far away. Stops when
    a step is at most tol (a heuristic test), when f is exactly zero, when two
    of the three values of f are equal, or after max_iter steps. Cost: one
    evaluation of f in each step plus three at the start; order about 1.839
    near a simple root. Raises ArithmeticError if f returns NaN or inf.
    """
    f0, f1, f2 = f(x0), f(x1), f(x2)  # @line L1
    evals = 3
    iterates: List[float] = []
    for v in (f0, f1, f2):
        if math.isnan(v) or math.isinf(v):
            raise ArithmeticError("f is not finite at a starting point")
    for x, v in ((x0, f0), (x1, f1), (x2, f2)):
        if v == 0:
            return IQIResult(x, 0, evals, "zero", iterates)
    for k in range(1, max_iter + 1):  # @line L2
        if f0 == f1 or f1 == f2 or f0 == f2:  # @line L3
            return IQIResult(x2, k - 1, evals, "equal-values", iterates)
        x3 = iqi_step(x0, f0, x1, f1, x2, f2)  # @line L4
        f3 = f(x3)  # @line L5
        evals += 1
        if math.isnan(f3) or math.isinf(f3):
            raise ArithmeticError("f is not finite at an iterate")
        iterates.append(x3)
        if f3 == 0:  # @line L6
            return IQIResult(x3, k, evals, "zero", iterates)
        if abs(x3 - x2) <= tol:
            return IQIResult(x3, k, evals, "step", iterates)
        x0, f0, x1, f1, x2, f2 = x1, f1, x2, f2, x3, f3  # @line L7
    return IQIResult(x2, max_iter, evals, "max-iter", iterates)
