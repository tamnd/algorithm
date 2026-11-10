# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/awerbuch-leader-election/. The authors are listed in prov/ESZB9E.jsonl.

import math
import random

from awerbuch_leader_election import awerbuch_structure, kruskal, random_connected_graph


def graphs(max_n: int, per_n: int):
    for n in range(1, max_n + 1):
        for s in range(per_n):
            rng = random.Random(7000 * n + s)
            adj = random_connected_graph(n, rng.randrange(0, 3 * n + 1), rng)
            ids = rng.sample(range(1, 100 * n + 100), n)
            yield n, adj, ids


def links(adj):
    return sum(len(a) for a in adj) // 2


def test_one_leader_known_to_all():
    for n, adj, ids in graphs(40, 15):
        res = awerbuch_structure(adj, ids)
        assert set(res["roots"]) == {res["leader"]}


def test_the_tree_is_the_minimum_spanning_tree():
    for n, adj, ids in graphs(40, 15):
        res = awerbuch_structure(adj, ids)
        assert res["tree"] == kruskal(adj, ids)


def test_phases_and_message_bound():
    for n, adj, ids in graphs(50, 10):
        res = awerbuch_structure(adj, ids)
        m = links(adj)
        phases = math.floor(math.log2(n)) + 1
        assert res["phases"] <= phases
        c = res["counts"]
        assert c["TEST"] - c["ACCEPT"] == c["REJECT"] <= 2 * m
        assert c["HELLO"] == 2 * m
        assert res["messages"] <= 5 * n * phases + 6 * m + (n - 1)


def test_page_example():
    ids = [4, 9, 2, 7, 5, 1]
    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4), (3, 5), (4, 5)]
    adj = [[] for _ in ids]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    res = awerbuch_structure(adj, ids)
    assert res["leader"] == 4
    assert res["phases"] == 3
    assert res["tree"] == [(0, 2), (1, 2), (2, 4), (3, 5), (4, 5)]
    assert res["messages"] == 74
    assert res["counts"] == {"HELLO": 16, "INITIATE": 9, "TEST": 13, "ACCEPT": 10, "REJECT": 3, "REPORT": 9,
                             "CHANGE": 1, "CONNECT": 8, "LEADER": 5}


def test_ring_and_complete_graph():
    rng = random.Random(5)
    n = 64
    ring = [[(v - 1) % n, (v + 1) % n] for v in range(n)]
    full = [[w for w in range(n) if w != v] for v in range(n)]
    for adj in (ring, full):
        ids = rng.sample(range(10**6), n)
        res = awerbuch_structure(adj, ids)
        assert res["tree"] == kruskal(adj, ids)
        assert res["messages"] <= 5 * n * 7 + 6 * links(adj) + n - 1
