# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-gradient-sign-method/. The authors are listed in prov/96QQ15.jsonl.

"""The fast gradient sign method of Goodfellow, Shlens and Szegedy (2015), on synthetic models only.

The tests run it on a seeded logistic model and a seeded two-layer ReLU network from
mlkit. Nothing here reads real data or touches a real system.
"""

from typing import Callable, Sequence

Vector = list[float]
Gradient = Callable[[Vector, int], Vector]


def sign(t: float) -> float:
    """The sign function with sign(0) = 0."""
    if t > 0:
        return 1.0
    if t < 0:
        return -1.0
    return 0.0


def fast_gradient_sign_method(grad: Gradient, x: Sequence[float], y: int, epsilon: float) -> Vector:
    """One FGSM step: x' = clip01(x + epsilon sign(grad(x, y))).

    grad(x, y) returns the gradient in the input of the loss L(theta, x, y) of a fixed
    model. Precondition: x in [0, 1]^d and epsilon >= 0. The result lies in
    B_inf(x, epsilon) intersected with [0, 1]^d. Cost: one gradient call and O(d).
    """
    g = grad(list(x), y)  # @line L1
    out: Vector = []
    for i in range(len(x)):  # @line L2
        v = x[i] + epsilon * sign(g[i])  # @line L3
        out.append(min(max(v, 0.0), 1.0))  # @line L4
    return out  # @line L5


def targeted_fgsm(grad: Gradient, x: Sequence[float], target: int, epsilon: float) -> Vector:
    """The targeted variant: x' = clip01(x - epsilon sign(grad(x, target))), a step down the loss of the target label."""
    g = grad(list(x), target)
    return [min(max(x[i] - epsilon * sign(g[i]), 0.0), 1.0) for i in range(len(x))]
