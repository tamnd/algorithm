# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adversarial-training/. The authors are listed in prov/SQBJ92.jsonl.

"""Adversarial training with FGSM and PGD attacks under an l_inf budget.

The model is a linear classifier f(x) = w.x + b with labels y in {-1, +1} and
the logistic loss l(m) = log(1 + exp(-m)) of the margin m = y f(x). For this
model the inner maximization of Madry et al. has the closed form

    max_{||d||_inf <= eps} l(y (w.(x + d) + b)) = l(y (w.x + b) - eps ||w||_1),

which the tests use to check the attacks. Training follows Madry et al.: for
each example find a perturbation with PGD, then take a gradient step on the
loss at the perturbed input (Danskin's theorem).
"""

import math
from typing import Callable, List, Sequence, Tuple

Vector = List[float]


def sign(a: float) -> int:
    return (a > 0) - (a < 0)


def logistic_loss(m: float) -> float:
    """log(1 + exp(-m)), computed without overflow."""
    return max(-m, 0.0) + math.log1p(math.exp(-abs(m)))


def logistic_loss_slope(m: float) -> float:
    """d/dm log(1 + exp(-m)) = -1 / (1 + exp(m))."""
    if m >= 0:
        e = math.exp(-m)
        return -e / (1.0 + e)
    return -1.0 / (1.0 + math.exp(m))


def margin(w: Sequence[float], b: float, x: Sequence[float], y: int) -> float:
    return y * (sum(a * c for a, c in zip(w, x)) + b)


def loss(w, b, x, y) -> float:
    return logistic_loss(margin(w, b, x, y))


def input_gradient(w, b, x, y) -> Vector:
    """The gradient of the loss with respect to the input x."""
    s = logistic_loss_slope(margin(w, b, x, y))
    return [s * y * a for a in w]


def worst_case_margin(w, b, x, y, eps: float) -> float:
    """min over ||d||_inf <= eps of y (w.(x + d) + b) = y (w.x + b) - eps ||w||_1."""
    return margin(w, b, x, y) - eps * sum(abs(a) for a in w)


def robust_loss(w, b, x, y, eps: float) -> float:
    """The exact inner maximum for the linear model: l(worst case margin)."""
    return logistic_loss(worst_case_margin(w, b, x, y, eps))


def fgsm(grad_x: Callable[[Vector], Vector], x: Sequence[float], eps: float) -> Vector:
    """Fast gradient sign method: x + eps sign(grad_x loss(x))."""
    g = grad_x(list(x))
    return [a + eps * sign(c) for a, c in zip(x, g)]


def project_linf(z: Sequence[float], x: Sequence[float], eps: float) -> Vector:
    """Projection onto the l_inf ball of radius eps around x: clip each coordinate."""
    return [min(max(a, c - eps), c + eps) for a, c in zip(z, x)]


def pgd(grad_x: Callable[[Vector], Vector], x: Sequence[float], eps: float, step: float, steps: int,
        rng=None) -> Vector:
    """Projected gradient ascent with sign steps (Madry et al.).

    With rng given, start at a uniform random point of the ball; else at x.
    Each step: z <- project(z + step * sign(grad_x loss(z))).
    """
    if rng is None:
        z = list(x)
    else:
        z = [a + rng.uniform(-eps, eps) for a in x]
    for _ in range(steps):
        g = grad_x(z)
        z = project_linf([a + step * sign(c) for a, c in zip(z, g)], x, eps)
    return z


def adversarial_train(data: Sequence[Tuple[Sequence[float], int]], eps: float, eta: float, epochs: int,
                      attack_steps: int = 10, rng=None) -> Tuple[Vector, float]:
    """Full batch adversarial training of the linear logistic model.

    eps = 0 is standard training. The inner problem is solved by PGD with
    step 2.5 eps / attack_steps; the outer step uses the gradient of the loss
    at the perturbed input.
    """
    d = len(data[0][0])
    w, b = [0.0] * d, 0.0
    for _ in range(epochs):
        gw, gb = adversarial_gradient(w, b, data, eps, attack_steps, rng)
        w = [a - eta * g for a, g in zip(w, gw)]
        b -= eta * gb
    return w, b


def adversarial_gradient(w, b, data, eps: float, attack_steps: int = 10, rng=None) -> Tuple[Vector, float]:
    """The mean gradient in (w, b) of the loss at the PGD points: the outer step of Madry et al.

    By Danskin's theorem this is the gradient of the mean robust loss when the
    attack finds the maximizer and the maximizer is unique.
    """
    d = len(w)
    gw, gb = [0.0] * d, 0.0
    for x, y in data:
        if eps > 0:
            xa = pgd(lambda z: input_gradient(w, b, z, y), x, eps, 2.5 * eps / attack_steps, attack_steps, rng)
        else:
            xa = x
        s = logistic_loss_slope(margin(w, b, xa, y)) * y
        for j in range(d):
            gw[j] += s * xa[j]
        gb += s
    n = len(data)
    return [g / n for g in gw], gb / n


def robust_accuracy(w, b, data, eps: float) -> float:
    """The fraction of examples whose worst case margin is positive."""
    return sum(worst_case_margin(w, b, x, y, eps) > 0 for x, y in data) / len(data)
