# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/breadth-first-search-distributed/. The authors are listed in prov/2CY7S7.jsonl.

import random

from breadth_first_search_distributed import bfs_bellman, bfs_layered, bfs_sync

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


def is_bfs_tree(adj, r, dist_out, parent):
    """The output distances are the true distances and each parent is one layer up."""
    dist = bfs_dist(adj, r)
    if list(dist_out) != dist or parent[r] != r:
        return False
    return all(parent[v] in adj[v] and dist[parent[v]] == dist[v] - 1 for v in range(len(adj)) if v != r)


def cases(count, offset):
    for seed in range(count):
        adj = make_graph(KINDS[seed % 4], 1 + seed % 30, seed + offset)
        n = len(adj)
        m = sum(len(a) for a in adj) // 2
        yield seed, adj, n, m, (5 * seed) % n


def test_worked_example():
    adj = edges_to_adj(6, {(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4), (4, 5)})
    res = bfs_sync(adj, 0)
    assert res["dist"] == [0, 1, 1, 2, 2, 3]
    assert res["parent"] == [0, 0, 0, 1, 2, 4]
    assert res["messages"] == 9


def test_sync_bfs_tree_messages_rounds():
    for _, adj, n, m, r in cases(150, 0):
        res = bfs_sync(adj, r)
        e = max(bfs_dist(adj, r))
        assert is_bfs_tree(adj, r, res["dist"], res["parent"])
        assert res["messages"] == 2 * m - (n - 1)
        assert res["rounds"] in (e, e + 1)


def test_bellman_ford_bfs_is_bfs_with_bounded_messages():
    worst_ratio = 0.0
    for seed, adj, n, m, r in cases(150, 3000):
        dist = bfs_dist(adj, r)
        e = max(dist)
        bound = len(adj[r]) + sum((n - dist[v]) * (len(adj[v]) - 1) for v in range(n) if v != r)
        for schedule in ("random", "skewed"):
            res = bfs_bellman(adj, r, seed, schedule)
            assert is_bfs_tree(adj, r, res["dist"], res["parent"])
            assert all(res["updates"][v] <= n - dist[v] for v in range(n) if v != r)
            assert 2 * m - (n - 1) <= res["messages"] <= bound
            assert res["time"] <= e + 1 + 1e-9
            if m:
                worst_ratio = max(worst_ratio, res["messages"] / m)
    # The skewed schedule makes some nodes change their distance many times.
    assert worst_ratio > 2.5


def test_bellman_ford_many_updates_on_a_ladder():
    # Root 0; a long path 0-1-...-(n-1) with fast edges and direct edges from 0
    # with slow delays: nodes first learn long distances, then correct them.
    n = 12
    edges = {(v - 1, v) for v in range(1, n)} | {(0, v) for v in range(2, n)}
    adj = edges_to_adj(n, edges)
    res = bfs_bellman(adj, 0, 1, "skewed")
    assert res["dist"] == [0] + [1] * (n - 1)
    assert sum(res["updates"]) > n - 1


def test_layered_bfs_tree_exact_messages_and_time():
    for seed, adj, n, m, r in cases(150, 7000):
        dist = bfs_dist(adj, r)
        e = max(dist)
        sizes = [sum(1 for d in dist if d <= k) for k in range(e + 1)]
        expected = 2 * (2 * m - (n - 1)) + 2 * sum(sizes[k - 1] - 1 for k in range(1, e + 2))
        for schedule in ("random", "skewed"):
            res = bfs_layered(adj, r, seed, schedule)
            assert is_bfs_tree(adj, r, res["dist"], res["parent"])
            assert res["phases"] == e + 1
            assert res["messages"] == expected
            assert res["by_kind"].get("EXPLORE", 0) == 2 * m - (n - 1)
            assert res["messages"] <= 2 * (2 * m) + 2 * (e + 1) * (n - 1)
            assert res["time"] <= (e + 1) * (e + 2) + 1e-9
