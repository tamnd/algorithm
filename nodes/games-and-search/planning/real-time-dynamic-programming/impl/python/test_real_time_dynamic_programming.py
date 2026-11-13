# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/real-time-dynamic-programming/. The authors are listed in prov/X8DWC2.jsonl.

import random
from fractions import Fraction as F
from itertools import product

from real_time_dynamic_programming import greedy_policy, h_min, q_value, rtdp

GOALS = {0}


# ---- exact reference: enumerate deterministic policies and solve each linear system ----

def proper(m, pi):
    good = set(GOALS)
    changed = True
    while changed:
        changed = False
        for s in m:
            if s not in good and any(p > 0 and t in good for p, t in m[s][pi[s]][1]):
                good.add(s)
                changed = True
    return all(s in good for s in m)


def solve(a, b):
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = next(r for r in range(col, n) if m[r][col] != 0)
        m[col], m[piv] = m[piv], m[col]
        inv = 1 / m[col][col]
        m[col] = [x * inv for x in m[col]]
        for r in range(n):
            if r != col and m[r][col] != 0:
                f = m[r][col]
                m[r] = [x - f * y for x, y in zip(m[r], m[col])]
    return [m[i][n] for i in range(n)]


def cost(m, pi):
    states = list(m)
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    a = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    b = [F(0)] * n
    for s in states:
        c, outs = m[s][pi[s]]
        b[idx[s]] = F(c)
        for p, t in outs:
            if t not in GOALS:
                a[idx[s]][idx[t]] -= p
    x = solve(a, b)
    return {s: x[idx[s]] for s in states}


def exact_optimum(m):
    best = None
    for choice in product(*(list(m[s]) for s in m)):
        pi = dict(zip(m, choice))
        if proper(m, pi):
            v = cost(m, pi)
            best = v if best is None else {s: min(best[s], v[s]) for s in m}
    return best


def to_float(m):
    return {s: {a: (float(c), [(float(p), t) for p, t in o]) for a, (c, o) in d.items()} for s, d in m.items()}


# ---- models ----

def corridor(n=10):
    m = {}
    for s in range(1, n + 1):
        sail = [(F(1, 2), 0), (F(1, 2), 2)] if s == 1 else [(F(2, 3), s - 1), (F(1, 3), min(s + 1, n))]
        m[s] = {"row": (F(2), [(F(1), s - 1)]), "sail": (F(1), sail)}
    return m


def random_model(rng, n, k):
    states = list(range(1, n + 1))
    m = {}
    for s in states:
        acts = {}
        for a in range(k):
            targets = states + [0]
            weights = [rng.randint(0, 2) for _ in targets]
            weights[-1] += 1  # every action can reach the goal, so every policy is proper
            total = sum(weights)
            acts[a] = (F(rng.randint(1, 6)), [(F(w, total), t) for w, t in zip(weights, targets) if w])
        m[s] = acts
    return m


def test_corridor_example():
    m = to_float(corridor())
    hm = h_min(m, GOALS)
    assert hm == {s: float(s) for s in range(1, 11)}
    h = hm.__getitem__
    backups = {}
    v, lengths = rtdp(m, GOALS, 3, h, 4, random.Random(1), backups=backups)
    assert lengths == [7, 7, 3, 7]
    assert sum(backups.values()) == 24
    assert all(abs(v[s] - 2 * s) < 1e-12 for s in (1, 2, 3))
    assert greedy_policy(m, GOALS, v, h, 3) == {3: "row", 2: "row", 1: "row"}
    assert all(s not in backups for s in range(6, 11))
    assert v[4] < 8 and v[5] < 10  # off the optimal path the values stay below V*


def test_h_min_is_admissible_and_monotone():
    rng = random.Random(2)
    for _ in range(40):
        m = random_model(rng, rng.randint(1, 4), rng.randint(1, 3))
        star = exact_optimum(m)
        fm = to_float(m)
        hm = h_min(fm, GOALS)
        for s in m:
            assert hm[s] <= float(star[s]) + 1e-12
            assert hm[s] <= min(q_value(fm, GOALS, dict(hm), hm.__getitem__, s, a) for a in fm[s]) + 1e-12


def test_values_stay_admissible_and_rise():
    rng = random.Random(3)
    for _ in range(30):
        m = random_model(rng, rng.randint(2, 4), rng.randint(1, 3))
        star = exact_optimum(m)
        fm = to_float(m)
        for h in (lambda s: 0.0, h_min(fm, GOALS).__getitem__):
            v = {}
            gen = random.Random(rng.random())
            old = {}
            for _ in range(30):
                rtdp(fm, GOALS, 1, h, 1, gen, v=v)
                for s, x in v.items():
                    assert x <= float(star[s]) + 1e-9
                    assert x >= old.get(s, h(s)) - 1e-9
                old = dict(v)


def test_converges_on_relevant_states():
    """2000 trials from state 1 with seed 100 + i; compare with the exact Fraction optimum."""
    rng = random.Random(4)
    for i in range(25):
        m = random_model(rng, rng.randint(2, 5), rng.randint(2, 3))
        star = exact_optimum(m)
        fm = to_float(m)
        for h in (lambda s: 0.0, h_min(fm, GOALS).__getitem__):
            v, _ = rtdp(fm, GOALS, 1, h, 2000, random.Random(100 + i))
            pi = greedy_policy(fm, GOALS, v, h, 1)
            for s in pi:  # the states that the greedy policy reaches from the start
                assert abs(v[s] - float(star[s])) < 1e-6
            # the greedy policy is optimal from the start
            full = {s: pi.get(s, next(iter(m[s]))) for s in m}
            sub = {s: m[s] for s in pi}
            assert cost(sub, {s: full[s] for s in sub})[1] == star[1]
