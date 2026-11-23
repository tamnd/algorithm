# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moments-accountant/. The authors are listed in prov/BBS4G5.jsonl.
"""The moments accountant of Abadi et al. (2016) for the subsampled Gaussian.

One step of DP-SGD keeps each record with probability q (Poisson sampling),
adds the clipped gradients (l2 norm at most 1), and adds N(0, sigma^2) noise
to each coordinate. Under add/remove neighbors, the log moment of order lam
of the privacy loss of one step is at most

    alpha(lam) = ln A_{lam+1},
    A_a = sum_{k=0}^{a} C(a, k) (1-q)^(a-k) q^k exp((k^2 - k) / (2 sigma^2)),

for integer lam >= 1 (Mironov, Talwar and Zhang 2019). Log moments add over
T steps, and the tail bound gives (epsilon, delta)-DP with

    epsilon = min over lam of (T alpha(lam) + ln(1/delta)) / lam.

The accountant only does arithmetic on the parameters. A deployment of the
mechanism that it accounts for needs a cryptographic source of randomness and
exact sampling of the noise, because float noise leaks through its low-order
bits (Mironov 2012; Canonne, Kamath and Steinke 2020).
"""

from __future__ import annotations

import math
from typing import List, Tuple


def _check(q: float, sigma: float) -> None:
    if not 0.0 <= q <= 1.0:
        raise ValueError("q must be in [0, 1]")
    if not sigma > 0.0:
        raise ValueError("sigma must be positive")


def log_moment(q: float, sigma: float, lam: int) -> float:
    """alpha(lam) = ln A_{lam+1} for one subsampled Gaussian step.

    Precondition: 0 <= q <= 1, sigma > 0, lam >= 1 an integer.
    Cost: O(lam) arithmetic operations in the real RAM.
    """
    _check(q, sigma)
    if lam < 1:
        raise ValueError("lam must be a positive integer")
    a = lam + 1  # @line L2
    terms: List[float] = []
    for k in range(a + 1):  # @line L3
        if (q == 0.0 and k > 0) or (q == 1.0 and k < a):
            continue  # this term is 0; its log is minus infinity
        t = math.log(math.comb(a, k)) + (k * k - k) / (2.0 * sigma * sigma)
        if k < a:
            t += (a - k) * math.log1p(-q)
        if k > 0:
            t += k * math.log(q)
        terms.append(t)
    m = max(terms)  # @line L4
    return m + math.log(sum(math.exp(t - m) for t in terms))


def moments_accountant(
    q: float, sigma: float, steps: int, delta: float, max_order: int = 32
) -> Tuple[float, int]:
    """The epsilon of `steps` subsampled Gaussian steps at the given delta.

    Returns (epsilon, lam) where lam is the order that gives the minimum.
    Precondition: 0 <= q <= 1, sigma > 0, steps >= 1, 0 < delta < 1,
    max_order >= 1. Cost: O(m^2) arithmetic operations for m = max_order,
    and O(m) extra space.
    """
    _check(q, sigma)
    if steps < 1 or max_order < 1 or not 0.0 < delta < 1.0:
        raise ValueError("need steps >= 1, max_order >= 1 and 0 < delta < 1")
    best_eps = math.inf
    best_lam = 0
    for lam in range(1, max_order + 1):  # @line L1
        alpha = log_moment(q, sigma, lam)  # lines L2 to L4
        eps_lam = (steps * alpha + math.log(1.0 / delta)) / lam  # @line L5
        if eps_lam < best_eps:  # @line L6
            best_eps, best_lam = eps_lam, lam
    return best_eps, best_lam  # @line L7


def delta_for_epsilon(
    q: float, sigma: float, steps: int, epsilon: float, max_order: int = 32
) -> float:
    """The delta that the tail bound gives for a target epsilon.

    delta = min over lam of exp(T alpha(lam) - lam epsilon), capped at 1.
    Precondition: as for moments_accountant, and epsilon >= 0.
    Cost: O(m^2) arithmetic operations for m = max_order.
    """
    _check(q, sigma)
    if steps < 1 or max_order < 1 or epsilon < 0:
        raise ValueError("need steps >= 1, max_order >= 1 and epsilon >= 0")
    best = 0.0  # log of the best delta so far; delta <= 1 always holds
    for lam in range(1, max_order + 1):
        best = min(best, steps * log_moment(q, sigma, lam) - lam * epsilon)
    return math.exp(best)
