# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-tempering/. The authors are listed in prov/381BFJ.jsonl.

import itertools
import math
import random
from fractions import Fraction
from typing import Callable, Sequence


def metropolis_local_step(sigma: float):
    """Return local_step(log_target, beta, x, rng): one random-walk Metropolis step for pi^beta on the reals.

    The step size is sigma / sqrt(beta), so that hot levels, which are wider, take longer steps.
    """

    def step(log_target, beta, x, rng):
        y = x + sigma / math.sqrt(beta) * rng.gauss(0.0, 1.0)
        d = beta * (log_target(y) - log_target(x))
        if d >= 0 or rng.random() < math.exp(d):
            return y
        return x

    return step


def parallel_tempering(
    log_target: Callable,
    betas: Sequence[float],
    x0: Sequence,
    local_step: Callable,
    n_steps: int,
    rng: random.Random,
) -> tuple[list[list], list[int], list[int]]:
    """Run parallel tempering on the levels pi^beta_k, with betas[0] = 1 > betas[1] > ... > 0.

    local_step(log_target, beta, x, rng) must leave pi^beta invariant.
    Returns (chains, swaps_proposed, swaps_accepted): chains[k] is the path of level k,
    and the swap counts are per neighbour pair (k, k + 1).
    """
    k_levels = len(betas)
    if k_levels < 2 or betas[0] != 1 or any(not b > c > 0 for b, c in zip(betas, betas[1:])):
        raise ValueError("need betas[0] = 1 > betas[1] > ... > betas[-1] > 0")
    if len(x0) != k_levels:
        raise ValueError("need one start per level")
    x = list(x0)
    chains: list[list] = [[] for _ in range(k_levels)]
    proposed = [0] * (k_levels - 1)
    accepted = [0] * (k_levels - 1)
    for _ in range(n_steps):  # @line L1
        for k in range(k_levels):  # @line L2
            x[k] = local_step(log_target, betas[k], x[k], rng)  # @line L3
        k = rng.randrange(k_levels - 1)  # @line L4
        log_r = (betas[k] - betas[k + 1]) * (log_target(x[k + 1]) - log_target(x[k]))  # @line L5
        u = rng.random()  # @line L6
        proposed[k] += 1
        if log_r >= 0 or u < math.exp(log_r):  # @line L7
            x[k], x[k + 1] = x[k + 1], x[k]
            accepted[k] += 1
        for j in range(k_levels):  # @line L8
            chains[j].append(x[j])
    return chains, proposed, accepted  # @line L9


def joint_transition_matrix(
    weights: Sequence[Sequence[Fraction]],
    local_kernels: Sequence[Sequence[Sequence[Fraction]]],
) -> tuple[list[tuple[int, ...]], list[list[Fraction]], list[list[Fraction]]]:
    """Exact kernels of one parallel tempering iteration on a finite space {0, ..., n - 1}.

    weights[k][x] is the unnormalized law of level k and local_kernels[k] a kernel that keeps it.
    Returns (states, local, swap): states lists the joint states (x_1, ..., x_K), local is the product
    of the local kernels (lines L2 and L3) and swap is the swap move (lines L4 to L7).
    One iteration is local followed by swap.
    """
    k_levels = len(weights)
    n = len(weights[0])
    states = list(itertools.product(range(n), repeat=k_levels))
    index = {s: i for i, s in enumerate(states)}
    m = len(states)
    local = [[Fraction(0)] * m for _ in range(m)]
    for i, s in enumerate(states):
        for t in states:
            p = Fraction(1)
            for k in range(k_levels):
                p *= local_kernels[k][s[k]][t[k]]
                if p == 0:
                    break
            local[i][index[t]] = p
    swap = [[Fraction(0)] * m for _ in range(m)]
    for i, s in enumerate(states):
        for k in range(k_levels - 1):
            a, b = s[k], s[k + 1]
            r = weights[k][b] * weights[k + 1][a] / (weights[k][a] * weights[k + 1][b])
            acc = min(Fraction(1), r) / (k_levels - 1)
            t = list(s)
            t[k], t[k + 1] = b, a
            swap[i][index[tuple(t)]] += acc
            swap[i][i] += Fraction(1, k_levels - 1) - acc
    return states, local, swap
