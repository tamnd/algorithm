# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/perceptron/. The authors are listed in prov/83YNZY.jsonl.

"""Rosenblatt's perceptron for labels in {-1, +1}, with two classic variants.

The bias is the weight of a constant extra feature c. With c = 1 the bias
update is b <- b + y. With a general c, the extra weight w0 has b = c * w0, so
the update w0 <- w0 + y * c is b <- b + y * c * c.
"""

import random
from typing import Callable, Optional, Sequence

Vector = Sequence[float]


def dot(u: Vector, v: Vector) -> float:
    return sum(a * b for a, b in zip(u, v))


def perceptron(
    xs: Sequence[Vector],
    ys: Sequence[int],
    max_epochs: int = 1000,
    bias: bool = True,
    c: float = 1.0,
    rng: Optional[random.Random] = None,
) -> tuple[list[float], float, int, bool]:
    """Run the perceptron until an epoch has no mistake or max_epochs pass.

    Returns (w, b, mistakes, converged). A mistake is y * (w . x + b) <= 0, so
    a point on the hyperplane counts as a mistake. If rng is given, each epoch
    visits the examples in a new random order.
    """
    d = len(xs[0]) if xs else 0
    w = [0.0] * d  # @line L1
    b = 0.0
    mistakes = 0
    order = list(range(len(xs)))
    for _ in range(max_epochs):  # @line L2
        if rng is not None:
            rng.shuffle(order)
        errors = 0  # @line L3
        for i in order:  # @line L4
            x, y = xs[i], ys[i]
            if y * (dot(w, x) + b) <= 0:  # @line L5
                for j in range(d):  # @line L6
                    w[j] += y * x[j]
                if bias:
                    b += y * c * c  # @line L7
                errors += 1  # @line L8
        mistakes += errors
        if errors == 0:  # @line L9
            return w, b, mistakes, True
    return w, b, mistakes, False  # @line L10


def averaged_perceptron(
    xs: Sequence[Vector], ys: Sequence[int], epochs: int
) -> tuple[list[float], float]:
    """Return the mean of the weight vectors after each example (bias c = 1).

    The run does exactly `epochs` passes in the given order. The sum is kept
    with the usual trick: a weight added at step t counts (T - t + 1) times.
    """
    d = len(xs[0]) if xs else 0
    w = [0.0] * d
    b = 0.0
    sw = [0.0] * d
    sb = 0.0
    steps = 0
    for _ in range(epochs):
        for x, y in zip(xs, ys):
            if y * (dot(w, x) + b) <= 0:
                for j in range(d):
                    w[j] += y * x[j]
                b += y
            for j in range(d):
                sw[j] += w[j]
            sb += b
            steps += 1
    if steps == 0:
        return w, b
    return [s / steps for s in sw], sb / steps


def kernel_perceptron(
    xs: Sequence[Vector],
    ys: Sequence[int],
    kernel: Callable[[Vector, Vector], float],
    max_epochs: int = 1000,
) -> tuple[list[int], bool]:
    """Dual perceptron: f(x) = sum_j a_j y_j (k(x_j, x) + 1).

    a_j counts the mistakes on example j. The +1 is the constant feature of
    the bias. Returns (a, converged).
    """
    n = len(xs)
    gram = [[kernel(xs[i], xs[j]) + 1.0 for j in range(n)] for i in range(n)]
    a = [0] * n
    for _ in range(max_epochs):
        errors = 0
        for i in range(n):
            f = sum(a[j] * ys[j] * gram[j][i] for j in range(n) if a[j])
            if ys[i] * f <= 0:
                a[i] += 1
                errors += 1
        if errors == 0:
            return a, True
    return a, False


def kernel_predict(
    xs: Sequence[Vector],
    ys: Sequence[int],
    a: Sequence[int],
    kernel: Callable[[Vector, Vector], float],
    x: Vector,
) -> int:
    f = sum(a[j] * ys[j] * (kernel(xs[j], x) + 1.0) for j in range(len(xs)) if a[j])
    return 1 if f > 0 else -1
