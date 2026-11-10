# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lp-rounding-vertex-cover/. The authors are listed in prov/SNS1K9.jsonl.

import random
from fractions import Fraction
from itertools import combinations

import pytest

from lp_rounding_vertex_cover import lp_rounding_vertex_cover, solve_vertex_cover_lp

HALF = Fraction(1, 2)


def brute_opt(weights, edges):
    n = len(weights)
    best = None
    for mask in range(1 << n):
        if all(mask >> u & 1 or mask >> v & 1 for u, v in edges):
            c = sum(weights[i] for i in range(n) if mask >> i & 1)
            if best is None or c < best:
                best = c
    return best


def solve_square(rows, rhs):
    k = len(rows)
    m = [[Fraction(x) for x in r] + [Fraction(y)] for r, y in zip(rows, rhs)]
    for c in range(k):
        p = next((r for r in range(c, k) if m[r][c] != 0), None)
        if p is None:
            return None
        m[c], m[p] = m[p], m[c]
        for r in range(k):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [a - f * b for a, b in zip(m[r], m[c])]
    return [m[i][-1] / m[i][i] for i in range(k)]


def all_vertices(n, edges):
    """Every vertex of {x >= 0 : x_u + x_v >= 1}, by enumeration of tight sets."""
    g = [[1 if j in e else 0 for j in range(n)] for e in edges]
    g += [[1 if j == i else 0 for j in range(n)] for i in range(n)]
    h = [1] * len(edges) + [0] * n
    out = set()
    for s in combinations(range(len(g)), n):
        x = solve_square([g[i] for i in s], [h[i] for i in s])
        if x is not None and all(sum(a * b for a, b in zip(g[i], x)) >= h[i] for i in range(len(g))):
            out.add(tuple(x))
    return out


def is_cover(c, edges):
    return all(u in c or v in c for u, v in edges)


def test_example():
    edges = [(0, 2), (0, 3), (1, 3), (1, 4), (2, 3), (3, 5), (4, 5)]
    w = [4, 1, 6, 6, 8, 3]
    cover, x, lp = lp_rounding_vertex_cover(w, edges)
    assert lp == 12
    assert brute_opt(w, edges) == 14
    assert is_cover(cover, edges)
    assert sum(w[v] for v in cover) <= 2 * lp
    assert all(v in (0, HALF, 1) for v in x)


def test_edges_cases():
    assert lp_rounding_vertex_cover([], []) == (set(), [], 0)
    assert lp_rounding_vertex_cover([5], []) == (set(), [0], 0)
    cover, x, lp = lp_rounding_vertex_cover([2, 3], [(0, 1)])
    assert lp == 2 and cover == {0}
    with pytest.raises(ValueError):
        lp_rounding_vertex_cover([1, -1], [(0, 1)])
    with pytest.raises(ValueError):
        lp_rounding_vertex_cover([1], [(0, 0)])


def test_zero_weights():
    cover, x, lp = lp_rounding_vertex_cover([0, 0, 0], [(0, 1), (1, 2), (0, 2)])
    assert lp == 0 and is_cover(cover, [(0, 1), (1, 2), (0, 2)])


def test_odd_cycle_tight():
    for k in range(1, 5):
        n = 2 * k + 1
        edges = [(i, (i + 1) % n) for i in range(n)]
        cover, x, lp = lp_rounding_vertex_cover([1] * n, edges)
        assert x == [HALF] * n and lp == Fraction(n, 2)
        assert len(cover) == n and brute_opt([1] * n, edges) == k + 1


def test_complete_graph_gap():
    for n in range(2, 7):
        edges = list(combinations(range(n), 2))
        lp, _ = solve_vertex_cover_lp([1] * n, edges)
        assert lp == (1 if n == 2 else Fraction(n, 2))
        assert brute_opt([1] * n, edges) == n - 1


def test_random_against_brute_force():
    rng = random.Random(2024)
    for _ in range(500):
        n = rng.randint(1, 6)
        p = rng.random()
        edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]
        w = [rng.randint(0, 9) for _ in range(n)]
        cover, x, lp = lp_rounding_vertex_cover(w, edges)
        opt = brute_opt(w, edges)
        alg = sum(w[v] for v in cover)
        assert is_cover(cover, edges)
        assert all(xu + xv >= 1 for xu, xv in ((x[u], x[v]) for u, v in edges))
        assert lp <= opt <= alg <= 2 * lp
        assert all(v in (0, HALF, 1) for v in x)


def test_every_vertex_is_half_integral():
    rng = random.Random(7)
    for _ in range(40):
        n = rng.randint(2, 5)
        edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.6]
        if not edges:
            continue
        verts = all_vertices(n, edges)
        assert verts
        assert all(v in (0, HALF, 1) for p in verts for v in p)
        w = [rng.randint(1, 9) for _ in range(n)]
        lp, x = solve_vertex_cover_lp(w, edges)
        assert tuple(x) in verts
        assert lp == min(sum(a * b for a, b in zip(w, p)) for p in verts)
