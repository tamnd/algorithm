# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/macaulay-matrix/. The authors are listed in prov/G8MNQA.jsonl.

import random
from fractions import Fraction
from math import comb

import pytest

from macaulay_matrix import MacaulayMatrix, monomials, order_key

ORDERS = ("lex", "grlex", "grevlex")


def independent_rank(rows):
    """Rank by row-by-row insertion into a list of reduced vectors."""
    basis = []  # pairs (pivot index, vector with 1 at the pivot)
    for r in rows:
        v = list(r)
        for j, b in basis:
            if v[j] != 0:
                c = v[j]
                v = [x - c * y for x, y in zip(v, b)]
        nz = next((j for j, x in enumerate(v) if x != 0), None)
        if nz is not None:
            inv = 1 / v[nz]
            basis.append((nz, [inv * x for x in v]))
    return len(basis)


def rand_hom(rng, n, d, size=5):
    return {m: Fraction(c) for m in monomials(n, d) if (c := rng.randint(-size, size)) != 0}


def series_coeff(degs, n, D):
    """Coefficient of t^D in prod (1 - t^d) / (1 - t)^n."""
    num = {0: 1}
    for d in degs:
        new = {}
        for e, c in num.items():
            new[e] = new.get(e, 0) + c
            new[e + d] = new.get(e + d, 0) - c
        num = new
    return sum(c * comb(D - e + n - 1, n - 1) for e, c in num.items() if e <= D)


def test_worked_example():
    F = [{(2, 0): 1, (0, 2): -1}, {(1, 1): 1}]  # x^2 - y^2, xy
    M = MacaulayMatrix(F, 2, 3, "grevlex", homogeneous=True)
    assert M.columns == [(3, 0), (2, 1), (1, 2), (0, 3)]
    assert M.rows == [[1, 0, -1, 0], [0, 1, 0, -1], [0, 1, 0, 0], [0, 0, 1, 0]]
    M.reduce_to_echelon()
    assert M.leading_monomials() == [(3, 0), (2, 1), (1, 2), (0, 3)]
    assert M.member({(0, 3): 1})  # y^3 is in the ideal: a new leading monomial
    M2 = MacaulayMatrix(F, 2, 2, "grevlex", homogeneous=True)
    M2.reduce_to_echelon()
    assert M2.rank() == 2 and not M2.member({(0, 2): 1})


def test_regular_sequences_hilbert_function():
    rng = random.Random(1902)
    for trial in range(500):
        n = rng.choice((2, 3))
        s = rng.randint(1, n)
        degs = [rng.randint(1, 2) for _ in range(s)]
        F = [rand_hom(rng, n, d, 10 ** 6) for d in degs]
        if any(not f for f in F):
            continue
        D = rng.randint(1, 4)
        M = MacaulayMatrix(F, n, D, ORDERS[trial % 3], homogeneous=True)
        M.reduce_to_echelon()
        assert len(M.columns) - M.rank() == series_coeff(degs, n, D)
        assert M.rank() == independent_rank(M.rows)


def test_row_space_and_leading_monomials():
    rng = random.Random(83)
    for trial in range(500):
        n = rng.choice((2, 3))
        order = ORDERS[trial % 3]
        F = []
        for _ in range(rng.randint(1, 3)):
            f = {}
            for _ in range(rng.randint(1, 4)):
                e = tuple(rng.randint(0, 2) for _ in range(n))
                if sum(e) <= 2:
                    f[e] = Fraction(rng.randint(-3, 3))
            F.append({a: c for a, c in f.items() if c != 0})
        D = rng.randint(0, 3)
        M = MacaulayMatrix(F, n, D, order)
        M.reduce_to_echelon()
        assert M.rank() == independent_rank(M.rows)
        assert independent_rank(M.rows + M.echelon) == M.rank()
        if not M.rows:
            continue
        coeffs = [Fraction(rng.randint(-2, 2)) for _ in M.rows]
        v = [sum(c * r[j] for c, r in zip(coeffs, M.rows)) for j in range(len(M.columns))]
        g = {M.columns[j]: x for j, x in enumerate(v) if x != 0}
        assert M.member(g)
        if g:
            lm = max(g, key=order_key(order))
            assert lm in M.leading_monomials()
        pivots = set(M.pivots)
        for j, m in enumerate(M.columns):
            if j not in pivots:
                assert not M.member({m: 1})


def test_homogeneous_multiples_are_members():
    rng = random.Random(7)
    F = [rand_hom(rng, 3, 2), rand_hom(rng, 3, 3)]
    M = MacaulayMatrix(F, 3, 5, "grevlex", homogeneous=True)
    M.reduce_to_echelon()
    for _ in range(50):
        i = rng.randint(0, 1)
        h = rand_hom(rng, 3, 5 - (2 if i == 0 else 3), 3)
        g = {}
        for a, c in h.items():
            for b, e in F[i].items():
                k = tuple(x + y for x, y in zip(a, b))
                g[k] = g.get(k, 0) + c * e
        assert M.member({k: c for k, c in g.items() if c != 0})


def test_affine_zero_dimensional():
    F = [{(2, 0): 1, (0, 2): 1, (0, 0): -1}, {(1, 0): 1, (0, 1): -1}]  # circle and line
    for D in range(2, 7):
        M = MacaulayMatrix(F, 2, D, "grevlex")
        M.reduce_to_echelon()
        assert len(M.columns) - M.rank() == 2  # two intersection points


def test_edge_cases():
    M = MacaulayMatrix([{(0, 0): 3}], 2, 3, "lex")  # the unit ideal
    M.reduce_to_echelon()
    assert M.rank() == comb(5, 2) == len(M.columns)
    f = {(1, 1): 1, (0, 0): 2}
    M = MacaulayMatrix([f], 2, 4, "grlex")  # single generator: no syzygies
    M.reduce_to_echelon()
    assert M.rank() == len(M.rows) == comb(4, 2)
    M = MacaulayMatrix([{}, {(2, 0): 1}], 2, 1)  # zero polynomial and D < deg f
    M.reduce_to_echelon()
    assert M.rows == [] and M.rank() == 0
    with pytest.raises(ValueError):
        MacaulayMatrix([{(1, 0): 1, (0, 0): 1}], 2, 2, homogeneous=True)
