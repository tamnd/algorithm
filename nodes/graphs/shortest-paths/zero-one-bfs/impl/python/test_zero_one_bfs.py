# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zero-one-bfs/. The authors are listed in prov/T8G377.jsonl.

import heapq
import random

import pytest

from zero_one_bfs import zero_one_bfs

S, A, B, C, D, T = range(6)
EXAMPLE = [(S, A, 1), (S, B, 0), (B, A, 0), (A, C, 1), (B, D, 1), (C, T, 0), (D, C, 0), (D, T, 1)]


def build(n: int, arcs: list[tuple[int, int, int]]) -> list[list[tuple[int, int]]]:
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in arcs:
        adj[u].append((v, w))
    return adj


def dijkstra(adj: list[list[tuple[int, int]]], s: int) -> list[int | None]:
    dist: list[int | None] = [None] * len(adj)
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if dist[u] is not None:
            continue
        dist[u] = d
        for v, w in adj[u]:
            if dist[v] is None:
                heapq.heappush(pq, (d + w, v))
    return dist


def check_tree(adj: list[list[tuple[int, int]]], s: int, dist: list[int | None], parent: list[int | None]) -> None:
    for v in range(len(adj)):
        if v == s or dist[v] is None:
            assert parent[v] is None
            continue
        u = parent[v]
        assert u is not None and dist[u] is not None
        assert any(x == v and dist[u] + w == dist[v] for x, w in adj[u])


def test_example() -> None:
    adj = build(6, EXAMPLE)
    dist, parent = zero_one_bfs(adj, S)
    assert dist == [0, 0, 0, 1, 1, 1]
    assert parent == [None, B, S, A, B, C]
    check_tree(adj, S, dist, parent)


def test_unreachable() -> None:
    adj = build(4, [(0, 1, 1), (2, 3, 0), (3, 0, 1)])
    dist, parent = zero_one_bfs(adj, 0)
    assert dist == [0, 1, None, None]
    assert parent == [None, 0, None, None]


def test_single_vertex_and_self_loop() -> None:
    assert zero_one_bfs([[]], 0) == ([0], [None])
    assert zero_one_bfs([[(0, 0), (0, 1)]], 0) == ([0], [None])


def test_zero_cycle() -> None:
    adj = build(3, [(0, 1, 1), (1, 2, 0), (2, 1, 0)])
    dist, parent = zero_one_bfs(adj, 0)
    assert dist == [0, 1, 1]
    assert parent == [None, 0, 1]


def test_rejects_negative_and_large_weights() -> None:
    with pytest.raises(ValueError):
        zero_one_bfs(build(2, [(0, 1, 0), (1, 0, -1)]), 0)  # a negative cycle
    with pytest.raises(ValueError):
        zero_one_bfs(build(2, [(0, 1, 2)]), 0)


def test_random_against_dijkstra() -> None:
    rng = random.Random(1201)
    for _ in range(600):
        n = rng.randint(1, 9)
        arcs = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 1)) for _ in range(rng.randint(0, 3 * n))]
        adj = build(n, arcs)
        s = rng.randrange(n)
        dist, parent = zero_one_bfs(adj, s)
        assert dist == dijkstra(adj, s)
        check_tree(adj, s, dist, parent)
