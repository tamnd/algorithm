# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/petkovsek-hyper-algorithm/. The authors are listed in prov/M8QSZ7.jsonl.
import random
from fractions import Fraction

import pytest

from petkovsek_hyper_algorithm import (evaluate, hyper, is_solution_ratio, op_mul, polynomial_solutions,
                             shift, trim, mul, rational_roots)


def P(*cs):
    return trim([Fraction(c) for c in cs])


def lin_product(roots):
    f = P(1)
    for k in roots:
        f = mul(f, P(-k, 1))
    return f


def integer_roots(polys):
    out = [0]
    for p in polys:
        if len(p) > 1:
            out += [int(x) for x in rational_roots(p) if x.denominator == 1]
    return out


def sequence(num, den, n0, length):
    t, out = Fraction(1), []
    for n in range(n0, n0 + length):
        out.append(t)
        t = t * evaluate(num, n) / evaluate(den, n)
    return out


def rank(rows):
    rows = [list(r) for r in rows]
    rk, ncols = 0, len(rows[0]) if rows else 0
    for c in range(ncols):
        piv = next((i for i in range(rk, len(rows)) if rows[i][c] != 0), None)
        if piv is None:
            continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        for i in range(rk + 1, len(rows)):
            f = rows[i][c] / rows[rk][c]
            rows[i] = [a - f * b for a, b in zip(rows[i], rows[rk])]
        rk += 1
    return rk


def in_span(L, ratios, target):
    """Is the hypergeometric term with ratio target a combination of the returned ones?"""
    polys = [p for pair in ratios + [target] for p in pair] + [shift(L[-1], -(len(L) - 2))]
    n0 = max(integer_roots(polys)) + 1
    W = len(ratios) + 4
    rows = [sequence(n, d, n0, W) for n, d in ratios]
    t = sequence(target[0], target[1], n0, W)
    return rank(rows + [t]) == rank(rows) if rows else False


def test_worked_example():
    L = [P(0, 2, 2), P(2, -3, -1), P(-1, 1)]  # (n-1) S^2 - (n^2+3n-2) S + 2n(n+1)
    trace = []
    out = hyper(L, trace)
    assert sorted(out) == sorted([(P(2), P(1)), (P(1, 1), P(1))])
    assert len(trace) == 8
    accepted = [(a, b, Z) for a, b, Z, C in trace if C]
    assert accepted == [((1,), (1,), 2), ((0, 1), (1,), 1), ((1, 1), (1,), 1)]
    # 2^n and n! solve it
    for n in range(0, 12):
        f = [Fraction(2) ** k for k in range(n, n + 3)]
        assert sum(evaluate(L[i], n) * f[i] for i in range(3)) == 0
        fac = [Fraction(1)]
        for k in range(1, n + 3):
            fac.append(fac[-1] * k)
        assert sum(evaluate(L[i], n) * fac[n + i] for i in range(3)) == 0


def test_constant_coefficients_and_edges():
    assert sorted(hyper([P(-1), P(0), P(1)])) == sorted([(P(1), P(1)), (P(-1), P(1))])
    out = hyper([P(1), P(-2), P(1)])  # (S - 1)^2: 1 and n
    assert sorted(out) == sorted([(P(1), P(1)), (P(1, 1), P(0, 1))])
    assert hyper([P(-1), P(-1), P(1)]) == []  # Fibonacci: roots are irrational
    assert hyper([P(-1, -1), P(1)]) == [(P(1, 1), P(1))]  # n!
    assert hyper([P(-1), P(1)]) == [(P(1), P(1))]
    with pytest.raises(ValueError):
        hyper([P(), P(1)])
    with pytest.raises(ValueError):
        hyper([P(1)])
    with pytest.raises(ValueError):
        hyper([P(1, 0, 1), P(1)])  # n^2 + 1 does not split over Q
    # polynomial solutions alone: c(n+1) - c(n) = 0 has only constants
    assert polynomial_solutions([P(-1), P(1)]) == [P(1)]
    assert polynomial_solutions([P(-1), P(2)]) == []


def random_split(rng, k, lo=-3, hi=3):
    return [rng.randint(lo, hi) for _ in range(k)]


def test_planted_solutions_found():
    rng = random.Random(1992)
    for _ in range(500):
        Z = Fraction(rng.choice([1, -1, 2, -2, 3]), rng.choice([1, 1, 2]))
        u = lin_product(random_split(rng, rng.randint(0, 2)))
        v = lin_product(random_split(rng, rng.randint(0, 2)))
        F = [scale_neg(mul(P(Z), u)), v]
        order = rng.choice([0, 1, 1, 2])
        if order == 0:
            M = [scale_c(lin_product(random_split(rng, rng.randint(0, 1))), rng.randint(1, 3))]
        else:
            M = [scale_c(lin_product(random_split(rng, rng.randint(0, 1))), rng.choice([1, -1, 2]))]
            for _ in range(order - 1):
                M.append(P(*[rng.randint(-3, 3) for _ in range(rng.randint(0, 2))]))
            M.append(scale_c(lin_product(random_split(rng, rng.randint(0, 1))), rng.choice([1, -2, 3])))
        L = op_mul(M, F)
        target = (mul(P(Z), u), v)
        assert is_solution_ratio(L, *target)
        out = hyper(L)
        for num, den in out:
            assert is_solution_ratio(L, num, den)
        assert in_span(L, out, target)


def scale_neg(p):
    return [-c for c in p]


def scale_c(p, c):
    return [c * a for a in p]


def test_against_brute_force_search():
    rng = random.Random(777)
    cands = [P(1)] + [P(-k, 1) for k in range(-2, 3)]
    for _ in range(25):
        F1 = [scale_neg(mul(P(rng.choice([1, 2, -1])), lin_product(random_split(rng, 1, -2, 2)))), P(1)]
        F2 = [scale_neg(P(rng.choice([1, 2, -2]))), lin_product(random_split(rng, rng.randint(0, 1), -2, 2))]
        L = op_mul(F2, F1)
        out = hyper(L)
        for num, den in out:
            assert is_solution_ratio(L, num, den)
        for Z in (1, -1, 2, -2):
            for a in cands:
                for b in cands:
                    if is_solution_ratio(L, mul(P(Z), a), b):
                        assert in_span(L, out, (mul(P(Z), a), b))
