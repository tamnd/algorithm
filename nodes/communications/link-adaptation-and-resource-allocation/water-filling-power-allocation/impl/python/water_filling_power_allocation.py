# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/water-filling-power-allocation/. The authors are listed in prov/1Y9CA5.jsonl.

"""Water-filling power allocation over N parallel Gaussian channels.

Channel i has the noise level nu[i] > 0, the noise power divided by the power
gain of the channel. With the power p[i] it carries log2(1 + p[i] / nu[i])
bits per channel use. The allocation that maximizes the sum of the rates under
sum(p) = P is p[i] = max(0, mu - nu[i]), where the water level mu makes the
powers add up to P. The function sorts the levels once and finds the number
of active channels with one pass, so it costs O(N log N).
"""

import math


def water_filling(nu: list[float], power: float) -> tuple[list[float], float]:
    """The powers p[i] = max(0, mu - nu[i]) with sum P, and the water level mu."""
    if not nu or any(not v > 0 for v in nu):
        raise ValueError("need at least one channel and positive noise levels")
    if power < 0:
        raise ValueError("the total power must not be negative")
    if power == 0:
        return [0.0] * len(nu), min(nu)
    s = sorted(nu)  # @line L1
    total, k = 0.0, 0  # @line L2
    while k < len(s) and k * s[k] < power + total:  # @line L3
        total, k = total + s[k], k + 1  # @line L4
    mu = (power + total) / k  # @line L5
    p = [max(0.0, mu - v) for v in nu]  # @line L6
    return p, mu  # @line L7


def sum_rate(nu: list[float], p: list[float]) -> float:
    """The sum over i of log2(1 + p[i] / nu[i]), in bits per channel use."""
    return sum(math.log2(1 + pi / v) for pi, v in zip(p, nu))


def water_level_by_bisection(nu: list[float], power: float, iters: int = 200) -> float:
    """A second method: bisection on mu for sum(max(0, mu - nu[i])) = P."""
    lo, hi = min(nu), max(nu) + power
    for _ in range(iters):
        mid = (lo + hi) / 2
        if sum(max(0.0, mid - v) for v in nu) < power:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def noise_levels(gains: list[complex], n0: list[float] | float, gap: float = 1.0) -> list[float]:
    """nu[i] = gap * N0[i] / |h[i]|^2 for channel gains h[i] and noise densities N0[i]."""
    if not isinstance(n0, list):
        n0 = [n0] * len(gains)
    return [gap * w / abs(h) ** 2 for h, w in zip(gains, n0)]
