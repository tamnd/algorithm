# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anf-algorithm/. The authors are listed in prov/MDNVAV.jsonl.

import random
from collections import deque

from anf_algorithm import anf_algorithm, fm_estimate, lowest_zero, random_ranks


def undirected(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def ball(adj: list[list[int]], v: int, h: int) -> list[int]:
    """The vertices reachable from v by at most h arcs, by breadth-first search."""
    dist = {v: 0}
    q = deque([v])
    while q:
        x = q.popleft()
        if dist[x] == h:
            continue
        for y in adj[x]:
            if y not in dist:
                dist[y] = dist[x] + 1
                q.append(y)
    return list(dist)


def direct_masks(adj: list[list[int]], h: int, ranks: list[list[int]]) -> list[list[int]]:
    n = len(adj)
    r = len(ranks[0]) if n else 0
    out = []
    for v in range(n):
        row = [0] * r
        for u in ball(adj, v, h):
            for j in range(r):
                row[j] |= 1 << ranks[u][j]
        out.append(row)
    return out


EXAMPLE = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6)]


def test_helpers() -> None:
    assert lowest_zero(0) == 0
    assert lowest_zero(0b1011) == 2
    assert lowest_zero(0b111) == 3
    assert abs(fm_estimate([0b1, 0b1]) - 2 / 0.77351) < 1e-12


def test_example() -> None:
    adj = undirected(7, EXAMPLE)
    exact = [sum(len(ball(adj, v, h)) for v in range(7)) for h in range(5)]
    assert exact == [7, 25, 35, 45, 49]
    ranks = random_ranks(7, 64, 1)
    est, masks = anf_algorithm(adj, 4, ranks)
    assert masks == direct_masks(adj, 4, ranks)
    assert len(est) == 5
    assert all(a <= b for a, b in zip(est, est[1:]))


def test_edges() -> None:
    assert anf_algorithm([], 3, []) == ([0, 0, 0, 0], [])
    est, masks = anf_algorithm([[]], 2, [[0, 1]])
    assert masks == [[1, 2]]
    assert est[0] == est[1] == est[2]
    # a directed path 0 -> 1 -> 2: vertex 0 reaches everything, vertex 2 only itself
    ranks = [[0], [1], [2]]
    _, masks = anf_algorithm([[1], [2], []], 2, ranks)
    assert masks == [[0b111], [0b110], [0b100]]


def test_accuracy_on_a_large_graph() -> None:
    rng = random.Random(77)
    n = 1500
    edges = [(i, i + 1) for i in range(n - 1)] + [(rng.randrange(n), rng.randrange(n)) for _ in range(300)]
    adj = undirected(n, edges)
    est, _ = anf_algorithm(adj, 6, random_ranks(n, 64, 5))
    for h in (3, 6):
        exact = sum(len(ball(adj, v, h)) for v in range(n))
        assert abs(est[h] - exact) < 0.1 * exact


def test_random_against_oracle() -> None:
    rng = random.Random(4242)
    for _ in range(500):
        n = rng.randint(1, 9)
        directed = rng.random() < 0.5
        adj: list[list[int]] = [[] for _ in range(n)]
        for _ in range(rng.randint(0, 2 * n)):
            u, v = rng.randrange(n), rng.randrange(n)
            adj[u].append(v)
            if not directed:
                adj[v].append(u)
        h = rng.randint(0, 4)
        ranks = random_ranks(n, rng.randint(1, 8), rng.randrange(10**6))
        est, masks = anf_algorithm(adj, h, ranks)
        want = direct_masks(adj, h, ranks)
        assert masks == want
        assert abs(est[-1] - sum(fm_estimate(row) for row in want)) < 1e-9
