# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reversible-jump-mcmc/. The authors are listed in prov/183JNF.jsonl.

import math
import random
from dataclasses import dataclass
from typing import Callable, Sequence


@dataclass
class DimensionJump:
    """A dimension-matching move from model k to model k + 1.

    draw_u(rng) draws the extra variables u, with log density log_u_density(u).
    up(theta, u) is a bijection onto the support of model k + 1, and down is its inverse.
    log_jacobian(theta, u) is log |det| of the derivative of up at (theta, u).
    """

    draw_u: Callable
    log_u_density: Callable
    up: Callable
    down: Callable
    log_jacobian: Callable


def log_up_ratio(log_target: Callable, jump: DimensionJump, k: int, theta, u, new) -> float:
    """The log acceptance ratio of the up move (k, theta) -> (k + 1, new) with new = up(theta, u)."""
    return log_target(k + 1, new) - log_target(k, theta) - jump.log_u_density(u) + jump.log_jacobian(theta, u)


def reversible_jump_mcmc(
    log_target: Callable,
    within_step: Callable,
    jumps: Sequence[DimensionJump],
    k0: int,
    theta0: Sequence[float],
    n_steps: int,
    rng: random.Random,
) -> tuple[list[tuple[int, tuple]], int, int]:
    """Reversible-jump MCMC on the models 0, ..., len(jumps).

    log_target(k, theta) is the log of the unnormalized joint density of model k and its parameters.
    within_step(k, theta, rng) must keep log_target(k, .) invariant.
    jumps[k] maps model k to model k + 1. Each step is a within-model step with probability 1/2,
    an up move with probability 1/4 and a down move with probability 1/4. A move to a model
    that does not exist is rejected.
    Returns (chain, jumps_proposed, jumps_accepted).
    """
    n_models = len(jumps) + 1
    if not 0 <= k0 < n_models:
        raise ValueError("k0 must name a model")
    k, theta = k0, tuple(theta0)
    if log_target(k, theta) == -math.inf:
        raise ValueError("the start must have positive density")
    chain = []
    proposed = accepted = 0
    for _ in range(n_steps):  # @line L1
        move = rng.random()  # @line L2
        log_r = None
        if move < 0.5:
            theta = tuple(within_step(k, theta, rng))  # @line L3
        elif move < 0.75 and k + 1 < n_models:
            u = jumps[k].draw_u(rng)  # @line L4
            new_k, new = k + 1, tuple(jumps[k].up(theta, u))
            log_r = log_up_ratio(log_target, jumps[k], k, theta, u, new)  # @line L5
        elif move >= 0.75 and k > 0:
            old, u = jumps[k - 1].down(theta)  # @line L6
            new_k, new = k - 1, tuple(old)
            log_r = -log_up_ratio(log_target, jumps[k - 1], k - 1, new, u, theta)  # @line L7
        if log_r is not None:
            proposed += 1
            if log_r >= 0 or rng.random() < math.exp(log_r):  # @line L8
                k, theta = new_k, new
                accepted += 1
        chain.append((k, theta))  # @line L9
    return chain, proposed, accepted  # @line L10
