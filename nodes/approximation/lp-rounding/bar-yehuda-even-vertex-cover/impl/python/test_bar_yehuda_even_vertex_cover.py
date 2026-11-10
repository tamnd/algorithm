# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bar-yehuda-even-vertex-cover/. The authors are listed in prov/V1VWVP.jsonl.

import random
from fractions import Fraction

import pytest

from bar_yehuda_even_vertex_cover import bar_yehuda_even_vertex_cover


def brute_opt(weights, edges):
    n = len(weights)
    best = None
    for mask in range(1 << n):
        if all(mask >> u & 1 or mask >> v & 1 for u, v in edges):
            c = sum(weights[i] for i in range(n) if mask >> i & 1)
            if best is None or c < best:
                best = c
    return best


def is_cover(edges, cover):
    return all(u in cover or v in cover for u, v in edges)


def test_example():
    # the page uses vertices 1..5; here they are 0..4
    w = [3, 5, 2, 4, 6]
    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4)]
    cover, eps, r = bar_yehuda_even_vertex_cover(w, edges)
    assert eps == [3, 0, 2, 0, 0, 4]
    assert r == [0, 0, 0, 0, 2]
    assert cover == {0, 1, 2, 3}
    assert sum(w[v] for v in cover) == 14
    assert brute_opt(w, edges) == 9 == sum(eps)
    # dropping the redundant vertex 1 (vertex 2 on the page) gives the optimum
    assert is_cover(edges, cover - {1})


def test_edge_cases():
    assert bar_yehuda_even_vertex_cover([], []) == (set(), [], [])
    # isolated vertices of weight 0 enter C; this is harmless
    assert bar_yehuda_even_vertex_cover([0, 3], []) == ({0}, [], [0, 3])
    with pytest.raises(ValueError):
        bar_yehuda_even_vertex_cover([1], [(0, 0)])
    with pytest.raises(ValueError):
        bar_yehuda_even_vertex_cover([-1, 1], [(0, 1)])


def test_tight_single_edge_and_star():
    cover, eps, r = bar_yehuda_even_vertex_cover([1, 1], [(0, 1)])
    assert cover == {0, 1} and brute_opt([1, 1], [(0, 1)]) == 1
    # a star with the centre scanned first in a heavy edge: the ratio stays at most 2
    w = [5, 5, 1, 1, 1]
    edges = [(0, 1), (0, 2), (0, 3), (0, 4)]
    cover, eps, r = bar_yehuda_even_vertex_cover(w, edges)
    assert cover == {0, 1} and brute_opt(w, edges) == 5


def test_fractions():
    w = [Fraction(1, 2), Fraction(1, 3), Fraction(1, 4)]
    edges = [(0, 1), (1, 2), (0, 2)]
    cover, eps, r = bar_yehuda_even_vertex_cover(w, edges)
    assert is_cover(edges, cover)
    assert sum(w[v] for v in cover) <= 2 * brute_opt(w, edges)


def test_random_against_brute_force():
    rng = random.Random(1981)
    for _ in range(600):
        n = rng.randint(1, 8)
        edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.4]
        rng.shuffle(edges)
        edges = [(v, u) if rng.random() < 0.5 else (u, v) for u, v in edges]
        w = [rng.randint(0, 9) for _ in range(n)]
        cover, eps, r = bar_yehuda_even_vertex_cover(w, edges)
        opt = brute_opt(w, edges)
        alg = sum(w[v] for v in cover)
        assert is_cover(edges, cover)
        assert all(x >= 0 for x in r)
        # eps is a feasible dual: the load on each vertex is w(v) - r(v) <= w(v)
        for v in range(n):
            assert sum(e for (a, b), e in zip(edges, eps) if v in (a, b)) == w[v] - r[v]
        assert sum(eps) <= opt <= alg <= 2 * sum(eps)
