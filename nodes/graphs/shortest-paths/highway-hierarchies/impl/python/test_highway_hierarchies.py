# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/highway-hierarchies/. The authors are listed in prov/B70115.jsonl.

import math
import random

import pytest

from highway_hierarchies import hh_preprocess, hh_query

INF = math.inf
# main road m0..m6 = 0..6 with 2 km segments, driveway leaves l0..l6 = 7..13 of 1 km
EXAMPLE_EDGES = [(i, i + 1, 2) for i in range(6)] + [(i, 7 + i, 1) for i in range(7)]


def undirected(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj


def bellman_ford(adj, s):
    """Independent oracle: n - 1 rounds of relaxing every edge."""
    n = len(adj)
    d = [INF] * n
    d[s] = 0
    for _ in range(n - 1):
        for u in range(n):
            for v, w in adj[u]:
                if d[u] + w < d[v]:
                    d[v] = d[u] + w
    return d


def path_weight(adj, p):
    return sum(min(w for v, w in adj[a] if v == b) for a, b in zip(p, p[1:]))


def highway_pairs(adj, hw):
    return sorted({(u, adj[u][i][0]) for u, i in hw.highway})


def test_example_highway_edges() -> None:
    adj = undirected(14, EXAMPLE_EDGES)
    hw = hh_preprocess(adj, 3)
    assert hw.rfwd == [2] * 7 + [3] * 7
    assert highway_pairs(adj, hw) == sorted(
        [(1, 2), (2, 1), (2, 3), (3, 2), (3, 4), (4, 3), (4, 5), (5, 4)]
    )


def test_example_query() -> None:
    adj = undirected(14, EXAMPLE_EDGES)
    d, p, scans = hh_query(adj, hh_preprocess(adj, 3), 7, 13)
    assert (d, p) == (14, [7, 0, 1, 2, 3, 4, 5, 6, 13])
    # with neighborhoods covering everything, the query is plain bidirectional Dijkstra
    assert scans == 16 and hh_query(adj, hh_preprocess(adj, 14), 7, 13)[2] == 26


def test_source_equals_target() -> None:
    adj = undirected(14, EXAMPLE_EDGES)
    assert hh_query(adj, hh_preprocess(adj, 2), 4, 4) == (0, [4], 0)


def test_unreachable() -> None:
    # 0 -> 1 -> 2 and 3 -> 0; nothing reaches 3, and 2 reaches nothing
    adj = [[(1, 1)], [(2, 1)], [], [(0, 1)]]
    for h in (1, 2, 3, 4):
        hw = hh_preprocess(adj, h)
        assert hh_query(adj, hw, 0, 3)[:2] == (INF, None)
        assert hh_query(adj, hw, 2, 0)[:2] == (INF, None)
        assert hh_query(adj, hw, 3, 2)[:2] == (3, [3, 0, 1, 2])


def test_negative_weight_rejected() -> None:
    with pytest.raises(ValueError):
        hh_preprocess([[(1, -1)], []], 2)


def test_negative_cycle_rejected() -> None:
    with pytest.raises(ValueError):
        hh_preprocess([[(1, 2)], [(0, -3)]], 2)


def test_random_against_bellman_ford() -> None:
    rng = random.Random(2005)
    for _ in range(600):
        n = rng.randint(1, 8)
        adj = [[] for _ in range(n)]
        for _ in range(rng.randint(0, 3 * n)):
            adj[rng.randrange(n)].append((rng.randrange(n), rng.randint(0, 9)))
        hw = hh_preprocess(adj, rng.randint(1, 4))
        for s in range(n):
            ref = bellman_ford(adj, s)
            for t in range(n):
                d, p, _ = hh_query(adj, hw, s, t)
                assert d == ref[t]
                if d == INF:
                    assert p is None
                else:
                    assert p[0] == s and p[-1] == t and path_weight(adj, p) == d
