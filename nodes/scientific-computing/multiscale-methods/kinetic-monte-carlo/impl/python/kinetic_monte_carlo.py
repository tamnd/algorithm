# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kinetic-monte-carlo/. The authors are listed in prov/SFQPD9.jsonl.
"""Kinetic Monte Carlo by the residence time algorithm (Bortz, Kalos and Lebowitz 1975).

The system is a continuous-time Markov jump process. In a state x, the
function events(x) gives the list of possible events as pairs (k_j, y_j):
the rate k_j > 0 of event j and the state y_j after it. One step of the
algorithm draws the waiting time from an exponential law with rate
R = k_1 + ... + k_M, picks event j with probability k_j / R, and jumps.

The catalog of events must be complete: an event that is missing has rate
zero in the simulation, and no later step can correct this.

Cost per step: one call of events(x) and Theta(M) work for the sum and the
linear search, for M events. A sum tree makes the search O(log M).
"""

import math
from typing import Callable, Hashable, Optional

State = Hashable
Events = Callable[[State], list[tuple[float, State]]]


def select_event(rates: list[float], r: float) -> int:
    """The smallest index j with k_0 + ... + k_j > r, for 0 <= r < sum(rates)."""
    acc = 0.0
    for j, k in enumerate(rates):
        acc += k
        if acc > r:
            return j
    # r is within rounding of the total: take the last event with a positive rate.
    for j in range(len(rates) - 1, -1, -1):
        if rates[j] > 0:
            return j
    raise ValueError("no event has a positive rate")


def kinetic_monte_carlo(
    x: State, events: Events, t_end: float, rng,
    observe: Optional[Callable[[State], float]] = None, max_steps: int = 10**6,
):
    """Run the residence time algorithm from state x until time t_end.

    rng needs a method random() that returns a float in [0, 1).
    Returns (x, t, path, average): the final state, the final time
    (t_end, or the time of the last event if no event is possible), the
    list of (time, state) after each event with (0, x) first, and the
    time average over [0, t] of observe(state) (None if observe is None).
    """
    t = 0.0                                                   # @line L1
    path = [(t, x)]
    integral = 0.0
    for _ in range(max_steps):
        if t >= t_end:                                        # @line L2
            break
        ev = events(x)                                        # @line L3
        rates = [k for k, _ in ev]
        total = sum(rates)                                    # @line L4
        if total <= 0.0:                                      # @line L5
            break
        u1 = rng.random()                                     # @line L6
        u2 = 1.0 - rng.random()                               # @line L6
        dt = -math.log(u2) / total                            # @line L7
        if t + dt >= t_end:                                   # @line L8
            if observe is not None:
                integral += observe(x) * (t_end - t)
            t = t_end
            break
        if observe is not None:                               # @line L9
            integral += observe(x) * dt
        j = select_event(rates, u1 * total)                   # @line L10
        t += dt                                               # @line L11
        x = ev[j][1]                                          # @line L11
        path.append((t, x))                                   # @line L12
    average = None
    if observe is not None and t > 0:
        average = integral / t
    return x, t, path, average                                # @line L13


def arrhenius_rate(prefactor: float, barrier: float, kT: float) -> float:
    """The harmonic transition state theory rate nu exp(-E / kT)."""
    return prefactor * math.exp(-barrier / kT)
