# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/harrell-c-index/. The authors are listed in prov/JWHWF0.jsonl.

import math
from collections.abc import Sequence
from fractions import Fraction
from typing import NamedTuple


class Concordance(NamedTuple):
    concordant: float  # comparable pairs where the earlier failure has the higher risk
    discordant: float  # comparable pairs where it has the lower risk
    tied_risk: float  # comparable pairs with equal risk
    comparable: float  # all comparable pairs (weighted for Uno's C)
    c_index: float  # (concordant + tied_risk / 2) / comparable


def _check(times, events, risk):
    n = len(times)
    if n == 0 or len(events) != n or len(risk) != n:
        raise ValueError("times, events and risk must have the same positive length")
    if any(e not in (0, 1) for e in events):
        raise ValueError("event flags must be 0 or 1")


class _Fenwick:
    """Prefix sums over positions 1..size, with point updates."""

    def __init__(self, size):
        self.tree = [0] * (size + 1)

    def add(self, pos, value):
        while pos < len(self.tree):
            self.tree[pos] += value
            pos += pos & -pos

    def prefix(self, pos):
        total = 0
        while pos > 0:
            total += self.tree[pos]
            pos -= pos & -pos
        return total


def _count(times, events, risk, weight):
    """Weighted counts of the comparable pairs (i, j): events[i] = 1 and j outlasts i.

    j outlasts i when times[j] > times[i], or times[j] == times[i] and j is censored.
    The pair has weight weight[i]. Subjects are visited from the latest time down,
    and a Fenwick tree over the risk ranks holds the subjects that outlast the current one.
    """
    n = len(times)
    ranks = {r: k + 1 for k, r in enumerate(sorted(set(risk)))}
    tree = _Fenwick(len(ranks))
    order = sorted(range(n), key=lambda k: times[k], reverse=True)
    conc = disc = tied = comp = 0
    inside = 0
    i = 0
    while i < n:
        t = times[order[i]]
        group = []
        while i < n and times[order[i]] == t:
            group.append(order[i])
            i += 1
        # Censored subjects at t outlast the events at t, so they enter the tree first.
        for k in group:
            if not events[k]:
                tree.add(ranks[risk[k]], 1)
                inside += 1
        for k in group:
            if events[k]:
                r = ranks[risk[k]]
                lower = tree.prefix(r - 1)
                equal = tree.prefix(r) - lower
                higher = inside - lower - equal
                w = weight[k]
                conc += w * lower
                tied += w * equal
                disc += w * higher
                comp += w * inside
        for k in group:
            if events[k]:
                tree.add(ranks[risk[k]], 1)
                inside += 1
    return conc, disc, tied, comp


def harrell_c(times: Sequence[float], events: Sequence[int], risk: Sequence[float], exact: bool = False) -> Concordance:
    """Harrell's C: among the comparable pairs, the fraction where the earlier failure has the
    higher predicted risk, with risk ties counted 1/2.

    A pair (i, j) is comparable when i has an observed event and j is known to outlast it:
    times[j] > times[i], or times[j] == times[i] with j censored. Pairs of two events at the
    same time are not comparable. A higher risk predicts an earlier event. O(n log n).
    """
    _check(times, events, risk)
    conc, disc, tied, comp = _count(times, events, risk, [1] * len(times))
    if comp == 0:
        raise ValueError("there are no comparable pairs")
    num = Fraction(2 * conc + tied, 2 * comp) if exact else (conc + tied / 2) / comp
    return Concordance(conc, disc, tied, comp, num)


def censoring_survival(times: Sequence[float], events: Sequence[int]) -> list[float]:
    """G(times[i]-) for each i, the Kaplan-Meier estimate of P(C >= t) with the censorings as
    the events. Events at a time precede censorings at the same time, so they stay at risk."""
    n = len(times)
    order = sorted(range(n), key=lambda k: times[k])
    g_before = [1.0] * n
    g, at_risk, i = 1.0, n, 0
    while i < n:
        t = times[order[i]]
        group = []
        while i < n and times[order[i]] == t:
            group.append(order[i])
            i += 1
        for k in group:
            g_before[k] = g
        c = sum(1 for k in group if not events[k])
        if c:
            g *= 1 - c / at_risk
        at_risk -= len(group)
    return g_before


def uno_c(times: Sequence[float], events: Sequence[int], risk: Sequence[float], tau: float = math.inf) -> Concordance:
    """Uno's C: Harrell's pair counts with weight G(t_i-)^(-2) on each pair whose earlier time
    t_i is an event before tau, where G is the Kaplan-Meier curve of the censoring times. It
    estimates P(risk_i > risk_j | T_i < T_j, T_i < tau) when censoring is independent of the
    risk score and of T. O(n log n)."""
    _check(times, events, risk)
    g = censoring_survival(times, events)
    weight = []
    for t, e, gi in zip(times, events, g):
        if e and t < tau:
            if gi <= 0:
                raise ValueError("the censoring survival is 0 before tau; choose a smaller tau")
            weight.append(1.0 / (gi * gi))
        else:
            weight.append(0.0)
    # Uno's pairs need t_j > t_i strictly; a censoring tied with an event is not counted.
    conc, disc, tied, comp = _count_strict(times, events, risk, weight)
    if comp == 0:
        raise ValueError("there are no comparable pairs before tau")
    return Concordance(conc, disc, tied, comp, (conc + tied / 2) / comp)


def _count_strict(times, events, risk, weight):
    """As _count, but j must have times[j] > times[i] strictly."""
    n = len(times)
    ranks = {r: k + 1 for k, r in enumerate(sorted(set(risk)))}
    tree = _Fenwick(len(ranks))
    order = sorted(range(n), key=lambda k: times[k], reverse=True)
    conc = disc = tied = comp = 0.0
    inside, i = 0, 0
    while i < n:
        t = times[order[i]]
        group = []
        while i < n and times[order[i]] == t:
            group.append(order[i])
            i += 1
        for k in group:
            if events[k] and weight[k]:
                r = ranks[risk[k]]
                lower = tree.prefix(r - 1)
                equal = tree.prefix(r) - lower
                w = weight[k]
                conc += w * lower
                tied += w * equal
                disc += w * (inside - lower - equal)
                comp += w * inside
        for k in group:
            tree.add(ranks[risk[k]], 1)
            inside += 1
    return conc, disc, tied, comp
