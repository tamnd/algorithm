# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/even-shiloach-tree/. The authors are listed in prov/VS2KBW.jsonl.

import heapq
import random

from even_shiloach_tree import INF, EvenShiloachTree


def _dist(n: int, edges: list[tuple[int, int, int]], alive: list[bool], s: int, depth: int) -> list[float]:
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for i, (u, v, w) in enumerate(edges):
        if alive[i]:
            adj[u].append((v, w))
    d = [INF] * n
    d[s] = 0
    pq = [(0, s)]
    while pq:
        du, u = heapq.heappop(pq)
        if du > d[u]:
            continue
        for v, w in adj[u]:
            if du + w < d[v]:
                d[v] = du + w
                heapq.heappush(pq, (d[v], v))
    return [x if x <= depth else INF for x in d]


def test_example() -> None:
    edges = [(0, 1, 1), (0, 2, 1), (1, 3, 1), (2, 3, 1), (3, 4, 1), (2, 4, 1), (4, 5, 1), (1, 5, 1)]
    t = EvenShiloachTree(6, edges, 0, 4)
    assert [t.distance(v) for v in range(6)] == [0, 1, 1, 2, 2, 2]
    t.delete(5)  # 2 -> 4
    assert [t.distance(v) for v in range(6)] == [0, 1, 1, 2, 3, 2]
    t.delete(0)  # 0 -> 1
    assert [t.distance(v) for v in range(6)] == [0, INF, 1, 2, 3, 4]
    t.delete(3)  # 2 -> 3
    assert [t.distance(v) for v in range(6)] == [0, INF, 1, INF, INF, INF]


def test_random_against_dijkstra() -> None:
    rng = random.Random(11)
    for _ in range(500):
        n = rng.randint(1, 8)
        m = rng.randint(0, 20)
        maxw = rng.choice([1, 1, 3])
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(1, maxw)) for _ in range(m)]
        s = rng.randrange(n)
        depth = rng.randint(0, 3 * n)
        t = EvenShiloachTree(n, edges, s, depth)
        alive = [True] * m
        order = list(range(m))
        rng.shuffle(order)
        assert [t.distance(v) for v in range(n)] == _dist(n, edges, alive, s, depth)
        for e in order:
            t.delete(e)
            alive[e] = False
            exp = _dist(n, edges, alive, s, depth)
            assert [t.distance(v) for v in range(n)] == exp
            for v in range(n):
                p = t.parent(v)
                if p != -1:
                    assert exp[p] < exp[v]


def test_long_path() -> None:
    n = 600
    edges = [(i, i + 1, 1) for i in range(n - 1)] + [(0, n - 1, 1)]
    t = EvenShiloachTree(n, edges, 0, n)
    assert t.distance(n - 1) == 1
    t.delete(n - 1)
    assert t.distance(n - 1) == n - 1
    t.delete(0)
    assert t.distance(5) == INF
