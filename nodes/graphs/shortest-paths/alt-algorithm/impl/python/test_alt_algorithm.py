# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alt-algorithm/. The authors are listed in prov/DBXZ34.jsonl.

import math
import random

import pytest

from alt_algorithm import alt_preprocess, alt_query

INF = math.inf
# s=0, a=1, b=2, t=3, x=4, y=5, z=6, l=7; every edge goes both ways
EXAMPLE_EDGES = [(0, 1, 2), (1, 2, 2), (2, 3, 2), (0, 4, 1), (4, 5, 1), (5, 6, 1), (3, 7, 1)]


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


def test_example_with_landmark() -> None:
    adj = undirected(8, EXAMPLE_EDGES)
    assert alt_query(adj, alt_preprocess(adj, [7]), 0, 3) == (6, [0, 1, 2, 3], 4)


def test_example_without_landmarks_is_dijkstra() -> None:
    adj = undirected(8, EXAMPLE_EDGES)
    assert alt_query(adj, alt_preprocess(adj, []), 0, 3) == (6, [0, 1, 2, 3], 7)


def test_source_equals_target() -> None:
    adj = undirected(8, EXAMPLE_EDGES)
    assert alt_query(adj, alt_preprocess(adj, [6]), 5, 5) == (0, [5], 1)


def test_unreachable_target() -> None:
    # 0 -> 1 -> 2, and 3 -> 0; vertex 3 is unreachable from 0
    adj = [[(1, 1)], [(2, 1)], [], [(0, 1)]]
    for lms in ([], [0], [2], [3], [1, 3]):
        tables = alt_preprocess(adj, lms)
        assert alt_query(adj, tables, 0, 3)[:2] == (INF, None)
        assert alt_query(adj, tables, 2, 0)[:2] == (INF, None)
        assert alt_query(adj, tables, 3, 2)[:2] == (3, [3, 0, 1, 2])


def test_landmark_proves_unreachability_without_search() -> None:
    # t=2 reaches the landmark 3, s=0 does not, so the bound at s is infinite
    adj = [[(1, 1)], [], [(3, 1)], []]
    assert alt_query(adj, alt_preprocess(adj, [3]), 0, 2) == (INF, None, 0)


def test_negative_weight_rejected() -> None:
    with pytest.raises(ValueError):
        alt_preprocess([[(1, -1)], []], [0])


def test_negative_cycle_rejected() -> None:
    with pytest.raises(ValueError):
        alt_preprocess([[(1, 1)], [(0, -2)]], [])


def test_zero_weights_and_parallel_edges() -> None:
    adj = [[(1, 0), (1, 5), (2, 4)], [(2, 0)], [(0, 0)]]
    d, p, _ = alt_query(adj, alt_preprocess(adj, [1, 2]), 0, 2)
    assert d == 0 and p == [0, 1, 2]


def test_random_against_bellman_ford() -> None:
    rng = random.Random(2005)
    for _ in range(600):
        n = rng.randint(1, 9)
        adj = [[] for _ in range(n)]
        for _ in range(rng.randint(0, 3 * n)):
            adj[rng.randrange(n)].append((rng.randrange(n), rng.randint(0, 9)))
        lms = rng.sample(range(n), rng.randint(0, min(3, n)))
        tables = alt_preprocess(adj, lms)
        s = rng.randrange(n)
        ref = bellman_ford(adj, s)
        for t in range(n):
            d, p, scans = alt_query(adj, tables, s, t)
            assert d == ref[t]
            if d == INF:
                assert p is None
            else:
                assert p[0] == s and p[-1] == t and path_weight(adj, p) == d
                # a consistent heuristic never scans a vertex twice
                assert scans <= n
