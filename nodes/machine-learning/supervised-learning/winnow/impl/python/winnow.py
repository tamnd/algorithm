# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/winnow/. The authors are listed in prov/ETYSJD.jsonl.

"""Littlestone's Winnow for Boolean examples x in {0, 1}^n and labels y in {0, 1}.

variant=1 is WINNOW1: a false positive sets the active weights to 0
(elimination). variant=2 is WINNOW2: a false positive divides them by alpha
(demotion). Both multiply the active weights by alpha on a false negative
(promotion), and predict 1 when the weighted sum is greater than theta.
"""

import math
from typing import Iterable, Sequence


class Winnow:
    def __init__(self, n: int, alpha: float = 2.0, theta: float | None = None, variant: int = 1):
        if alpha <= 1:
            raise ValueError("alpha must be greater than 1")
        if variant not in (1, 2):
            raise ValueError("variant is 1 or 2")
        self.n = n
        self.alpha = alpha
        self.theta = n / 2 if theta is None else theta
        self.variant = variant
        self.w = [1.0] * n  # @line L1
        self.mistakes = 0

    def predict(self, x: Sequence[int]) -> int:
        s = sum(self.w[i] for i in range(self.n) if x[i])
        return 1 if s > self.theta else 0  # @line L3

    def update(self, x: Sequence[int], y: int) -> bool:
        """Predict on x, learn from the true label y, return True on a mistake."""
        yhat = self.predict(x)
        if yhat == 0 and y == 1:  # @line L4
            for i in range(self.n):
                if x[i]:
                    self.w[i] *= self.alpha  # @line L5
        elif yhat == 1 and y == 0:  # @line L6
            for i in range(self.n):
                if x[i]:
                    if self.variant == 1:
                        self.w[i] = 0.0  # @line L7
                    else:
                        self.w[i] /= self.alpha
        else:
            return False
        self.mistakes += 1  # @line L8
        return True


def run(model: Winnow, stream: Iterable[tuple[Sequence[int], int]]) -> int:  # @line L2
    for x, y in stream:
        model.update(x, y)
    return model.mistakes


def winnow1_bound(n: int, k: int, alpha: float, theta: float) -> float:
    """Littlestone (1988), Theorem 7: alpha k (log_alpha theta + 1) + n / theta.

    It holds for alpha > 1 and theta >= 1 / alpha, when the target is a
    monotone disjunction of k of the n variables.
    """
    return alpha * k * (math.log(theta) / math.log(alpha) + 1) + n / theta


def disjunction(relevant: Sequence[int]):
    def f(x: Sequence[int]) -> int:
        return 1 if any(x[i] for i in relevant) else 0

    return f
