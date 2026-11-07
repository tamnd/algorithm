# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ben-or-tiwari-algorithm/. The authors are listed in prov/RHYB1V.jsonl.

import random
from fractions import Fraction

from ben_or_tiwari_algorithm import ben_or_tiwari, berlekamp_massey, integer_roots


def evaluate(poly, point):
    total = Fraction(0)
    for e, c in poly.items():
        v = Fraction(c)
        for xi, ei in zip(point, e):
            v *= Fraction(xi) ** ei
        total += v
    return total


def black_box(poly, counter=None):
    def f(point):
        if counter is not None:
            counter.append(point)
        return evaluate(poly, point)
    return f


def random_sparse(rng, n, t, d):
    poly = {}
    while len(poly) < t:
        e = tuple(rng.randint(0, d) for _ in range(n))
        c = Fraction(rng.randint(-20, 20), rng.randint(1, 6))
        if c:
            poly[e] = c
    return poly


def test_worked_example():
    # f = 3 x^2 y - 2 y^3 + 5, T = 3
    poly = {(2, 1): Fraction(3), (0, 3): Fraction(-2), (0, 0): Fraction(5)}
    calls = []
    out = ben_or_tiwari(black_box(poly, calls), 2, 3)
    assert out == poly
    assert calls == [(1, 1), (2, 3), (4, 9), (8, 27), (16, 81), (32, 243)]


def test_worked_example_values():
    poly = {(2, 1): Fraction(3), (0, 3): Fraction(-2), (0, 0): Fraction(5)}
    a = [evaluate(poly, (2 ** i, 3 ** i)) for i in range(6)]
    assert a == [6, -13, -1021, -34177, -1000669, -27951313]
    C = berlekamp_massey(a)
    # Lambda(z) = (z - 12)(z - 27)(z - 1)
    assert [C[3 - i] for i in range(4)] == [-324, 363, -40, 1]


def test_edge_cases():
    assert ben_or_tiwari(black_box({}), 2, 3) == {}
    assert ben_or_tiwari(black_box({(0, 0): Fraction(7)}), 2, 1) == {(0, 0): 7}
    assert ben_or_tiwari(black_box({(0, 0, 0): Fraction(-1, 3)}), 3, 4) == {(0, 0, 0): Fraction(-1, 3)}
    assert ben_or_tiwari(black_box({(5,): Fraction(2)}), 1, 1) == {(5,): 2}
    assert ben_or_tiwari(black_box({}), 1, 1) == {}
    one = {(0, 9, 0, 1): Fraction(4, 7)}
    assert ben_or_tiwari(black_box(one), 4, 1) == one


def test_univariate_dense():
    poly = {(k,): Fraction(k + 1) for k in range(8)}
    assert ben_or_tiwari(black_box(poly), 1, 8) == poly


def test_integer_roots():
    rng = random.Random(7)
    for _ in range(200):
        t = rng.randint(1, 6)
        roots = rng.sample(range(-500, 500), t)
        P = [1]
        for r in roots:
            Q = [0] * (len(P) + 1)
            for i, c in enumerate(P):
                Q[i + 1] += c
                Q[i] -= r * c
            P = Q
        assert integer_roots(P) == sorted(roots)


def test_random_exact_bound():
    rng = random.Random(2024)
    for trial in range(400):
        n = rng.randint(1, 3)
        d = rng.randint(0, 5)
        t = rng.randint(0, min(6, (d + 1) ** n))
        poly = random_sparse(rng, n, t, d)
        calls = []
        out = ben_or_tiwari(black_box(poly, calls), n, t)
        assert out == poly
        assert len(calls) == 2 * t


def test_random_loose_bound():
    rng = random.Random(99)
    for trial in range(200):
        n = rng.randint(1, 4)
        d = rng.randint(0, 4)
        t = rng.randint(0, min(5, (d + 1) ** n))
        T = t + rng.randint(0, 4)
        poly = random_sparse(rng, n, t, d)
        out = ben_or_tiwari(black_box(poly), n, T)
        assert out == poly
        # the defining property: agreement at random points
        for _ in range(3):
            pt = tuple(rng.randint(-50, 50) for _ in range(n))
            assert evaluate(out, pt) == evaluate(poly, pt)


def test_high_degree_sparse():
    rng = random.Random(5)
    for _ in range(20):
        n = 3
        poly = random_sparse(rng, n, 4, 30)
        assert ben_or_tiwari(black_box(poly), n, 4) == poly
