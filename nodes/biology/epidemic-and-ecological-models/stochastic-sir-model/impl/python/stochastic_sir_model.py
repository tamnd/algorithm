# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stochastic-sir-model/. The authors are listed in prov/EFGZYZ.jsonl.
"""The general stochastic epidemic: the Markov SIR model in continuous time.

The state is (S, I) in a population of N, with R = N - S - I. Infection
(S, I) -> (S - 1, I + 1) has rate beta S I / N, and recovery
(S, I) -> (S, I - 1) has rate gamma I. R0 = beta / gamma.

simulate is Gillespie's direct method written out for this model. It draws
its random numbers in the same order as biostoch.ssa_direct with the
reactions (infection, recovery), so with the same seed both give the same
path. final_size_distribution is exact: it runs over the embedded jump
chain, where the next event is an infection with probability
R0 S / (R0 S + N).
"""

from __future__ import annotations

from typing import Dict, List, Tuple

STOICH = [(-1, 1), (0, -1)]


def propensity(beta: float, gamma: float, n: int):
    """The rates (beta S I / N, gamma I) as a function of the state (S, I)."""
    return lambda x: (beta * x[0] * x[1] / n, gamma * x[1])


def simulate(rng, n: int, s0: int, i0: int, beta: float, gamma: float,
             t_end: float = float("inf")) -> Tuple[List[float], List[Tuple[int, int]]]:
    """One path: the event times and the states (S, I) just after them.

    Draw order: per event, rng.expovariate(a0) for the waiting time, then
    rng.random() to choose the event. The run stops when I = 0 or when the
    next event would come after t_end.
    """
    t, s, i = 0.0, s0, i0  # @line L1
    times, states = [t], [(s, i)]
    while i > 0:  # @line L2
        a_inf = beta * s * i / n  # @line L3
        a_rec = gamma * i
        a0 = a_inf + a_rec
        t += rng.expovariate(a0)  # @line L4
        if t > t_end:  # @line L5
            break
        if rng.random() * a0 < a_inf:  # @line L6
            s, i = s - 1, i + 1
        else:  # @line L7
            i -= 1
        times.append(t)  # @line L8
        states.append((s, i))
    return times, states


def final_size(states: List[Tuple[int, int]]) -> int:
    """The number of infections during the run: S_0 - S_end."""
    return states[0][0] - states[-1][0]


def final_size_distribution(n: int, s0: int, i0: int, r0,
                            max_size: int | None = None) -> Dict[int, object]:
    """The exact law of the final size by the embedded jump chain.

    Each event lowers 2S + I by one, so the states are visited level by
    level. With max_size set, states with more than max_size infections are
    dropped, and the returned masses are P(final size = k) for k <= max_size.
    With r0 a fractions.Fraction, the result is exact.
    """
    if max_size is None:
        max_size = s0
    levels: Dict[int, Dict[Tuple[int, int], object]] = {2 * s0 + i0: {(s0, i0): 1 + 0 * r0}}
    out: Dict[int, object] = {}
    for level in range(2 * s0 + i0, -1, -1):
        for (s, i), w in levels.pop(level, {}).items():
            if i == 0:
                out[s0 - s] = out.get(s0 - s, 0 * r0) + w
                continue
            p_inf = r0 * s / (r0 * s + n)
            nxt = levels.setdefault(level - 1, {})
            if s > 0 and s0 - s + 1 <= max_size:
                key = (s - 1, i + 1)
                nxt[key] = nxt.get(key, 0 * r0) + w * p_inf
            key = (s, i - 1)
            nxt[key] = nxt.get(key, 0 * r0) + w * (1 - p_inf)
    return dict(sorted(out.items()))
