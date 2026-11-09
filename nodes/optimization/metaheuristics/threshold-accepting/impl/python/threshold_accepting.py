# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/threshold-accepting/. The authors are listed in prov/89MGMB.jsonl.

import random
from typing import Callable, Sequence, TypeVar

S = TypeVar("S")


def threshold_accepting(
    x0: S,
    f: Callable[[S], float],
    neighbor: Callable[[S, random.Random], S],
    thresholds: Sequence[float],
    steps_per_threshold: int,
    rng: random.Random,
    trace: list | None = None,
) -> tuple[S, float]:
    """Minimize f by threshold accepting. Return (best solution, its value).

    A neighbor y of x is accepted if and only if f(y) - f(x) < tau, for the
    current threshold tau. If trace is a list, append (tau, x, y, f(x), f(y), accepted)
    for each step.
    """
    x, fx = x0, f(x0)  # @line L1
    best, fb = x, fx
    for tau in thresholds:  # @line L2
        for _ in range(steps_per_threshold):  # @line L3
            y = neighbor(x, rng)  # @line L4
            fy = f(y)
            accepted = fy - fx < tau  # @line L5
            if trace is not None:
                trace.append((tau, x, y, fx, fy, accepted))
            if accepted:
                x, fx = y, fy  # @line L6
                if fx < fb:  # @line L7
                    best, fb = x, fx
    return best, fb  # @line L8


def linear_thresholds(first: float, count: int) -> list[float]:
    """count thresholds that fall linearly from first to first / count."""
    return [first * (count - j) / count for j in range(count)]
