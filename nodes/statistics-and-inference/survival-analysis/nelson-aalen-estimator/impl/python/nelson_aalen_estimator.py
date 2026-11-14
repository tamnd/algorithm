# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nelson-aalen-estimator/. The authors are listed in prov/2X5FTW.jsonl.

import math
from collections.abc import Sequence
from fractions import Fraction
from typing import NamedTuple


class Step(NamedTuple):
    """One distinct event time t_j of the Nelson-Aalen table."""

    time: float
    at_risk: int  # n_j, the number with y_i >= t_j
    events: int  # d_j, the number of events at t_j
    cum_hazard: float  # H-hat(t_j)
    var_poisson: float  # sum over t_l <= t_j of d_l / n_l^2 (Aalen's estimate)
    var_binomial: float  # sum over t_l <= t_j of d_l (n_l - d_l) / n_l^3


def _increment(r: int, d: int, ties: str, exact: bool):
    if ties == "breslow":
        return Fraction(d, r) if exact else d / r
    if ties == "sequential":
        # The events at t_j are taken one after another: 1/r + 1/(r - 1) + ... + 1/(r - d + 1).
        s = sum((Fraction(1, r - l) for l in range(d)), Fraction(0))
        return s if exact else float(s)
    raise ValueError("ties must be 'breslow' or 'sequential'")


def nelson_aalen(times: Sequence[float], events: Sequence[int], exact: bool = False, ties: str = "breslow") -> list[Step]:
    """Nelson-Aalen estimate of the cumulative hazard from right-censored data.

    times[i] is y_i = min(T_i, C_i) and events[i] is 1 for an event and 0 for a
    censoring. A censoring tied with an event counts as at risk at that time.
    ties='breslow' adds d_j / n_j at each event time; ties='sequential' adds
    1/n_j + 1/(n_j - 1) + ... + 1/(n_j - d_j + 1). With exact=True the values
    are Fractions. Cost: one sort, O(n log n), and one O(n) scan.
    """
    n = len(times)
    if n == 0 or len(events) != n:
        raise ValueError("need the same positive number of times and event flags")
    if any(e not in (0, 1) for e in events):
        raise ValueError("event flags must be 0 or 1")
    zero = Fraction(0) if exact else 0.0
    order = sorted(range(n), key=lambda k: times[k])  # @line L1
    r, h, v, w, out = n, zero, zero, zero, []  # @line L2
    i = 0  # @line L3
    while i < n:  # @line L4
        t, d, c = times[order[i]], 0, 0  # @line L5
        while i < n and times[order[i]] == t:  # @line L6
            if events[order[i]]:
                d += 1
            else:
                c += 1
            i += 1
        if d > 0:  # @line L7
            h += _increment(r, d, ties, exact)
            v += Fraction(d, r * r) if exact else d / (r * r)
            w += Fraction(d * (r - d), r**3) if exact else d * (r - d) / r**3
            out.append(Step(t, r, d, h, v, w))
        r -= d + c  # @line L8
    return out  # @line L9


def evaluate(steps: list[Step], t: float, field: str = "cum_hazard"):
    """The value of a step-function field at time t (0 before the first event time)."""
    value = 0
    for step in steps:
        if step.time > t:
            break
        value = getattr(step, field)
    return value


def survival_from_hazard(steps: list[Step], t: float) -> float:
    """The estimate exp(-H-hat(t)) of the survival function."""
    return math.exp(-float(evaluate(steps, t)))
