# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/primal-dual-weighted-vertex-cover/. The authors are listed in prov/7D7Y44.jsonl.

import random
from fractions import Fraction
from itertools import combinations

import pytest

from primal_dual_weighted_vertex_cover import primal_dual_weighted_vertex_cover


def brute_opt(weights, edges):
    vs = list(weights)
    best = None
    for r in range(len(vs) + 1):
        for c in combinations(vs, r):
            s = set(c)
            if all(u in s or v in s for u, v in edges):
                val = sum(weights[x] for x in c)
                if best is None or val < best:
                    best = val
    return best


def solve_square(a, b):
    k = len(a)
    m = [[Fraction(x) for x in row] + [Fraction(y)] for row, y in zip(a, b)]
    for c in range(k):
        p = next((r for r in range(c, k) if m[r][c] != 0), None)
        if p is None:
            return None
        m[c], m[p] = m[p], m[c]
        for r in range(k):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [m[r][t] - f * m[c][t] for t in range(k + 1)]
    return [m[i][k] / m[i][i] for i in range(k)]


def lp_value(weights, edges):
    """min w.x subject to x_u + x_v >= 1 on each edge, x >= 0. Vertex enumeration; tiny graphs only."""
    vs = list(weights)
    n = len(vs)
    rows = [([1 if x in e else 0 for x in vs], 1) for e in edges]
    rows += [([1 if x == v else 0 for x in vs], 0) for v in vs]
    best = None
    for pick in combinations(range(len(rows)), n):
        x = solve_square([rows[i][0] for i in pick], [rows[i][1] for i in pick])
        if x is None:
            continue
        if all(sum(a * t for a, t in zip(r, x)) >= rhs for r, rhs in rows):
            val = sum(Fraction(weights[v]) * t for v, t in zip(vs, x))
            if best is None or val < best:
                best = val
    return best


def check(weights, edges):
    cover, y = primal_dual_weighted_vertex_cover(weights, edges)
    assert all(u in cover or v in cover for u, v in edges)
    for v in weights:  # dual feasibility, and each cover vertex is tight
        load = sum(val for e, val in y.items() if v in e)
        assert load <= weights[v]
        if v in cover:
            assert load == weights[v]
    alg = sum(weights[v] for v in cover)
    assert alg <= 2 * sum(y.values())
    return cover, y, alg


def test_example_page():
    edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5), (4, 6), (5, 7), (6, 7)]
    w = {1: 4, 2: 3, 3: 5, 4: 2, 5: 6, 6: 3, 7: 2}
    cover, y, alg = check(w, edges)
    assert cover == {1, 2, 3, 4, 5, 7}
    assert alg == 22
    assert sum(y.values()) == 12
    assert [y[e] for e in edges] == [3, 1, 0, 0, 4, 2, 0, 0, 2]
    assert brute_opt(w, edges) == 12
    assert lp_value(w, edges) == 12


def test_random_against_brute_force_and_lp():
    rng = random.Random(1981)
    for trial in range(120):
        n = rng.randint(2, 6)
        edges = [e for e in combinations(range(n), 2) if rng.random() < 0.5]
        rng.shuffle(edges)
        w = {v: rng.randint(0, 7) for v in range(n)}
        cover, y, alg = check(w, edges)
        opt = brute_opt(w, edges)
        assert alg <= 2 * opt
        if n <= 5:
            lp = lp_value(w, edges)
            assert sum(y.values()) <= lp <= opt
            assert alg <= 2 * lp
            assert 2 * lp == int(2 * lp)  # half-integral optimum


def test_tight_complete_bipartite_unit_weights():
    for k in range(1, 6):
        w = {("a", i): 1 for i in range(k)} | {("b", i): 1 for i in range(k)}
        edges = [(("a", i), ("b", j)) for i in range(k) for j in range(k)]
        cover, y, alg = check(w, edges)
        assert alg == 2 * k
        if k <= 4:
            assert brute_opt(w, edges) == k


def test_star_heavy_center():
    # center of weight 10, five leaves of weight 1: the leaves become tight first
    w = {0: 10} | {i: 1 for i in range(1, 6)}
    edges = [(0, i) for i in range(1, 6)]
    cover, y, alg = check(w, edges)
    assert cover == {1, 2, 3, 4, 5} and alg == 5 == brute_opt(w, edges)


def test_bad_input():
    with pytest.raises(ValueError):
        primal_dual_weighted_vertex_cover({1: 1}, [(1, 1)])
    with pytest.raises(ValueError):
        primal_dual_weighted_vertex_cover({1: -1, 2: 1}, [(1, 2)])
