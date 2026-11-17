# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/first-reaction-method/. The authors are listed in prov/4TMPNZ.jsonl.
"""Gillespie's first reaction method for the chemical master equation.

A network with n species and m reactions is given by stoich, the m change
vectors (stoich[j][i] = S[i][j]), and propensity(x), which returns the m
propensities for a state x (a tuple of n integer counts).

Draw order in each step: one rng.expovariate(a_j) for each reaction j with
a_j > 0, in index order j = 0, 1, ..., m - 1. Reactions with a_j = 0 draw
nothing. A step therefore uses as many random numbers as there are
reactions with a positive propensity.
"""

from __future__ import annotations

import math
from typing import Callable, Sequence, Tuple

State = Tuple[int, ...]


def first_reaction_method(rng, x0: Sequence[int], stoich: Sequence[Sequence[int]],
                          propensity: Callable[[State], Sequence[float]], t_end: float,
                          max_events: int = 10 ** 6):
    """Simulate one trajectory from x0 at time 0 up to time t_end.

    Returns (times, states, complete) in the format of the direct method:
    times[0] = 0.0, states[0] = x0, and entry k > 0 is the time of event k
    and the state just after it. complete is False only if max_events
    events fired before t_end.
    """
    t = 0.0  # @line L1
    x = tuple(int(v) for v in x0)
    times = [t]
    states = [x]
    m = len(stoich)
    for _ in range(max_events):  # @line L2
        a = propensity(x)  # @line L3
        best = math.inf  # @line L4
        mu = -1
        for j in range(m):  # @line L5
            if a[j] < 0:
                raise ValueError("propensities must be >= 0")
            if a[j] > 0:
                tau_j = rng.expovariate(a[j])  # @line L6
                if tau_j < best:  # @line L7
                    best = tau_j
                    mu = j
        if mu < 0:  # @line L8
            return times, states, True
        if t + best > t_end:  # @line L9
            return times, states, True
        t += best  # @line L10
        nu = stoich[mu]
        x = tuple(x[i] + nu[i] for i in range(len(x)))
        times.append(t)  # @line L11
        states.append(x)
    return times, states, False
