# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/convergecast/. The authors are listed in prov/T9HDCH.jsonl.

import operator
import random

from convergecast import convergecast_async, convergecast_sync, pif_sync, tree_height

OPS = [(operator.add, sum), (max, max), (min, min)]


def bfs_parent(adj, r):
    parent = [-1] * len(adj)
    parent[r] = r
    frontier = [r]
    while frontier:
        nxt = []
        for v in frontier:
            for w in adj[v]:
                if parent[w] < 0:
                    parent[w] = v
                    nxt.append(w)
        frontier = nxt
    return parent


def random_rooted_tree(kind, n, seed):
    """Seeded rooted spanning trees: random recursive tree, path, BFS tree of a grid or of G(n, p)."""
    rng = random.Random(seed)
    if kind == "tree":
        order = list(range(n))
        rng.shuffle(order)
        parent = [0] * n
        parent[order[0]] = order[0]
        for i in range(1, n):
            parent[order[i]] = order[rng.randrange(i)]
        return parent
    if kind == "path":
        return [max(0, v - 1) for v in range(n)]
    adj = [[] for _ in range(n)]
    if kind == "grid":
        b = max(1, int(n**0.5))
        for v in range(n):
            if (v + 1) % b and v + 1 < n:
                adj[v].append(v + 1)
                adj[v + 1].append(v)
            if v + b < n:
                adj[v].append(v + b)
                adj[v + b].append(v)
    else:
        p = rng.uniform(0.1, 0.5)
        for v in range(1, n):
            u = rng.randrange(v)
            adj[u].append(v)
            adj[v].append(u)
        for u in range(n):
            for v in range(u + 2, n):
                if rng.random() < p:
                    adj[u].append(v)
                    adj[v].append(u)
    return bfs_parent(adj, rng.randrange(n))


def test_small_example():
    # Root 0 with children 1 and 2; node 3 is a child of 1.
    parent = [0, 0, 0, 1]
    x = [5, 3, 9, 4]
    res = convergecast_sync(parent, x, operator.add)
    assert res == {"result": 21, "messages": 3, "rounds": 2}
    assert convergecast_sync(parent, x, max)["result"] == 9


def test_single_node():
    assert convergecast_sync([0], [7], operator.add) == {"result": 7, "messages": 0, "rounds": 0}
    assert pif_sync([0], [7], operator.add)["result"] == 7


def test_sync_matches_direct_value_messages_and_height():
    for seed in range(200):
        kind = ["tree", "path", "grid", "gnp"][seed % 4]
        n = 1 + seed % 40
        parent = random_rooted_tree(kind, n, seed)
        rng = random.Random(seed)
        x = [rng.randrange(-1000, 1000) for _ in range(n)]
        h = tree_height(parent)
        for op, direct in OPS:
            res = convergecast_sync(parent, x, op)
            assert res["result"] == direct(x)
            assert res["messages"] == n - 1
            assert res["rounds"] == h


def test_async_matches_direct_value_and_time():
    for seed in range(150):
        kind = ["tree", "path", "grid", "gnp"][seed % 4]
        n = 1 + seed % 40
        parent = random_rooted_tree(kind, n, seed + 77)
        rng = random.Random(seed)
        x = [rng.randrange(0, 10**6) for _ in range(n)]
        h = tree_height(parent)
        for op, direct in OPS:
            res = convergecast_async(parent, x, op, seed)
            assert res["result"] == direct(x)
            assert res["messages"] == n - 1
            assert res["time"] <= h + 1e-9


def test_broadcast_then_convergecast():
    for seed in range(100):
        kind = ["tree", "path", "grid", "gnp"][seed % 4]
        n = 2 + seed % 40
        parent = random_rooted_tree(kind, n, seed + 5)
        x = list(range(n))
        res = pif_sync(parent, x, operator.add)
        assert res["result"] == n * (n - 1) // 2
        assert res["messages"] == 2 * (n - 1)
        assert res["rounds"] == 2 * tree_height(parent)
