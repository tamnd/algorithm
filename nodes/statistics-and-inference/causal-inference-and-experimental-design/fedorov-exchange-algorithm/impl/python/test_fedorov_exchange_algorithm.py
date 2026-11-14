# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fedorov-exchange-algorithm/. The authors are listed in prov/75MV1N.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from fedorov_exchange_algorithm import (
    delta, determinant, dot, fedorov_exchange, info_matrix, inverse, mat_vec,
    polynomial_row, quadratic_surface_row,
)

GRID = [Fraction(k, 4) for k in range(-4, 5)]
QUAD = [polynomial_row(x, 2) for x in GRID]
SQUARE = [(Fraction(a), Fraction(b)) for a in (-1, 0, 1) for b in (-1, 0, 1)]
SURFACE = [quadratic_surface_row(*p) for p in SQUARE]


def brute_force_max_det(cands, n):
    return max(determinant(info_matrix([cands[j] for j in d]))
               for d in itertools.combinations_with_replacement(range(len(cands)), n))


def random_start(rng, cands, n):
    while True:
        s = [rng.randrange(len(cands)) for _ in range(n)]
        if determinant(info_matrix([cands[j] for j in s])) != 0:
            return s


def test_worked_example():
    start = [GRID.index(Fraction(-1, 2)), GRID.index(0), GRID.index(Fraction(1, 2))]
    res = fedorov_exchange(QUAD, start)
    assert sorted(GRID[j] for j in res.design) == [-1, 0, 1]
    assert res.det == 4
    assert [e[3] for e in res.exchanges] == [8, Fraction(55, 9)]


def test_quadratic_three_runs_find_minus_one_zero_one():
    assert brute_force_max_det(QUAD, 3) == 4
    rng = random.Random(1)
    for _ in range(3):
        res = fedorov_exchange(QUAD, random_start(rng, QUAD, 3))
        assert sorted(GRID[j] for j in res.design) == [-1, 0, 1]
        assert res.det == 4


def test_determinant_ratio_formula_exact():
    rng = random.Random(7)
    for _ in range(200):
        cands = SURFACE if rng.random() < 0.5 else QUAD
        n = len(cands[0]) + rng.randrange(3)
        s = random_start(rng, cands, n)
        m = info_matrix([cands[j] for j in s])
        a = inverse(m)
        i, j = rng.randrange(n), rng.randrange(len(cands))
        t = list(s)
        t[i] = j
        m2 = info_matrix([cands[k] for k in t])
        assert determinant(m2) == determinant(m) * (1 + delta(a, cands[s[i]], cands[j]))


def test_each_exchange_raises_determinant():
    rng = random.Random(3)
    for _ in range(20):
        s = random_start(rng, SURFACE, 8)
        d0 = determinant(info_matrix([SURFACE[j] for j in s]))
        res = fedorov_exchange(SURFACE, s)
        prod = Fraction(1)
        for _, _, _, dl in res.exchanges:
            assert dl > 0
            prod *= 1 + dl
        assert res.det == d0 * prod


def test_stops_at_one_exchange_optimum():
    rng = random.Random(5)
    s = random_start(rng, SURFACE, 7)
    res = fedorov_exchange(SURFACE, s)
    d = res.det
    for i in range(len(res.design)):
        for j in range(len(SURFACE)):
            t = list(res.design)
            t[i] = j
            assert determinant(info_matrix([SURFACE[k] for k in t])) <= d


def test_second_order_surface_against_brute_force():
    best = brute_force_max_det(SURFACE, 6)
    assert best == 256
    rng = random.Random(20261114)
    found = [fedorov_exchange(SURFACE, random_start(rng, SURFACE, 6)).det for _ in range(10)]
    assert max(found) == best
    assert all(f <= best for f in found)


def test_equivalence_theorem_at_the_optimum():
    res = fedorov_exchange(QUAD, [0, 1, 2])
    m = info_matrix([QUAD[j] for j in res.design])
    a = inverse(m)
    n = len(res.design)
    dn = [n * dot(f, mat_vec(a, f)) for f in QUAD]
    assert max(dn) == 3
    assert {GRID[j] for j, v in enumerate(dn) if v == 3} == {-1, 0, 1}


def test_floating_point_with_threshold():
    grid = [k / 10 for k in range(-10, 11)]
    cands = [polynomial_row(x, 3) for x in grid]
    start = [grid.index(v) for v in (-0.5, -0.2, 0.3, 0.6)]
    res = fedorov_exchange(cands, start, eps=1e-9)
    pts = sorted(grid[j] for j in res.design)
    exact = brute_force_max_det(cands, 4)
    assert res.det == pytest.approx(exact, rel=1e-9)
    assert pts[0] == -1.0 and pts[-1] == 1.0


def test_singular_start_rejected():
    with pytest.raises(ValueError):
        fedorov_exchange(QUAD, [0, 0, 1])
