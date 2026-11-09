# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robbins-monro-algorithm/. The authors are listed in prov/WZNBN6.jsonl.

"""Robbins-Monro stochastic approximation: find a root of h(x) = E[H(x, xi)] from noisy values.

The iteration is x <- P(x - a_n H(x, xi_n)) with steps a_n > 0 such that sum a_n = infinity and
sum a_n^2 < infinity. Vectors are lists of floats; P is an optional projection onto a closed
convex set that contains the root.
"""

import random
from collections.abc import Callable

Vector = list[float]


def robbins_monro(
    observe: Callable[[Vector, random.Random], Vector],
    x0: Vector,
    step: Callable[[int], float],
    iters: int,
    rng: random.Random,
    project: Callable[[Vector], Vector] | None = None,
) -> list[Vector]:
    """Return [x_0, ..., x_iters]. observe(x, rng) is a noisy value of h(x) with mean h(x)."""
    x = list(x0)  # @line L1
    xs = [x]
    for n in range(iters):  # @line L2
        y = observe(x, rng)  # @line L3
        x = [a - step(n) * b for a, b in zip(x, y)]  # @line L4
        if project is not None:
            x = project(x)  # @line L5
        xs.append(x)
    return xs  # @line L6


def quantile_observer(alpha: float, sample: Callable[[random.Random], float]) -> Callable[[Vector, random.Random], Vector]:
    """Noisy value of h(x) = P(xi <= x) - alpha; its root is the alpha-quantile of xi."""

    def observe(x: Vector, rng: random.Random) -> Vector:
        return [(1.0 if sample(rng) <= x[0] else 0.0) - alpha]

    return observe
