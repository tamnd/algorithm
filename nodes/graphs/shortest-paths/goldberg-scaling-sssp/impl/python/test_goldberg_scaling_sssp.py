# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/goldberg-scaling-sssp/. The authors are listed in prov/A13K1H.jsonl.

import math
import random

import pytest

from goldberg_scaling_sssp import goldberg_scaling

INF = math.inf
# s=0, a=1, b=2, c=3
EXAMPLE = [(0, 1, -1), (1, 2, -3), (1, 3, 4)]


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
    d, parent = goldberg_scaling(build(4, EXAMPLE), 0, trace)
    assert d == [0, -1, -4, 3]
    assert parent == [None, 0, 1, 1]
    assert trace == [(1, "cut", 1), (2, "path", 2)]


def test_reachable_negative_cycle() -> None:
    adj = build(3, [(0, 1, 1), (1, 2, -2), (2, 1, 1)])
    trace = []
    assert goldberg_scaling(adj, 0, trace) is None
    assert trace == [(1, "cut", 1)]  # found in scale 2, inside an admissible component


def test_unreachable_negative_cycle_is_ignored() -> None:
    adj = build(4, [(0, 1, 1), (2, 3, -5), (3, 2, 1)])
    d, parent = goldberg_scaling(adj, 0)
    assert d == [0, 1, INF, INF] and parent == [None, 0, None, None]


def test_negative_self_loop() -> None:
    assert goldberg_scaling(build(2, [(0, 1, 2), (1, 1, -1)]), 0) is None


def test_zero_weight_cycle() -> None:
    adj = build(3, [(0, 1, -2), (1, 2, 3), (2, 1, -3)])
    d, _ = goldberg_scaling(adj, 0)
    assert d == [0, -2, 1]


def test_nonnegative_weights_need_no_scale() -> None:
    trace = []
    d, _ = goldberg_scaling(build(3, [(0, 1, 5), (1, 2, 0), (0, 2, 7)]), 0, trace)
    assert d == [0, 5, 5] and trace == []


def test_non_integer_weight_is_rejected() -> None:
    with pytest.raises(ValueError):
        goldberg_scaling(build(2, [(0, 1, -0.5)]), 0)


def test_long_negative_path_uses_path_steps() -> None:
    # a path of -1 edges: every layer has one improvable vertex, so the path case runs
    n = 30
    adj = build(n, [(i, i + 1, -1) for i in range(n - 1)])
    trace = []
    d, _ = goldberg_scaling(adj, 0, trace)
    assert d == [-i for i in range(n)]
    assert [kind for _, kind, _ in trace] == ["path"]


def test_random_against_bellman_ford() -> None:
    rng = random.Random(1995)
    negative = 0
    for _ in range(1500):
        n = rng.randint(1, 9)
        low = rng.choice([1, 4, 40, 1000])
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(-low, 3 * low))
                 for _ in range(rng.randint(0, 3 * n))]
        adj = build(n, edges)
        s = rng.randrange(n)
        want = bellman_ford(adj, s)
        got = goldberg_scaling(adj, s)
        if want is None:
            negative += 1
            assert got is None
        else:
            assert got is not None and got[0] == want
            check_tree(adj, s, got[0], got[1])
    assert negative > 100
