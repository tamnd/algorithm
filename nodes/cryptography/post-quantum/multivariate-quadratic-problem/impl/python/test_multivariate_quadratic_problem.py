# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multivariate-quadratic-problem/. The authors are listed in prov/3KTP1K.jsonl.
"""Tests for the MQ solvers. MQ has no official test vectors. The page
example is checked by hand; the solvers are checked against plain brute
force on random toy systems with fixed seeds."""

import itertools
import random

from multivariate_quadratic_problem import (
    BinarySystem,
    column_order,
    evaluate,
    exhaustive_search,
    fast_exhaustive_search,
    monomials,
    random_quadratic_system,
    xl_degree,
    xl_rows,
    xl_solve,
)

P31 = 31


def brute_binary(terms, n):
    """Independent oracle: each polynomial is a list of terms, each term a
    tuple of variable indices (the empty tuple is the constant 1)."""
    sols = []
    for x in range(1 << n):
        if all(sum(all((x >> j) & 1 for j in t) for t in poly) % 2 == 0 for poly in terms):
            sols.append(x)
    return sols


def pack(terms, n):
    """Build the packed system from the term lists."""
    quad, lin, const = {(j, l): 0 for j in range(n) for l in range(j + 1, n)}, [0] * n, 0
    for i, poly in enumerate(terms):
        for t in poly:
            vs = sorted(set(t))
            if not vs:
                const ^= 1 << i
            elif len(vs) == 1:
                lin[vs[0]] ^= 1 << i
            else:
                quad[(vs[0], vs[1])] ^= 1 << i
    return BinarySystem(n, len(terms), quad, lin, const)


def test_page_example_gf2():
    """x0 x1 + x2 + 1, x0 x2 + x1 + x0, x1 x2 + x0 + x2: the only solution,
    found by hand on the page, is (x0, x1, x2) = (1, 0, 1)."""
    terms = [[(0, 1), (2,), ()], [(0, 2), (1,), (0,)], [(1, 2), (0,), (2,)]]
    P = pack(terms, 3)
    assert fast_exhaustive_search(P) == [0b101]
    assert brute_binary(terms, 3) == [0b101]


def test_gray_code_search_against_brute_force():
    rng = random.Random(1)
    for _ in range(500):
        n, m = rng.randint(1, 7), rng.randint(1, 3)
        terms = []
        for _ in range(m):
            poly = [t for t in itertools.chain([()], [(j,) for j in range(n)],
                                               itertools.combinations(range(n), 2)) if rng.random() < 0.5]
            terms.append(poly)
        assert sorted(fast_exhaustive_search(pack(terms, n))) == brute_binary(terms, n)


def test_gray_code_search_planted_n16():
    rng = random.Random(2)
    x = rng.getrandbits(16)
    P = BinarySystem.random(16, 16, rng, planted=x)
    sols = fast_exhaustive_search(P)
    assert x in sols
    assert all(P.evaluate(s) == 0 for s in sols)


def test_xl_counts():
    """XL at degree D multiplies each of the m polynomials by the
    C(n + D - 2, D - 2) monomials of degree at most D - 2, and works on the
    C(n + D, D) monomials of degree at most D."""
    rng = random.Random(3)
    S = random_quadratic_system(3, 4, P31, rng)
    for D, rows, cols in [(2, 4, 10), (3, 16, 20), (4, 40, 35)]:
        assert len(xl_rows(S, 3, D, P31)) == rows
        assert len(column_order(3, D)) == len(monomials(3, D)) == cols


def test_linearization_n3_m9():
    """With 9 equations in 3 variables there are as many equations as
    nonconstant monomials, and plain linearization (D = 2) works."""
    rng = random.Random(4)
    for _ in range(5):
        s = tuple(rng.randrange(P31) for _ in range(3))
        S = random_quadratic_system(3, 9, P31, rng, planted=s)
        assert xl_degree(S, 3, P31) == 2
        assert xl_solve(S, 3, P31) == exhaustive_search(S, 3, P31) == [s]


def test_xl_against_brute_force_two_variables():
    rng = random.Random(5)
    for k in range(200):
        m = 2 + k % 2
        planted = tuple(rng.randrange(P31) for _ in range(2)) if k % 3 else None
        S = random_quadratic_system(2, m, P31, rng, planted=planted)
        assert sorted(xl_solve(S, 2, P31, max_degree=8)) == exhaustive_search(S, 2, P31)


def test_xl_overdetermined_planted():
    rng = random.Random(6)
    for n, m in [(3, 5), (4, 6), (4, 8), (5, 10)]:
        s = tuple(rng.randrange(P31) for _ in range(n))
        S = random_quadratic_system(n, m, P31, rng, planted=s)
        sols = xl_solve(S, n, P31)
        assert s in sols
        assert all(evaluate(f, x, P31) == 0 for f in S for x in sols)
