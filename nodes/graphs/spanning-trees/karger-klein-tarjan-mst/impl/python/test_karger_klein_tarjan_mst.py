# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karger-klein-tarjan-mst/. The authors are listed in prov/YYGGT8.jsonl.

import random

from karger_klein_tarjan_mst import _drop_heavy, karger_klein_tarjan_mst

EXAMPLE = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 4), (2, 4, 5), (3, 4, 7), (3, 5, 6), (4, 5, 2)]


def kruskal(n, edges):
    """The minimum spanning forest for the order by (weight, index)."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    out = []
    for i in sorted(range(len(edges)), key=lambda i: (edges[i][2], i)):
        a, b = find(edges[i][0]), find(edges[i][1])
        if a != b:
            parent[a] = b
            out.append(i)
    return sorted(out)


def test_example():
    for seed in range(20):
        assert karger_klein_tarjan_mst(6, EXAMPLE, random.Random(seed)) == [1, 2, 3, 5, 8]


def test_trivial_graphs():
    assert karger_klein_tarjan_mst(0, []) == []
    assert karger_klein_tarjan_mst(1, [(0, 0, 1)]) == []
    assert karger_klein_tarjan_mst(4, []) == []
    assert karger_klein_tarjan_mst(2, [(0, 1, 5)]) == [0]


def test_ties_and_parallel_edges():
    edges = [(0, 1, 1), (0, 1, 1), (1, 2, 1), (0, 2, 1), (2, 2, 0)]
    for seed in range(10):
        assert karger_klein_tarjan_mst(3, edges, random.Random(seed)) == [0, 2]


def test_disconnected():
    edges = [(0, 1, 2), (2, 3, 1), (3, 4, 1), (2, 4, 1), (6, 7, 0)]
    assert karger_klein_tarjan_mst(8, edges, random.Random(1)) == kruskal(8, edges) == [0, 1, 2, 4]


def test_heavy_edges_are_dropped():
    # Forest F = path 0 - 1 - 2 with keys 1 and 2; the edge 0-2 of key 3 is F-heavy.
    edges = [(0, 1, (1, 0)), (1, 2, (2, 1)), (0, 2, (3, 2)), (0, 2, (1.5, 3)), (2, 3, (9, 4))]
    keep = _drop_heavy(4, edges, {0, 1})
    assert [e[2][1] for e in keep] == [0, 1, 3, 4]


def test_random_against_kruskal():
    rng = random.Random(20261105)
    for trial in range(800):
        n = rng.randint(1, 15)
        m = rng.randint(0, 40)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(-3, 5)) for _ in range(m)]
        assert karger_klein_tarjan_mst(n, edges, random.Random(trial)) == kruskal(n, edges)


def test_larger_graphs():
    rng = random.Random(9)
    for trial in range(30):
        n = rng.randint(100, 400)
        m = rng.randint(n, 5 * n)
        edges = [(rng.randrange(n), rng.randrange(n), rng.random()) for _ in range(m)]
        assert karger_klein_tarjan_mst(n, edges, random.Random(trial)) == kruskal(n, edges)
