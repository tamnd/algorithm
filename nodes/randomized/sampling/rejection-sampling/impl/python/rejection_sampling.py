# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rejection-sampling/. The authors are listed in prov/TF4M5C.jsonl.

"""Rejection sampling (von Neumann, 1951).

To sample the density f, draw Y from a proposal g and accept it with
probability f(Y) / (M g(Y)), where f <= M g everywhere. Each try is accepted
with probability 1 / M (or Z / M if f is known only up to the constant Z),
and the accepted Y has density f. The real-valued form is exact only in
exact arithmetic; the discrete form with integer weights is exact.
"""

import math
import random
from typing import Callable, List, Sequence, Tuple


def rejection_sample_counted(
    f: Callable[[float], float],
    g_sample: Callable[[random.Random], float],
    g: Callable[[float], float],
    m: float,
    rng: random.Random,
) -> Tuple[float, int]:
    """Return (y, tries): y has density proportional to f, given f <= m g."""
    tries = 0
    while True:  # @line L1
        tries += 1
        y = g_sample(rng)  # @line L2
        u = rng.random()  # @line L3
        if u * m * g(y) <= f(y):  # @line L4
            return y, tries  # @line L5


def rejection_sample(f, g_sample, g, m, rng) -> float:
    y, _ = rejection_sample_counted(f, g_sample, g, m, rng)
    return y


def rejection_discrete(weights: Sequence[int], rng) -> int:
    """Index i with probability weights[i] / sum(weights), exactly.

    Proposal: a uniform index. Envelope: the maximum weight. A try is
    accepted with probability W / (n * max(weights)).
    """
    n = len(weights)
    wmax = max(weights)
    if wmax <= 0 or min(weights) < 0:
        raise ValueError("weights must be non-negative with a positive maximum")
    while True:
        i = rng.randrange(n)
        t = rng.randrange(wmax)
        if t < weights[i]:
            return i


SQRT_2E_OVER_PI = math.sqrt(2.0 * math.e / math.pi)


def normal_from_exponential(rng: random.Random) -> float:
    """A standard normal variate: half-normal by rejection from Exp(1), then a sign.

    f(y) = sqrt(2 / pi) exp(-y^2 / 2), g(y) = exp(-y), and f / g is at most
    M = sqrt(2 e / pi), at y = 1.
    """
    y = rejection_sample(
        lambda x: math.sqrt(2.0 / math.pi) * math.exp(-0.5 * x * x),
        lambda r: -math.log(1.0 - r.random()),
        lambda x: math.exp(-x),
        SQRT_2E_OVER_PI,
        rng,
    )
    return y if rng.random() < 0.5 else -y


def beta22(rng: random.Random) -> float:
    """Beta(2, 2), density 6 x (1 - x), from the uniform proposal with M = 3 / 2."""
    return rejection_sample(lambda x: 6.0 * x * (1.0 - x), lambda r: r.random(), lambda x: 1.0, 1.5, rng)


def acceptance_probability(weights: Sequence[int]) -> Tuple[int, int]:
    """The exact acceptance probability of rejection_discrete as (numerator, denominator)."""
    return sum(weights), len(weights) * max(weights)


def target(weights: Sequence[int]) -> List[float]:
    s = sum(weights)
    return [w / s for w in weights]
