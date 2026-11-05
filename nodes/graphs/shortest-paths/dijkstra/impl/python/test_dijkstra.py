# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dijkstra/. The authors are listed in prov/27XR9T.jsonl.

import math
import random

import pytest

from dijkstra import dijkstra

NAMES = "sabcdt"
EDGES = [("s", "a", 7), ("s", "b", 2), ("b", "a", 3), ("b", "c", 8), ("a", "c", 1),
         ("a", "d", 6), ("c", "d", 2), ("c", "t", 9), ("d", "t", 3)]


def build(n: int, edges: list[tuple[int, int, float]]) -> list[list[tuple[int, float]]]:
    adj: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    return adj


def oracle(n: int, edges: list[tuple[int, int, float]], s: int) -> list[float]:
    """Independent check: n - 1 rounds of relaxing every edge (Bellman-Ford)."""
    d = [math.inf] * n
    d[s] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    return d


def check_tree(adj, s, d, parent) -> None:
    for v in range(len(adj)):
        if v == s:
            assert parent[v] is None and d[v] == 0
        elif d[v] == math.inf:
            assert parent[v] is None
        else:
            u = parent[v]
            assert u is not None
            assert any(x == v and d[u] + w == d[v] for x, w in adj[u])


def test_example() -> None:
    ix = {c: i for i, c in enumerate(NAMES)}
    adj = build(6, [(ix[u], ix[v], w) for u, v, w in EDGES])
    d, parent = dijkstra(adj, 0)
    assert d == [0, 5, 2, 6, 8, 11]
    assert parent == [None, 2, 0, 1, 3, 4]


def test_single_vertex_and_self_loop() -> None:
    assert dijkstra([[]], 0) == ([0], [None])
    assert dijkstra([[(0, 5)]], 0) == ([0], [None])


def test_unreachable() -> None:
    adj = build(4, [(0, 1, 3), (2, 3, 1), (3, 1, 0)])
    d, parent = dijkstra(adj, 0)
    assert d == [0, 3, math.inf, math.inf]
    assert parent == [None, 0, None, None]


def test_zero_weights_and_parallel_edges() -> None:
    adj = build(3, [(0, 1, 0), (0, 1, 4), (1, 2, 0), (0, 2, 1)])
    d, _ = dijkstra(adj, 0)
    assert d == [0, 0, 0]


def test_negative_edge_rejected() -> None:
    # The page's counterexample: without the check the answer for c would be 3, not 2.
    adj = build(4, [(0, 1, 2), (1, 3, 1), (0, 2, 4), (2, 1, -3)])
    with pytest.raises(ValueError):
        dijkstra(adj, 0)


def test_negative_cycle_rejected() -> None:
    adj = build(3, [(0, 1, 1), (1, 2, 2), (2, 1, -3)])
    with pytest.raises(ValueError):
        dijkstra(adj, 0)


def test_large_weights_exact() -> None:
    big = 2**62
    adj = build(3, [(0, 1, big), (1, 2, big), (0, 2, 2**63 + 1)])
    d, _ = dijkstra(adj, 0)
    assert d[2] == 2**63


def test_random_against_bellman_ford() -> None:
    rng = random.Random(1959)
    for _ in range(600):
        n = rng.randint(1, 8)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 9))
                 for _ in range(rng.randint(0, 3 * n))]
        adj = build(n, edges)
        s = rng.randrange(n)
        d, parent = dijkstra(adj, s)
        assert d == oracle(n, edges, s)
        check_tree(adj, s, d, parent)
