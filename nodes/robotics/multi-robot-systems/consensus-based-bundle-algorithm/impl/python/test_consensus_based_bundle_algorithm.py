# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/consensus-based-bundle-algorithm/. The authors are listed in prov/FENCPV.jsonl.

import itertools
import random
from collections import deque

from consensus_based_bundle_algorithm import (
    assignment_value,
    cbba,
    decide,
    sequential_greedy,
)


def path_graph(u):
    return [[k for k in (i - 1, i + 1) if 0 <= k < u] for i in range(u)]


def random_graph(rng, u):
    nb = [set() for _ in range(u)]
    for i in range(1, u):
        k = rng.randrange(i)
        nb[i].add(k)
        nb[k].add(i)
    for _ in range(rng.randint(0, u)):
        if u > 1:
            i, k = rng.sample(range(u), 2)
            nb[i].add(k)
            nb[k].add(i)
    return [sorted(v) for v in nb]


def diameter(nb):
    best = 0
    for src in range(len(nb)):
        dist = {src: 0}
        queue = deque([src])
        while queue:
            x = queue.popleft()
            for w in nb[x]:
                if w not in dist:
                    dist[w] = dist[x] + 1
                    queue.append(w)
        best = max(best, max(dist.values()))
    return best


def brute_optimum(a, gamma, cap):
    """Brute force over every way to give each task to one agent or to nobody."""
    u, t = len(a), len(a[0])
    best = 0
    for choice in itertools.product(range(-1, u), repeat=t):
        bundles = [[j for j in range(t) if choice[j] == i] for i in range(u)]
        if any(len(bd) > cap for bd in bundles):
            continue
        best = max(best, assignment_value(a, bundles, gamma))
    return best


def check_consistent(res, u, t, cap):
    z = res["winners"]
    for i in range(u):
        assert z[i] == z[0]
        assert res["bids"][i] == res["bids"][0]
    for i in range(u):
        assert len(res["bundles"][i]) <= cap
        for j in res["bundles"][i]:
            assert z[0][j] == i
    owners = [j for i in range(u) for j in res["bundles"][i]]
    assert len(owners) == len(set(owners))
    assert sorted(owners) == sorted(j for j in range(t) if z[0][j] is not None)


def test_three_agents_on_a_path():
    a = [[10, 9], [4, 6], [8, 1]]
    res = cbba(a, path_graph(3), gamma=1.0, cap=1)
    check_consistent(res, 3, 2, 1)
    assert res["bundles"] == [[0], [1], []]
    assert res["winners"][0] == [0, 1]
    assert res["bids"][0] == [10, 6]
    assert res["rounds"] == 2
    assert assignment_value(a, res["bundles"]) == 16
    assert brute_optimum(a, 1.0, 1) == 17


def test_decision_table_cases():
    s_old, s_new = [0, 0, 0, 0], [1, 1, 1, 1]
    # sender 1 says it wins with a better bid than receiver 0
    assert decide(0, 1, 5, 1, s_old, 3, 0, s_old) == "update"
    assert decide(0, 1, 2, 1, s_old, 3, 0, s_old) == "leave"
    # sender says the receiver wins, receiver thinks the sender wins
    assert decide(0, 1, 3, 0, s_old, 4, 1, s_old) == "reset"
    # sender reports a third agent 2 with newer information
    assert decide(0, 1, 7, 2, s_new, 4, 3, s_old) == "update"
    assert decide(0, 1, 7, 2, s_old, 4, None, s_old) == "leave"
    # sender has no winner and the receiver thinks the sender wins
    assert decide(0, 1, 0, None, s_old, 4, 1, s_old) == "update"


def test_agreement_and_equal_to_sequential_greedy():
    rng = random.Random(2024)
    for _ in range(300):
        u = rng.randint(1, 6)
        t = rng.randint(1, 7)
        nb = random_graph(rng, u)
        a = [[rng.random() for _ in range(t)] for _ in range(u)]
        gamma = rng.choice([1.0, 0.9, 0.5])
        cap = rng.randint(1, t)
        res = cbba(a, nb, gamma, cap)
        check_consistent(res, u, t, cap)
        sga = sequential_greedy(a, gamma, cap)
        assert res["winners"][0] == sga["winners"]
        n_min = min(t, cap * u)
        assert res["rounds"] <= n_min * max(1, diameter(nb))


def test_ties_still_agree():
    rng = random.Random(17)
    for _ in range(200):
        u = rng.randint(2, 5)
        t = rng.randint(1, 6)
        nb = random_graph(rng, u)
        a = [[rng.randint(1, 3) for _ in range(t)] for _ in range(u)]
        cap = rng.randint(1, t)
        res = cbba(a, nb, 1.0, cap)
        check_consistent(res, u, t, cap)


def test_half_of_optimum_under_dmg():
    rng = random.Random(99)
    worst = 1.0
    for _ in range(60):
        u = rng.randint(1, 3)
        t = rng.randint(1, 5)
        nb = random_graph(rng, u)
        a = [[rng.uniform(0.1, 1.0) for _ in range(t)] for _ in range(u)]
        gamma = rng.choice([1.0, 0.8, 0.5])
        cap = rng.randint(1, t)
        res = cbba(a, nb, gamma, cap)
        got = assignment_value(a, res["bundles"], gamma)
        assert abs(got - sum(v for v in res["bids"][0] if v)) < 1e-12
        opt = brute_optimum(a, gamma, cap)
        assert got <= opt + 1e-12
        assert 2 * got >= opt - 1e-12
        worst = min(worst, got / opt)
    assert worst < 1.0


def test_line_needs_diameter_rounds():
    # One task that every agent wants; the best agent sits at one end.
    for u in range(2, 8):
        a = [[float(i + 1)] for i in range(u)]
        res = cbba(a, path_graph(u), cap=1)
        assert res["winners"][0] == [u - 1]
        assert res["rounds"] == u - 1
