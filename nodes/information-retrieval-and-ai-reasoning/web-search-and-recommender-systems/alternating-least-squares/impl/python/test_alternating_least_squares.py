# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alternating-least-squares/. The authors are listed in prov/S7Y3XE.jsonl.

import random
from fractions import Fraction

import recs
import alternating_least_squares as als

TOL = 1e-9


def exact_solve(a, b):
    """Gaussian elimination in exact rational arithmetic."""
    n = len(a)
    m = [[Fraction(x) for x in row] + [Fraction(y)] for row, y in zip(a, b)]
    for c in range(n):
        piv = next(k for k in range(c, n) if m[k][c] != 0)
        m[c], m[piv] = m[piv], m[c]
        for k in range(n):
            if k != c and m[k][c] != 0:
                f = m[k][c] / m[c][c]
                m[k] = [x - f * y for x, y in zip(m[k], m[c])]
    return [m[k][n] / m[k][k] for k in range(n)]


def ridge_exact(rows, fixed, lam, weighted):
    """The ridge solution of one user from scratch, in Fractions."""
    r = len(next(iter(fixed)))
    c = len(rows) if weighted else 1
    a = [[sum(Fraction(fixed[j][s]) * Fraction(fixed[j][t]) for j in rows) for t in range(r)] for s in range(r)]
    for s in range(r):
        a[s][s] += Fraction(lam) * c
    b = [sum(Fraction(v) * Fraction(fixed[j][s]) for j, v in rows.items()) for s in range(r)]
    return exact_solve(a, b)


def test_half_step_is_exact_ridge_solution():
    for weighted in (False, True):
        full = recs.planted(7, 6, 3, 2, noise=0.3)
        train, _ = recs.split(full, 0.4, 2)
        rng = random.Random(6)
        q = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(6)]
        by_user, by_item = als.group(train)
        p = als.half_step(by_user, 7, q, 0.5, weighted, 3)
        for u in range(7):
            want = ridge_exact(by_user[u], q, 0.5, weighted)
            for x, y in zip(p[u], want):
                assert abs(x - float(y)) < TOL
        q2 = als.half_step(by_item, 6, p, 0.5, weighted, 3)
        for i in range(6):
            want = ridge_exact(by_item[i], p, 0.5, weighted)
            for x, y in zip(q2[i], want):
                assert abs(x - float(y)) < TOL


def test_block_gradient_is_zero_after_half_step():
    full = recs.planted(8, 7, 2, 4, noise=0.2)
    train, _ = recs.split(full, 0.3, 4)
    lam = 0.2
    for weighted in (False, True):
        p, q, _ = als.als(train, 8, 7, 2, lam, 3, seed=1, weighted=weighted)
        # The last half step solved for Q, so the gradient in each q_i is zero.
        by_user, by_item = als.group(train)
        for i, rows in by_item.items():
            c = len(rows) if weighted else 1
            for f in range(2):
                g = 2 * lam * c * q[i][f]
                for u, v in rows.items():
                    e = v - sum(a * b for a, b in zip(p[u], q[i]))
                    g -= 2 * e * p[u][f]
                assert abs(g) < TOL


def test_objective_never_increases():
    for seed in range(3):
        full = recs.planted(12, 10, 3, seed, rounded=True)
        train, _ = recs.split(full, 0.4, seed)
        for weighted in (False, True):
            _, _, hist = als.als(train, 12, 10, 3, 0.1, 25, seed=seed, weighted=weighted)
            for a, b in zip(hist, hist[1:]):
                assert b <= a + TOL * max(1.0, a)


def test_rank_one_hand_example():
    train = recs.toy()
    p, q, hist = als.als(train, 4, 4, 1, 1.0, 1, q0=[[1.0]] * 4)
    for x, y in zip(p, [2.5, 3.0, 2.0, 1.5]):
        assert abs(x[0] - y) < TOL
    for x, y in zip(q, [106 / 81, 61 / 45, 14 / 13, 49 / 45]):
        assert abs(x[0] - y) < TOL
    assert abs(hist[0] - 159) < TOL and abs(hist[1] - 60) < TOL
    assert abs(hist[2] - 54.9526116) < 1e-6
    # The weighted (ALS-WR) user step: p_u = sum of r_ui / (2 n_u).
    p, _, _ = als.als(train, 4, 4, 1, 1.0, 1, q0=[[1.0]] * 4, weighted=True)
    for x, y in zip(p, [5 / 3, 15 / 8, 5 / 4, 1.0]):
        assert abs(x[0] - y) < TOL


def test_zero_start_is_a_fixed_point():
    train = recs.toy()
    p, q, hist = als.als(train, 4, 4, 2, 1.0, 3, q0=[[0.0, 0.0]] * 4)
    assert all(a == 0.0 for row in p + q for a in row)
    assert hist == [155.0] * 7


def test_user_without_ratings_and_cholesky():
    p, _, _ = als.als({(0, 0): 4.0, (0, 1): 2.0}, 2, 2, 2, 0.5, 2)
    assert p[1] == [0.0, 0.0]
    x = als.cholesky_solve([[4.0, 2.0], [2.0, 3.0]], [2.0, 1.0])
    assert abs(4 * x[0] + 2 * x[1] - 2) < 1e-12 and abs(2 * x[0] + 3 * x[1] - 1) < 1e-12
    try:
        als.cholesky_solve([[1.0, 2.0], [2.0, 1.0]], [1.0, 1.0])
    except ValueError:
        pass
    else:
        raise AssertionError("an indefinite matrix was accepted")
