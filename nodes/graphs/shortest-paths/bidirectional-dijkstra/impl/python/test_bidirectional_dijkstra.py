# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bidirectional-dijkstra/. The authors are listed in prov/BPW9SV.jsonl.

import math
import random

import pytest

from bidirectional_dijkstra import bidirectional_dijkstra

INF = math.inf
# s=0, a=1, b=2, x=3, t=4
EXAMPLE = [[(1, 3), (3, 6)], [(2, 4)], [(4, 3)], [(4, 6)], []]


def bellman_ford(adj, s):
    """Independent oracle: distances from s by n - 1 rounds of relaxing every edge."""
    n = len(adj)
    d = [INF] * n
    d[s] = 0
    for _ in range(n - 1):
        for u in range(n):
            for v, w in adj[u]:
                if d[u] + w < d[v]:
                    d[v] = d[u] + w
    return d


def path_weight(adj, p):
    return sum(min(w for v, w in adj[a] if v == b) for a, b in zip(p, p[1:]))


def test_example() -> None:
    assert bidirectional_dijkstra(EXAMPLE, 0, 4) == (10, [0, 1, 2, 4])


def test_meeting_vertex_is_not_on_the_shortest_path() -> None:
    # x is the first vertex scanned by both searches if they alternate, but s-x-t costs 12
    dist, p = bidirectional_dijkstra(EXAMPLE, 0, 4)
    assert dist == 10 and 3 not in p


def test_unreachable() -> None:
    adj = [[(1, 2)], [], [(0, 1)]]
    assert bidirectional_dijkstra(adj, 0, 2) == (INF, None)
    assert bidirectional_dijkstra([[], []], 0, 1) == (INF, None)


def test_same_vertex_and_self_loops() -> None:
    assert bidirectional_dijkstra([[(0, 0)]], 0, 0) == (0, [0])
    adj = [[(0, 0), (1, 5)], [(1, 0)]]
    assert bidirectional_dijkstra(adj, 0, 1) == (5, [0, 1])


def test_zero_weights_and_parallel_edges() -> None:
    adj = [[(1, 0), (1, 3)], [(2, 0), (0, 0)], [(0, 0)]]
    assert bidirectional_dijkstra(adj, 0, 2) == (0, [0, 1, 2])


def test_negative_weight_rejected() -> None:
    # with a negative edge (and here a negative cycle 0 -> 1 -> 0) there is no valid answer
    with pytest.raises(ValueError):
        bidirectional_dijkstra([[(1, 1)], [(0, -2)]], 0, 1)


def test_random_against_bellman_ford() -> None:
    rng = random.Random(1969)
    for _ in range(800):
        n = rng.randint(1, 9)
        adj = [[] for _ in range(n)]
        for _ in range(rng.randint(0, 3 * n)):
            adj[rng.randrange(n)].append((rng.randrange(n), rng.choice([0, rng.randint(1, 9)])))
        s, t = rng.randrange(n), rng.randrange(n)
        dist, p = bidirectional_dijkstra(adj, s, t)
        assert dist == bellman_ford(adj, s)[t]
        if dist == INF:
            assert p is None
        else:
            assert p[0] == s and p[-1] == t and path_weight(adj, p) == dist
