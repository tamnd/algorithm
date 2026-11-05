# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/contraction-hierarchies/. The authors are listed in prov/K2PFVE.jsonl.

import math
import random

import pytest

from contraction_hierarchies import ch_preprocess, ch_query

INF = math.inf
# a=0, b=1, c=2, d=3, e=4; every edge goes both ways
EXAMPLE_EDGES = [(0, 1, 1), (1, 2, 1), (2, 3, 1), (0, 4, 3), (4, 3, 1)]
EXAMPLE_ORDER = [1, 4, 2, 0, 3]


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


def test_example_shortcuts() -> None:
    ch = ch_preprocess(undirected(5, EXAMPLE_EDGES), EXAMPLE_ORDER)
    # a-c through b, and a-d through c, each in both directions; none for e
    assert ch.shortcuts == 4
    assert ch.mid[(0, 2)] == 1 and ch.mid[(0, 3)] == 2
    assert sorted(ch.up[0]) == [(3, 3)]


def test_example_queries() -> None:
    ch = ch_preprocess(undirected(5, EXAMPLE_EDGES), EXAMPLE_ORDER)
    assert ch_query(ch, 1, 4) == (3, [1, 2, 3, 4])
    assert ch_query(ch, 0, 3) == (3, [0, 1, 2, 3])
    assert ch_query(ch, 2, 2) == (0, [2])


def test_unreachable() -> None:
    # 0 -> 1 -> 2 and 3 -> 0; nothing reaches 3, and 2 reaches nothing
    adj = [[(1, 1)], [(2, 1)], [], [(0, 1)]]
    for order in (None, [0, 1, 2, 3], [3, 2, 1, 0], [1, 3, 0, 2]):
        ch = ch_preprocess(adj, order)
        assert ch_query(ch, 0, 3) == (INF, None)
        assert ch_query(ch, 2, 0) == (INF, None)
        assert ch_query(ch, 3, 2) == (3, [3, 0, 1, 2])


def test_isolated_vertices() -> None:
    ch = ch_preprocess([[], [], []])
    assert ch_query(ch, 0, 2) == (INF, None)


def test_negative_weight_rejected() -> None:
    with pytest.raises(ValueError):
        ch_preprocess([[(1, -1)], []])


def test_negative_cycle_rejected() -> None:
    with pytest.raises(ValueError):
        ch_preprocess([[(1, 2)], [(0, -3)]])


def test_zero_weights_parallel_edges_self_loops() -> None:
    adj = [[(1, 0), (1, 4), (0, 0)], [(2, 0)], [(0, 5)]]
    ch = ch_preprocess(adj, [1, 0, 2])
    assert ch_query(ch, 0, 2) == (0, [0, 1, 2])
    assert ch_query(ch, 2, 1) == (5, [2, 0, 1])


def test_random_against_bellman_ford() -> None:
    rng = random.Random(2008)
    for trial in range(600):
        n = rng.randint(1, 9)
        adj = [[] for _ in range(n)]
        for _ in range(rng.randint(0, 3 * n)):
            adj[rng.randrange(n)].append((rng.randrange(n), rng.randint(0, 9)))
        if trial % 2:
            order = list(range(n))
            rng.shuffle(order)
        else:
            order = None
        ch = ch_preprocess(adj, order)
        assert sorted(ch.rank) == list(range(n))
        for s in range(n):
            ref = bellman_ford(adj, s)
            for t in range(n):
                d, p = ch_query(ch, s, t)
                assert d == ref[t]
                if d == INF:
                    assert p is None
                else:
                    assert p[0] == s and p[-1] == t and path_weight(adj, p) == d
