# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bellman-ford/. The authors are listed in prov/2PW2HK.jsonl.

import math
import random

from bellman_ford import bellman_ford

NAMES = "sabcd"
EDGES = [("c", "d", 3), ("b", "c", -4), ("a", "b", 2), ("s", "a", 3), ("s", "b", 6),
         ("a", "d", 4), ("d", "b", 1), ("s", "c", 5)]


def named(edges):
    ix = {c: i for i, c in enumerate(NAMES)}
    return [(ix[u], ix[v], w) for u, v, w in edges]


def floyd(n, edges):
    """Independent oracle: all-pairs walk distances; D[x][x] < 0 means x is on a negative cycle."""
    D = [[math.inf] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = 0
    for u, v, w in edges:
        D[u][v] = min(D[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if D[i][k] + D[k][j] < D[i][j]:
                    D[i][j] = D[i][k] + D[k][j]
    return D


def check_cycle(edges, cycle):
    w = {(u, v): x for u, v, x in edges}
    k = len(cycle)
    assert k >= 1 and len(set(cycle)) == k
    assert all((cycle[i], cycle[(i + 1) % k]) in w for i in range(k))
    assert sum(w[cycle[i], cycle[(i + 1) % k]] for i in range(k)) < 0


def test_example() -> None:
    d, parent, cycle = bellman_ford(5, named(EDGES), 0)
    assert cycle is None
    assert d == [0, 3, 5, 1, 4]
    assert parent == [None, 0, 1, 2, 3]


def test_example_with_negative_cycle() -> None:
    edges = named(EDGES + [("c", "a", -2)])
    _, _, cycle = bellman_ford(5, edges, 0)
    assert cycle is not None
    assert sorted(cycle) == [1, 2, 3]
    check_cycle(edges, cycle)


def test_unreachable_and_unreachable_negative_cycle() -> None:
    # vertices 2 and 3 form a negative cycle that s = 0 cannot reach
    edges = [(0, 1, 5), (2, 3, -2), (3, 2, -2), (3, 1, -100)]
    d, parent, cycle = bellman_ford(4, edges, 0)
    assert cycle is None
    assert d == [0, 5, math.inf, math.inf]
    assert parent == [None, 0, None, None]


def test_negative_self_loop_and_cycle_through_source() -> None:
    _, _, cycle = bellman_ford(2, [(0, 1, 1), (1, 1, -1)], 0)
    assert cycle == [1]
    _, _, cycle = bellman_ford(2, [(0, 1, 1), (1, 0, -2)], 0)
    assert cycle is not None and sorted(cycle) == [0, 1]


def test_zero_cycle_is_not_negative() -> None:
    d, _, cycle = bellman_ford(3, [(0, 1, 1), (1, 2, -3), (2, 1, 3)], 0)
    assert cycle is None and d == [0, 1, -2]


def test_small_cases() -> None:
    assert bellman_ford(1, [], 0) == ([0], [None], None)
    assert bellman_ford(1, [(0, 0, 0)], 0) == ([0], [None], None)
    big = 2**62
    d, _, _ = bellman_ford(3, [(0, 1, big), (1, 2, big), (0, 2, -big)], 0)
    assert d == [0, big, -big]


def test_random_against_floyd_warshall() -> None:
    rng = random.Random(1958)
    for _ in range(800):
        n = rng.randint(1, 7)
        w = {}
        for _ in range(rng.randint(0, 3 * n)):
            w[rng.randrange(n), rng.randrange(n)] = rng.randint(-4, 9)
        edges = [(u, v, x) for (u, v), x in w.items()]
        rng.shuffle(edges)
        s = rng.randrange(n)
        D = floyd(n, edges)
        neg = any(D[s][x] < math.inf and D[x][x] < 0 for x in range(n))
        d, parent, cycle = bellman_ford(n, edges, s)
        if neg:
            assert cycle is not None
            check_cycle(edges, cycle)
        else:
            assert cycle is None
            assert d == D[s]
            for v in range(n):
                if v != s and d[v] < math.inf:
                    assert d[parent[v]] + w[parent[v], v] == d[v]
