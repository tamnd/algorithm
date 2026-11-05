# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/desopo-pape-algorithm/. The authors are listed in prov/5Q4Y55.jsonl.

import math
import random

from desopo_pape_algorithm import desopo_pape

INF = math.inf
# s=0, a=1, b=2, c=3, d=4
EXAMPLE = [[(1, 2), (2, 6), (3, 7)], [(2, 3), (4, 8)], [(4, 1)], [(1, -6)], []]


def bellman_ford(adj, s):
    """Independent oracle: distances from s, or None if a negative cycle is reachable."""
    n = len(adj)
    d = [INF] * n
    d[s] = 0
    for _ in range(n - 1):
        for u in range(n):
            for v, w in adj[u]:
                if d[u] + w < d[v]:
                    d[v] = d[u] + w
    for u in range(n):
        for v, w in adj[u]:
            if d[u] + w < d[v]:
                return None
    return d


def check_tree(adj, s, d, parent):
    for v in range(len(adj)):
        if v == s or d[v] == INF:
            assert parent[v] is None or v == s
            continue
        u = parent[v]
        assert d[v] == d[u] + min(w for x, w in adj[u] if x == v)


def test_example() -> None:
    d, parent = desopo_pape(EXAMPLE, 0)
    assert d == [0, 1, 4, 7, 5]
    assert parent == [None, 3, 1, 0, 2]


def test_unreachable() -> None:
    adj = [[(1, -2)], [], [(0, 1), (1, 1)]]
    d, parent = desopo_pape(adj, 0)
    assert d == [0, -2, INF] and parent[2] is None


def test_negative_cycle() -> None:
    adj = [[(1, 1)], [(2, -3)], [(1, 1), (3, 0)], []]
    assert desopo_pape(adj, 0) is None
    assert desopo_pape([[(0, -1)]], 0) is None


def test_negative_cycle_not_reachable() -> None:
    adj = [[(1, 4)], [], [(3, -2)], [(2, 1)]]
    assert desopo_pape(adj, 0) == ([0, 4, INF, INF], [None, 0, None, None])


def test_zero_cycle_terminates() -> None:
    adj = [[(1, 0)], [(2, 0)], [(0, 0), (3, -1)], []]
    d, _ = desopo_pape(adj, 0)
    assert d == [0, 0, 0, -1]


def test_random_against_bellman_ford() -> None:
    rng = random.Random(1974)
    for _ in range(800):
        n = rng.randint(1, 8)
        adj = [[] for _ in range(n)]
        low = rng.choice([0, -1, -3, -6])
        for _ in range(rng.randint(0, 3 * n)):
            adj[rng.randrange(n)].append((rng.randrange(n), rng.randint(low, 9)))
        s = rng.randrange(n)
        want = bellman_ford(adj, s)
        got = desopo_pape(adj, s)
        if want is None:
            assert got is None
        else:
            assert got is not None and got[0] == want
            check_tree(adj, s, got[0], got[1])
