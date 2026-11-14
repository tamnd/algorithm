# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aalen-johansen-estimator/. The authors are listed in prov/ZVA82Z.jsonl.
"""Aalen-Johansen estimator: cumulative incidence functions and multistate transition matrices.

Competing risks input: times[i] = y_i and causes[i] = 0 if subject i is
censored at y_i, or k in 1..K if the subject has an event of cause k at y_i.
A censored time tied with an event time counts as at risk at that time.
All the arithmetic is done in Fractions, so every output is exact for exact
input times; convert with float() for display.
"""

from collections.abc import Sequence
from fractions import Fraction
from typing import NamedTuple


class Row(NamedTuple):
    time: float  # t_j, a distinct event time (of any cause)
    at_risk: int  # n_j
    events: tuple  # (d_1j, ..., d_Kj)
    surv: Fraction  # S-hat(t_j), the all-cause Kaplan-Meier estimate
    cif: tuple  # (F_1-hat(t_j), ..., F_K-hat(t_j))


def cumulative_incidence(times: Sequence, causes: Sequence[int], n_causes: int | None = None) -> list[Row]:
    """F_k-hat(t) = sum over t_j <= t of S-hat(t_j-) d_kj / n_j, for every cause k.

    One sort, O(n log n), then one pass that costs O(K) per distinct event time.
    """
    n = len(times)
    if n == 0 or len(causes) != n:
        raise ValueError("times and causes must have the same positive length")
    if any(not isinstance(c, int) or c < 0 for c in causes):
        raise ValueError("causes must be integers >= 0 (0 = censored)")
    K = max(causes) if n_causes is None else n_causes
    if max(causes) > K:
        raise ValueError("a cause is larger than n_causes")
    order = sorted(range(n), key=lambda i: times[i])  # @line L1
    S, F, at_risk, out, i = Fraction(1), [Fraction(0)] * K, n, [], 0  # @line L2
    while i < n:  # @line L3
        t, d, leave = times[order[i]], [0] * K, 0
        while i < n and times[order[i]] == t:  # @line L4
            c = causes[order[i]]
            if c:
                d[c - 1] += 1
            leave += 1
            i += 1
        total = sum(d)
        if total:  # @line L5
            F = [F[k] + S * Fraction(d[k], at_risk) for k in range(K)]  # @line L6
            S = S * Fraction(at_risk - total, at_risk)  # @line L7
            out.append(Row(t, at_risk, tuple(d), S, tuple(F)))
        at_risk -= leave  # @line L8
    return out


def evaluate(rows: list[Row], t: float, k: int | None = None):
    """F_k-hat(t) for cause k (1-based), or S-hat(t) when k is None; step function, right-continuous."""
    value = Fraction(1) if k is None else Fraction(0)
    for r in rows:
        if r.time > t:
            break
        value = r.surv if k is None else r.cif[k - 1]
    return value


def kaplan_meier(times: Sequence, events: Sequence[int]) -> list[tuple]:
    """Plain Kaplan-Meier (time, S-hat) at each event time, for comparisons."""
    out, S = [], Fraction(1)
    for t in sorted(set(y for y, e in zip(times, events) if e)):
        n_j = sum(1 for y in times if y >= t)
        d_j = sum(1 for y, e in zip(times, events) if e and y == t)
        S *= Fraction(n_j - d_j, n_j)
        out.append((t, S))
    return out


class Subject(NamedTuple):
    start: int  # state at time 0
    moves: tuple  # ((time, new_state), ...) in increasing time
    end: float  # end of follow-up, at least the last move time


def transition_matrices(subjects: Sequence[Subject], n_states: int) -> list[tuple]:
    """Aalen-Johansen product integral P-hat(0, t) = prod over t_j <= t of (I + dA-hat(t_j)).

    dA-hat_gh(t_j) = N_gh(t_j) / Y_g(t_j) for g != h, and each row of dA-hat sums
    to 0. Y_g(t_j) counts the subjects in state g just before t_j that are under
    observation at t_j. Returns a list of (t_j, P-hat(0, t_j)), the matrix as a
    list of rows of Fractions. Cost: O(n log n + m s^2) for m distinct
    transition times and s states.
    """
    s = n_states
    events = []
    for idx, sub in enumerate(subjects):
        last = 0
        for t, h in sub.moves:
            if t < last or t > sub.end or not 0 <= h < s:
                raise ValueError("moves must be in time order, inside follow-up and to a valid state")
            last = t
            events.append((t, 0, idx, h))
        events.append((sub.end, 1, idx, None))
    events.sort(key=lambda e: (e[0], e[1]))
    state = [sub.start for sub in subjects]
    Y = [0] * s
    for g in state:
        Y[g] += 1
    P = [[Fraction(int(a == b)) for b in range(s)] for a in range(s)]
    out, i = [], 0
    while i < len(events):
        t = events[i][0]
        N = {}
        j = i
        while j < len(events) and events[j][0] == t and events[j][1] == 0:
            _, _, idx, h = events[j]
            g = state[idx]
            if h != g:
                N[(g, h)] = N.get((g, h), 0) + 1
            j += 1
        if N:
            # P <- P (I + dA): copy the old columns of the source states first.
            old = {g: [P[a][g] for a in range(s)] for g, _ in N}
            for (g, h), c in N.items():
                rate = Fraction(c, Y[g])
                for a in range(s):
                    P[a][h] += old[g][a] * rate
                    P[a][g] -= old[g][a] * rate
            out.append((t, [row[:] for row in P]))
        for e in events[i:j]:
            _, _, idx, h = e
            Y[state[idx]] -= 1
            Y[h] += 1
            state[idx] = h
        while j < len(events) and events[j][0] == t:
            Y[state[events[j][2]]] -= 1
            j += 1
        i = j
    return out


def competing_risks_subjects(times: Sequence, causes: Sequence[int]) -> list[Subject]:
    """The competing risks data as a multistate model: state 0 alive, state k for death of cause k."""
    return [Subject(0, ((y, c),) if c else (), y) for y, c in zip(times, causes)]
