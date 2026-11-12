# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/birth-death-process/. The authors are listed in prov/PEBREY.jsonl.
"""The constant-rate birth-death process: Kendall's distribution, a
Gillespie simulator, and the reconstructed process of surviving lineages.

The process starts from one lineage at time 0. Each lineage splits at rate
lam and dies at rate mu. z stands for exp((lam - mu) * t), so that the exact
functions accept rational inputs.
"""

import math
import random
from fractions import Fraction


def kendall_alpha_beta(lam, mu, z):
    """Kendall's alpha and beta for z = exp((lam - mu) t), with lam != mu.

    P(N(t) = 0) = alpha and P(N(t) = n) = (1 - alpha)(1 - beta) beta^(n-1).
    """
    denom = lam * z - mu
    return mu * (z - 1) / denom, lam * (z - 1) / denom


def kendall_alpha_beta_critical(a):
    """alpha and beta for lam = mu, with a = lam * t."""
    return a / (1 + a), a / (1 + a)


def probability(n, alpha, beta):
    """P(N(t) = n) from alpha and beta."""
    if n == 0:
        return alpha
    return (1 - alpha) * (1 - beta) * beta ** (n - 1)


def pgf(x, alpha, beta):
    """The generating function E[x^N(t)] = alpha + (1 - alpha)(1 - beta) x / (1 - beta x)."""
    return alpha + (1 - alpha) * (1 - beta) * x / (1 - beta * x)


def survival_probability(lam: float, mu: float, u: float) -> float:
    """P(N(u) > 0) = r / (lam - mu exp(-r u)) with r = lam - mu, or 1 / (1 + lam u) if r = 0."""
    r = lam - mu
    if r == 0:
        return 1 / (1 + lam * u)
    return r / (lam - mu * math.exp(-r * u))


def extinction_probability(lam: float, mu: float) -> float:
    """The probability that the process ever dies out: min(1, mu / lam)."""
    return 1.0 if mu >= lam else mu / lam


def simulate_count(lam: float, mu: float, t_max: float, rng: random.Random) -> int:
    """Gillespie simulation of the number of lineages at time t_max."""
    k, t = 1, 0.0  # @line L1
    while True:  # @line L2
        if k == 0:  # @line L3
            return 0
        w = rng.expovariate(k * (lam + mu))  # @line L4
        if t + w > t_max:  # @line L5
            return k
        t += w  # @line L6
        if rng.random() * (lam + mu) < lam:  # @line L7: a birth
            k += 1
        else:  # @line L8: a death
            k -= 1


def simulate_tree(lam: float, mu: float, t_max: float, rng: random.Random) -> list:
    """Simulate the complete tree up to t_max.

    Returns a list of lineages (birth, death, parent). At a split of lineage x
    a new lineage starts with parent x, and x goes on. death is None for a
    lineage alive at t_max. Lineage 0 is the root lineage, born at time 0.
    """
    lineages = [(0.0, None, None)]
    alive, t = [0], 0.0
    while alive:
        w = rng.expovariate(len(alive) * (lam + mu))
        if t + w > t_max:
            break
        t += w
        i = rng.randrange(len(alive))
        x = alive[i]
        if rng.random() * (lam + mu) < lam:
            lineages.append((t, None, x))
            alive.append(len(lineages) - 1)
        else:
            b, _, p = lineages[x]
            lineages[x] = (b, t, p)
            alive[i] = alive[-1]
            alive.pop()
    return lineages


def reconstructed_count(lineages: list, s: float) -> int:
    """The number of lineages alive at time s that have a descendant alive at the end."""
    seen = set()
    for y, (_, death, _) in enumerate(lineages):
        if death is not None:
            continue
        while lineages[y][0] > s:
            y = lineages[y][2]
        seen.add(y)
    return len(seen)


def expected_reconstructed(lam: float, mu: float, s: float, t_max: float) -> float:
    """E[reconstructed lineages at s] = exp((lam - mu) s) * P(survive for t_max - s)."""
    return math.exp((lam - mu) * s) * survival_probability(lam, mu, t_max - s)
