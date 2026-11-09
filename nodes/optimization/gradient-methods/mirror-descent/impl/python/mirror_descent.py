# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mirror-descent/. The authors are listed in prov/41N7NJ.jsonl.

"""Mirror descent: a subgradient step in the dual space of a mirror map, then a Bregman projection.

Vectors are lists of floats. A geometry is three functions: mirror (the gradient of psi),
inverse (the gradient of the conjugate of psi) and project (the Bregman projection onto C).
Two geometries are given: the entropy on the probability simplex and the Euclidean one.
"""

import math
from collections.abc import Callable

Vector = list[float]


def mirror_descent(
    subgrad: Callable[[Vector], Vector],
    mirror: Callable[[Vector], Vector],
    inverse: Callable[[Vector], Vector],
    project: Callable[[Vector], Vector],
    x0: Vector,
    step: Callable[[int], float] | float,
    iters: int,
) -> list[Vector]:
    """Return [x_0, ..., x_iters]. The step is a constant or a function of k."""
    x = list(x0)  # @line L1
    xs = [x]
    for k in range(iters):  # @line L2
        eta = step(k) if callable(step) else step
        g = subgrad(x)  # @line L3
        theta = [a - eta * b for a, b in zip(mirror(x), g)]  # @line L4
        x = project(inverse(theta))  # @line L5
        xs.append(x)
    return xs  # @line L6


def weighted_average(xs: list[Vector], weights: list[float]) -> Vector:
    """The average sum_k w_k x_k / sum_k w_k, which carries the guarantee of the theorem."""
    total = sum(weights)
    return [sum(w * x[i] for w, x in zip(weights, xs)) / total for i in range(len(xs[0]))]


def entropy_simplex() -> tuple[Callable, Callable, Callable]:
    """psi(x) = sum x_i log x_i on the simplex. The step is x_i <- x_i exp(-eta g_i) / Z.

    inverse returns exp(theta - max theta), which is the gradient of the conjugate up to a
    positive factor; the KL projection onto the simplex (a division by the sum) removes it.
    """

    def mirror(x: Vector) -> Vector:
        return [math.log(a) for a in x]

    def inverse(theta: Vector) -> Vector:
        top = max(theta)
        return [math.exp(t - top) for t in theta]

    def project(y: Vector) -> Vector:
        total = sum(y)
        return [a / total for a in y]

    return mirror, inverse, project


def euclidean(project: Callable[[Vector], Vector]) -> tuple[Callable, Callable, Callable]:
    """psi(x) = ||x||^2 / 2: mirror descent is then the projected subgradient method."""

    def identity(x: Vector) -> Vector:
        return list(x)

    return identity, identity, project


def kl(p: Vector, q: Vector) -> float:
    """The Bregman divergence of the entropy between two points of the simplex."""
    return sum(a * math.log(a / b) for a, b in zip(p, q) if a > 0)
