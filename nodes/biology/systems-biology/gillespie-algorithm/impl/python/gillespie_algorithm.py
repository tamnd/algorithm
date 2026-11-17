# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gillespie-algorithm/. The authors are listed in prov/TDM41K.jsonl.
"""Gillespie's direct method for the chemical master equation.

A network with n species and m reactions is given by:
- stoich: the m change vectors nu_1, ..., nu_m (stoich[j][i] = S[i][j]);
- propensity(x): the m propensities a_1(x), ..., a_m(x) for a state x, a
  tuple of n integer counts.

Random numbers are drawn in this order in each step: first the waiting time
tau = rng.expovariate(a0), then u = rng.random() * a0 for the choice of the
reaction. A step whose time passes t_end draws only the first number. This is
the same order as ssa_direct in biostoch.py, so both give the same
trajectory for the same seed.
"""

from __future__ import annotations

from typing import Callable, List, Sequence, Tuple

State = Tuple[int, ...]


def mass_action(reactants: Sequence[Sequence[int]], rates: Sequence[float]):
    """Return a propensity function for stochastic mass action.

    reactants[j][i] is the number of molecules of species i that reaction j
    uses (0, 1 or 2). The propensity is c_j times the number of distinct
    reactant combinations: c x for one X, c x_A x_B for A + B, and
    c x (x - 1) / 2 for 2X. So c for 2X is the convention with the factor 1/2
    inside the combination count.
    """
    def propensity(x: State) -> List[float]:
        out = []
        for row, c in zip(reactants, rates):
            a = c
            for i, k in enumerate(row):
                if k == 1:
                    a *= x[i]
                elif k == 2:
                    a *= x[i] * (x[i] - 1) / 2.0
                elif k != 0:
                    raise ValueError("only orders 0, 1 and 2 per species")
            out.append(float(a))
        return out
    return propensity


def direct_method(rng, x0: Sequence[int], stoich: Sequence[Sequence[int]],
                  propensity: Callable[[State], Sequence[float]], t_end: float,
                  max_events: int = 10 ** 6):
    """Simulate one trajectory from x0 at time 0 up to time t_end.

    Returns (times, states, complete). times[0] = 0.0 and states[0] = x0;
    entry k > 0 is the time of event k and the state just after it. The state
    at t_end is states[-1]. complete is False only if max_events events
    fired before t_end.
    """
    t = 0.0  # @line L1
    x = tuple(int(v) for v in x0)
    times = [t]
    states = [x]
    m = len(stoich)
    for _ in range(max_events):  # @line L2
        a = propensity(x)  # @line L3
        a0 = 0.0
        for v in a:
            if v < 0:
                raise ValueError("propensities must be >= 0")
            a0 += v
        if a0 <= 0.0:  # @line L4
            return times, states, True
        tau = rng.expovariate(a0)  # @line L5
        if t + tau > t_end:  # @line L6
            return times, states, True
        u = rng.random() * a0  # @line L7
        acc = 0.0  # @line L8
        j = -1
        for i in range(m):
            if a[i] > 0:
                acc += a[i]
                j = i
                if u < acc:
                    break
        t += tau  # @line L9
        nu = stoich[j]
        x = tuple(x[i] + nu[i] for i in range(len(x)))
        times.append(t)  # @line L10
        states.append(x)
    return times, states, False


def state_at(times: Sequence[float], states: Sequence[State], t: float) -> State:
    """The state of a piecewise constant trajectory at time t >= 0."""
    lo, hi = 0, len(times)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if times[mid] <= t:
            lo = mid
        else:
            hi = mid
    return states[lo]
