# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/echo-algorithm/. The authors are listed in prov/F5917B.jsonl.

import random

from echo_algorithm import echo_async, echo_sync

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
    p = rng.uniform(0.05, 0.5)
    edges = set(tree)
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < p:
                edges.add((u, v))
    return edges_to_adj(n, edges)


def bfs_dist(adj, s):
    dist = [-1] * len(adj)
    dist[s] = 0
    frontier = [s]
    while frontier:
        nxt = []
        for v in frontier:
            for w in adj[v]:
                if dist[w] < 0:
                    dist[w] = dist[v] + 1
                    nxt.append(w)
        frontier = nxt
    return dist


def tree_height(parent, s):
    """Height of the parent tree, or -1 if it is not a spanning tree rooted at s."""
    n = len(parent)
    best = 0
    for v in range(n):
        x, depth = v, 0
        while x != s:
            x = parent[x]
            depth += 1
            if x is None or depth > n:
                return -1
        best = max(best, depth)
    return best


def size(adj):
    return len(adj), sum(len(a) for a in adj) // 2


def test_worked_example():
    adj = edges_to_adj(6, {(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4), (4, 5)})
    res = echo_sync(adj, 0)
    assert res["messages"] == 14 == 2 * 7
    assert res["parent"] == [None, 0, 0, 1, 2, 4]
    assert res["decide_round"] == 6
    assert res["clean"]


def test_small_cases():
    assert echo_sync([[]], 0)["messages"] == 0
    res = echo_sync([[1], [0]], 0)
    assert res["messages"] == 2 and res["decide_round"] == 2 and res["clean"]


def test_sync_exact_count_tree_and_rounds():
    for seed in range(120):
        adj = make_graph(KINDS[seed % 4], 2 + seed % 25, seed)
        n, m = size(adj)
        s = seed % n
        res = echo_sync(adj, s)
        dist = bfs_dist(adj, s)
        e = max(dist)
        assert res["messages"] == 2 * m
        assert res["clean"]
        parent = list(res["parent"])
        parent[s] = s
        assert tree_height(parent, s) == e
        for v in range(n):
            if v != s:
                assert dist[parent[v]] == dist[v] - 1
        assert 2 * e <= res["decide_round"] <= 2 * e + 1


def test_path_from_endpoint_takes_2e_rounds():
    for n in range(2, 12):
        adj = edges_to_adj(n, {(v - 1, v) for v in range(1, n)})
        assert echo_sync(adj, 0)["decide_round"] == 2 * (n - 1)


def test_async_exact_count_clean_decision_and_time():
    for seed in range(150):
        adj = make_graph(KINDS[seed % 4], 2 + seed % 25, seed + 500)
        n, m = size(adj)
        s = (7 * seed) % n
        e = max(bfs_dist(adj, s))
        for schedule in ("random", "chain"):
            res = echo_async(adj, s, seed, schedule)
            assert res["messages"] == 2 * m
            assert res["clean"]
            parent = list(res["parent"])
            parent[s] = s
            h = tree_height(parent, s)
            assert h >= e
            assert res["decide_time"] <= e + 1 + h + 1e-9


def test_async_tree_can_be_deep():
    # Complete graph, D = 1: the initiator's first copy is fast and all its
    # other copies are slow, so the tokens race along other edges first and
    # the tree is much deeper than D.
    n = 12
    adj = edges_to_adj(n, {(u, v) for u in range(n) for v in range(u + 1, n)})
    heights = []
    for seed in range(20):
        res = echo_async(adj, 0, seed, "chain")
        parent = list(res["parent"])
        parent[0] = 0
        heights.append(tree_height(parent, 0))
        assert res["messages"] == n * (n - 1)
    assert min(heights) >= 2 and max(heights) >= 4
