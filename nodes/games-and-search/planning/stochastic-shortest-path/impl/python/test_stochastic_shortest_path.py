# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stochastic-shortest-path/. The authors are listed in prov/4D16F2.jsonl.

import heapq
import random
from fractions import Fraction as F
from itertools import product

import pytest

from stochastic_shortest_path import (
    all_policies_proper,
    bellman_operator,
    greedy_policy,
    is_proper,
    optimal_by_enumeration,
    policy_cost,
    proper_states,
    value_iteration,
    with_give_up,
)

GOALS = {0}


def boat():
    m = {}
    for s in (1, 2, 3):
        sail = [(F(1, 2), 0), (F(1, 2), 2)] if s == 1 else [(F(2, 3), s - 1), (F(1, 3), s)]
        m[s] = {"row": (F(2), [(F(1), s - 1)]), "sail": (F(1), sail)}
    return m


def to_float(m):
    return {s: {a: (float(c), [(float(p), t) for p, t in o]) for a, (c, o) in d.items()} for s, d in m.items()}


def close(v, w, tol=1e-7):
    return all(abs(float(v[s]) - float(w[s])) <= tol * (1 + abs(float(v[s]))) for s in v)


def test_boat_exact():
    m = boat()
    v, pi = optimal_by_enumeration(m, GOALS)
    assert v == {1: F(2), 2: F(7, 2), 3: F(5)}
    assert pi == {1: "row", 2: "sail", 3: "sail"}
    assert bellman_operator(m, GOALS, v) == v
    assert policy_cost(m, GOALS, {1: "sail", 2: "sail", 3: "sail"}) == {1: F(7, 2), 2: F(5), 3: F(13, 2)}


def test_value_iteration_from_any_start():
    m = boat()
    v, _ = optimal_by_enumeration(m, GOALS)
    for start in [0.0, 100.0, -50.0]:
        x, _ = value_iteration(to_float(m), GOALS, {s: start for s in m}, 1e-12, 10000)
        assert close(v, x)


def test_improper_policy_with_infinite_cost_keeps_the_theorem():
    m = boat()
    for s in m:
        m[s]["anchor"] = (F(1), [(F(1), s)])
    assert not all_policies_proper(m, GOALS)
    v, pi = optimal_by_enumeration(m, GOALS)
    assert v == {1: F(2), 2: F(7, 2), 3: F(5)}
    x, _ = value_iteration(to_float(m), GOALS, {s: 0.0 for s in m}, 1e-12, 10000)
    assert close(v, x)


def test_zero_cost_improper_loop_breaks_uniqueness():
    m = boat()
    m[2]["drift"] = (F(0), [(F(1), 2)])
    low, _ = value_iteration(to_float(m), GOALS, {s: 0.0 for s in m}, 1e-12, 10000)
    high, _ = value_iteration(to_float(m), GOALS, {s: 100.0 for s in m}, 1e-12, 10000)
    assert abs(low[2]) < 1e-9  # drifting forever costs 0
    assert abs(high[2] - 3.5) < 1e-9  # the proper optimum is also a fixed point
    assert abs(high[3] - 5.0) < 1e-9


def test_dead_end():
    m = boat()
    m[3]["rocks"] = (F(1), [(F(3, 4), 0), (F(1, 4), "W")])
    m["W"] = {"wait": (F(1), [(F(1), "W")])}
    assert proper_states(m, GOALS) == {1, 2, 3}
    with pytest.raises(ValueError):
        optimal_by_enumeration(m, GOALS)
    with pytest.raises(RuntimeError):
        value_iteration(to_float(m), GOALS, {s: 0.0 for s in m}, 1e-9, 2000)
    x = {s: 0.0 for s in m}
    fm = to_float(m)
    for k in range(1, 30):
        x = bellman_operator(fm, GOALS, x)
        assert greedy_policy(fm, GOALS, x)[3] == ("rocks" if k <= 15 else "sail")
        assert x["W"] == k
    cheap, pi = optimal_by_enumeration(with_give_up(m, 0, F(8)), GOALS)
    assert pi[3] == "rocks" and cheap[3] == F(3) and cheap["W"] == F(8)
    dear, pi = optimal_by_enumeration(with_give_up(m, 0, F(20)), GOALS)
    assert pi[3] == "sail" and dear[3] == F(5)


def random_model(rng, n, k, loops):
    states = list(range(1, n + 1))
    m = {}
    for s in states:
        acts = {}
        for a in range(k):
            targets = states + [0]
            weights = [rng.randint(0, 2) for _ in targets]
            if not loops:
                weights[-1] += 1
            if sum(weights) == 0:
                weights[rng.randrange(len(weights))] = 1
            total = sum(weights)
            acts[a] = (F(rng.randint(1, 5)), [(F(w, total), t) for w, t in zip(weights, targets) if w])
        m[s] = acts
    return m


def brute_proper_from(m, s):
    for choice in product(*(list(m[t]) for t in m)):
        pi = dict(zip(m, choice))
        good = set(GOALS)
        changed = True
        while changed:
            changed = False
            for t in m:
                if t not in good and any(p > 0 and u in good for p, u in m[t][pi[t]][1]):
                    good.add(t)
                    changed = True
        # every state reachable from s under pi must be able to reach the goal
        seen, stack = {s}, [s]
        while stack:
            t = stack.pop()
            for p, u in m[t][pi[t]][1]:
                if p > 0 and u not in GOALS and u not in seen:
                    seen.add(u)
                    stack.append(u)
        if seen <= good:
            return True
    return False


def test_structure_checks_against_brute_force():
    rng = random.Random(11)
    for _ in range(150):
        m = random_model(rng, rng.randint(1, 4), rng.randint(1, 2), True)
        every = all(is_proper(m, GOALS, dict(zip(m, c))) for c in product(*(list(m[s]) for s in m)))
        assert all_policies_proper(m, GOALS) == every
        assert proper_states(m, GOALS) == {s for s in m if brute_proper_from(m, s)}


def test_value_iteration_against_exact_solve():
    rng = random.Random(5)
    for _ in range(30):
        m = random_model(rng, rng.randint(1, 4), rng.randint(1, 3), False)
        assert all_policies_proper(m, GOALS)
        v, _ = optimal_by_enumeration(m, GOALS)
        x, _ = value_iteration(to_float(m), GOALS, {s: 0.0 for s in m}, 1e-13, 100000)
        assert close(v, x, 1e-8)


def test_deterministic_ssp_is_shortest_path():
    rng = random.Random(3)
    for _ in range(40):
        n = rng.randint(2, 7)
        edges = {s: {} for s in range(1, n + 1)}
        for s in edges:
            for t in rng.sample(range(n + 1), rng.randint(1, 3)):
                if t != s:
                    edges[s][t] = rng.randint(1, 9)
        m = {s: {t: (F(c), [(F(1), t)]) for t, c in out.items()} for s, out in edges.items() if out}
        # Dijkstra on the reversed graph from the goal
        rev = {}
        for s, out in edges.items():
            for t, c in out.items():
                rev.setdefault(t, []).append((s, c))
        dist = {0: 0}
        heap = [(0, 0)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for s, c in rev.get(u, []):
                if d + c < dist.get(s, float("inf")):
                    dist[s] = d + c
                    heapq.heappush(heap, (d + c, s))
        if not m or any(s not in dist for s in m):
            continue
        v, _ = optimal_by_enumeration(m, GOALS)
        assert all(v[s] == dist[s] for s in m)
