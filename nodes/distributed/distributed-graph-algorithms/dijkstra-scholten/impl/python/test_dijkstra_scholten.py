# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dijkstra-scholten/. The authors are listed in prov/PQWDHA.jsonl.

import random

from dijkstra_scholten import DSNode, simulate

KINDS = ["tree", "path", "grid", "gnp"]


def edges_to_adj(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in sorted(edges):
        adj[u].append(v)
        adj[v].append(u)
    return adj


def make_graph(kind, n, seed):
    rng = random.Random(seed)
    tree = {(rng.randrange(v), v) for v in range(1, n)}
    if kind == "path":
        return edges_to_adj(n, {(v - 1, v) for v in range(1, n)})
    if kind == "tree":
        return edges_to_adj(n, tree)
    if kind == "grid":
        a = max(1, int(n**0.5))
        b = max(1, n // a)
        edges = set()
        for i in range(a):
            for j in range(b):
                v = i * b + j
                if j + 1 < b:
                    edges.add((v, v + 1))
                if i + 1 < a:
                    edges.add((v, v + b))
        return edges_to_adj(a * b, edges)
    p = rng.uniform(0.05, 0.4)
    edges = set(tree)
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < p:
                edges.add((u, v))
    return edges_to_adj(n, edges)


def test_hand_trace():
    # Root 0 sends to 1; 1 sends to 2 and back to 0; everyone goes passive.
    r, a, b = DSNode(0, 0), DSNode(1, 0), DSNode(2, 0)
    r.on_send_basic()
    assert a.on_basic(0) == [] and a.parent == 0  # 1 is engaged by 0
    assert r.on_passive() == [] and not r.announced  # deficit of 0 is 1
    a.on_send_basic()
    a.on_send_basic()
    assert b.on_basic(1) == [] and b.parent == 1
    assert r.on_basic(1) == [1]  # root is engaged: signal at once
    assert a.on_signal() == []  # 1 still has deficit 1
    assert r.on_passive() == [] and not r.announced
    assert a.on_passive() == []  # deficit 1 (node 2 is its child)
    assert b.on_passive() == [1] and not b.engaged  # 2 leaves and signals 1
    assert a.on_signal() == [0] and not a.engaged  # 1 leaves and signals 0
    assert r.on_signal() == [] and r.announced


def test_announces_exactly_after_termination_with_one_signal_per_message():
    for seed in range(300):
        adj = make_graph(KINDS[seed % 4], 2 + seed % 25, seed)
        n = len(adj)
        res = simulate(adj, seed % n, budget=1 + (seed * 7) % 200, seed=seed)
        assert res["announced_at"] is not None  # liveness
        assert res["clean"]  # safety: terminated at the moment of the announcement
        assert res["terminated_at"] <= res["announced_at"]
        assert res["signal"] == res["basic"]  # exactly one signal per basic message
        assert all(d == 0 for d in res["deficits"])
        root = seed % n
        assert [v for v in range(n) if res["engaged"][v]] == [root]


def test_large_fanout_long_computation():
    adj = make_graph("gnp", 30, 4)
    for seed in range(20):
        res = simulate(adj, 0, budget=600, seed=seed, fanout=3)
        assert res["clean"] and res["signal"] == res["basic"]
        assert res["announced_at"] >= res["terminated_at"]


def test_root_alone():
    res = simulate([[]], 0, budget=0, seed=1)
    assert res["basic"] == 0 and res["clean"] and res["announced_at"] is not None
