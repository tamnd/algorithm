# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dial-algorithm/. The authors are listed in prov/T0RAP2.jsonl.

import math
import random

import pytest

from dial_algorithm import dial

INF = math.inf
# s=0, a=1, b=2, c=3, t=4, z=5
EXAMPLE = [[(1, 2), (2, 3)], [(2, 0), (3, 3)], [(3, 3), (4, 3)], [(4, 1)], [], [(0, 1)]]


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


def test_example() -> None:
    d, parent = dial(EXAMPLE, 0)
    assert d == [0, 2, 2, 5, 5, INF]
    assert parent == [None, 0, 1, 1, 2, None]


def test_unreachable_and_single_vertex() -> None:
    assert dial([[]], 0) == ([0], [None])
    d, _ = dial([[], [(0, 4)]], 0)
    assert d == [0, INF]


def test_zero_weights_only() -> None:
    adj = [[(1, 0)], [(2, 0), (0, 0)], [(2, 0)]]
    assert dial(adj, 0)[0] == [0, 0, 0]


def test_negative_or_fractional_weight_rejected() -> None:
    # a negative edge (here on the negative cycle 0 -> 1 -> 0) is outside the model
    with pytest.raises(ValueError):
        dial([[(1, 1)], [(0, -2)]], 0)
    with pytest.raises(ValueError):
        dial([[(1, 1.5)], []], 0)


def test_wraparound_of_the_circular_array() -> None:
    # a long path of weight-C edges sends the index around the array many times
    n, C = 30, 7
    adj = [[(i + 1, C)] if i + 1 < n else [] for i in range(n)]
    adj[0].append((n - 1, C * n))
    d, _ = dial(adj, 0)
    assert d == [C * i for i in range(n)]


def test_random_against_bellman_ford() -> None:
    rng = random.Random(1969)
    for _ in range(800):
        n = rng.randint(1, 9)
        C = rng.choice([0, 1, 3, 10])
        adj = [[] for _ in range(n)]
        for _ in range(rng.randint(0, 3 * n)):
            adj[rng.randrange(n)].append((rng.randrange(n), rng.randint(0, C)))
        s = rng.randrange(n)
        d, parent = dial(adj, s)
        assert d == bellman_ford(adj, s)
        for v in range(n):
            if v != s and d[v] < INF:
                u = parent[v]
                assert d[v] == d[u] + min(w for x, w in adj[u] if x == v)
