# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tau-leaping/. The authors are listed in prov/Q8TJ4W.jsonl.
"""Explicit tau-leaping for stochastic chemical kinetics.

A network with n species and m reactions is given by:
- stoich: the m change vectors (stoich[j][i] = S[i][j]);
- propensity(x): the m propensities a_j(x) of the state x;
- reactants: reactants[j][i] is the number of molecules of species i that
  reaction j uses. Only the adaptive method needs it, for the order rules
  of the step size.

fixed_step_leap is the plain method of Gillespie (2001) with a constant
step. adaptive_tau_leap is the method of Cao, Gillespie and Petzold (2006):
critical reactions, the step size of their eq. (33), the fall back to the
direct method when the step is short, and halving of the step when a leap
gives a negative count.

Both functions return (times, states, info). times[0] = 0.0 and states[0] =
tuple(x0). fixed_step_leap records every step; adaptive_tau_leap records
each step that changes the state, as the direct method does. In both,
states[-1] is the state at t_end (or at the time when all propensities are
0). info counts the leaps, the direct method steps and the rejected leaps.
"""

from __future__ import annotations

import math
from typing import Callable, Dict, List, Sequence, Tuple

from biostoch import poisson

State = Tuple[int, ...]


def _apply(x: State, stoich, k: Sequence[int]) -> List[int]:
    y = list(x)
    for j, kj in enumerate(k):
        if kj:
            for i, d in enumerate(stoich[j]):
                y[i] += kj * d
    return y


def fixed_step_leap(rng, x0: Sequence[int], stoich: Sequence[Sequence[int]],
                    propensity: Callable[[State], Sequence[float]], tau: float,
                    t_end: float):
    """Leap with the step tau (the last step ends at t_end).

    Each step draws k_j = poisson(rng, a_j h) for j = 0, ..., m - 1 with
    a_j > 0, in index order. If the new state has a negative count, the
    draws are thrown away and the same step is tried again with h / 2. The
    next step starts again from h = tau.
    """
    if tau <= 0:
        raise ValueError("tau must be > 0")
    x = tuple(int(v) for v in x0)
    t = 0.0
    times, states = [t], [x]
    info = {"leaps": 0, "ssa_steps": 0, "rejected": 0}
    m = len(stoich)
    while t < t_end:
        a = propensity(x)
        if sum(a) <= 0:
            break
        h = min(tau, t_end - t)
        while True:
            k = [poisson(rng, a[j] * h) if a[j] > 0 else 0 for j in range(m)]
            y = _apply(x, stoich, k)
            if min(y) >= 0:
                break
            info["rejected"] += 1
            h /= 2.0
        t = t_end if h == t_end - t else t + h
        x = tuple(y)
        times.append(t)
        states.append(x)
        info["leaps"] += 1
    return times, states, info


def highest_order_factors(reactants: Sequence[Sequence[int]]):
    """For each species i, a function g_i(x_i) as in eq. (27) of Cao,
    Gillespie and Petzold (2006). The highest order of reaction (HOR) of i
    is the largest total order of a reaction that uses i; if a reaction of
    that order uses i more than once, g_i depends on x_i."""
    n = len(reactants[0]) if reactants else 0
    out = []
    for i in range(n):
        hor, mult = 0, 0
        for row in reactants:
            if row[i] > 0:
                order = sum(row)
                if order > hor or (order == hor and row[i] > mult):
                    hor, mult = order, row[i]
        out.append(_g_rule(hor, mult))
    return out


def _g_rule(hor: int, mult: int):
    if hor <= 1:
        return lambda xi: 1.0
    if hor == 2:
        if mult == 1:
            return lambda xi: 2.0
        return lambda xi: 2.0 + 1.0 / (xi - 1) if xi > 1 else 2.0
    if hor == 3:
        if mult == 1:
            return lambda xi: 3.0
        if mult == 2:
            return lambda xi: 1.5 * (2.0 + 1.0 / (xi - 1)) if xi > 1 else 3.0
        return lambda xi: 3.0 + 1.0 / (xi - 1) + 2.0 / (xi - 2) if xi > 2 else 3.0
    raise ValueError("reactions of order above 3 are not supported")


