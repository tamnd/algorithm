# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/log-rank-test/. The authors are listed in prov/W9TSMC.jsonl.

import itertools
import math
import random
from collections.abc import Sequence
from fractions import Fraction
from typing import NamedTuple

from stdist import chi2_sf


class Row(NamedTuple):
    """One distinct event time of the log-rank table."""

    time: float
    at_risk: int  # n_j
    at_risk1: int  # n_1j, at risk in group 1
    events: int  # d_j
    events1: int  # d_1j, events in group 1
    expected1: float  # E_1j = d_j n_1j / n_j
    variance: float  # V_j = n_1j n_0j d_j (n_j - d_j) / (n_j^2 (n_j - 1))
    weight: float  # w_j


class LogRankResult(NamedTuple):
    observed1: int  # O_1, events in group 1
    expected1: float  # E_1 = sum of E_1j
    score: float  # U = sum of w_j (d_1j - E_1j)
    variance: float  # V = sum of w_j^2 V_j
    statistic: float  # U^2 / V
    p_value: float  # upper tail of chi-square with 1 degree of freedom
    rows: list[Row]


WEIGHTS = ("logrank", "gehan", "tarone-ware", "peto-peto", "fleming-harrington")


def _check(times, events, groups):
    n = len(times)
    if n == 0 or len(events) != n or len(groups) != n:
        raise ValueError("times, events and groups must have the same positive length")
    if any(e not in (0, 1) for e in events) or any(g not in (0, 1) for g in groups):
        raise ValueError("event flags and group labels must be 0 or 1")
    if sum(groups) in (0, n):
        raise ValueError("both groups must be non-empty")


def log_rank(
    times: Sequence[float],
    events: Sequence[int],
    groups: Sequence[int],
    weights: str = "logrank",
    rho: float = 0.0,
    gamma: float = 0.0,
    exact: bool = False,
) -> LogRankResult:
    """Two-sample weighted log-rank test.

    times[i] = min(T_i, C_i), events[i] = 1 for an event and 0 for a censoring,
    groups[i] in {0, 1}. U > 0 means more events in group 1 than expected under
    equal hazards. weights: 'logrank' (w = 1), 'gehan' (w = n_j), 'tarone-ware'
    (w = sqrt(n_j)), 'peto-peto' (w = prod over t_l <= t_j of (1 - d_l/(n_l + 1)))
    or 'fleming-harrington' (w = S(t_j-)^rho (1 - S(t_j-))^gamma, S the pooled
    Kaplan-Meier). exact=True keeps the table and U and V as Fractions (only for
    the rational weights 'logrank' and 'gehan'). Cost: O(n log n).
    """
    _check(times, events, groups)
    if weights not in WEIGHTS:
        raise ValueError(f"weights must be one of {WEIGHTS}")
    if exact and weights not in ("logrank", "gehan"):
        raise ValueError("exact arithmetic needs rational weights")
    num = (lambda a, b: Fraction(a, b)) if exact else (lambda a, b: a / b)
    n = len(times)
    order = sorted(range(n), key=lambda k: times[k])  # @line L1
    r, r1, u, v = n, sum(groups), 0, 0  # @line L2
    km, peto = 1.0, 1.0  # pooled Kaplan-Meier S(t-) and the Peto-Peto product
    rows, o1, e1 = [], 0, 0
    i = 0  # @line L3
    while i < n:  # @line L4
        t, d, d1, m, m1 = times[order[i]], 0, 0, 0, 0  # @line L5
        while i < n and times[order[i]] == t:  # @line L6
            k = order[i]
            m += 1
            m1 += groups[k]
            if events[k]:
                d += 1
                d1 += groups[k]
            i += 1
        if d > 0:  # @line L7
            e = num(d * r1, r)  # @line L8
            var = num(r1 * (r - r1) * d * (r - d), r * r * (r - 1)) if r > 1 else 0 * e
            if weights == "logrank":
                w = 1
            elif weights == "gehan":
                w = r
            elif weights == "tarone-ware":
                w = math.sqrt(r)
            elif weights == "peto-peto":
                peto *= 1 - d / (r + 1)
                w = peto
            else:
                w = km**rho * (1 - km) ** gamma
            u += w * (d1 - e)  # @line L9
            v += w * w * var
            o1 += d1
            e1 += e
            rows.append(Row(t, r, r1, d, d1, e, var, w))
            km *= 1 - d / r
        r -= m  # @line L10
        r1 -= m1
    if v == 0:
        raise ValueError("the variance is zero: no event time with both groups at risk")
    stat = u * u / v  # @line L11
    return LogRankResult(o1, e1, u, v, stat, chi2_sf(float(stat), 1), rows)


def log_rank_permutation(
    times: Sequence[float],
    events: Sequence[int],
    groups: Sequence[int],
    weights: str = "logrank",
    b: int | None = None,
    rng: random.Random | None = None,
) -> float:
    """Two-sided permutation p-value of the weighted log-rank score U.

    Under H0 the labels are exchangeable given the observed (time, event)
    pairs; this holds when the two groups have the same censoring distribution.
    With b=None every relabelling with the same group sizes is enumerated and
    the p-value is the exact fraction with |U*| >= |U|. Otherwise b random
    relabellings give (1 + #{|U*| >= |U|}) / (1 + b).
    """
    _check(times, events, groups)
    n, n1 = len(times), sum(groups)

    def score(labels):
        try:
            return abs(log_rank(times, events, labels, weights=weights).score)
        except ValueError:  # V = 0 for this labelling; U is then 0 as well
            return 0.0

    obs = score(groups)
    tol = 1e-9 * (1 + obs)

    def extreme(labels):
        return score(labels) >= obs - tol

    if b is None:
        count = total = 0
        for chosen in itertools.combinations(range(n), n1):
            labels = [0] * n
            for k in chosen:
                labels[k] = 1
            total += 1
            count += extreme(labels)
        return count / total
    if rng is None:
        raise ValueError("pass a random.Random for the Monte Carlo version")
    labels = list(groups)
    count = 0
    for _ in range(b):
        rng.shuffle(labels)
        count += extreme(labels)
    return (1 + count) / (1 + b)
