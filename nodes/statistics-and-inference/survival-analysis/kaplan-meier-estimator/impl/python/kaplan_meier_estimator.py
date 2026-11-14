# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kaplan-meier-estimator/. The authors are listed in prov/FNVF5H.jsonl.

from collections.abc import Sequence
from fractions import Fraction
from typing import NamedTuple


class Step(NamedTuple):
    """One distinct event time t_j of the Kaplan-Meier table."""

    time: float
    at_risk: int  # n_j, the number with y_i >= t_j
    events: int  # d_j, the number of events at t_j
    survival: float  # S-hat(t_j), a Fraction when exact=True


class KaplanMeier:
    """The Kaplan-Meier estimate S-hat as a right-continuous step function.

    steps holds one row per distinct event time. t_max is the largest observed
    time. S-hat(t) is defined for t <= t_max, and also for t > t_max when the
    largest time is an event or S-hat has reached 0; otherwise S-hat is
    undefined beyond t_max and __call__ raises ValueError there.
    """

    def __init__(self, steps: list[Step], t_max: float, last_is_event: bool, one) -> None:
        self.steps = steps
        self.t_max = t_max
        self.last_is_event = last_is_event
        self._one = one

    def __call__(self, t: float):
        s = self._one
        for step in self.steps:
            if step.time > t:
                break
            s = step.survival
        if t > self.t_max and not self.last_is_event and s != 0:
            raise ValueError("S-hat is undefined after the largest time when that time is censored")
        return s

    def median(self):
        """The smallest event time t with S-hat(t) <= 1/2, or None if S-hat stays above 1/2."""
        for step in self.steps:
            if step.survival <= self._one / 2:
                return step.time
        return None


def kaplan_meier(times: Sequence[float], events: Sequence[int], exact: bool = False) -> KaplanMeier:
    """Kaplan-Meier estimate from right-censored data.

    times[i] is the observed time y_i = min(T_i, C_i) and events[i] is 1 when
    y_i is an event time and 0 when it is a censoring time. A censoring tied
    with an event counts as at risk at that time. With exact=True the survival
    values are Fractions. Cost: one sort, O(n log n), and one O(n) scan.
    """
    n = len(times)
    if n == 0 or len(events) != n:
        raise ValueError("need the same positive number of times and event flags")
    if any(e not in (0, 1) for e in events):
        raise ValueError("event flags must be 0 or 1")
    one = Fraction(1) if exact else 1.0
    order = sorted(range(n), key=lambda k: times[k])  # @line L1
    r, s, out = n, one, []  # @line L2
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
            s = s * (one - Fraction(d, r)) if exact else s * (1.0 - d / r)
            out.append(Step(t, r, d, s))
        r -= d + c  # @line L8
    last = times[order[-1]]
    last_is_event = any(times[k] == last and events[k] for k in range(n))
    return KaplanMeier(out, last, last_is_event, one)  # @line L9


def greenwood_variance(km: KaplanMeier, t: float):
    """Greenwood's estimate S-hat(t)^2 * sum over t_j <= t of d_j / (n_j (n_j - d_j)).

    A term with d_j = n_j makes S-hat(t) = 0, and the estimate is then 0.
    """
    s = km(t)
    if s == 0:
        return s
    total = 0 * s
    for step in km.steps:
        if step.time > t:
            break
        n, d = step.at_risk, step.events
        total += Fraction(d, n * (n - d)) if isinstance(s, Fraction) else d / (n * (n - d))
    return s * s * total
