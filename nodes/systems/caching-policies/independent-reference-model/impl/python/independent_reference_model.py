# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/independent-reference-model/. The authors are listed in prov/A6MTB2.jsonl.

"""Exact hit ratios under the independent reference model (IRM), with Fraction arithmetic."""

import itertools
import random
from fractions import Fraction
from typing import Dict, List, Sequence, Tuple


def a0_hit_ratio(p: Sequence[Fraction], k: int) -> Fraction:
    """A0 keeps the k most probable pages, so its long-run hit ratio is the sum of the k largest p_i."""
    return sum(sorted(p, reverse=True)[:k], Fraction(0))


def lru_state_probability(p: Sequence[Fraction], state: Tuple[int, ...]) -> Fraction:
    """Limit probability that the LRU cache holds state, most recent page first:
    the product over j of p[i_j] / (1 - p[i_1] - ... - p[i_(j-1)])."""
    prob, used = Fraction(1), Fraction(0)
    for i in state:
        prob *= p[i] / (1 - used)
        used += p[i]
    return prob


def lru_hit_ratio(p: Sequence[Fraction], k: int) -> Fraction:
    """Long-run LRU hit ratio from the closed form, by a sum over the ordered k-tuples of pages."""
    n = len(p)
    if k >= n:
        return Fraction(1)
    total = Fraction(0)
    for state in itertools.permutations(range(n), k):
        total += lru_state_probability(p, state) * sum((p[i] for i in state), Fraction(0))
    return total


def _transitions(p: Sequence[Fraction], k: int) -> Tuple[List[Tuple[int, ...]], Dict[Tuple[int, ...], Dict[Tuple[int, ...], Fraction]]]:
    n = len(p)
    states = list(itertools.permutations(range(n), k))
    step: Dict[Tuple[int, ...], Dict[Tuple[int, ...], Fraction]] = {}
    for s in states:
        row: Dict[Tuple[int, ...], Fraction] = {}
        for i in range(n):
            if i in s:
                t = (i,) + tuple(x for x in s if x != i)
            else:
                t = (i,) + s[:-1]
            row[t] = row.get(t, Fraction(0)) + p[i]
        step[s] = row
    return states, step


State = Tuple[int, ...]
Step = Dict[State, Dict[State, Fraction]]


def _solve(states: List[State], step: Step) -> Dict[State, Fraction]:
    """Stationary distribution of an irreducible chain on states, by exact Gaussian elimination."""
    index = {s: j for j, s in enumerate(states)}
    m = len(states)
    # Equations: sum_s pi(s) P(s, t) - pi(t) = 0 for each t, with the last one replaced by sum pi = 1.
    a = [[Fraction(0)] * (m + 1) for _ in range(m)]
    for s in states:
        for t, q in step[s].items():
            a[index[t]][index[s]] += q
    for j in range(m):
        a[j][j] -= 1
    a[m - 1] = [Fraction(1)] * m + [Fraction(1)]
    for col in range(m):
        piv = next(r for r in range(col, m) if a[r][col] != 0)
        a[col], a[piv] = a[piv], a[col]
        lead = a[col][col]
        a[col] = [v / lead for v in a[col]]
        for r in range(m):
            if r != col and a[r][col] != 0:
                f = a[r][col]
                a[r] = [x - f * y for x, y in zip(a[r], a[col])]
    return {s: a[index[s]][m] for s in states}


def lru_stationary(p: Sequence[Fraction], k: int) -> Dict[State, Fraction]:
    """Stationary distribution of the LRU chain on full caches (ordered, most recent first)."""
    states, step = _transitions(p, k)
    return _solve(states, step)


def _reachable(start: State, step: Step) -> List[State]:
    seen, todo = {start}, [start]
    while todo:
        s = todo.pop()
        for t in step[s]:
            if t not in seen:
                seen.add(t)
                todo.append(t)
    return sorted(seen)


def _hit_ratio(p: Sequence[Fraction], pi: Dict[State, Fraction]) -> Fraction:
    return sum((w * sum((p[i] for i in s), Fraction(0)) for s, w in pi.items()), Fraction(0))


def fifo_hit_ratio_by_chain(p: Sequence[Fraction], k: int) -> Fraction:
    """Long-run FIFO hit ratio. State: the queue, newest first. A hit leaves it unchanged; a miss on i
    gives (i,) + s[:-1]. The chain can have several closed classes, so solve on the class reached
    from the start state (0, 1, ..., k - 1)."""
    n = len(p)
    if k >= n:
        return Fraction(1)
    step: Step = {}
    for s in itertools.permutations(range(n), k):
        row: Dict[State, Fraction] = {}
        for i in range(n):
            t = s if i in s else (i,) + s[:-1]
            row[t] = row.get(t, Fraction(0)) + p[i]
        step[s] = row
    states = _reachable(tuple(range(k)), step)
    return _hit_ratio(p, _solve(states, {s: step[s] for s in states}))


def random_hit_ratio_by_chain(p: Sequence[Fraction], k: int) -> Fraction:
    """Long-run hit ratio of RANDOM replacement: on a miss on i, each of the k resident pages is
    evicted with probability 1/k. State: the sorted set of resident pages."""
    n = len(p)
    if k >= n:
        return Fraction(1)
    states = list(itertools.combinations(range(n), k))
    step: Step = {}
    for s in states:
        row: Dict[State, Fraction] = {}
        for i in range(n):
            if i in s:
                row[s] = row.get(s, Fraction(0)) + p[i]
                continue
            for out in s:
                t = tuple(sorted([x for x in s if x != out] + [i]))
                row[t] = row.get(t, Fraction(0)) + p[i] / k
        step[s] = row
    return _hit_ratio(p, _solve(states, step))


def product_form_hit_ratio(p: Sequence[Fraction], k: int) -> Fraction:
    """Closed form for FIFO and RANDOM: the set S is resident with probability proportional to the
    product of p_i over i in S."""
    n = len(p)
    if k >= n:
        return Fraction(1)
    weights = {}
    for s in itertools.combinations(range(n), k):
        w = Fraction(1)
        for i in s:
            w *= p[i]
        weights[s] = w
    z = sum(weights.values(), Fraction(0))
    return _hit_ratio(p, {s: w / z for s, w in weights.items()})


def lru_hit_ratio_by_chain(p: Sequence[Fraction], k: int) -> Fraction:
    """The long-run hit ratio from the exact stationary distribution of the chain."""
    if k >= len(p):
        return Fraction(1)
    pi = lru_stationary(p, k)
    return sum((w * sum((p[i] for i in s), Fraction(0)) for s, w in pi.items()), Fraction(0))


def irm_trace(p: Sequence[float], n: int, rng: random.Random) -> List[int]:
    """n independent requests with P(page i) = p[i]."""
    return rng.choices(range(len(p)), weights=p, k=n)
