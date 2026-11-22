# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boundary-attack/. The authors are listed in prov/0K6SWG.jsonl.

"""The boundary attack of Brendel, Rauber and Bethge (2018), untargeted l2 version, on synthetic models only.

The attack sees only the label that the model returns for a query. The model is a
Python function from an input to a label; the tests build it from seeded affine models
and seeded ReLU networks of mlkit. Nothing here reads real data or touches a real system.
"""

import math
import random
from typing import Callable, Sequence

Vector = list[float]
Label = Callable[[Vector], int]


def _dist(u: Sequence[float], v: Sequence[float]) -> float:
    return math.sqrt(math.fsum((a - b) ** 2 for a, b in zip(u, v)))


def _clip(v: Sequence[float]) -> Vector:
    return [min(max(a, 0.0), 1.0) for a in v]


def candidate(x: Sequence[float], adv: Sequence[float], noise: Sequence[float], alpha: float,
              beta: float) -> tuple[Vector, Vector]:
    """The orthogonal candidate and the full candidate of one step.

    The noise is scaled to length alpha * D, where D = ||adv - x||, and added to adv. The
    sum is moved back to the sphere of radius D around x: this is the orthogonal
    candidate. The full candidate then moves a fraction beta of the way to x. Both are
    clipped to [0, 1]^d. Precondition: adv != x and noise != 0. Cost O(d).
    """
    dist = _dist(adv, x)
    nn = math.sqrt(math.fsum(t * t for t in noise))
    moved = [a + alpha * dist * t / nn for a, t in zip(adv, noise)]
    back = dist / _dist(moved, x)
    ortho = [c + (a - c) * back for a, c in zip(moved, x)]
    full = [a + beta * (c - a) for a, c in zip(ortho, x)]
    return _clip(ortho), _clip(full)


def boundary_attack(label: Label, x: Sequence[float], y: int, start: Sequence[float], steps: int,
                    rng: random.Random, alpha: float = 0.1, beta: float = 0.1) -> tuple[Vector, int]:
    """Walk along the boundary from the adversarial input start toward x.

    Every step costs at most two label queries. Every 10 steps the step sizes adapt: alpha
    grows by 1.5 when more than half of the orthogonal candidates were adversarial and
    shrinks otherwise; beta grows by 1.5 when more than a fifth of the full candidates
    were accepted and shrinks otherwise, and stays below 0.9. Returns (the adversarial
    input, the number of label queries). Preconditions: label(start) != y and start in
    [0, 1]^d. Cost O(steps d) plus the queries.
    """
    adv = list(start)  # @line L1
    queries = 0
    ortho_ok = full_ok = 0
    for t in range(1, steps + 1):  # @line L2
        if adv == list(x):
            break
        noise = [rng.gauss(0.0, 1.0) for _ in x]  # @line L3
        ortho, full = candidate(x, adv, noise, alpha, beta)  # @line L4
        queries += 1
        if label(ortho) != y:  # @line L5
            ortho_ok += 1
            queries += 1
            if label(full) != y:  # @line L6
                adv = full
                full_ok += 1
        if t % 10 == 0:  # @line L7
            alpha = alpha * 1.5 if ortho_ok > 5 else alpha / 1.5
            beta = min(beta * 1.5, 0.9) if full_ok > 2 else beta / 1.5
            ortho_ok = full_ok = 0
    return adv, queries  # @line L8
