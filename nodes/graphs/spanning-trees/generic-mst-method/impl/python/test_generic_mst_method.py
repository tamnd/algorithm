# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generic-mst-method/. The authors are listed in prov/AA7K7S.jsonl.

import itertools
import random

import pytest

from generic_mst_method import generic_mst

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


def test_example_prim_like():
    # the tree of vertex a (label 0) is always the open tree with the smallest label
    f = generic_mst(6, EXAMPLE)
    assert f == [1, 2, 3, 5, 8]
    assert sum(EXAMPLE[i][2] for i in f) == 13


def test_example_free_cuts():
    # the cuts of the page: {d}, {e}, {a}, {a, c}, {e, f}
    script = iter([3, 4, 0, 0, 4])

    def choose(comp, open_trees):
        return {comp[next(script)]}

    f = generic_mst(6, EXAMPLE, choose)
    assert f == [3, 8, 1, 2, 5]


def test_bad_cut_is_rejected():
    with pytest.raises(ValueError):
        generic_mst(3, [(0, 1, 1)], lambda comp, open_trees: {comp[2]})


def test_edge_cases():
    assert generic_mst(0, []) == []
    assert generic_mst(1, [(0, 0, 1)]) == []
    assert generic_mst(3, []) == []
    f = generic_mst(3, [(0, 1, 1), (1, 2, 1), (2, 0, 1)])
    assert len(f) == 2


def test_against_brute_force_with_random_cuts():
    rng = random.Random(211)
    for _ in range(600):
        n = rng.randrange(1, 7)
        m = rng.randrange(0, 9)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randrange(0, 3)) for _ in range(m)]

        def choose(comp, open_trees):
            # a random union of trees; fall back to one open tree if no edge crosses it
            s = {t for t in set(comp) if rng.random() < 0.5}
            if any((comp[u] in s) != (comp[v] in s) for u, v, _ in edges):
                return s
            return {rng.choice(open_trees)}

        f = generic_mst(n, edges, choose)
        assert is_forest(n, edges, f)
        assert components(n, edges, f) == components(n, edges, range(m))
        assert sum(edges[i][2] for i in f) == brute_force(n, edges)
