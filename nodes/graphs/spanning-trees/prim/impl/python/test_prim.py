# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prim/. The authors are listed in prov/6NDZ9M.jsonl.

import itertools
import random

from prim import prim

# a=0, b=1, c=2, d=3, e=4, f=5
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
    """Least weight of a spanning forest, by trying every edge set of the right size."""
    k = n - components(n, edges, range(len(edges)))
    best = None
    for s in itertools.combinations(range(len(edges)), k):
        if is_forest(n, edges, s):
            w = sum(edges[i][2] for i in s)
            best = w if best is None or w < best else best
    return best


def weight(edges, chosen):
    return sum(edges[i][2] for i in chosen)


def test_example():
    t = prim(6, EXAMPLE)
    assert sorted(t) == [1, 2, 3, 5, 8]  # ac, bc, bd, ce, ef
    assert weight(EXAMPLE, t) == 13


def test_edge_cases():
    assert prim(0, []) == []
    assert prim(1, []) == []
    assert prim(1, [(0, 0, -7)]) == []  # a self-loop is never taken
    assert prim(2, [(0, 1, 5), (0, 1, 2)]) == [1]  # parallel edges: the lighter one
    t = prim(3, [(0, 1, 1), (1, 2, 1), (0, 2, 1)])  # all weights tie
    assert len(t) == 2 and is_forest(3, [(0, 1, 1), (1, 2, 1), (0, 2, 1)], t)
    assert sorted(prim(3, [(0, 1, -2), (1, 2, -5), (0, 2, 0)])) == [0, 1]  # negative weights


def test_disconnected():
    edges = [(0, 1, 3), (2, 3, 1), (3, 4, 2), (2, 4, 9)]
    t = prim(6, edges)
    assert sorted(t) == [0, 1, 2]
    assert components(6, edges, t) == 3


def test_not_shortest_path_tree():
    # The shortest-path tree from 0 uses 0-2 (weight 3); the MST uses 0-1 and 1-2.
    edges = [(0, 1, 2), (1, 2, 2), (0, 2, 3)]
    assert sorted(prim(3, edges)) == [0, 1]


def test_tree_vertex_not_overwritten():
    # Without the in-tree test of line L10, vertex 0 would get parent edge 2 (weight -1 < key 0).
    edges = [(0, 1, 1), (1, 2, 1), (0, 2, -1)]
    t = prim(3, edges)
    assert len(t) == 2 and weight(edges, t) == 0


def test_large_integers():
    big = 2**62
    edges = [(0, 1, big), (1, 2, big + 1), (0, 2, big - 1)]
    assert sorted(prim(3, edges)) == [0, 2]


def test_against_brute_force():
    rng = random.Random(6157)
    for _ in range(600):
        n = rng.randrange(1, 7)
        m = rng.randrange(0, 9)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randrange(-2, 4)) for _ in range(m)]
        t = prim(n, edges)
        assert len(set(t)) == len(t)
        assert is_forest(n, edges, t)
        assert components(n, edges, t) == components(n, edges, range(m))
        assert weight(edges, t) == brute_force(n, edges)
