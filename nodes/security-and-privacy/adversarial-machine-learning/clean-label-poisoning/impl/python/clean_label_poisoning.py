# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clean-label-poisoning/. The authors are listed in prov/9VQR2S.jsonl.

"""Clean-label poisoning by forward-backward splitting (Shafahi et al. 2018), as an abstract model on synthetic data.

The poison x minimizes F(x) = ||f(x) - f(t)||^2 + beta ||x - b||^2 over the box [0, 1]^d,
where f is a feature map, t the target input and b the base input. The feature maps
here are a fixed linear map and the hidden layer of a seeded tiny_relu_net from mlkit;
the tests build every input from a fixed seed. Nothing here reads a real data set or
touches a real model.
"""

import math
from typing import Callable, Sequence

from mlkit import Net, Vector, dot

GradFn = Callable[[Sequence[float]], Vector]


def linear_features(a: Sequence[Sequence[float]], x: Sequence[float]) -> Vector:
    """f(x) = A x for a k by d matrix A. Cost O(k d)."""
    return [dot(row, x) for row in a]


def linear_collision_grad(a: Sequence[Sequence[float]], target: Sequence[float]) -> GradFn:
    """The gradient map x -> 2 A^T (A x - A t) of ||A x - A t||^2. Cost O(k d) per call."""
    ft = linear_features(a, target)

    def grad(x: Sequence[float]) -> Vector:
        r = [u - v for u, v in zip(linear_features(a, x), ft, strict=True)]
        return [2.0 * math.fsum(r[i] * a[i][j] for i in range(len(a))) for j in range(len(x))]

    return grad


def relu_features(net: Net, x: Sequence[float]) -> Vector:
    """f(x) = relu(W1 x + b1), the hidden layer of a tiny_relu_net. Cost O(h d)."""
    return [max(dot(row, x) + bi, 0.0) for row, bi in zip(net["W1"], net["b1"], strict=True)]


def relu_collision_grad(net: Net, target: Sequence[float]) -> GradFn:
    """The gradient map of ||f(x) - f(t)||^2 for the ReLU features, 2 W1^T (relu'(pre) * (f(x) - f(t))).

    The derivative of the ReLU is taken as 0 at a pre-activation of exactly 0. Cost O(h d) per call.
    """
    ft = relu_features(net, target)

    def grad(x: Sequence[float]) -> Vector:
        g = [0.0] * len(x)
        for row, bi, fi in zip(net["W1"], net["b1"], ft, strict=True):
            pre = dot(row, x) + bi
            if pre > 0:
                c = 2.0 * (pre - fi)
                for j in range(len(x)):
                    g[j] += c * row[j]
        return g

    return grad


def objective(features: Callable[[Sequence[float]], Vector], x: Sequence[float], target: Sequence[float], base: Sequence[float], beta: float) -> float:
    """F(x) = ||f(x) - f(t)||^2 + beta ||x - b||^2. Cost: two calls of f and O(d)."""
    fx, ft = features(x), features(target)
    return math.fsum((u - v) ** 2 for u, v in zip(fx, ft, strict=True)) + beta * math.fsum(
        (u - v) ** 2 for u, v in zip(x, base, strict=True)
    )


def craft_poison(grad: GradFn, base: Sequence[float], beta: float, lam: float, steps: int, tol: float = 0.0) -> Vector:
    """Forward-backward splitting for min F over [0, 1]^d, started at the base.

    The forward step is a gradient step of size lam on the collision term; the backward
    step is the exact proximal step of beta ||x - b||^2 plus the box, which is the clip
    of (x_hat + 2 lam beta b) / (1 + 2 lam beta). Stops after steps iterations or when
    no coordinate moves by more than tol. Precondition: base in [0, 1]^d, beta > 0,
    lam > 0 (at most 1/L for a collision term whose gradient is L-Lipschitz).
    Cost O(steps (g + d)), where g is the cost of one call of grad.
    """
    x = list(base)  # @line L1
    c = 2.0 * lam * beta
    for _ in range(steps):  # @line L2
        g = grad(x)
        x_hat = [xj - lam * gj for xj, gj in zip(x, g, strict=True)]  # @line L3
        new = [min(max((h + c * bj) / (1.0 + c), 0.0), 1.0) for h, bj in zip(x_hat, base, strict=True)]  # @line L4
        moved = max(abs(u - v) for u, v in zip(new, x))
        x = new
        if moved <= tol:
            break
    return x  # @line L5
