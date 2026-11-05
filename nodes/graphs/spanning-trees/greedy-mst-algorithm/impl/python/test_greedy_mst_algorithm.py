# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-mst-algorithm/. The authors are listed in prov/701F07.jsonl.

import itertools
import random

from greedy_mst_algorithm import greedy_mst

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
    k = n - components(n, edges, range(len(edges)))
    best = None
    for s in itertools.combinations(range(len(edges)), k):
        if is_forest(n, edges, s):
            w = sum(edges[i][2] for i in s)
            best = w if best is None or w < best else best
    return best


def test_example():
    blue, log = greedy_mst(6, EXAMPLE)
    assert log == [
        ("blue", 1), ("blue", 2), ("red", 0), ("blue", 3), ("red", 4),
        ("blue", 5), ("red", 6), ("blue", 8), ("red", 7),
    ]
    assert blue == [1, 2, 3, 5, 8]


def test_edge_cases():
    assert greedy_mst(0, []) == ([], [])
    assert greedy_mst(1, [(0, 0, 4)]) == ([], [("red", 0)])
    assert greedy_mst(2, [(0, 1, 3), (0, 1, 1)]) == ([1], [("blue", 1), ("red", 0)])
    blue, _ = greedy_mst(3, [(0, 1, 1), (1, 2, 1), (2, 0, 1)])
    assert len(blue) == 2
    blue, _ = greedy_mst(4, [(0, 1, 2), (2, 3, 5)])
    assert blue == [0, 1]


def test_against_brute_force_with_random_choices():
    rng = random.Random(1983)
    for _ in range(600):
        n = rng.randrange(1, 7)
        m = rng.randrange(0, 9)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randrange(0, 3)) for _ in range(m)]
        blue, log = greedy_mst(n, edges, rng)
        assert len(log) == m
        assert sorted(i for _, i in log) == list(range(m))
        assert is_forest(n, edges, blue)
        assert components(n, edges, blue) == components(n, edges, range(m))
        assert sum(edges[i][2] for i in blue) == brute_force(n, edges)
