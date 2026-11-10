# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wang-landau/. The authors are listed in prov/V5BYBD.jsonl.

import math
import random
from typing import Callable, Hashable, Sequence


def wang_landau(
    levels: Sequence[Hashable],
    propose: Callable,
    x0,
    e0: Hashable,
    rng: random.Random,
    ln_f_final: float = 1e-5,
    flatness: float = 0.8,
    one_over_t: bool = True,
    check_every: int = 1000,
    max_steps: int = 10**8,
) -> tuple[dict, int]:
    """Estimate the density of states g(e), the number (or volume) of states with energy e.

    levels lists every energy value. propose(x, e, rng) returns (y, e_y): a proposal from a
    symmetric kernel and its energy. e0 is the energy of x0.
    With one_over_t, the modification factor follows the 1/t rule of Belardinelli and Pereyra
    once it falls below len(levels) / t; without it, this is the original halving schedule.
    Returns (ln_g, steps), with ln_g[e] defined up to one additive constant.
    """
    if e0 not in levels:
        raise ValueError("e0 must be one of the levels")
    if not 0 < flatness < 1 or ln_f_final <= 0:
        raise ValueError("need 0 < flatness < 1 and ln_f_final > 0")
    n = len(levels)
    ln_g = {e: 0.0 for e in levels}  # @line L1
    hist = {e: 0 for e in levels}
    ln_f, t, x, e, tail = 1.0, 0, x0, e0, False
    while ln_f > ln_f_final and t < max_steps:  # @line L2
        y, e_y = propose(x, e, rng)  # @line L3
        d = ln_g[e] - ln_g[e_y]
        if d >= 0 or rng.random() < math.exp(d):  # @line L4
            x, e = y, e_y
        ln_g[e] += ln_f  # @line L5
        hist[e] += 1
        t += 1
        if tail:
            ln_f = n / t  # @line L6
        elif t % check_every == 0 and min(hist.values()) >= flatness * sum(hist.values()) / n:  # @line L7
            ln_f /= 2
            hist = {k: 0 for k in levels}
            if one_over_t and ln_f <= n / t:
                tail, ln_f = True, n / t
    return ln_g, t  # @line L8


def frozen_walk_matrix(states, energy, neighbours, g):
    """The exact kernel of lines L3 and L4 when the estimate is frozen at g (a dict of exact positive numbers).

    neighbours(s) lists the states that the symmetric proposal picks, each with probability 1 / len.
    The move to y is accepted with probability min(1, g[energy(s)] / g[energy(y)]), so the kernel is
    Metropolis for the law proportional to 1 / g[energy(s)]. With the true g, the energy is uniform on the levels.
    """
    index = {s: i for i, s in enumerate(states)}
    m = len(states)
    mat = [[0] * m for _ in range(m)]
    for i, s in enumerate(states):
        nb = neighbours(s)
        for y in nb:
            g_s, g_y = g[energy(s)], g[energy(y)]
            mat[i][index[y]] += min(g_s, g_y) / g_y / len(nb)  # min(1, g_s / g_y) in the type of g
        mat[i][i] += 1 - sum(mat[i])
    return mat
