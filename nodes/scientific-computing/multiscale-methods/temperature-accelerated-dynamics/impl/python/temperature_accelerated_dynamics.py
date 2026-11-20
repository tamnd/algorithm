# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/temperature-accelerated-dynamics/. The authors are listed in prov/FJ0MZ4.jsonl.
"""One basin of temperature accelerated dynamics (Sorensen and Voter 2000).

The dynamics runs at a high temperature T_high. Each escape from the basin
is an event: its saddle energy E_a (above the minimum) is found, and the
system goes back into the basin. The time t_high of the first occurrence
of each event is extrapolated to the low temperature T_low with harmonic
transition state theory (HTST):

    t_low = t_high exp(E_a (1 / kT_low - 1 / kT_high)).

The event with the shortest t_low is the one that happens first at T_low.
The high temperature run stops at

    t_stop = (ln(1/delta) / nu_min) (nu_min t_short / ln(1/delta))^(T_low / T_high),

where t_short is the shortest t_low so far. If every event has an HTST
prefactor of at least nu_min, then with confidence 1 - delta no event not
seen by t_stop would have a shorter t_low.

The method assumes HTST at both temperatures: each event is a Poisson
process with the rate nu exp(-E_a / kT), with the same nu at both
temperatures. The boost t_short / t_high is a measurement.
"""

import math
from typing import Callable, Hashable


def temperature_accelerated_dynamics(run_high: Callable, barrier: Callable[[Hashable], float],
                                     kT_low: float, kT_high: float, nu_min: float, delta: float,
                                     rng, max_escapes: int = 10**6):
    """Find the first event of the basin at the low temperature.

    run_high(rng) runs the high temperature dynamics from the basin to the
    next escape and returns (dt, event), the time and a label of the escape;
    after it the system is back in the basin. barrier(event) returns E_a.

    Returns (event, t_low, t_high, escapes, seen): the accepted event, its
    low temperature time (the advance of the low temperature clock), the
    total high temperature time, the number of escapes, and a dict from
    each event seen to its extrapolated time.
    """
    t_high = 0.0                                                        # @line L1
    t_short, best, t_stop = math.inf, None, math.inf
    log_inv = math.log(1.0 / delta)
    seen = {}
    escapes = 0
    while t_high < t_stop:                                              # @line L2
        if escapes >= max_escapes:
            raise RuntimeError("temperature_accelerated_dynamics: max_escapes exceeded")
        dt, event = run_high(rng)                                       # @line L3
        escapes += 1
        if t_high + dt >= t_stop:
            t_high = t_stop
            break
        t_high += dt
        if event in seen:
            continue
        e_a = barrier(event)                                            # @line L4
        t_low = t_high * math.exp(e_a * (1.0 / kT_low - 1.0 / kT_high))  # @line L5
        seen[event] = t_low
        if t_low < t_short:                                             # @line L6
            t_short, best = t_low, event
            t_stop = (log_inv / nu_min) * (nu_min * t_short / log_inv) ** (kT_low / kT_high)  # @line L7
    return best, t_short, t_high, escapes, seen                         # @line L8


def catalog_high_temperature_run(events, kT_high):
    """Return run_high(rng) for a catalog {event: (nu, E_a)} of HTST events.

    The escape at T_high is the first of independent Poisson processes with
    the rates nu exp(-E_a / kT_high), the model that TAD assumes. This stands
    in for molecular dynamics in tests and examples.
    """
    labels = list(events)
    rates = [events[e][0] * math.exp(-events[e][1] / kT_high) for e in labels]
    total = sum(rates)

    def run_high(rng):
        dt = rng.expovariate(total)
        u = rng.random() * total
        for e, r in zip(labels, rates):
            u -= r
            if u < 0.0:
                return dt, e
        return dt, labels[-1]
    return run_high
