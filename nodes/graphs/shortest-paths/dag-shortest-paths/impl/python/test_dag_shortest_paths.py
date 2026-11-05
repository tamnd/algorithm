# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dag-shortest-paths/. The authors are listed in prov/277N5Y.jsonl.

import math
import random

import pytest

from dag_shortest_paths import dag_shortest_paths

NAMES = "qsabcde"
EDGES = [("q", "s", 3), ("q", "c", -9), ("s", "a", 5), ("s", "b", 3), ("b", "a", 1),
         ("a", "c", 6), ("b", "c", 7), ("b", "d", 4), ("c", "d", -1), ("c", "e", 1),
         ("d", "e", -2), ("a", "d", 2)]


def build(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    return adj


def oracle(n, edges, s):
    """Independent check: n - 1 rounds of relaxing every edge (Bellman-Ford)."""
    d = [math.inf] * n
    d[s] = 0
    for _ in range(max(n - 1, 0)):
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    return d


def test_example() -> None:
    ix = {c: i for i, c in enumerate(NAMES)}
    adj = build(7, [(ix[u], ix[v], w) for u, v, w in EDGES])
    d, parent = dag_shortest_paths(adj, ix["s"])
    assert d == [math.inf, 0, 4, 3, 10, 6, 4]
    assert parent == [None, None, 3, 1, 3, 2, 5]


def test_longest_path_by_negation() -> None:
    ix = {c: i for i, c in enumerate(NAMES)}
    adj = build(7, [(ix[u], ix[v], -w) for u, v, w in EDGES])
    d, _ = dag_shortest_paths(adj, ix["s"])
    assert [-x for x in d[1:]] == [0, 5, 3, 11, 10, 12]


def test_unreachable_with_negative_edge_out() -> None:
    adj = build(3, [(1, 2, -5)])
    assert dag_shortest_paths(adj, 0) == ([0, math.inf, math.inf], [None, None, None])


def test_cycle_rejected() -> None:
    with pytest.raises(ValueError):
        dag_shortest_paths(build(2, [(0, 1, 1), (1, 0, -3)]), 0)  # a negative cycle
    with pytest.raises(ValueError):
        dag_shortest_paths(build(1, [(0, 0, 0)]), 0)  # a self-loop is a cycle


def test_single_vertex() -> None:
    assert dag_shortest_paths([[]], 0) == ([0], [None])


def test_random_dags_against_bellman_ford() -> None:
    rng = random.Random(277)
    for _ in range(700):
        n = rng.randint(1, 9)
        perm = list(range(n))
        rng.shuffle(perm)
        edges = []
        for _ in range(rng.randint(0, 3 * n)):
            i, j = sorted(rng.sample(range(n), 2)) if n > 1 else (0, 0)
            if i < j:
                edges.append((perm[i], perm[j], rng.randint(-9, 9)))
        adj = build(n, edges)
        s = rng.randrange(n)
        d, parent = dag_shortest_paths(adj, s)
        assert d == oracle(n, edges, s)
        for v in range(n):
            if v != s and d[v] < math.inf:
                u = parent[v]
                assert any(x == v and d[u] + w == d[v] for x, w in adj[u])
