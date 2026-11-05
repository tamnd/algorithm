# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/goldberg-radzik/. The authors are listed in prov/FBHX78.jsonl.

import math
import random

from goldberg_radzik import goldberg_radzik

INF = math.inf
# s=0, a=1, b=2, c=3, d=4
EXAMPLE = [(0, 1, 2), (0, 2, 6), (0, 3, 7), (1, 2, 3), (1, 4, 8), (2, 4, 1), (3, 1, -6)]


def build(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    return adj


def bellman_ford(adj, s):
    """Independent oracle: distances, or None if a negative cycle is reachable."""
    n = len(adj)
    d = [INF] * n
    d[s] = 0
    for _ in range(n - 1):
        for u in range(n):
            for v, w in adj[u]:
                if d[u] + w < d[v]:
                    d[v] = d[u] + w
    for u in range(n):
        for v, w in adj[u]:
            if d[u] + w < d[v]:
                return None
    return d


def check_tree(adj, s, d, parent):
    for v in range(len(adj)):
        if v == s or d[v] == INF:
            assert v == s or parent[v] is None
            continue
        u = parent[v]
        assert d[v] == d[u] + min(w for x, w in adj[u] if x == v)


def test_example() -> None:
    trace = []
    d, parent = goldberg_radzik(build(5, EXAMPLE), 0, trace)
    assert d == [0, 1, 4, 7, 5]
    assert parent == [None, 3, 1, 0, 2]
    assert trace == [[0, 3, 2, 1], [2, 4]]


def test_unreachable_vertices_stay_infinite() -> None:
    adj = build(4, [(0, 1, -2), (2, 3, 1), (3, 0, 1)])
    d, parent = goldberg_radzik(adj, 0)
    assert d == [0, -2, INF, INF] and parent[2] is None and parent[3] is None


def test_negative_cycle_reported() -> None:
    assert goldberg_radzik(build(3, [(0, 1, 1), (1, 2, -2), (2, 1, 1)]), 0) is None


def test_negative_self_loop_reported() -> None:
    assert goldberg_radzik(build(1, [(0, 0, -1)]), 0) is None
    assert goldberg_radzik(build(2, [(0, 1, 3), (1, 1, -1)]), 0) is None


def test_unreachable_negative_cycle_ignored() -> None:
    adj = build(4, [(0, 1, 5), (2, 3, -4), (3, 2, 1)])
    assert goldberg_radzik(adj, 0)[0] == [0, 5, INF, INF]


def test_zero_cycle_is_not_negative() -> None:
    adj = build(4, [(0, 1, 1), (1, 2, -3), (2, 1, 3), (2, 3, 2)])
    assert goldberg_radzik(adj, 0)[0] == [0, 1, -2, 0]


def test_isolated_source() -> None:
    assert goldberg_radzik(build(3, []), 1) == ([INF, 0, INF], [None, None, None])


def test_dag() -> None:
    adj = build(5, [(0, 1, 4), (0, 2, 1), (2, 1, -2), (1, 3, 1), (2, 3, 5), (3, 4, -1)])
    assert goldberg_radzik(adj, 0)[0] == [0, -1, 1, 0, -1]


def test_random_against_bellman_ford() -> None:
    rng = random.Random(1993)
    for _ in range(1500):
        n = rng.randint(1, 8)
        edges = [
            (rng.randrange(n), rng.randrange(n), rng.randint(-4, 9))
            for _ in range(rng.randint(0, 3 * n))
        ]
        adj = build(n, edges)
        s = rng.randrange(n)
        ref = bellman_ford(adj, s)
        trace = []
        got = goldberg_radzik(adj, s, trace)
        if ref is None:
            assert got is None
        else:
            assert got is not None and got[0] == ref
            check_tree(adj, s, *got)
            assert len(trace) <= n
