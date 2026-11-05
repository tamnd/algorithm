# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kruskal/. The authors are listed in prov/1DB0HR.jsonl.

import itertools
import random

from kruskal import kruskal

EXAMPLE = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 4), (2, 4, 5), (3, 4, 7), (3, 5, 6), (4, 5, 2)]


def components(n, edges, chosen):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for i in chosen:
        u, v, _ = edges[i]
        parent[find(u)] = find(v)
    return len({find(x) for x in range(n)})


def is_forest(n, edges, chosen):
    return components(n, edges, chosen) == n - len(chosen)


def brute_force(n, edges):
    """Least weight of a spanning forest with as many components as the graph."""
    c = components(n, edges, range(len(edges)))
    k = n - c
    best = None
    for s in itertools.combinations(range(len(edges)), k):
        if is_forest(n, edges, s):
            w = sum(edges[i][2] for i in s)
            best = w if best is None or w < best else best
    return best


def test_example():
    f = kruskal(6, EXAMPLE)
    assert f == [2, 3, 8, 1, 5]
    assert sum(EXAMPLE[i][2] for i in f) == 13


def test_edges_cases():
    assert kruskal(0, []) == []
    assert kruskal(1, []) == []
    assert kruskal(1, [(0, 0, 5)]) == []  # a self-loop is never taken
    assert kruskal(3, []) == []  # no edges: a forest of single vertices
    assert kruskal(2, [(0, 1, 5), (0, 1, 2)]) == [1]  # parallel edges
    assert kruskal(3, [(0, 1, 1), (1, 2, 1), (0, 2, 1)]) == [0, 1]  # all weights tie
    assert kruskal(3, [(0, 1, -2), (1, 2, -5), (0, 2, 0)]) == [1, 0]  # negative weights


def test_disconnected():
    edges = [(0, 1, 3), (2, 3, 1), (3, 4, 2), (2, 4, 9)]
    f = kruskal(6, edges)
    assert sorted(f) == [0, 1, 2]
    assert components(6, edges, f) == 3


def test_large_integers():
    big = 2**62
    edges = [(0, 1, big), (1, 2, big + 1), (0, 2, big - 1)]
    assert sorted(kruskal(3, edges)) == [0, 2]


def test_against_brute_force():
    rng = random.Random(20261105)
    for _ in range(600):
        n = rng.randrange(1, 7)
        m = rng.randrange(0, 9)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randrange(-2, 4)) for _ in range(m)]
        f = kruskal(n, edges)
        assert len(set(f)) == len(f)
        assert is_forest(n, edges, f)
        assert components(n, edges, f) == components(n, edges, range(m))
        assert sum(edges[i][2] for i in f) == brute_force(n, edges)
