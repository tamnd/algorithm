# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/svrg/. The authors are listed in prov/F7HP8J.jsonl.

"""Stochastic variance reduced gradient (SVRG) for F(x) = (1/n) sum_i f_i(x).

Each epoch computes the full gradient at a snapshot, then takes m cheap steps along
v = grad f_i(x) - grad f_i(snapshot) + full gradient, which is unbiased for grad F(x).
Vectors are lists of floats; grad(i, x) returns the gradient of the component f_i at x.
"""

import random
from collections.abc import Callable

Vector = list[float]


def full_gradient(grad: Callable[[int, Vector], Vector], n: int, x: Vector) -> Vector:
    total = [0.0] * len(x)
    for i in range(n):
        total = [a + b for a, b in zip(total, grad(i, x))]
    return [a / n for a in total]


def svrg_direction(grad: Callable[[int, Vector], Vector], i: int, x: Vector, snapshot: Vector, mu: Vector) -> Vector:
    """The variance-reduced estimate grad f_i(x) - grad f_i(snapshot) + mu."""
    return [a - b + c for a, b, c in zip(grad(i, x), grad(i, snapshot), mu)]


def svrg(
    grad: Callable[[int, Vector], Vector],
    n: int,
    x0: Vector,
    step: float,
    inner: int,
    epochs: int,
    rng: random.Random,
    option: str = "random",
    indices: list[int] | None = None,
) -> list[Vector]:
    """Return the snapshots [x~_0, ..., x~_epochs].

    option "random" (Option II of Johnson and Zhang) takes the next snapshot uniformly from
    x_0, ..., x_(m-1), which is the version with a proof; option "last" takes x_m.
    If indices is given, it fixes the sampled components, for traces.
    """
    snapshot = list(x0)  # @line L1
    snapshots = [snapshot]
    picks = iter(indices) if indices is not None else None
    for _ in range(epochs):  # @line L2
        mu = full_gradient(grad, n, snapshot)  # @line L3
        x = list(snapshot)  # @line L4
        inner_points = []
        for _ in range(inner):  # @line L5
            i = next(picks) if picks is not None else rng.randrange(n)  # @line L6
            v = svrg_direction(grad, i, x, snapshot, mu)  # @line L7
            inner_points.append(x)
            x = [a - step * b for a, b in zip(x, v)]  # @line L8
        snapshot = rng.choice(inner_points) if option == "random" and inner_points else x  # @line L9
        snapshots.append(snapshot)
    return snapshots  # @line L10
