# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gram-schmidt-process/. The authors are listed in prov/5JCA6Q.jsonl.

import random
from fractions import Fraction

import pytest

from gram_schmidt_process import RankDeficient, cgs, least_squares, mgs

U = Fraction(1, 2**53)
KAPPA2_HILBERT = {4: 1.55e4, 6: 1.50e7, 8: 1.53e10, 10: 1.60e13}


def orth_loss_frobenius(q):
    """||I - Q^T Q||_F computed exactly from the float entries (an upper bound on the 2-norm)."""
    m, n = len(q), len(q[0])
    qf = [[Fraction(v) for v in row] for row in q]
    s = Fraction(0)
    for i in range(n):
        for j in range(n):
            g = sum(qf[k][i] * qf[k][j] for k in range(m)) - (1 if i == j else 0)
            s += g * g
    return float(s) ** 0.5


def det(m):
    m = [list(r) for r in m]
    n, d = len(m), Fraction(1)
    for k in range(n):
        p = next((i for i in range(k, n) if m[i][k] != 0), None)
        if p is None:
            return Fraction(0)
        if p != k:
            m[k], m[p] = m[p], m[k]
            d = -d
        d *= m[k][k]
        for i in range(k + 1, n):
            f = m[i][k] / m[k][k]
            for j in range(k, n):
                m[i][j] -= f * m[k][j]
    return d


def exact_r_squared(a):
    """r_jj^2 = det(G_j) / det(G_{j-1}) with G = A^T A in rational arithmetic: an independent oracle."""
    m, n = len(a), len(a[0])
    af = [[Fraction(v) for v in row] for row in a]
    g = [[sum(af[k][i] * af[k][j] for k in range(m)) for j in range(n)] for i in range(n)]
    dets = [Fraction(1)] + [det([row[:j] for row in g[:j]]) for j in range(1, n + 1)]
    return [dets[j + 1] / dets[j] for j in range(n)]


def column_residual_ok(a, q, r, c):
    m, n = len(a), len(a[0])
    for j in range(n):
        res = [Fraction(a[i][j]) - sum(Fraction(q[i][k]) * Fraction(r[k][j]) for k in range(j + 1)) for i in range(m)]
        lhs = sum(t * t for t in res)
        rhs = (c * m * n * U) ** 2 * sum(Fraction(a[i][j]) ** 2 for i in range(m))
        if lhs > rhs:
            return False
    return True


def test_page_example():
    a = [[1, 3, 5], [2, 3, 1], [2, 0, 1]]
    want_q = [[1, 2, 2], [2, 1, -2], [2, -2, 1]]
    want_r = [[3, 3, 3], [0, 3, 3], [0, 0, 3]]
    for f in (mgs, cgs):
        q, r = f(a)
        assert all(abs(q[i][j] - want_q[i][j] / 3) <= 4e-16 for i in range(3) for j in range(3))
        assert all(abs(r[i][j] - want_r[i][j]) <= 1e-15 for i in range(3) for j in range(3))


def test_lauchli_cgs_loses_mgs_keeps():
    e = 1e-8
    a = [[1, 1, 1], [e, 0, 0], [0, e, 0], [0, 0, e]]
    qc, _ = cgs(a)
    qm, _ = mgs(a)
    q2, _ = cgs(a, reorthogonalize=True)
    dot = lambda q, i, j: sum(row[i] * row[j] for row in q)
    assert abs(dot(qc, 1, 2) - 0.5) < 1e-12  # complete loss of orthogonality
    assert abs(dot(qm, 1, 2)) < 1e-15 and abs(dot(qm, 0, 2)) < 1e-8  # loss about u * kappa
    assert orth_loss_frobenius(q2) < 1e-15


