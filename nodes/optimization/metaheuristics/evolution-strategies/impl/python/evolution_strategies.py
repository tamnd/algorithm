# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/evolution-strategies/. The authors are listed in prov/ZYGTRG.jsonl.

import math
import random
from typing import Callable, Sequence

Vector = list[float]


def one_plus_one_es(
    f: Callable[[Sequence[float]], float],
    x0: Sequence[float],
    sigma0: float,
    steps: int,
    rng: random.Random,
    trace: list | None = None,
) -> tuple[Vector, float, float]:
    """Minimize f by the (1+1)-ES with the 1/5 success rule. Return (x, f(x), sigma).

    The rule is the per-step form: multiply sigma by exp(1/D) after a success
    (f(y) <= f(x)) and by exp(-1/(4D)) after a failure, with D = sqrt(n + 1).
    The two factors balance when one step in five is a success. If trace is a
    list, append (f(x), sigma, success) for each step.
    """
    n = len(x0)
    d = math.sqrt(n + 1)  # @line L1
    up, down = math.exp(1 / d), math.exp(-1 / (4 * d))
    x, fx, sigma = list(x0), f(x0), sigma0
    for _ in range(steps):  # @line L2
        y = [xi + sigma * rng.gauss(0.0, 1.0) for xi in x]  # @line L3
        fy = f(y)
        success = fy <= fx  # @line L4
        if trace is not None:
            trace.append((fx, sigma, success))
        if success:
            x, fx = y, fy  # @line L5
            sigma *= up  # @line L6
        else:
            sigma *= down  # @line L7
    return x, fx, sigma  # @line L8


def sphere(x: Sequence[float]) -> float:
    return sum(t * t for t in x)


def ellipsoid(x: Sequence[float]) -> float:
    """sum_i 10^(6 (i-1)/(n-1)) x_i^2, with condition number 10^6."""
    n = len(x)
    return sum(10 ** (6 * i / (n - 1)) * t * t for i, t in enumerate(x))
