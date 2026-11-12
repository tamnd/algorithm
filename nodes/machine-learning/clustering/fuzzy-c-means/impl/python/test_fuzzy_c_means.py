# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fuzzy-c-means/. The authors are listed in prov/YQJKEX.jsonl.

import random
from fractions import Fraction

from fuzzy_c_means import centers, fuzzy_c_means, memberships, objective, sqdist


def frac_points(rng, n, d=2):
    return [[Fraction(rng.randint(0, 30)) for _ in range(d)] for _ in range(n)]


def test_objective_does_not_increase_exactly():
    rng = random.Random(1)
    # exact numbers grow fast, so the runs are short
    for _ in range(20):
        pts = frac_points(rng, rng.randint(3, 5), d=1)
        c = rng.randint(2, 3)
        trace = []
        fuzzy_c_means(pts, c, m=2, rng=rng, max_iter=2, trace=trace)
        assert all(b <= a for a, b in zip(trace, trace[1:]))


def test_objective_does_not_increase_for_other_m():
    rng = random.Random(2)
    for m in [1.2, 1.5, 3.0]:
        pts = [[rng.gauss(0, 1) + 4 * (i % 3), rng.gauss(0, 1)] for i in range(40)]
        trace = []
        fuzzy_c_means(pts, 3, m=m, rng=rng, max_iter=40, trace=trace)
        assert all(b <= a + 1e-9 * (1 + abs(a)) for a, b in zip(trace, trace[1:]))


def test_memberships_are_on_the_simplex_and_optimal():
    rng = random.Random(3)
    for m in [2, 1.5, 2.5]:
        pts = [[rng.uniform(0, 10), rng.uniform(0, 10)] for _ in range(10)]
        V = [[rng.uniform(0, 10), rng.uniform(0, 10)] for _ in range(3)]
        U = memberships(pts, V, m)
        for row in U:
            assert all(u >= 0 for u in row) and abs(sum(row) - 1) < 1e-12
        best = objective(pts, U, V, m)
        for _ in range(200):  # random memberships never do better
            R = []
            for _ in pts:
                w = [rng.random() for _ in V]
                R.append([a / sum(w) for a in w])
            assert objective(pts, R, V, m) >= best - 1e-9


def test_center_step_is_optimal():
    rng = random.Random(4)
    pts = frac_points(rng, 6)
    V0 = [[Fraction(3), Fraction(4)], [Fraction(20), Fraction(10)]]
    U = memberships(pts, V0, 2)
    V = centers(pts, U, 2, V0)
    base = objective(pts, U, V, 2)
    for j in range(2):
        for t in range(2):
            for h in [Fraction(1, 7), Fraction(-1, 7)]:
                W = [list(v) for v in V]
                W[j][t] += h
                assert objective(pts, U, W, 2) > base


def test_zero_distance():
    p = [[Fraction(0)], [Fraction(4)]]
    U = memberships(p, [[Fraction(0)], [Fraction(10)]], 2)
    assert U[0] == [1, 0]
    # two centers on the point share it
    U = memberships(p, [[Fraction(0)], [Fraction(0)], [Fraction(9)]], 2)
    assert U[0] == [Fraction(1, 2), Fraction(1, 2), 0]
    assert sum(U[1]) == 1


def test_example():
    pts = [[Fraction(x)] for x in [0, 1, 3, 9, 10]]
    U = memberships(pts, [[Fraction(0)], [Fraction(10)]], 2)
    assert U[1] == [Fraction(81, 82), Fraction(1, 82)]
    assert U[2] == [Fraction(49, 58), Fraction(9, 58)]
    U, V = fuzzy_c_means(pts, 2, m=2, init=[[Fraction(0)], [Fraction(10)]], max_iter=1)
    assert V == [[Fraction(5877871, 5069869)], [Fraction(106618373, 11309687)]]
    fl = [[float(x)] for x in [0, 1, 3, 9, 10]]
    U, V = fuzzy_c_means(fl, 2, m=2, init=[[0.0], [10.0]], eps=1e-12)
    assert abs(V[0][0] - 1.2751) < 1e-3 and abs(V[1][0] - 9.4844) < 1e-3
    assert abs(objective(fl, U, V, 2) - 4.9499) < 1e-3


def test_small_m_is_nearly_hard_and_large_m_is_nearly_uniform():
    pts = [[0.0], [1.0], [2.0], [10.0], [11.0], [12.0]]
    U, V = fuzzy_c_means(pts, 2, m=1.05, init=[[0.0], [12.0]])
    assert all(max(row) > 0.999 for row in U)
    # for fixed centers and large m, the memberships go to 1 / c
    U = memberships([[1.0], [3.0], [11.0]], [[0.0], [12.0]], 200.0)
    assert all(abs(row[0] - 0.5) < 0.02 for row in U)
