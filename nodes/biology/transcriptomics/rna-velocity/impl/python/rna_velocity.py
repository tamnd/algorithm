# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rna-velocity/. The authors are listed in prov/MT9F81.jsonl.
"""RNA velocity with the steady-state model, small and dense.

The model of one gene in one cell, with time in units of the splicing rate
(beta = 1 unless given):

    du/dt = alpha - beta u        (unspliced: made at rate alpha, spliced at rate beta)
    ds/dt = beta u - gamma s      (spliced: made from u, degraded at rate gamma)

At a steady state u = (gamma / beta) s. The steady-state model (La Manno et al.
2018) fits the ratio gamma' = gamma / beta for each gene by least squares
through the origin on the cells with the smallest and the largest spliced
counts, which it takes to be near the two steady states, and sets the velocity
of a cell to v = u - gamma' s, which is ds/dt in units of beta.

What this version leaves out: the pooling of counts over nearest neighbors
(the moments), the dynamical model of scVelo (Bergen et al. 2020) fitted by
expectation maximization, the stochastic model, the transition probabilities
between cells, and the projection of the velocities onto an embedding.
"""

from __future__ import annotations

import math
from typing import List, Sequence, Tuple


def solution(alpha: float, beta: float, gamma: float, u0: float, s0: float, t: float) -> Tuple[float, float]:
    """The exact (u, s) after time t from (u0, s0) with a constant alpha."""
    if beta <= 0 or gamma <= 0:
        raise ValueError("beta and gamma must be positive")
    eb, eg = math.exp(-beta * t), math.exp(-gamma * t)
    u = u0 * eb + alpha / beta * (1 - eb)
    if math.isclose(beta, gamma, rel_tol=1e-12, abs_tol=0.0):
        s = s0 * eg + alpha / gamma * (1 - eg) + (beta * u0 - alpha) * t * eg
    else:
        s = s0 * eg + alpha / gamma * (1 - eg) + (alpha - beta * u0) / (gamma - beta) * (eg - eb)
    return u, s


def fit_gamma(u: Sequence[float], s: Sequence[float], q: float = 0.05) -> float:
    """gamma' by least squares through the origin on the cells in the lowest and highest q fraction of s."""
    n = len(s)
    if n != len(u) or n == 0:
        raise ValueError("u and s must have the same nonzero length")
    if not 0 < q <= 0.5:
        raise ValueError("q must be in (0, 0.5]")
    m = max(1, math.ceil(q * n))
    order = sorted(range(n), key=lambda i: (s[i], i))
    chosen = sorted(set(order[:m]) | set(order[n - m:]))  # @line L1
    ss = sum(s[i] * s[i] for i in chosen)
    if ss == 0.0:
        raise ValueError("the chosen cells have no spliced counts")
    return sum(u[i] * s[i] for i in chosen) / ss  # @line L2


def velocity(U: Sequence[Sequence[float]], S: Sequence[Sequence[float]], q: float = 0.05) -> Tuple[List[float], List[List[float]]]:
    """Per-gene gamma' and the cells by genes matrix of velocities. U and S are cells by genes."""
    n, g = len(S), len(S[0])
    gammas = [fit_gamma([U[i][j] for i in range(n)], [S[i][j] for i in range(n)], q) for j in range(g)]
    V = [[U[i][j] - gammas[j] * S[i][j] for j in range(g)] for i in range(n)]  # @line L3
    return gammas, V


def extrapolate(S: Sequence[Sequence[float]], V: Sequence[Sequence[float]], dt: float) -> List[List[float]]:
    """The predicted spliced state after a short time dt: s + dt v."""
    return [[s + dt * v for s, v in zip(rs, rv)] for rs, rv in zip(S, V)]  # @line L4
