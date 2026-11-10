# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-bfs/. The authors are listed in prov/M17THE.jsonl.

import random
from collections import deque

from parallel_bfs import Cost, log2_ceil, parallel_bfs


def undirected(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def family(rng: random.Random) -> list[list[list[int]]]:
    """Empty, path, star, cycle, complete and random sparse and dense graphs."""
    out = []
    for n in (1, 2, 5, 17, 40):
        out.append(undirected(n, []))
        out.append(undirected(n, [(i, i + 1) for i in range(n - 1)]))
        out.append(undirected(n, [(0, i) for i in range(1, n)]))
        if n >= 3:
            out.append(undirected(n, [(i, (i + 1) % n) for i in range(n)]))
        out.append(undirected(n, [(i, j) for i in range(n) for j in range(i + 1, n)]))
    for _ in range(60):
        n = rng.randint(1, 60)
        p = rng.choice([0.02, 0.05, 0.1, 0.3, 0.7])
        out.append(undirected(n, [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]))
    return out


def seq_bfs(adj: list[list[int]], s: int) -> list[float]:
    dist = [float("inf")] * len(adj)
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == float("inf"):
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def test_example() -> None:
    adj = undirected(7, [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5), (5, 6)])
    dist, parent = parallel_bfs(adj, 0, random.Random(1))
    assert dist == [0, 1, 1, 2, 2, 3, 4]
    assert parent[0] == 0 and parent[6] == 5


def test_against_sequential_bfs() -> None:
    rng = random.Random(4101)
    for adj in family(rng):
        n = len(adj)
        for s in {0, n - 1, rng.randrange(n)}:
            c = Cost()
            dist, parent = parallel_bfs(adj, s, random.Random(rng.random()), c)
            assert dist == seq_bfs(adj, s)
            for v in range(n):
                if v == s:
                    assert parent[v] == s
                elif dist[v] == float("inf"):
                    assert parent[v] is None
                else:  # the parent is a neighbour one level up
                    p = parent[v]
                    assert p is not None and v in adj[p] and dist[p] == dist[v] - 1
            arcs = sum(len(a) for a in adj)
            levels = max(d for d in dist if d != float("inf")) + 1
            assert c.rounds == levels
            assert c.work <= 3 * n + 3 * arcs + 1
            assert c.span <= 1 + levels * (2 * log2_ceil(arcs + 1) + 4)


def test_directed() -> None:
    rng = random.Random(77)
    for _ in range(200):
        n = rng.randint(1, 30)
        adj = [[j for j in range(n) if j != i and rng.random() < 0.1] for i in range(n)]
        dist, _ = parallel_bfs(adj, 0, random.Random(rng.random()))
        assert dist == seq_bfs(adj, 0)


def test_each_vertex_enters_one_frontier() -> None:
    # complete graph: every vertex of level 1 is claimed by many writers, but appears once
    adj = undirected(30, [(i, j) for i in range(30) for j in range(i + 1, 30)])
    for seed in range(20):
        c = Cost()
        dist, parent = parallel_bfs(adj, 3, random.Random(seed), c)
        assert sorted(dist) == [0] + [1] * 29
        assert c.rounds == 2
