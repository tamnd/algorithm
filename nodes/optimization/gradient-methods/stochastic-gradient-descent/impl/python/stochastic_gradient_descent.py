# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stochastic-gradient-descent/. The authors are listed in prov/BTB2HV.jsonl.

"""Stochastic gradient descent: x <- P(x - eta_k G(x, xi_k)) with a fresh sample at each step.

Vectors are lists of floats. The oracle receives the point and a random.Random and returns
an unbiased estimate of the gradient (one sample or a mini-batch average).
"""

import random
from collections.abc import Callable

Vector = list[float]


def sgd(
    oracle: Callable[[Vector, random.Random], Vector],
    x0: Vector,
    step: Callable[[int], float] | float,
    iters: int,
    rng: random.Random,
    project: Callable[[Vector], Vector] | None = None,
) -> list[Vector]:
    """Return [x_0, ..., x_iters]. step is a constant or a function of k; project is optional."""
    x = list(x0)  # @line L1
    xs = [x]
    for k in range(iters):  # @line L2
        eta = step(k) if callable(step) else step
        g = oracle(x, rng)  # @line L3
        x = [a - eta * b for a, b in zip(x, g)]  # @line L4
        if project is not None:
            x = project(x)  # @line L5
        xs.append(x)
    return xs  # @line L6


def average(xs: list[Vector], weights: list[float] | None = None) -> Vector:
    """The (weighted) average of the points, the output that carries the convex rate."""
    if weights is None:
        weights = [1.0] * len(xs)
    total = sum(weights)
    return [sum(w * x[i] for w, x in zip(weights, xs)) / total for i in range(len(xs[0]))]


def minibatch(sample_grad: Callable[[Vector, random.Random], Vector], size: int) -> Callable[[Vector, random.Random], Vector]:
    """Average `size` independent sample gradients; the variance drops by the factor 1/size."""

    def oracle(x: Vector, rng: random.Random) -> Vector:
        total = [0.0] * len(x)
        for _ in range(size):
            g = sample_grad(x, rng)
            total = [a + b for a, b in zip(total, g)]
        return [a / size for a in total]

    return oracle
