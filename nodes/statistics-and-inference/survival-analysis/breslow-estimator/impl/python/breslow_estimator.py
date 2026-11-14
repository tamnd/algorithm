# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/breslow-estimator/. The authors are listed in prov/NMKKND.jsonl.
"""Breslow estimator of the cumulative baseline hazard of a Cox model.

Input: times[i] = y_i, events[i] = delta_i (1 event, 0 censored) and the risk
scores w_i = exp(x_i' beta) for a given coefficient vector beta (usually the
Cox estimate). A censored time tied with an event time counts as at risk.
With ints or Fractions as scores the output is exact.
"""

import math
from collections.abc import Sequence
from fractions import Fraction
from typing import NamedTuple


class Step(NamedTuple):
    time: float  # t_j, a distinct event time
    risk_sum: object  # S0_j, the sum of w_i over the risk set {i : y_i >= t_j}
    events: int  # d_j
    increment: object  # the jump of H0-hat at t_j
    cum_hazard: object  # H0-hat(t_j)
    var: object  # sum over t_l <= t_j of d_l / S0_l^2, the variance with beta held fixed


def _div(a, b):
    if isinstance(a, (int, Fraction)) and isinstance(b, (int, Fraction)):
        return Fraction(a) / b
    return a / b


def breslow(times: Sequence, events: Sequence[int], scores: Sequence, ties: str = "breslow") -> list[Step]:
    """Cumulative baseline hazard H0-hat at each distinct event time.

    ties='breslow' adds d_j / S0_j; ties='efron' adds the sum over r < d_j of
    1 / (S0_j - (r / d_j) D_j), with D_j the sum of w over the d_j events.
    The risk sums are accumulated from the largest time down, so no running
    subtraction loses accuracy. Cost: one sort, O(n log n), and two O(n) passes.
    """
    n = len(times)
    if n == 0 or len(events) != n or len(scores) != n:
        raise ValueError("times, events and scores must have the same positive length")
    if any(e not in (0, 1) for e in events):
        raise ValueError("event flags must be 0 or 1")
    if any(not w > 0 for w in scores):
        raise ValueError("risk scores must be positive")
    if ties not in ("breslow", "efron"):
        raise ValueError("ties must be 'breslow' or 'efron'")
    order = sorted(range(n), key=lambda k: times[k], reverse=True)  # @line L1
    S, rows, i = 0, [], 0  # @line L2
    while i < n:  # @line L3
        t, d, D = times[order[i]], 0, 0
        while i < n and times[order[i]] == t:  # @line L4
            k = order[i]
            S += scores[k]
            if events[k]:
                d += 1
                D += scores[k]
            i += 1
        if d > 0:  # @line L5
            rows.append((t, S, d, D))
    rows.reverse()  # @line L6
    H, V, out = 0, 0, []
    for t, S, d, D in rows:  # @line L7
        if ties == "breslow" or d == 1:
            inc = _div(d, S)  # @line L8
        else:
            inc = sum(_div(1, S - _div(r * D, d)) for r in range(d))
        H += inc  # @line L9
        V += _div(d, S * S)
        out.append(Step(t, S, d, inc, H, V))
    return out


def risk_scores(X: Sequence[Sequence[float]], beta: Sequence[float]) -> list[float]:
    """w_i = exp(x_i' beta); the integer 1 for every i when beta = 0."""
    if all(b == 0 for b in beta):
        return [1] * len(X)
    return [math.exp(sum(a * b for a, b in zip(x, beta))) for x in X]


def evaluate(steps: list[Step], t: float):
    """H0-hat(t): the value at the last event time <= t, and 0 before the first."""
    lo, hi = 0, len(steps)
    while lo < hi:
        mid = (lo + hi) // 2
        if steps[mid].time <= t:
            lo = mid + 1
        else:
            hi = mid
    return steps[lo - 1].cum_hazard if lo else 0


def survival(steps: list[Step], t: float, score: float) -> float:
    """S-hat(t | x) = exp(-H0-hat(t) exp(x' beta)), with score = exp(x' beta)."""
    return math.exp(-float(evaluate(steps, t)) * float(score))


def cox_snell_residuals(times: Sequence, steps: list[Step], scores: Sequence) -> list:
    """r_i = H0-hat(y_i) w_i. With Breslow ties they sum to the number of events, for any beta."""
    return [evaluate(steps, y) * w for y, w in zip(times, scores)]
