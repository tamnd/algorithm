# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hamiltonian-monte-carlo/. The authors are listed in prov/8S8XNZ.jsonl.

import math
import random
from typing import Callable, Sequence

Vector = list
Point = tuple[float, ...]


def leapfrog(
    grad_log_target: Callable[[Sequence], Sequence],
    q: Sequence,
    p: Sequence,
    eps,
    n_leapfrog: int,
) -> tuple[Vector, Vector]:
    """Take n_leapfrog leapfrog steps of size eps for H(q, p) = -log pi(q) + |p|^2 / 2.

    grad_log_target(q) is the gradient of log pi, which is -grad U.
    The arithmetic is generic, so Fraction inputs give exact results for a linear gradient.
    """
    q = list(q)
    p = list(p)
    half = eps / 2
    for _ in range(n_leapfrog):  # @line L5
        g = grad_log_target(q)
        p = [a + half * b for a, b in zip(p, g)]  # @line L6
        q = [a + eps * b for a, b in zip(q, p)]  # @line L7
        g = grad_log_target(q)
        p = [a + half * b for a, b in zip(p, g)]  # @line L8
    return q, p


def hamiltonian(log_target: Callable[[Sequence], float], q: Sequence, p: Sequence):
    """H(q, p) = U(q) + K(p) with U = -log pi and K = |p|^2 / 2."""
    return -log_target(q) + sum(v * v for v in p) / 2


def hamiltonian_monte_carlo(
    log_target: Callable[[Sequence], float],
    grad_log_target: Callable[[Sequence], Sequence],
    x0: Sequence[float],
    eps: float,
    n_leapfrog: int,
    n_steps: int,
    rng: random.Random,
) -> tuple[list[Point], int]:
    """Run HMC with identity mass matrix, step size eps and n_leapfrog steps per proposal.

    log_target is log of the unnormalized density and grad_log_target its gradient.
    Returns (chain X_1..X_T, number of accepted proposals).
    Cost: T * n_leapfrog gradient calls and T target calls.
    """
    if eps <= 0 or n_leapfrog < 1:
        raise ValueError("eps must be positive and n_leapfrog at least 1")
    q = [float(v) for v in x0]  # @line L1
    if log_target(q) == -math.inf:
        raise ValueError("x0 must be in the support of the target")
    chain: list[Point] = []
    accepted = 0
    for _ in range(n_steps):  # @line L2
        p = [rng.gauss(0.0, 1.0) for _ in q]  # @line L3
        h0 = hamiltonian(log_target, q, p)
        q_new, p_new = leapfrog(grad_log_target, q, p, eps, n_leapfrog)  # @line L4
        p_new = [-v for v in p_new]  # @line L9
        h1 = hamiltonian(log_target, q_new, p_new)
        u = rng.random()  # @line L10
        if math.isfinite(h1) and (h1 <= h0 or u < math.exp(h0 - h1)):  # @line L11
            q = q_new
            accepted += 1
        chain.append(tuple(q))  # @line L12
    return chain, accepted  # @line L13
