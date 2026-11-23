# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-mechanism/. The authors are listed in prov/B229GK.jsonl.
"""The Gaussian mechanism with the classical and the analytic calibration.

The mechanism adds independent N(0, sigma^2) noise to each coordinate of a
query with l2-sensitivity Delta. The classical calibration of Dwork and Roth
(Theorem 3.22) needs 0 < epsilon < 1. The analytic calibration of Balle and
Wang (2018) finds the smallest sigma with delta(epsilon) <= delta, using the
exact formula

    delta(epsilon) = Phi(Delta / (2 s) - epsilon s / Delta)
                     - e^epsilon Phi(-Delta / (2 s) - epsilon s / Delta).

Floats and random.Random.gauss are used so that the tests are reproducible.
They are not a safe sampler: a deployment needs a cryptographic source of
randomness and an exact sampler such as the discrete Gaussian.
"""

from __future__ import annotations

import math
import random
from typing import Callable, Sequence, TypeVar

X = TypeVar("X")


def normal_cdf(t: float) -> float:
    """Phi(t), the standard normal CDF, from math.erfc. Cost: O(1)."""
    return 0.5 * math.erfc(-t / math.sqrt(2.0))


def classical_sigma(sensitivity: float, epsilon: float, delta: float) -> float:
    """sigma = sqrt(2 ln(1.25 / delta)) Delta / epsilon (Dwork and Roth, Theorem 3.22).

    Precondition: Delta > 0, 0 < epsilon < 1 and 0 < delta < 1. The bound is
    proved only for epsilon < 1, so other values raise. Cost: O(1).
    """
    if sensitivity <= 0 or not 0 < epsilon < 1 or not 0 < delta < 1:
        raise ValueError("need Delta > 0, 0 < epsilon < 1 and 0 < delta < 1")
    return math.sqrt(2.0 * math.log(1.25 / delta)) * sensitivity / epsilon


def analytic_delta(sensitivity: float, sigma: float, epsilon: float) -> float:
    """The exact smallest delta at epsilon for N(0, sigma^2) noise and l2-sensitivity Delta.

    Precondition: Delta > 0, sigma > 0, epsilon >= 0. Cost: O(1).
    """
    if sensitivity <= 0 or sigma <= 0 or epsilon < 0:
        raise ValueError("need Delta > 0, sigma > 0 and epsilon >= 0")
    a = sensitivity / (2.0 * sigma)
    b = epsilon * sigma / sensitivity
    return max(0.0, normal_cdf(a - b) - math.exp(epsilon) * normal_cdf(-a - b))


def analytic_sigma(sensitivity: float, epsilon: float, delta: float, rel_tol: float = 1e-12) -> float:
    """The smallest sigma with analytic_delta(Delta, sigma, epsilon) <= delta, by bisection.

    delta(epsilon) falls as sigma grows, so bisection applies. The returned
    sigma is the upper end of the final bracket, so it is never too small.
    Precondition: Delta > 0, epsilon >= 0, 0 < delta < 1.
    Cost: O(log(1 / rel_tol)) evaluations of analytic_delta.
    """
    if sensitivity <= 0 or epsilon < 0 or not 0 < delta < 1:
        raise ValueError("need Delta > 0, epsilon >= 0 and 0 < delta < 1")
    lo, hi = sensitivity, sensitivity
    while analytic_delta(sensitivity, hi, epsilon) > delta:
        lo, hi = hi, 2.0 * hi
    while analytic_delta(sensitivity, lo, epsilon) <= delta and lo > 1e-300:
        hi, lo = lo, lo / 2.0
    while hi - lo > rel_tol * hi:
        mid = 0.5 * (lo + hi)
        if analytic_delta(sensitivity, mid, epsilon) <= delta:
            hi = mid
        else:
            lo = mid
    return hi


def gaussian_mechanism(
    x: X,
    f: Callable[[X], Sequence[float]],
    sensitivity: float,
    epsilon: float,
    delta: float,
    rng: random.Random,
    analytic: bool = True,
) -> list[float]:
    """Return f(x) + Z with Z_i independent N(0, sigma^2).

    Precondition: f has l2-sensitivity at most Delta under the chosen neighbor
    relation. With analytic=True the output is (epsilon, delta)-DP for any
    epsilon >= 0; with analytic=False it needs 0 < epsilon < 1.
    Cost: O(k) for k coordinates, plus O(log(1 / rel_tol)) for the calibration.
    """
    if analytic:
        sigma = analytic_sigma(sensitivity, epsilon, delta)  # @line L1
    else:
        sigma = classical_sigma(sensitivity, epsilon, delta)  # @line L1
    v = list(f(x))  # @line L2
    y: list[float] = []
    for vi in v:  # @line L3
        z = rng.gauss(0.0, sigma)  # @line L4
        y.append(vi + z)  # @line L5
    return y  # @line L6


def gaussian_log_density(y: float, center: float, sigma: float) -> float:
    """ln of the N(center, sigma^2) density at y."""
    return -((y - center) ** 2) / (2.0 * sigma * sigma) - math.log(sigma * math.sqrt(2.0 * math.pi))
