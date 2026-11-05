# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gabow-scaling-sssp/. The authors are listed in prov/N36TQW.jsonl.

import math
import random

import pytest

from gabow_scaling_sssp import gabow_scaling

INF = math.inf
# s=0, a=1, b=2, c=3
EXAMPLE = [(0, 1, 5), (0, 2, 3), (2, 1, 1), (1, 3, 2), (2, 3, 7)]


def build(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    return adj


def bellman_ford(adj, s):
    """Independent oracle: distances from s, or None if a negative cycle is reachable."""
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
            assert parent[v] is None
            continue
        u = parent[v]
        assert d[v] == d[u] + min(w for x, w in adj[u] if x == v)


def test_example() -> None:
    trace = []
    adj = build(4, EXAMPLE)
    d, parent = gabow_scaling(adj, 0, trace)
    assert d == [0, 4, 3, 6]
    assert parent == [None, 2, 0, 1]
    assert trace == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 2], [0, 4, 3, 6]]


def test_unreachable_vertices_stay_infinite() -> None:
    adj = build(4, [(0, 1, 3), (2, 3, 1), (3, 0, 1)])
    d, parent = gabow_scaling(adj, 0)
    assert d == [0, 3, INF, INF] and parent == [None, 0, None, None]


def test_all_zero_weights() -> None:
    adj = build(3, [(0, 1, 0), (1, 2, 0), (2, 0, 0)])
    d, parent = gabow_scaling(adj, 0)
    assert d == [0, 0, 0] and parent == [None, 0, 1]


def test_single_vertex() -> None:
    assert gabow_scaling([[]], 0) == ([0], [None])


def test_negative_weight_is_rejected() -> None:
    with pytest.raises(ValueError):
        gabow_scaling(build(2, [(0, 1, -1)]), 0)


def test_negative_cycle_is_rejected() -> None:
    # every negative cycle has a negative edge, so it is rejected up front
    adj = build(3, [(0, 1, 2), (1, 2, -3), (2, 1, 1)])
    with pytest.raises(ValueError):
        gabow_scaling(adj, 0)


def test_non_integer_weight_is_rejected() -> None:
    with pytest.raises(ValueError):
        gabow_scaling(build(2, [(0, 1, 1.5)]), 0)


def test_large_weights() -> None:
    adj = build(3, [(0, 1, 10**12), (1, 2, 10**12 + 7), (0, 2, 3 * 10**12)])
    d, _ = gabow_scaling(adj, 0)
    assert d == [0, 10**12, 2 * 10**12 + 7]


def test_each_scale_is_the_scaled_distance() -> None:
    rng = random.Random(7)
    adj = build(6, [(rng.randrange(6), rng.randrange(6), rng.randint(0, 50)) for _ in range(15)])
    trace = []
    d, _ = gabow_scaling(adj, 0, trace)
    b = max([w for row in adj for _, w in row] + [0]).bit_length()
    for i, labels in enumerate(trace):
        scaled = [[(v, w >> (b - i)) for v, w in row] for row in adj]
        assert labels == bellman_ford(scaled, 0)


def test_random_against_bellman_ford() -> None:
    rng = random.Random(1985)
    for _ in range(800):
        n = rng.randint(1, 9)
        top = rng.choice([1, 3, 20, 1000, 10**6])
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, top))
                 for _ in range(rng.randint(0, 3 * n))]
        adj = build(n, edges)
        s = rng.randrange(n)
        d, parent = gabow_scaling(adj, s)
        assert d == bellman_ford(adj, s)
        check_tree(adj, s, d, parent)
