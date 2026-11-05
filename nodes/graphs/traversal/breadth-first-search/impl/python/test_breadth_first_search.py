# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/breadth-first-search/. The authors are listed in prov/HAEH1M.jsonl.

import random

from breadth_first_search import breadth_first_search


def undirected(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def oracle(adj: list[list[int]], s: int) -> list[int | None]:
    """Distances by repeated relaxation (Bellman-Ford with unit weights)."""
    n = len(adj)
    inf = n + 1
    d = [inf] * n
    d[s] = 0
    for _ in range(n):
        for u in range(n):
            for v in adj[u]:
                if d[u] + 1 < d[v]:
                    d[v] = d[u] + 1
    return [x if x < inf else None for x in d]


def check_parents(adj: list[list[int]], s: int, dist: list[int | None], parent: list[int | None]) -> None:
    for v in range(len(adj)):
        p = parent[v]
        if v == s or dist[v] is None:
            assert p is None
        else:
            assert p is not None and v in adj[p]
            assert dist[p] is not None and dist[p] + 1 == dist[v]


def test_example() -> None:
    adj = undirected(8, [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5), (5, 6)])
    dist, parent = breadth_first_search(adj, 0)
    assert dist == [0, 1, 1, 2, 2, 3, 4, None]
    assert parent == [None, 0, 0, 1, 2, 3, 5, None]


def test_edges() -> None:
    assert breadth_first_search([[]], 0) == ([0], [None])
    assert breadth_first_search([[0]], 0) == ([0], [None])  # a self-loop
    assert breadth_first_search([[1], []], 1) == ([None, 0], [None, None])  # directed
    dist, _ = breadth_first_search(undirected(5, [(0, 1), (1, 2), (2, 3), (3, 4)]), 0)
    assert dist == [0, 1, 2, 3, 4]
    dist, _ = breadth_first_search([[1, 1], [0, 0]], 0)  # parallel edges
    assert dist == [0, 1]


def test_random_against_oracle() -> None:
    rng = random.Random(4219)
    for _ in range(600):
        n = rng.randint(1, 12)
        directed = rng.random() < 0.5
        adj: list[list[int]] = [[] for _ in range(n)]
        for _ in range(rng.randint(0, 2 * n)):
            u, v = rng.randrange(n), rng.randrange(n)
            adj[u].append(v)
            if not directed:
                adj[v].append(u)
        s = rng.randrange(n)
        dist, parent = breadth_first_search(adj, s)
        assert dist == oracle(adj, s)
        check_parents(adj, s, dist, parent)
