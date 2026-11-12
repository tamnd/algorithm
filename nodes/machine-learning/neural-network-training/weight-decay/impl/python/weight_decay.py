# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weight-decay/. The authors are listed in prov/TNFCZV.jsonl.
"""Weight decay in its two forms: an L2 penalty (lam / 2) ||theta||^2 added to the loss, and decoupled
weight decay theta <- (1 - decay) theta - alpha grad f (Hanson and Pratt; Loshchilov and Hutter).
For plain SGD the two are equal with lam = decay / alpha; with momentum or Adam they differ.
"""

import math

Vec = list


def sgd_l2_step(theta: Vec, grad: Vec, alpha, lam) -> Vec:
    """Gradient step on f + (lam / 2) ||theta||^2: theta - alpha (grad f + lam theta)."""
    return [t - alpha * (g + lam * t) for t, g in zip(theta, grad)]


def sgd_decoupled_step(theta: Vec, grad: Vec, alpha, decay) -> Vec:
    """Decoupled weight decay: theta <- (1 - decay) theta - alpha grad f."""
    return [(1 - decay) * t - alpha * g for t, g in zip(theta, grad)]


def momentum_l2_step(theta: Vec, buf: Vec, grad: Vec, alpha, mu, lam) -> tuple[Vec, Vec]:
    """Heavy-ball momentum on f + (lam / 2) ||theta||^2: the penalty gradient enters the buffer."""
    buf = [mu * b + g + lam * t for b, g, t in zip(buf, grad, theta)]
    return [t - alpha * b for t, b in zip(theta, buf)], buf


def momentum_decoupled_step(theta: Vec, buf: Vec, grad: Vec, alpha, mu, decay) -> tuple[Vec, Vec]:
    """Momentum on f only, then decoupled decay of the weights (SGDW of Loshchilov and Hutter)."""
    buf = [mu * b + g for b, g in zip(buf, grad)]
    return [(1 - decay) * t - alpha * b for t, b in zip(theta, buf)], buf


class Adam:
    """Adam with either an L2 penalty folded into the gradient or decoupled weight decay (AdamW)."""

    def __init__(self, n: int, alpha: float, lam: float, decoupled: bool,
                 beta1: float = 0.9, beta2: float = 0.999, eps: float = 1e-8) -> None:
        self.m = [0.0] * n
        self.v = [0.0] * n
        self.t = 0
        self.alpha, self.lam, self.decoupled = alpha, lam, decoupled
        self.beta1, self.beta2, self.eps = beta1, beta2, eps

    def step(self, theta: Vec, grad: Vec) -> Vec:
        if not self.decoupled:
            grad = [g + self.lam * t for g, t in zip(grad, theta)]
        self.t += 1
        b1, b2 = self.beta1, self.beta2
        self.m = [b1 * m + (1 - b1) * g for m, g in zip(self.m, grad)]
        self.v = [b2 * v + (1 - b2) * g * g for v, g in zip(self.v, grad)]
        c1, c2 = 1 - b1 ** self.t, 1 - b2 ** self.t
        decay = self.alpha * self.lam if self.decoupled else 0.0
        return [(1 - decay) * t - self.alpha * (m / c1) / (math.sqrt(v / c2) + self.eps)
                for t, m, v in zip(theta, self.m, self.v)]


def quadratic_grad(h: list, target: Vec, theta: Vec) -> Vec:
    """Gradient of f(theta) = (1/2) (theta - target)^T H (theta - target)."""
    d = [t - c for t, c in zip(theta, target)]
    return [sum(hij * dj for hij, dj in zip(row, d)) for row in h]
