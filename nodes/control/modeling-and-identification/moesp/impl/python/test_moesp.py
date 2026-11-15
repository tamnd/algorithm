# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moesp/. The authors are listed in prov/7ZZDNB.jsonl.

import random

from ctlmat import charpoly, mul, polyroots, transpose
from moesp import block_hankel, householder_lq, jacobi_svd, moesp, pinv, simulate


def _close(a, b, tol):
    return all(abs(x - y) <= tol for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def _eig_error(A, A0):
    eig = polyroots(charpoly(A))
    true = polyroots(charpoly(A0))
    return max(min(abs(e - t) for t in true) for e in eig)


def _markov(A, B, C, K):
    out = []
    P = [list(row) for row in B]
    for _ in range(K):
        out.append(mul(C, P))
        P = mul(A, P)
    return out


def test_lq_factor():
    rng = random.Random(1)
    for _ in range(10):
        d, ncol = rng.randint(1, 6), rng.randint(6, 12)
        a = [[rng.uniform(-1, 1) for _ in range(ncol)] for _ in range(d)]
        L = householder_lq(a)
        assert all(L[r][c] == 0.0 for r in range(d) for c in range(r + 1, d))
        # a = L Q with Q Q^T = I implies a a^T = L L^T
        assert _close(mul(L, transpose(L)), mul(a, transpose(a)), 1e-12)


def test_block_hankel_layout():
    w = [[k, 10 * k] for k in range(5)]
    assert block_hankel(w, 2, 3) == [[0, 1, 2], [0, 10, 20], [1, 2, 3], [10, 20, 30]]


def test_pinv_of_rank_deficient_matrix():
    a = [[1.0, 2.0], [2.0, 4.0], [0.0, 0.0]]
    p = pinv(a)
    assert _close(mul(mul(a, p), a), a, 1e-12)
    assert _close(mul(mul(p, a), p), p, 1e-12)


def test_exact_siso_with_initial_state():
    A0 = [[0.7, 0.4], [-0.4, 0.7]]
    B0 = [[1.0], [0.5]]
    C0 = [[1.0, 0.0]]
    D0 = [[0.2]]
    rng = random.Random(7)
    u = [[rng.gauss(0.0, 1.0)] for _ in range(300)]
    y = simulate(A0, B0, C0, D0, u, [0.5, -1.0])
    A, B, C, D, x0, s = moesp(u, y, 4)
    assert len(A) == 2
    assert s[2] < 1e-12 * s[0]
    assert _eig_error(A, A0) < 1e-10
    assert abs(D[0][0] - 0.2) < 1e-10
    yh = simulate(A, B, C, D, u, x0)
    assert max(abs(a[0] - b[0]) for a, b in zip(y, yh)) < 1e-9
    for g, g0 in zip(_markov(A, B, C, 12), _markov(A0, B0, C0, 12)):
        assert _close(g, g0, 1e-10)


def test_exact_mimo():
    A0 = [[0.5, 0.3, 0.0], [-0.3, 0.5, 0.2], [0.0, 0.0, -0.6]]
    B0 = [[1.0, 0.0], [0.0, 1.0], [1.0, -1.0]]
    C0 = [[1.0, 0.0, 1.0], [0.0, 1.0, 0.0]]
    D0 = [[0.0, 0.1], [0.0, 0.0]]
    rng = random.Random(11)
    u = [[rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0)] for _ in range(250)]
    y = simulate(A0, B0, C0, D0, u, [0.0, 0.0, 0.0])
    A, B, C, D, x0, s = moesp(u, y, 5)
    assert len(A) == 3
    assert _eig_error(A, A0) < 1e-9
    assert _close(D, D0, 1e-9)
    for g, g0 in zip(_markov(A, B, C, 12), _markov(A0, B0, C0, 12)):
        assert _close(g, g0, 1e-9)


def test_white_output_noise():
    # measurement: white output noise with standard deviation 0.1, N = 2000
    A0 = [[0.7, 0.4], [-0.4, 0.7]]
    B0 = [[1.0], [0.5]]
    C0 = [[1.0, 0.0]]
    D0 = [[0.2]]
    for seed in (1, 2, 3):
        rng = random.Random(seed)
        u = [[rng.gauss(0.0, 1.0)] for _ in range(2000)]
        y = simulate(A0, B0, C0, D0, u, [0.0, 0.0])
        yn = [[v[0] + rng.gauss(0.0, 0.1)] for v in y]
        A, B, C, D, x0, s = moesp(u, yn, 6, n=2)
        assert s[1] > 5 * s[2]
        assert _eig_error(A, A0) < 0.01
        assert abs(D[0][0] - 0.2) < 0.02


def test_svd_reconstruction():
    rng = random.Random(5)
    a = [[rng.uniform(-1, 1) for _ in range(4)] for _ in range(6)]
    U, s, V = jacobi_svd(a)
    S = [[s[i] if i == j else 0.0 for j in range(4)] for i in range(4)]
    assert _close(mul(mul(U, S), transpose(V)), a, 1e-12)


def test_too_few_samples_rejected():
    u = [[1.0]] * 10
    try:
        moesp(u, u, 6)
    except ValueError:
        return
    assert False, "moesp must reject too few samples"
