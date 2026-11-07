# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fixed-point-iteration/. The authors are listed in prov/KFHFSG.jsonl.

"""Fixed-point iteration x <- g(x) with an a posteriori stop test."""

import math
from dataclasses import dataclass, field
from typing import Callable, List, Optional


@dataclass
class FixedPointResult:
    """The returned point, the number of evaluations of g and the iterates."""

    root: float
    evaluations: int
    converged: bool
    iterates: List[float] = field(default_factory=list)


def fixed_point_iteration(g: Callable[[float], float], x0: float, tol: float = 1e-12,
                          max_iter: int = 10000,
                          lipschitz: Optional[float] = None) -> FixedPointResult:
    """Iterate x <- g(x) from x0 until two iterates differ by at most tau.

    tau = tol * (1 - L) / L when a Lipschitz constant 0 < L < 1 of g is given;
    then, if g is a contraction on an interval that it maps into itself and
    that holds x0, the result is within tol of the fixed point. Without L,
    tau = tol and the test is a heuristic. Raises ArithmeticError when g
    returns NaN or an infinite value. Cost: one evaluation of g per step,
    O(log(r / ((1 - L) tol)) / log(1 / L)) steps under the contraction
    hypothesis, O(1) extra space besides the list of iterates.
    """
    if lipschitz is not None and 0 < lipschitz < 1:
        tau = tol * (1 - lipschitz) / lipschitz  # @line L1
    else:
        tau = tol
    x = x0  # @line L2
    iterates = [x]
    for k in range(1, max_iter + 1):  # @line L3
        y = g(x)  # @line L4
        iterates.append(y)
        if math.isnan(y) or math.isinf(y):  # @line L5
            raise ArithmeticError("the iteration diverged at step %d" % k)
        if abs(y - x) <= tau:  # @line L6
            return FixedPointResult(y, k, True, iterates)
        x = y  # @line L7
    return FixedPointResult(x, max_iter, False, iterates)  # @line L8
