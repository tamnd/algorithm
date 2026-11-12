# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rauch-tung-striebel-smoother/. The authors are listed in prov/Z7JZYG.jsonl.

import random
from fractions import Fraction as F

from rauch_tung_striebel_smoother import inverse, kalman_filter, mat_mul, mat_vec, rts_smoother, transpose


def joint_posterior(A, Q, H, R, m0, P0, ys):
    """Stack x_0..x_T, build the precision matrix L and the vector b of the
    joint Gaussian posterior, and return L^(-1) b and L^(-1)."""
    n, T = len(m0), len(ys)
    N = n * (T + 1)
    L = [[0] * N for _ in range(N)]
    b = [0] * N

    def add(i, j, M):
        for r in range(n):
            for c in range(n):
                L[i * n + r][j * n + c] += M[r][c]

    P0i, Qi, Ri = inverse(P0), inverse(Q), inverse(R)
    add(0, 0, P0i)
    for r, v in enumerate(mat_vec(P0i, m0)):
        b[r] += v
    At, Ht = transpose(A), transpose(H)
    for t in range(1, T + 1):
        add(t, t, Qi)
        add(t - 1, t - 1, mat_mul(mat_mul(At, Qi), A))
        add(t - 1, t, [[-x for x in row] for row in mat_mul(At, Qi)])
        add(t, t - 1, [[-x for x in row] for row in mat_mul(Qi, A)])
        add(t, t, mat_mul(mat_mul(Ht, Ri), H))
        for r, v in enumerate(mat_vec(mat_mul(Ht, Ri), ys[t - 1])):
            b[t * n + r] += v
    cov = inverse(L)
    mean = mat_vec(cov, b)
    return mean, cov


def check(A, Q, H, R, m0, P0, ys, exact, tol=0):
    n, T = len(m0), len(ys)
    ms, Ps = rts_smoother(A, Q, H, R, m0, P0, ys)
    mean, cov = joint_posterior(A, Q, H, R, m0, P0, ys)
    for t in range(T + 1):
        for r in range(n):
            d = ms[t][r] - mean[t * n + r]
            assert d == 0 if exact else abs(d) < tol
            for c in range(n):
                d = Ps[t][r][c] - cov[t * n + r][t * n + c]
                assert d == 0 if exact else abs(d) < tol


def test_exact_2d() -> None:
    A = [[F(1), F(1)], [F(0), F(1)]]
    Q = [[F(1, 4), F(1, 8)], [F(1, 8), F(1, 2)]]
    H = [[F(1), F(0)]]
    R = [[F(1, 2)]]
    m0 = [F(0), F(1)]
    P0 = [[F(1), F(0)], [F(0), F(1)]]
    ys = [[F(1)], [F(3, 2)], [F(4)], [F(5)]]
    check(A, Q, H, R, m0, P0, ys, exact=True)


def test_exact_scalar_worked_example() -> None:
    A, Q, H, R = [[F(1)]], [[F(1)]], [[F(1)]], [[F(1)]]
    m0, P0 = [F(0)], [[F(1)]]
    ys = [[F(1)], [F(2)], [F(0)]]
    ms, Ps = rts_smoother(A, Q, H, R, m0, P0, ys)
    _, _, mf, Pf = kalman_filter(A, Q, H, R, m0, P0, ys)
    assert [m[0] for m in mf] == [0, F(2, 3), F(3, 2), F(4, 7)]
    assert [P[0][0] for P in Pf] == [1, F(2, 3), F(5, 8), F(13, 21)]
    assert [m[0] for m in ms] == [F(3, 7), F(6, 7), F(8, 7), F(4, 7)]
    assert [P[0][0] for P in Ps] == [F(13, 21), F(10, 21), F(10, 21), F(13, 21)]
    check(A, Q, H, R, m0, P0, ys, exact=True)


def test_exact_two_observations() -> None:
    A = [[F(1, 2), F(0)], [F(1), F(1, 3)]]
    Q = [[F(1), F(0)], [F(0), F(2)]]
    H = [[F(1), F(0)], [F(1), F(1)]]
    R = [[F(1), F(1, 3)], [F(1, 3), F(1)]]
    m0 = [F(1), F(-1)]
    P0 = [[F(2), F(1)], [F(1), F(2)]]
    ys = [[F(1), F(0)], [F(-1), F(2)], [F(0), F(1)]]
    check(A, Q, H, R, m0, P0, ys, exact=True)


def test_random_float_models() -> None:
    rng = random.Random(3)
    for _ in range(20):
        n = rng.randint(1, 3)
        m = rng.randint(1, 2)
        T = rng.randint(1, 6)
        A = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        B = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        Q = mat_mul(B, transpose(B))
        for i in range(n):
            Q[i][i] += 0.1
        H = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(m)]
        R = [[0.5 if i == j else 0.0 for j in range(m)] for i in range(m)]
        m0 = [rng.gauss(0, 1) for _ in range(n)]
        P0 = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        ys = [[rng.gauss(0, 1) for _ in range(m)] for _ in range(T)]
        check(A, Q, H, R, m0, P0, ys, exact=False, tol=1e-9)


def test_last_step_and_shrinkage() -> None:
    A, Q, H, R = [[F(9, 10)]], [[F(1, 2)]], [[F(1)]], [[F(1)]]
    ys = [[F(1)], [F(-1)], [F(2)], [F(0)], [F(1)]]
    ms, Ps = rts_smoother(A, Q, H, R, [F(0)], [[F(1)]], ys)
    _, _, mf, Pf = kalman_filter(A, Q, H, R, [F(0)], [[F(1)]], ys)
    assert ms[-1] == mf[-1] and Ps[-1] == Pf[-1]
    for t in range(len(ys)):
        assert Ps[t][0][0] <= Pf[t][0][0]
