# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ramalingam-reps/. The authors are listed in prov/Q56GAS.jsonl.

import heapq
import random

import pytest

from ramalingam_reps import INF, RamalingamReps


def _static(n: int, s: int, edges: dict[tuple[int, int], int]) -> list[float]:
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for (u, v), w in edges.items():
        adj[u].append((v, w))
    d = [INF] * n
    d[s] = 0
    pq = [(0, s)]
    while pq:
        dx, x = heapq.heappop(pq)
        if dx > d[x]:
            continue
        for z, w in adj[x]:
            if dx + w < d[z]:
                d[z] = dx + w
                heapq.heappush(pq, (d[z], z))
    return d


def test_example() -> None:
    g = RamalingamReps(5, 0, [(0, 1, 2), (0, 2, 5), (1, 2, 1), (1, 3, 6), (2, 3, 2), (3, 4, 1)])
    assert g.d == [0, 2, 3, 5, 6]
    g.delete(1, 2)
    assert g.d == [0, 2, 5, 7, 8]
    g.insert(4, 1, 1)
    assert g.d == [0, 2, 5, 7, 8]
    g.set_edge(0, 3, 3)
    assert g.d == [0, 2, 5, 3, 4]
    g.delete(0, 1)
    assert g.d == [0, 5, 5, 3, 4]


def test_rejects_bad_weights() -> None:
    g = RamalingamReps(2, 0)
    with pytest.raises(ValueError):
        g.insert(0, 1, 0)


def test_random_against_dijkstra() -> None:
    rng = random.Random(11)
    for _ in range(600):
        n = rng.randint(1, 8)
        s = rng.randrange(n)
        edges: dict[tuple[int, int], int] = {}
        for _ in range(rng.randint(0, 2 * n)):
            u, v = rng.randrange(n), rng.randrange(n)
            if u != v:
                edges[(u, v)] = rng.randint(1, 6)
        g = RamalingamReps(n, s, [(u, v, w) for (u, v), w in edges.items()])
        assert g.d == _static(n, s, edges)
        for _ in range(rng.randint(1, 30)):
            u, v = rng.randrange(n), rng.randrange(n)
            if u == v:
                continue
            if (u, v) in edges and rng.random() < 0.4:
                del edges[(u, v)]
                g.delete(u, v)
            else:
                w = rng.randint(1, 6)
                edges[(u, v)] = w
                g.set_edge(u, v, w)
            assert g.d == _static(n, s, edges)
            for x in range(n):
                cnt = g.cnt[x]
                g._recount(x)
                assert cnt == g.cnt[x]


def test_long_chain() -> None:
    n = 3000
    g = RamalingamReps(n, 0, [(i, i + 1, 1) for i in range(n - 1)])
    assert g.distance(n - 1) == n - 1
    g.insert(0, n // 2, 1)
    assert g.distance(n - 1) == n - n // 2
    g.delete(0, n // 2)
    assert g.distance(n - 1) == n - 1
    g.delete(10, 11)
    assert g.distance(n - 1) == INF
