# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/near-linear-negative-sssp/. The authors are listed in prov/KXQB8V.jsonl.

import random

import pytest

from near_linear_negative_sssp import near_linear_negative_sssp

S, T, X, Y, Z = range(5)
G1 = [(S, T, 6), (S, Y, 7), (T, X, 5), (T, Y, 8), (T, Z, -4), (X, T, -2), (Y, X, -3), (Y, Z, 9), (Z, S, 2), (Z, X, 7)]


def bellman_ford(n, edges, s):
    """Independent oracle: Bellman-Ford with a final negative-cycle check."""
    inf = float("inf")
    d = [inf] * n
    d[s] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    for u, v, w in edges:
        if d[u] + w < d[v]:
            return None
    return [None if x == inf else x for x in d]


def test_clrs_example():
    assert near_linear_negative_sssp(5, G1, S) == [0, 2, 4, 7, -2]


def test_reachable_negative_cycle():
    g = [(u, v, -6 if (u, v) == (X, T) else w) for u, v, w in G1]
    assert near_linear_negative_sssp(5, g, S) is None


def test_negative_cycle_not_reachable_is_ignored():
    edges = [(0, 1, 4), (1, 2, -1), (3, 4, -2), (4, 3, 1)]
    assert near_linear_negative_sssp(5, edges, 0) == [0, 4, 3, None, None]


def test_unreachable_and_single_vertex():
    assert near_linear_negative_sssp(3, [(1, 2, -5)], 0) == [0, None, None]
    assert near_linear_negative_sssp(1, [], 0) == [0]
    assert near_linear_negative_sssp(1, [(0, 0, -1)], 0) is None
    assert near_linear_negative_sssp(1, [(0, 0, 0)], 0) == [0]


def test_non_integer_weight_rejected():
    with pytest.raises(ValueError):
        near_linear_negative_sssp(2, [(0, 1, 1.5)], 0)


def test_result_does_not_depend_on_seed():
    rng = random.Random(7)
    edges = [(rng.randrange(12), rng.randrange(12), rng.randint(-4, 9)) for _ in range(40)]
    want = bellman_ford(12, edges, 0)
    for seed in range(20):
        assert near_linear_negative_sssp(12, edges, 0, seed) == want


def test_random_against_bellman_ford():
    rng = random.Random(20261105)
    cycles = 0
    for case in range(800):
        n = rng.randint(1, 10)
        m = rng.randint(0, 3 * n)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(-6, 12)) for _ in range(m)]
        s = rng.randrange(n)
        want = bellman_ford(n, edges, s)
        cycles += want is None
        assert near_linear_negative_sssp(n, edges, s, seed=case) == want
    assert cycles > 50


def test_larger_graphs_without_negative_cycles():
    rng = random.Random(99)
    for case in range(30):
        n = rng.randint(20, 40)
        pot = [rng.randint(0, 50) for _ in range(n)]
        edges = []
        for _ in range(4 * n):
            u, v = rng.randrange(n), rng.randrange(n)
            edges.append((u, v, rng.randint(0, 20) + pot[v] - pot[u]))
        assert near_linear_negative_sssp(n, edges, 0, seed=case) == bellman_ford(n, edges, 0)
