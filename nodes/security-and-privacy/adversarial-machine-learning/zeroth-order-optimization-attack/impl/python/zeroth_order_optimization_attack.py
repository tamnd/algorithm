# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zeroth-order-optimization-attack/. The authors are listed in prov/7Y1PKM.jsonl.

"""The ZOO attack of Chen et al. (2017), untargeted, with coordinate-wise Adam, on synthetic models only.

The attack sees only the probability vector that the model returns for a query. It
estimates one partial derivative at a time with a symmetric difference. The model is a
Python function from an input to probabilities; the tests build it from seeded affine
models and seeded ReLU networks of mlkit. Nothing here reads real data or touches a
real system.
"""

import math
import random
from typing import Callable, Optional, Sequence

Vector = list[float]
Scores = Callable[[Vector], Vector]


def log_margin(p: Sequence[float], y: int, kappa: float) -> float:
    """max(ln p_y - max over i != y of ln p_i, -kappa). Probabilities are floored at 1e-300."""
    ly = math.log(max(p[y], 1e-300))
    lo = max(math.log(max(p[i], 1e-300)) for i in range(len(p)) if i != y)
    return max(ly - lo, -kappa)


def objective(scores: Scores, x: Sequence[float], u: Sequence[float], y: int, c: float, kappa: float) -> float:
    """The loss ||u - x||^2 + c * log_margin(scores(u), y, kappa). One query."""
    d2 = math.fsum((a - b) ** 2 for a, b in zip(u, x))
    return d2 + c * log_margin(scores(list(u)), y, kappa)


def coordinate_estimate(scores: Scores, x: Sequence[float], u: Sequence[float], y: int, c: float, kappa: float,
                        i: int, h: float) -> float:
    """Symmetric difference estimate of the i-th partial derivative of the objective. Two queries."""
    up, dn = list(u), list(u)
    up[i] += h
    dn[i] -= h
    return (objective(scores, x, up, y, c, kappa) - objective(scores, x, dn, y, c, kappa)) / (2.0 * h)


def zoo_attack(scores: Scores, x: Sequence[float], y: int, rng: random.Random, c: float = 1.0,
               kappa: float = 0.0, steps: int = 1000, lr: float = 0.01, h: float = 1e-4) -> tuple[Optional[Vector], int]:
    """Run ZOO-ADAM from x with a fixed constant c.

    Every step picks one coordinate at random, estimates its partial derivative with two
    queries, takes one Adam step on it (beta1 0.9, beta2 0.999) and clips it to [0, 1];
    a third query checks the label. Returns (the closest input found whose label is not
    y, or None, and the number of queries). Precondition: x in [0, 1]^d.
    Cost: 3 queries and O(d) work per step.
    """
    d = len(x)
    u = list(x)  # @line L1
    mom, vel, cnt = [0.0] * d, [0.0] * d, [0] * d
    best, best_d, queries = None, math.inf, 0
    for _ in range(steps):  # @line L2
        i = rng.randrange(d)  # @line L3
        g = coordinate_estimate(scores, x, u, y, c, kappa, i, h)  # @line L4
        cnt[i] += 1  # @line L5
        mom[i] = 0.9 * mom[i] + 0.1 * g
        vel[i] = 0.999 * vel[i] + 0.001 * g * g
        mh = mom[i] / (1 - 0.9 ** cnt[i])
        vh = vel[i] / (1 - 0.999 ** cnt[i])
        u[i] = min(max(u[i] - lr * mh / (math.sqrt(vh) + 1e-8), 0.0), 1.0)  # @line L6
        p = scores(list(u))  # @line L7
        queries += 3
        dist = math.sqrt(math.fsum((a - b) ** 2 for a, b in zip(u, x)))
        if max(range(len(p)), key=lambda k: p[k]) != y and dist < best_d:
            best, best_d = list(u), dist
    return best, queries  # @line L8
