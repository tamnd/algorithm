# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boruvka/. The authors are listed in prov/1APEF6.jsonl.

import itertools
import random

from boruvka import boruvka

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
    f = boruvka(6, EXAMPLE)
    assert f == [1, 2, 3, 8, 5]
    assert sum(EXAMPLE[i][2] for i in f) == 13


def test_ties_do_not_make_a_cycle():
    triangle = [(0, 1, 1), (1, 2, 1), (2, 0, 1)]
    f = boruvka(3, triangle)
    assert len(f) == 2 and is_forest(3, triangle, f)
    square = [(0, 1, 5), (1, 2, 5), (2, 3, 5), (3, 0, 5)]
    f = boruvka(4, square)
    assert len(f) == 3 and is_forest(4, square, f)


def test_edge_cases():
    assert boruvka(0, []) == []
    assert boruvka(1, [(0, 0, 3)]) == []
    assert boruvka(4, []) == []
    assert boruvka(2, [(0, 1, 7), (1, 0, 7), (0, 1, 2)]) == [2]
    assert sorted(boruvka(5, [(0, 1, 1), (2, 3, 1), (3, 4, -4)])) == [0, 1, 2]


def test_long_path():
    n = 64
    edges = [(i, i + 1, (i * 37) % 11) for i in range(n - 1)]
    assert sorted(boruvka(n, edges)) == list(range(n - 1))


def test_against_brute_force():
    rng = random.Random(1926)
    for _ in range(600):
        n = rng.randrange(1, 7)
        m = rng.randrange(0, 9)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randrange(0, 3)) for _ in range(m)]
        f = boruvka(n, edges)
        assert len(set(f)) == len(f)
        assert is_forest(n, edges, f)
        assert components(n, edges, f) == components(n, edges, range(m))
        assert sum(edges[i][2] for i in f) == brute_force(n, edges)
