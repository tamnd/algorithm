# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/floyd-warshall/. The authors are listed in prov/HSBPN7.jsonl.

import math
import random

from floyd_warshall import floyd_warshall, has_negative_cycle, path

INF = math.inf
EDGES = [(0, 1, 3), (0, 2, 8), (1, 3, 1), (1, 2, 4), (2, 1, -2), (3, 0, 2), (3, 2, 2)]


def bellman_ford(n, edges, s):
    """Independent oracle: distances from s, or None if a negative cycle is reachable."""
    d = [INF] * n
    d[s] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    if any(d[u] + w < d[v] for u, v, w in edges):
        return None
    return d


def test_example() -> None:
    D, nxt = floyd_warshall(4, EDGES)
    assert D == [[0, 3, 6, 4], [3, 0, 3, 1], [1, -2, 0, -1], [2, 0, 2, 0]]
    assert not has_negative_cycle(D)
    assert path(nxt, 0, 2) == [0, 1, 3, 2]
    assert path(nxt, 2, 0) == [2, 1, 3, 0]


def test_example_with_negative_cycle() -> None:
    edges = EDGES[:-1] + [(3, 2, -5)]
    D, _ = floyd_warshall(4, edges)
    assert has_negative_cycle(D)
    # the vertices 1, 2, 3 lie on the negative cycle 1 -> 3 -> 2 -> 1 of weight -6
    assert all(D[i][i] < 0 for i in (1, 2, 3))


def test_unreachable_pairs() -> None:
    D, nxt = floyd_warshall(3, [(0, 1, -4)])
    assert D == [[0, -4, INF], [INF, 0, INF], [INF, INF, 0]]
    assert path(nxt, 1, 0) is None and path(nxt, 2, 2) == [2]


def test_self_loops_and_parallel_edges() -> None:
    D, _ = floyd_warshall(2, [(0, 1, 5), (0, 1, 2), (1, 1, 3)])
    assert D == [[0, 2], [INF, 0]]
    D, _ = floyd_warshall(2, [(1, 1, -1)])
    assert has_negative_cycle(D) and D[0][0] == 0


def test_empty_graph() -> None:
    assert floyd_warshall(0, []) == ([], [])


def test_random_against_bellman_ford() -> None:
    rng = random.Random(1962)
    for _ in range(600):
        n = rng.randint(1, 7)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(-3, 9))
                 for _ in range(rng.randint(0, 3 * n))]
        D, nxt = floyd_warshall(n, edges)
        rows = [bellman_ford(n, edges, s) for s in range(n)]
        negative = any(r is None for r in rows)
        assert has_negative_cycle(D) == negative
        if not negative:
            assert D == rows
            best = {}
            for u, v, w in edges:
                best[u, v] = min(best.get((u, v), INF), w)
            for i in range(n):
                for j in range(n):
                    p = path(nxt, i, j)
                    if D[i][j] == INF:
                        assert p is None
                    else:
                        assert p[0] == i and p[-1] == j
                        assert sum(best[p[t], p[t + 1]] for t in range(len(p) - 1)) == D[i][j]
