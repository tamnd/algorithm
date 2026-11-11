# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flooding/. The authors are listed in prov/0WMBJP.jsonl.

import random

from flooding import bfs_dist, edges_to_adj, flood_async, flood_sync, make_graph

KINDS = ["tree", "path", "grid", "gnp"]


def size(adj):
    n = len(adj)
    m = sum(len(a) for a in adj) // 2
    return n, m


def is_spanning_tree(parent, s):
    n = len(parent)
    if parent[s] != s:
        return False
    for v in range(n):
        seen = set()
        x = v
        while x != s:
            if x in seen or parent[x] is None:
                return False
            seen.add(x)
            x = parent[x]
    return True


def test_worked_example():
    # The 6 node graph of the page: edges 0-1, 0-2, 1-2, 1-3, 2-4, 3-4, 4-5.
    adj = edges_to_adj(6, {(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4), (4, 5)})
    res = flood_sync(adj, 0)
    assert res["round"] == [0, 1, 1, 2, 2, 3]
    assert res["per_round"] == [2, 4, 3]
    assert res["messages"] == 9 == 2 * 7 - (6 - 1)
    assert res["parent"] == [0, 0, 0, 1, 2, 4]
    assert res["rounds"] == 3


def test_single_node_and_edge():
    assert flood_sync([[]], 0)["messages"] == 0
    res = flood_sync([[1], [0]], 0)
    assert res["messages"] == 1 and res["round"] == [0, 1]


def test_sync_counts_rounds_and_bfs_parents():
    for seed in range(120):
        kind = KINDS[seed % 4]
        adj = make_graph(kind, 2 + seed % 25, seed)
        n, m = size(adj)
        s = seed % n
        res = flood_sync(adj, s)
        dist = bfs_dist(adj, s)
        assert res["messages"] == 2 * m - (n - 1)
        assert res["round"] == dist
        ecc = max(dist)
        # Activity ends in round ecc, or ecc + 1 when a node at distance ecc
        # has a neighbour other than its parent.
        assert res["rounds"] in (ecc, ecc + 1)
        assert is_spanning_tree(res["parent"], s)
        for v in range(n):
            if v != s:
                assert dist[res["parent"][v]] == dist[v] - 1


def test_async_counts_and_tree():
    for seed in range(150):
        kind = KINDS[seed % 4]
        adj = make_graph(kind, 2 + seed % 25, seed + 1000)
        n, m = size(adj)
        s = (3 * seed) % n
        ecc = max(bfs_dist(adj, s))
        for schedule in ("random", "slow", "lifo"):
            res = flood_async(adj, s, seed, schedule, slow=s)
            assert res["messages"] == 2 * m - (n - 1)
            assert is_spanning_tree(res["parent"], s)
            assert all(t is not None and t <= ecc + 1e-9 for t in res["reached_at"])
            assert res["time"] <= ecc + 1 + 1e-9


def test_async_tree_need_not_be_bfs():
    # A triangle 0-1-2: when the copy from the source to node 2 is slow,
    # node 2 hears the message from node 1 first, so its parent is 1
    # although it is a neighbour of the source.
    adj = edges_to_adj(3, {(0, 1), (0, 2), (1, 2)})
    found = False
    for seed in range(50):
        res = flood_async(adj, 0, seed)
        if res["parent"][2] == 1 or res["parent"][1] == 2:
            found = True
    assert found


def test_count_does_not_depend_on_schedule():
    rng = random.Random(7)
    for _ in range(40):
        adj = make_graph("gnp", rng.randrange(2, 30), rng.randrange(10**6))
        n, m = size(adj)
        counts = {flood_async(adj, 0, seed)["messages"] for seed in range(5)}
        assert counts == {2 * m - n + 1}
