# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/report-noisy-max/. The authors are listed in prov/GKS5RH.jsonl.
"""Report Noisy Max with Laplace noise (Dwork and Roth, Claim 3.9).

Add independent Laplace noise to each of m scores and release only the index
of the largest noisy score. For counting queries under add/remove neighbors
the scale Delta / epsilon is enough (monotone=True). For scores whose changes
can go in both directions the scale is 2 Delta / epsilon (monotone=False).

Floats and random.Random are used so that the tests are reproducible; a
deployment needs a cryptographic source of randomness and exact sampling.
"""

from __future__ import annotations

import math
import random
from typing import Sequence


def laplace_sample(b: float, rng: random.Random) -> float:
    """One draw of Lap(b) by the inverse CDF. Cost: O(1)."""
    u = rng.random() - 0.5
    while u == -0.5:
        u = rng.random() - 0.5
    return -b * math.copysign(1.0, u) * math.log(1.0 - 2.0 * abs(u))


def noise_scale(sensitivity: float, epsilon: float, monotone: bool = True) -> float:
    """b = Delta / epsilon if the scores are monotone in the data, else 2 Delta / epsilon."""
    if sensitivity <= 0 or epsilon <= 0:
        raise ValueError("need sensitivity > 0 and epsilon > 0")
    return (1.0 if monotone else 2.0) * sensitivity / epsilon


def report_noisy_max(
    scores: Sequence[float],
    epsilon: float,
    rng: random.Random,
    sensitivity: float = 1.0,
    monotone: bool = True,
) -> int:
    """Return the index of the largest score after Lap(b) noise is added to each score.

    Precondition: at least one score; each score has sensitivity at most
    Delta under the chosen neighbor relation; monotone=True only if every
    score moves in the same direction between neighbors. Ties, which have
    probability 0, go to the lowest index. Only the index is released.
    Cost: O(m) for m scores.
    """
    if not scores:
        raise ValueError("need at least one score")
    b = noise_scale(sensitivity, epsilon, monotone)  # @line L1
    best, best_i = -math.inf, -1  # @line L2
    for i, c in enumerate(scores):  # @line L3
        y = c + laplace_sample(b, rng)  # @line L4
        if y > best:  # @line L5
            best, best_i = y, i
    return best_i  # @line L6


def accuracy_gap(b: float, m: int, beta: float) -> float:
    """2 b ln(m / beta): with probability at least 1 - beta, the chosen score is within this of the maximum."""
    if m < 1 or not 0 < beta < 1:
        raise ValueError("need m >= 1 and 0 < beta < 1")
    return 2.0 * b * math.log(m / beta)