def test_edges_and_rank_deficiency():
    assert mgs([[-2.0]]) == ([[-1.0]], [[2.0]])
    q, r = mgs([[3.0, 0.0], [0.0, -5.0], [0.0, 0.0]])
    assert q == [[1.0, 0.0], [0.0, -1.0], [0.0, 0.0]] and r == [[3.0, 0.0], [0.0, 5.0]]
    for f in (mgs, cgs):
        with pytest.raises(RankDeficient):
            f([[1.0, 2.0], [0.0, 0.0]])
        with pytest.raises(RankDeficient):
            f([[0.0, 1.0], [0.0, 1.0]])
        with pytest.raises(RankDeficient):
            f([[1.0, 2.0, 3.0]])


def test_random_backward_error_and_r_against_exact():
    rng = random.Random(2028)
    for _ in range(500):
        m = rng.randint(1, 7)
        n = rng.randint(1, m)
        a = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(m)]
        r2 = exact_r_squared(a)
        if min(r2) < Fraction(1, 10**6):
            continue  # nearly rank deficient: covered by the Hilbert tests
        for f in (mgs, cgs, lambda x: cgs(x, True)):
            q, r = f(a)
            assert all(r[i][j] == 0 for i in range(n) for j in range(i))
            assert all(r[j][j] > 0 for j in range(n))
            assert column_residual_ok(a, q, r, 3)
            for j in range(n):
                assert abs(Fraction(r[j][j]) ** 2 - r2[j]) <= Fraction(1, 10**9) * (1 + r2[j])


def test_hilbert_loss_of_orthogonality_against_theory():
    for n, k2 in KAPPA2_HILBERT.items():
        h = [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]
        lm = orth_loss_frobenius(mgs(h)[0])
        lc = orth_loss_frobenius(cgs(h)[0])
        l2 = orth_loss_frobenius(cgs(h, True)[0])
        assert lm <= n * float(U) * k2  # Bjorck: O(u kappa)
        assert l2 <= 10 * n * float(U)  # CGS2: O(u)
        assert lc >= lm  # CGS is never better here
        assert column_residual_ok(h, *mgs(h), 3)
        assert column_residual_ok(h, *cgs(h), 3)  # both are backward stable as factorizations
    assert orth_loss_frobenius(cgs([[1.0 / (i + j + 1) for j in range(8)] for i in range(8)])[0]) > 0.5


def test_least_squares_line_fit():
    x, res = least_squares([[1, 0], [1, 1], [1, 2]], [1, 2, 4])
    assert abs(x[0] - 5 / 6) < 1e-14 and abs(x[1] - 1.5) < 1e-14
    assert all(abs(a - b) < 1e-14 for a, b in zip(res, [1 / 6, -1 / 3, 1 / 6]))


def test_least_squares_random_against_normal_equations_exact():
    rng = random.Random(7)
    for _ in range(100):
        m = rng.randint(2, 7)
        n = rng.randint(1, m - 1)
        a = [[rng.randint(-4, 4) for _ in range(n)] for _ in range(m)]
        b = [rng.randint(-4, 4) for _ in range(m)]
        af = [[Fraction(v) for v in row] for row in a]
        g = [[sum(af[k][i] * af[k][j] for k in range(m)) for j in range(n)] for i in range(n)]
        if det(g) == 0:
            continue
        rhs = [sum(af[k][i] * b[k] for k in range(m)) for i in range(n)]
        # Solve G x = A^T b exactly by Cramer-free elimination.
        aug = [g[i] + [rhs[i]] for i in range(n)]
        for k in range(n):
            p = next(i for i in range(k, n) if aug[i][k] != 0)
            aug[k], aug[p] = aug[p], aug[k]
            for i in range(n):
                if i != k:
                    f = aug[i][k] / aug[k][k]
                    aug[i] = [u - f * v for u, v in zip(aug[i], aug[k])]
        xe = [aug[i][n] / aug[i][i] for i in range(n)]
        x, _ = least_squares(a, b)
        scale = 1 + max(abs(v) for v in xe)
        assert max(abs(Fraction(u) - v) for u, v in zip(x, xe)) <= Fraction(1, 10**8) * scale
