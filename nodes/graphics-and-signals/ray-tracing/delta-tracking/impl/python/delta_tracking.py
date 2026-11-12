# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delta-tracking/. The authors are listed in prov/Y968MV.jsonl.

"""Delta tracking (Woodcock tracking) and ratio tracking along one ray.

The medium is given as a function sigma_t(t) >= 0 of the distance t along the ray,
on the segment [0, t_max). The majorant is a constant mu with sigma_t(t) <= mu on the segment.
"""

import math
import random
from collections.abc import Callable

Sigma = Callable[[float], float]


def _check(s: float, majorant: float) -> None:
    if s < 0.0 or s > majorant:
        raise ValueError(f"sigma_t = {s} is not in [0, majorant = {majorant}]")


def delta_tracking(sigma_t: Sigma, majorant: float, t_max: float, rng: random.Random) -> tuple[float | None, int]:
    """Sample a free-flight distance.

    Return (t, steps). t is the distance of the first real collision, or None if the ray
    leaves the segment [0, t_max) first. steps is the number of tentative collisions.
    """
    if majorant <= 0.0:
        raise ValueError("the majorant must be positive")
    t = 0.0  # @line L1
    steps = 0
    while True:  # @line L2
        t -= math.log(1.0 - rng.random()) / majorant  # @line L3
        if t >= t_max:  # @line L4
            return None, steps
        steps += 1
        u = rng.random()  # @line L5
        s = sigma_t(t)
        _check(s, majorant)
        if u * majorant < s:  # @line L6
            return t, steps
        continue  # @line L7


def track_length_transmittance(sigma_t: Sigma, majorant: float, t_max: float, rng: random.Random) -> float:
    """One sample of the transmittance: 1 if delta tracking escapes, else 0."""
    t, _ = delta_tracking(sigma_t, majorant, t_max, rng)
    return 1.0 if t is None else 0.0


def ratio_tracking(sigma_t: Sigma, majorant: float, t_max: float, rng: random.Random) -> float:
    """One sample of the transmittance by ratio tracking: the product of 1 - sigma_t / mu
    over the tentative collisions in [0, t_max)."""
    if majorant <= 0.0:
        raise ValueError("the majorant must be positive")
    t, weight = 0.0, 1.0  # @line L8
    while True:  # @line L9
        t -= math.log(1.0 - rng.random()) / majorant  # @line L10
        if t >= t_max:  # @line L11
            return weight
        s = sigma_t(t)
        _check(s, majorant)
        weight *= 1.0 - s / majorant  # @line L12


def estimate_transmittance(sigma_t: Sigma, majorant: float, t_max: float, n: int, rng: random.Random, method: str = "delta") -> tuple[float, float]:
    """Mean of n samples and the standard error of the mean."""
    one = track_length_transmittance if method == "delta" else ratio_tracking
    total = 0.0
    total2 = 0.0
    for _ in range(n):
        x = one(sigma_t, majorant, t_max, rng)
        total += x
        total2 += x * x
    mean = total / n
    var = max(total2 / n - mean * mean, 0.0) * n / (n - 1)
    return mean, math.sqrt(var / n)
