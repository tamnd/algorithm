# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-linear-method/. The authors are listed in prov/XKTFZV.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

import sparse_linear_method as slim

KKT_TOL = 1e-9
REF_TOL = 1e-9


def random_matrix(m: int, n: int, density: float, seed: int) -> list[list[float]]:
    rng = random.Random(seed)
    return [[1.0 if rng.random() < density else 0.0 for _ in range(n)] for _ in range(m)]


def exact_solve(a, b):
    n = len(a)
    m = [row[:] + [y] for row, y in zip(a, b)]
    for c in range(n):
        piv = next(k for k in range(c, n) if m[k][c] != 0)
        m[c], m[piv] = m[piv], m[c]
        for k in range(n):
            if k != c and m[k][c] != 0:
                f = m[k][c] / m[c][c]
                m[k] = [x - f * y for x, y in zip(m[k], m[c])]
    return [m[k][n] / m[k][k] for k in range(n)]


def brute_force_column(a, j, beta, lam):
    """The exact minimizer by trying every support, in rational arithmetic.

    On a support S the minimizer solves (A_S^T A_S + beta I) w_S = A_S^T a_j - lam 1.
    It is the answer if w_S > 0 and the KKT inequality holds off S.
    """
    m, n = len(a), len(a[0])
    A = [[Fraction(x) for x in row] for row in a]
    beta, lam = Fraction(beta), Fraction(lam)
    others = [k for k in range(n) if k != j]
    found = []
    for size in range(len(others) + 1):
        for supp in itertools.combinations(others, size):
            w = [Fraction(0)] * n
            if supp:
                g = [[sum(A[u][p] * A[u][q] for u in range(m)) + (beta if p == q else 0) for q in supp] for p in supp]
                rhs = [sum(A[u][p] * A[u][j] for u in range(m)) - lam for p in supp]
                sol = exact_solve(g, rhs)
                if any(v <= 0 for v in sol):
                    continue
                for p, v in zip(supp, sol):
                    w[p] = v
            e = [A[u][j] - sum(A[u][k] * w[k] for k in range(n)) for u in range(m)]
            ok = all(-sum(A[u][k] * e[u] for u in range(m)) + lam >= 0 for k in others if k not in supp)
            if ok:
                found.append(w)
    assert len(found) == 1
    return [float(v) for v in found[0]]


def test_kkt_conditions_hold_at_the_solution():
    for seed in range(6):
        a = random_matrix(12, 7, 0.4, seed)
        for beta, lam in ((0.5, 0.1), (1.0, 1.0), (0.1, 0.0), (2.0, 3.0)):
            for j in range(7):
                w = slim.slim_column(a, j, beta, lam)
                assert slim.kkt_violation(a, j, w, beta, lam) <= KKT_TOL


def test_matches_brute_force_over_supports():
    for seed in range(4):
        a = random_matrix(10, 6, 0.45, 100 + seed)
        for beta, lam in ((0.5, 0.2), (1.0, 1.5)):
            for j in range(6):
                w = slim.slim_column(a, j, beta, lam)
                ref = brute_force_column(a, j, beta, lam)
                for x, y in zip(w, ref):
                    assert abs(x - y) <= REF_TOL


def test_nonnegative_zero_diagonal_and_sparse():
    a = random_matrix(15, 8, 0.35, 42)
    w = slim.slim(a, 0.5, 0.5)
    for k in range(8):
        assert w[k][k] == 0.0
        for i in range(8):
            assert w[k][i] >= 0.0
    big = slim.slim(a, 0.5, 50.0)
    assert all(v == 0.0 for row in big for v in row)


def test_coordinate_steps_do_not_increase_the_objective():
    a = random_matrix(10, 6, 0.4, 8)
    beta, lam = 0.3, 0.2
    for j in range(6):
        prev = slim.column_objective(a, j, [0.0] * 6, beta, lam)
        for sweeps in range(1, 6):
            w = slim.slim_column(a, j, beta, lam, tol=-1.0, max_sweeps=sweeps)
            cur = slim.column_objective(a, j, w, beta, lam)
            assert cur <= prev + 1e-12
            prev = cur


def test_page_example():
    a = [
        [1.0, 1.0, 0.0, 0.0],
        [1.0, 1.0, 1.0, 0.0],
        [0.0, 1.0, 1.0, 0.0],
        [0.0, 0.0, 1.0, 1.0],
        [1.0, 0.0, 0.0, 1.0],
    ]
    w = slim.slim(a, 0.5, 0.5)
    want = [
        [0.0, 1 / 3, 0.0, 1 / 9],
        [3 / 7, 0.0, 3 / 7, 0.0],
        [0.0, 1 / 3, 0.0, 1 / 9],
        [1 / 5, 0.0, 1 / 5, 0.0],
    ]
    for row, ref in zip(w, want):
        for x, y in zip(row, ref):
            assert abs(x - y) <= REF_TOL
    assert slim.recommend(a, w, 0, 2) == [2, 3]


def test_preconditions():
    with pytest.raises(ValueError):
        slim.slim_column([[1.0, 0.0]], 0, 0.0, 1.0)