def _ssa_step(rng, x: State, stoich, a: Sequence[float], a0: float, t: float, t_end: float):
    """One step of the direct method, with the draw order of ssa_direct.
    Returns the new (t, x), or None when the next event is after t_end."""
    tau = rng.expovariate(a0)
    if t + tau > t_end:
        return None
    u = rng.random() * a0
    acc, j = 0.0, -1
    for i, v in enumerate(a):
        if v > 0:
            acc += v
            j = i
            if u < acc:
                break
    nu = stoich[j]
    return t + tau, tuple(x[i] + nu[i] for i in range(len(x)))


def adaptive_tau_leap(rng, x0: Sequence[int], stoich: Sequence[Sequence[int]],
                      propensity: Callable[[State], Sequence[float]],
                      reactants: Sequence[Sequence[int]], t_end: float,
                      eps: float = 0.03, n_c: int = 10, ssa_factor: float = 10.0,
                      ssa_steps: int = 100):
    """The tau-leaping method of Cao, Gillespie and Petzold (2006).

    Draw order in a leap: tau'' = rng.expovariate(a0c) if a0c > 0; then
    k_j = poisson(rng, a_j tau) for the noncritical j with a_j > 0, in index
    order; then, if a critical reaction fires, one u = rng.random() * a0c
    and a cumulative search over the critical reactions. A rejected leap
    draws again in the same order with tau' halved. A step of the direct
    method draws as ssa_direct does.
    """
    x = tuple(int(v) for v in x0)
    t = 0.0  # @line L1
    times, states = [t], [x]
    info = {"leaps": 0, "ssa_steps": 0, "rejected": 0}
    m, n = len(stoich), len(x)
    g = highest_order_factors(reactants)
    reactant_species = [i for i in range(n) if any(row[i] > 0 for row in reactants)]
    while t < t_end:  # @line L2
        a = list(propensity(x))  # @line L3
        a0 = sum(a)
        if a0 <= 0:
            break
        critical = [False] * m  # @line L4
        for j in range(m):
            if a[j] > 0:
                limit = math.inf
                for i, d in enumerate(stoich[j]):
                    if d < 0:
                        limit = min(limit, x[i] // (-d))
                critical[j] = limit < n_c
        tau1 = math.inf  # @line L5
        for i in reactant_species:
            mu = sum(stoich[j][i] * a[j] for j in range(m) if not critical[j])
            var = sum(stoich[j][i] ** 2 * a[j] for j in range(m) if not critical[j])
            bound = max(eps * x[i] / g[i](x[i]), 1.0)
            if mu != 0:
                tau1 = min(tau1, bound / abs(mu))
            if var > 0:
                tau1 = min(tau1, bound * bound / var)
        if tau1 < ssa_factor / a0:  # @line L6
            for _ in range(ssa_steps):
                step = _ssa_step(rng, x, stoich, a, a0, t, t_end)
                if step is None:
                    t = t_end
                    break
                t, x = step
                times.append(t)
                states.append(x)
                info["ssa_steps"] += 1
                a = list(propensity(x))
                a0 = sum(a)
                if a0 <= 0:
                    break
            if a0 <= 0:
                break
            continue
        a0c = sum(a[j] for j in range(m) if critical[j])
        while True:
            tau2 = rng.expovariate(a0c) if a0c > 0 else math.inf  # @line L7
            tau = min(tau1, tau2, t_end - t)  # @line L8
            k = [poisson(rng, a[j] * tau) if a[j] > 0 and not critical[j] else 0  # @line L9
                 for j in range(m)]
            if tau == tau2:  # @line L10
                u = rng.random() * a0c
                acc = 0.0
                for j in range(m):
                    if critical[j]:
                        acc += a[j]
                        jc = j
                        if u < acc:
                            break
                k[jc] = 1
            y = _apply(x, stoich, k)
            if min(y) >= 0:  # @line L11
                break
            info["rejected"] += 1
            tau1 /= 2.0
        if tau == math.inf:
            raise ValueError("no finite step: give a finite t_end")
        t = t_end if tau == t_end - t else t + tau  # @line L12
        info["leaps"] += 1
        if any(k):
            x = tuple(y)
            times.append(t)
            states.append(x)
    return times, states, info
