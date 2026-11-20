# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subset-simulation/. The authors are listed in prov/2D3RV8.jsonl.
"""Subset simulation of Au and Beck for a small failure probability P[g(U) <= 0].

U is a standard normal vector in R^d; map physical inputs to U first, for
example by the inverse CDF of each marginal. The failure set F = {g <= 0} is
reached through nested sets F_j = {g <= b_j} with b_1 > b_2 > ... > b_m = 0.
Each threshold b_j is the p0 quantile of the current samples, so every
conditional probability P[F_j | F_(j-1)] is about p0. The samples of the next
level are Markov chains, by the component-wise modified Metropolis method,
started from the samples that already lie in F_j.
"""

import math
import random
from typing import Callable

Vector = list[float]


def mm_step(g: Callable[[Vector], float], u: Vector, gu: float, b: float, rng: random.Random, width: float = 1.0) -> tuple[Vector, float, bool]:
    """One modified Metropolis step whose stationary law is the standard normal law conditioned on g <= b.

    Returns the next state, its g value, and whether g was called.
    """
    cand = list(u)
    moved = False
    for k, uk in enumerate(u):
        xi = uk + rng.uniform(-width, width)
        if rng.random() < math.exp(0.5 * (uk * uk - xi * xi)):
            cand[k] = xi
            moved = True
    if not moved:
        return u, gu, False
    gc = g(cand)
    if gc <= b:
        return cand, gc, True
    return u, gu, True


def subset_simulation(g: Callable[[Vector], float], d: int, rng: random.Random, n: int = 1000, p0: float = 0.1, max_levels: int = 30, width: float = 1.0) -> dict:
    """Estimate P[g(U) <= 0]; returns the estimate, the thresholds, the level probabilities and the number of g calls."""
    nc = round(p0 * n)
    if not 0 < nc < n or abs(nc - p0 * n) > 1e-9 or n % nc != 0:
        raise ValueError("p0 n must be an integer that divides n")
    chain_len = n // nc
    us = [[rng.gauss(0.0, 1.0) for _ in range(d)] for _ in range(n)]  # @line L1
    gs = [g(u) for u in us]
    calls = n
    thresholds: list[float] = []
    probs: list[float] = []
    for _ in range(max_levels):  # @line L2
        order = sorted(range(n), key=lambda i: gs[i])
        b = gs[order[nc - 1]]  # @line L3
        if b <= 0.0:  # @line L4
            probs.append(sum(1 for v in gs if v <= 0.0) / n)
            thresholds.append(0.0)
            return {"pf": math.prod(probs), "thresholds": thresholds, "probs": probs, "calls": calls}  # @line L5
        thresholds.append(b)
        probs.append(p0)  # @line L6
        new_u: list[Vector] = []
        new_g: list[float] = []
        for i in order[:nc]:  # @line L7
            u, gu = us[i], gs[i]
            new_u.append(u)
            new_g.append(gu)
            for _ in range(chain_len - 1):
                u, gu, called = mm_step(g, u, gu, b, rng, width)
                calls += called
                new_u.append(u)
                new_g.append(gu)
        us, gs = new_u, new_g  # @line L8
    raise RuntimeError("the failure set was not reached within max_levels levels")
