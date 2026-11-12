# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/logistic-loss/. The authors are listed in prov/XQYJDD.jsonl.
"""The logistic loss log(1 + exp(-y f)), computed without overflow, and its gradient."""

import math


def softplus(t: float) -> float:
    """log(1 + exp(t)) for any real t: max(t, 0) + log1p(exp(-|t|))."""
    return max(t, 0.0) + math.log1p(math.exp(-abs(t)))


def sigmoid(t: float) -> float:
    """1 / (1 + exp(-t)) without overflow for large |t|."""
    if t >= 0:
        return 1.0 / (1.0 + math.exp(-t))
    e = math.exp(t)
    return e / (1.0 + e)


def logistic_loss(y: int, f: float) -> float:
    """Loss for a label y in {-1, +1} and a real score f."""
    if y not in (-1, 1):
        raise ValueError("labels must be -1 or +1")
    return softplus(-y * f)


def binary_cross_entropy(t: int, f: float) -> float:
    """The same loss for a label t in {0, 1}: -t log s(f) - (1 - t) log(1 - s(f)), s the sigmoid."""
    if t not in (0, 1):
        raise ValueError("labels must be 0 or 1")
    return softplus(f) - t * f


def loss_derivative(y: int, f: float) -> float:
    """d/df log(1 + exp(-y f)) = -y * sigmoid(-y f)."""
    return -y * sigmoid(-y * f)


def dot(a: list[float], b: list[float]) -> float:
    return sum(u * v for u, v in zip(a, b))


def risk(w: list[float], xs: list[list[float]], ys: list[int]) -> float:
    """Empirical risk of the linear score f(x) = w . x."""
    return sum(logistic_loss(y, dot(w, x)) for x, y in zip(xs, ys)) / len(xs)


def risk_gradient(w: list[float], xs: list[list[float]], ys: list[int]) -> list[float]:
    g = [0.0] * len(w)
    for x, y in zip(xs, ys):
        c = loss_derivative(y, dot(w, x)) / len(xs)
        for j, xj in enumerate(x):
            g[j] += c * xj
    return g


def smoothness_bound(xs: list[list[float]]) -> float:
    """A Lipschitz constant of risk_gradient: (1/4) * mean of ||x_i||^2."""
    return sum(dot(x, x) for x in xs) / (4 * len(xs))
