# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pgd-attack/. The authors are listed in prov/YAKX8W.jsonl.

"""The projected gradient descent attack of Madry et al. (2018), on synthetic models only.

The tests run it on a seeded logistic model and a seeded two-layer ReLU network from
mlkit. Nothing here reads real data or touches a real system.
"""

import math
import random
from typing import Callable, Sequence

Vector = list[float]
Gradient = Callable[[Vector, int], Vector]
Loss = Callable[[Vector, int], float]


def sign(t: float) -> float:
    """The sign function with sign(0) = 0."""
    return 1.0 if t > 0 else (-1.0 if t < 0 else 0.0)


def project(v: Sequence[float], x: Sequence[float], epsilon: float, norm: str) -> Vector:
    """Map v into B_p(x, epsilon) intersected with [0, 1]^d, for norm "inf" or "2".

    For "inf" this is the exact Euclidean projection: the set is a box, so clip each
    coordinate to [max(x_i - epsilon, 0), min(x_i + epsilon, 1)]. For "2" it rescales
    v - x onto the ball and then clips to [0, 1]; the clip cannot leave the ball
    because it moves each coordinate toward x_i in [0, 1]. Cost O(d).
    """
    if norm == "inf":
        return [min(max(a, c - epsilon, 0.0), c + epsilon, 1.0) for a, c in zip(v, x, strict=True)]
    diff = [a - c for a, c in zip(v, x, strict=True)]
    r = math.sqrt(math.fsum(t * t for t in diff))
    f = 1.0 if r <= epsilon else epsilon / r
    return [min(max(c + f * t, 0.0), 1.0) for c, t in zip(x, diff)]


def ascent_direction(g: Sequence[float], norm: str) -> Vector:
    """The steepest ascent step of unit size for the norm: sign(g) for l_inf, g / ||g||_2 for l2."""
    if norm == "inf":
        return [sign(t) for t in g]
    r = math.sqrt(math.fsum(t * t for t in g))
    return [0.0] * len(g) if r == 0 else [t / r for t in g]


def random_start(rng: random.Random, x: Sequence[float], epsilon: float, norm: str) -> Vector:
    """A random point of the ball: uniform in the l_inf box, or uniform in the l2 ball; then mapped into [0, 1]^d."""
    d = len(x)
    if norm == "inf":
        u = [rng.uniform(-epsilon, epsilon) for _ in range(d)]
    else:
        u = [rng.gauss(0.0, 1.0) for _ in range(d)]
        r = math.sqrt(math.fsum(t * t for t in u)) or 1.0
        rad = epsilon * rng.random() ** (1.0 / d) if d else 0.0
        u = [rad * t / r for t in u]
    return project([a + b for a, b in zip(x, u)], x, epsilon, norm)


def pgd_attack(grad: Gradient, loss: Loss, x: Sequence[float], y: int, epsilon: float, alpha: float,
               steps: int, norm: str = "inf", rng: random.Random | None = None) -> Vector:
    """PGD on the loss over B_p(x, epsilon) cap [0, 1]^d. Returns the iterate with the largest loss.

    grad(x, y) and loss(x, y) are the input gradient and the loss of a fixed model.
    With rng the start is a random point of the ball; without it the start is x.
    Precondition: x in [0, 1]^d, epsilon >= 0, alpha > 0, steps >= 0.
    Cost: steps gradient calls, steps + 1 loss calls and O(steps d) more.
    """
    xt = random_start(rng, x, epsilon, norm) if rng is not None else list(x)  # @line L1
    best, best_loss = xt, loss(xt, y)  # @line L2
    for _ in range(steps):  # @line L3
        g = grad(xt, y)  # @line L4
        step = ascent_direction(g, norm)
        xt = project([a + alpha * s for a, s in zip(xt, step)], x, epsilon, norm)  # @line L5
        lt = loss(xt, y)  # @line L6
        if lt > best_loss:
            best, best_loss = xt, lt
    return best  # @line L7
