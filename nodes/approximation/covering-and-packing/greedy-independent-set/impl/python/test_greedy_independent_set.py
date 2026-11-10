# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-independent-set/. The authors are listed in prov/V2FWT9.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from greedy_independent_set import greedy_independent_set


def adjacency(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def alpha(n, edges):
    adj = adjacency(n, edges)
    for r in range(n, -1, -1):
        for c in combinations(range(n), r):
            if all(not (adj[v] & set(c)) for v in c):
                return r
    return 0


def caro_wei(n, edges):
    adj = adjacency(n, edges)
    return sum((Fraction(1, len(adj[v]) + 1) for v in range(n)), Fraction(0))


def check(n, edges):
    s = greedy_independent_set(n, edges)
    adj = adjacency(n, edges)
    chosen = set(s)
    assert len(chosen) == len(s)
    assert all(not (adj[v] & chosen) for v in s)  # independent
    assert all(v in chosen or adj[v] & chosen for v in range(n))  # maximal
    assert len(s) >= caro_wei(n, edges)
    return s


def test_example_page():
    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6)]
    assert check(7, edges) == [0, 3, 5]
    assert caro_wei(7, edges) == 2
    assert alpha(7, edges) == 3


def test_greedy_not_optimal():
    edges = [(0, 1), (0, 2), (1, 6), (2, 3), (2, 6), (3, 4), (3, 5), (4, 6), (5, 6)]
    assert check(7, edges) == [0, 3, 6]
    assert alpha(7, edges) == 4
    assert caro_wei(7, edges) == Fraction(61, 30)


def test_random_against_brute_force():
    rng = random.Random(1997)
    for trial in range(300):
        n = rng.randint(0, 10)
        p = rng.choice([0.15, 0.3, 0.5, 0.7])
        edges = [e for e in combinations(range(n), 2) if rng.random() < p]
        s = check(n, edges)
        a = alpha(n, edges)
        assert len(s) <= a
        if edges:
            delta = max(len(x) for x in adjacency(n, edges))
            # Halldorsson and Radhakrishnan: ratio (delta + 2) / 3 when delta >= 1
            assert 3 * a <= (delta + 2) * len(s)
        else:
            assert len(s) == a == n


def test_disjoint_cliques_equality():
    for sizes in ([1], [3], [2, 2, 2], [1, 4, 3], [5, 1, 2, 2]):
        edges, start = [], 0
        for k in sizes:
            edges += [(start + i, start + j) for i, j in combinations(range(k), 2)]
            start += k
        s = check(start, edges)
        assert len(s) == caro_wei(start, edges) == len(sizes) == alpha(start, edges)


def test_empty_graph():
    assert greedy_independent_set(0, []) == []
    assert greedy_independent_set(3, []) == [0, 1, 2]
