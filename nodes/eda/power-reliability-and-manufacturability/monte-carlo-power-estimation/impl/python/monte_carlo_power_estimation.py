# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monte-carlo-power-estimation/. The authors are listed in prov/QFM309.jsonl.
"""Monte Carlo power estimation with a stopping rule (after Burch, Najm, Yang and Trick 1993).

monte_carlo_power(sample, eps, alpha) draws independent power samples until
the half width of the normal confidence interval at level 1 - alpha is below
eps times the sample mean, after at least n_min samples. It returns the mean,
the half width and the number of samples. The mean and the variance are kept
by Welford's update.

power_sampler(c, up, down, cap, T, rng) builds a sampler for a netlist.Circuit:
each input is a two-state Markov chain per clock cycle (0 -> 1 with
probability up, 1 -> 0 with probability down), independent of the other
inputs. One sample starts from the stationary law, simulates T cycles and
returns the mean energy per cycle, sum over transitions of cap[node] / 2, in
units of V_DD^2. Power is this value times the clock frequency.
"""

from __future__ import annotations

import math
import random
from statistics import NormalDist
from typing import Callable, Mapping, Sequence

from netlist import transitions


def monte_carlo_power(
    sample: Callable[[], float],
    eps: float,
    alpha: float = 0.05,
    n_min: int = 30,
    n_max: int = 10**6,
) -> tuple[float, float, int]:
    """Return (mean, half width, N) of the estimate of E[sample()]."""
    z = NormalDist().inv_cdf(1 - alpha / 2)  # @line L1
    n, mean, m2, half = 0, 0.0, 0.0, math.inf  # @line L2
    while True:  # @line L3
        e = sample()  # @line L4
        n += 1
        delta = e - mean
        mean += delta / n
        m2 += delta * (e - mean)  # @line L5
        if n >= 2:
            half = z * math.sqrt(m2 / (n - 1)) / math.sqrt(n)  # @line L6
        if n >= n_max or (n >= n_min and half < eps * mean):  # @line L7
            return mean, half, n  # @line L8


def power_sampler(
    c,
    up: Sequence[float],
    down: Sequence[float],
    cap: Mapping[str, float],
    T: int,
    rng: random.Random,
    delay_model: str = "zero",
) -> Callable[[], float]:
    """A sampler of the mean energy per cycle over T cycles, from a stationary start."""
    n = len(c.inputs)
    pi1 = [up[i] / (up[i] + down[i]) for i in range(n)]

    def sample() -> float:
        x = [1 if rng.random() < pi1[i] else 0 for i in range(n)]
        energy = 0.0
        for _ in range(T):
            y = [(1 - b) if rng.random() < (down[i] if b else up[i]) else b for i, b in enumerate(x)]
            for v, k in transitions(c, x, y, delay_model).items():
                if k:
                    energy += 0.5 * cap.get(v, 0.0) * k
            x = y
        return energy / T

    return sample
