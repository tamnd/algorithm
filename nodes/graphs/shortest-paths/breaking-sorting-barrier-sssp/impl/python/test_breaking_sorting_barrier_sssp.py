# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/breaking-sorting-barrier-sssp/. The authors are listed in prov/WVPFW7.jsonl.

import heapq
import math
import random

import pytest

from breaking_sorting_barrier_sssp import bmssp_sssp

INF = math.inf
# s=0, a=1, b=2, c=3, d=4, e=5
EXAMPLE = [(0, 1, 1), (0, 2, 4), (1, 2, 2), (1, 3, 6), (2, 3, 1), (2, 4, 5), (3, 4, 1), (3, 5, 3), (4, 5, 1)]


def build(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    return adj


def dijkstra(adj, s):
    """Independent oracle: plain binary-heap Dijkstra."""
    d = [INF] * len(adj)
    d[s] = 0
    heap = [(0, s)]
    while heap:
        du, u = heapq.heappop(heap)
        if du > d[u]:
            continue
        for v, w in adj[u]:
            if du + w < d[v]:
                d[v] = du + w
                heapq.heappush(heap, (d[v], v))
    return d


def check_tree(adj, s, d, parent):
    for v in range(len(adj)):
        if v == s or d[v] == INF:
            assert parent[v] is None
            continue
        p = parent[v]
        assert p is not None
        assert any(x == v and d[p] + w == d[v] for x, w in adj[p])
    # parent pointers lead back to s without cycles
    for v in range(len(adj)):
        seen = set()
        while v is not None and d[v] < INF:
            assert v not in seen
            seen.add(v)
            v = parent[v]


def test_example():
    adj = build(6, EXAMPLE)
    d, parent = bmssp_sssp(adj, 0)
    assert d == [0, 1, 3, 4, 5, 6]
    assert parent == [None, 0, 1, 2, 3, 4]


def test_example_trace():
    adj = build(6, EXAMPLE)
    trace = []
    d, _ = bmssp_sssp(adj, 0, k=2, t=1, trace=trace)
    assert d == [0, 1, 3, 4, 5, 6]
    assert trace == [
        (0, INF, [0], None, 3, [0, 1]),
        (0, INF, [2], None, 5, [2, 3]),
        (1, INF, [0], [0], 5, [0, 1, 2, 3]),
        (0, INF, [4], None, INF, [4, 5]),
        (1, INF, [4], [4], INF, [4, 5]),
        (2, INF, [0], [0], INF, [0, 1, 2, 3, 4, 5]),
        (3, INF, [0], [0], INF, [0, 1, 2, 3, 4, 5]),
    ]


def test_unreachable():
    adj = build(5, [(0, 1, 2), (3, 4, 1), (4, 0, 1)])
    d, parent = bmssp_sssp(adj, 0)
    assert d == [0, 2, INF, INF, INF]
    assert parent == [None, 0, None, None, None]


def test_negative_weight_rejected():
    with pytest.raises(ValueError):
        bmssp_sssp(build(3, [(0, 1, 1), (1, 2, -1)]), 0)


def test_negative_cycle_rejected():
    with pytest.raises(ValueError):
        bmssp_sssp(build(3, [(0, 1, 1), (1, 2, -3), (2, 1, 1)]), 0)


def test_nan_rejected():
    with pytest.raises(ValueError):
        bmssp_sssp(build(2, [(0, 1, math.nan)]), 0)


def test_zero_cycle_self_loop_parallel():
    adj = build(4, [(0, 1, 0), (1, 0, 0), (1, 1, 0), (1, 2, 5), (1, 2, 2), (2, 3, 0), (3, 2, 0)])
    d, parent = bmssp_sssp(adj, 0)
    assert d == [0, 0, 2, 2]
    check_tree(adj, 0, d, parent)


def test_single_vertex():
    assert bmssp_sssp([[]], 0) == ([0], [None])


def test_random_against_dijkstra():
    rng = random.Random(2025)
    for _ in range(1500):
        n = rng.randint(1, 60)
        adj = [[] for _ in range(n)]
        for _ in range(rng.randint(0, 4 * n)):
            w = rng.choice([0, 1, 2, 3, rng.randint(0, 50), rng.random() * 10])
            adj[rng.randrange(n)].append((rng.randrange(n), w))
        s = rng.randrange(n)
        k = rng.choice([None, 1, 2, 3])
        t = rng.choice([None, 1, 2, 3])
        d, parent = bmssp_sssp(adj, s, k, t)
        assert d == dijkstra(adj, s)
        check_tree(adj, s, d, parent)


def test_larger_default_parameters():
    rng = random.Random(17)
    for _ in range(10):
        n = rng.randint(200, 600)
        adj = [[] for _ in range(n)]
        for _ in range(3 * n):
            adj[rng.randrange(n)].append((rng.randrange(n), rng.randint(0, 100)))
        d, parent = bmssp_sssp(adj, 0)
        assert d == dijkstra(adj, 0)
        check_tree(adj, 0, d, parent)
