# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direction-optimizing-bfs/. The authors are listed in prov/HZS2BB.jsonl.

import random
from collections import deque

from direction_optimizing_bfs import Cost, direction_optimizing_bfs


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


def check_tree(adj: list[list[int]], s: int, dist: list[float], parent: list[int | None]) -> None:
    for v in range(len(adj)):
        if v == s:
            assert parent[v] == s
        elif dist[v] == float("inf"):
            assert parent[v] is None
        else:
            p = parent[v]
            assert p is not None and v in adj[p] and dist[p] == dist[v] - 1


def test_example() -> None:
    adj = undirected(7, [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5), (5, 6)])
    c = Cost()
    dist, parent = direction_optimizing_bfs(adj, 0, alpha=2, beta=2, cost=c)
    assert dist == [0, 1, 1, 2, 2, 3, 4]
    assert c.modes == ["top-down", "bottom-up", "bottom-up", "top-down", "top-down"]
    assert c.examined == 14  # top-down only looks at 16 edge slots
    assert parent[3] == 1 and parent[4] == 2 and parent[5] == 3  # first hit in the in-list order


def test_all_modes_against_sequential_bfs() -> None:
    rng = random.Random(5150)
    runs = 0
    for adj in family(rng):
        n = len(adj)
        arcs = sum(len(a) for a in adj)
        for s in {0, n - 1, rng.randrange(n)}:
            want = seq_bfs(adj, s)
            levels = max(d for d in want if d != float("inf")) + 1
            for force in (None, "top-down", "bottom-up"):
                alpha = rng.choice([1.0, 4.0, 14.0, 100.0])
                beta = rng.choice([2.0, 24.0, 1000.0])
                c = Cost()
                dist, parent = direction_optimizing_bfs(adj, s, alpha, beta, rng=random.Random(rng.random()), cost=c, force=force)
                assert dist == want
                check_tree(adj, s, dist, parent)
                assert c.rounds == levels
                assert c.work <= 10 * (n + arcs) * levels + 10
                if force == "top-down":
                    assert c.examined == sum(len(adj[v]) for v in range(n) if want[v] != float("inf"))
                runs += 1
    assert runs >= 500


def test_directed() -> None:
    rng = random.Random(78)
    for _ in range(200):
        n = rng.randint(1, 30)
        adj = [[j for j in range(n) if j != i and rng.random() < 0.15] for i in range(n)]
        for force in (None, "bottom-up"):
            dist, parent = direction_optimizing_bfs(adj, 0, 1.0, 2.0, rng=random.Random(rng.random()), force=force)
            assert dist == seq_bfs(adj, 0)
            check_tree(adj, 0, dist, parent)


def test_fewer_edges_on_dense_random_graph() -> None:
    rng = random.Random(9)
    n = 300
    adj = undirected(n, [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.05])
    hybrid, top = Cost(), Cost()
    direction_optimizing_bfs(adj, 0, cost=hybrid)
    direction_optimizing_bfs(adj, 0, cost=top, force="top-down")
    assert "bottom-up" in hybrid.modes
    assert hybrid.examined < top.examined / 2
