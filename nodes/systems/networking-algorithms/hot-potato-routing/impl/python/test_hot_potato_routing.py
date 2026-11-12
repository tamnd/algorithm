# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hot-potato-routing/. The authors are listed in prov/P3PE21.jsonl.

import random

from hot_potato_routing import (choose_egresses, dijkstra, nearest_egress,
                                nearest_egress_brute)


def random_graph(rng, n, extra, maxw=6):
    g = {u: {} for u in range(n)}
    for v in range(1, n):
        u = rng.randrange(v)
        g[u][v] = g[v][u] = rng.randint(1, maxw)
    for _ in range(extra if n > 1 else 0):
        u, v = rng.sample(range(n), 2)
        g[u][v] = g[v][u] = rng.randint(1, maxw)
    return g


def test_matches_brute_force_with_ties():
    for seed in range(60):
        rng = random.Random(seed)
        n = rng.randint(1, 15)
        g = random_graph(rng, n, rng.randint(0, 15), maxw=rng.choice([1, 3, 6]))
        E = rng.sample(range(n), rng.randint(1, min(n, 4)))
        label, nxt = nearest_egress(g, E)
        assert label == nearest_egress_brute(g, E)


def test_next_hops_lead_to_the_chosen_egress():
    # every router on the way picks the same egress, so forwarding is consistent
    for seed in range(40):
        rng = random.Random(1000 + seed)
        n = rng.randint(2, 15)
        g = random_graph(rng, n, rng.randint(0, 15), maxw=rng.choice([1, 4]))
        E = rng.sample(range(n), rng.randint(1, min(n, 4)))
        label, nxt = nearest_egress(g, E)
        for v in g:
            d, e = label[v]
            u, cost, steps = v, 0, 0
            while nxt[u] is not None:
                assert label[nxt[u]][1] == e
                cost += g[u][nxt[u]]
                u = nxt[u]
                steps += 1
                assert steps <= n
            assert u == e and cost == d


def test_egress_shift_after_an_igp_change():
    # D - C - A - B with egresses B and D for one prefix
    g = {"A": {"B": 5, "C": 3}, "B": {"A": 5}, "C": {"A": 3, "D": 4}, "D": {"C": 4}}
    label, _ = nearest_egress(g, ["B", "D"])
    assert label["A"] == (5, "B") and label["C"] == (4, "D")
    g["A"]["B"] = g["B"]["A"] = 9
    label, _ = nearest_egress(g, ["B", "D"])
    assert label["A"] == (7, "D") and label["C"] == (4, "D")


def test_one_change_moves_many_prefixes():
    # all prefixes reachable through both peering points move together
    rng = random.Random(5)
    g = random_graph(rng, 30, 25)
    E = [0, 29]
    before, _ = nearest_egress(g, E)
    for u in list(g[0]):                 # the links around egress 0 get dearer
        g[0][u] = g[u][0] = 20
    after, _ = nearest_egress(g, E)
    moved = [v for v in g if before[v][1] != after[v][1]]
    assert len(moved) >= 5
    d0 = dijkstra(g, 0)
    d29 = dijkstra(g, 29)
    for v in moved:
        assert (d29[v], 29) < (d0[v], 0)


def test_only_tied_routes_compete():
    routes = {"B": (-200, 2, 0), "D": (-200, 2, 0), "F": (-100, 1, 0)}
    assert choose_egresses(routes) == ["B", "D"]
    g = {"A": {"B": 5, "F": 1}, "B": {"A": 5}, "F": {"A": 1}, "D": {"B": 1}}
    g["B"]["D"] = 1
    label, _ = nearest_egress(g, choose_egresses(routes))
    # F is the nearest exit, but its route has a lower local preference
    assert label["A"] == (5, "B")
