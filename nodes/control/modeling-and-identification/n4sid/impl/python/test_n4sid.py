# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/n4sid/. The authors are listed in prov/0NXMFM.jsonl.

import random

from ctlmat import add, charpoly, mul, polyroots, transpose
from n4sid import householder_lq, n4sid, oblique_projection, simulate


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


def _rand(rng, r, c):
    return [[rng.uniform(-1, 1) for _ in range(c)] for _ in range(r)]


def test_oblique_projection_splits_a_sum():
    # if a = M c + P b and the row spaces of b and c meet only in 0, then a /_b c = M c
    rng = random.Random(2)
    for _ in range(10):
        b, c = _rand(rng, 2, 9), _rand(rng, 3, 9)
        M, P = _rand(rng, 4, 3), _rand(rng, 4, 2)
        a = add(mul(M, c), mul(P, b))
        assert _close(oblique_projection(a, b, c), mul(M, c), 1e-10)


def test_lq_factor():
    rng = random.Random(1)
    a = _rand(rng, 5, 11)
    L = householder_lq(a)
    assert all(L[r][c] == 0.0 for r in range(5) for c in range(r + 1, 5))
    assert _close(mul(L, transpose(L)), mul(a, transpose(a)), 1e-12)


def test_exact_siso():
    A0 = [[0.7, 0.4], [-0.4, 0.7]]
    B0 = [[1.0], [0.5]]
    C0 = [[1.0, 0.0]]
    D0 = [[0.2]]
    rng = random.Random(7)
    u = [[rng.gauss(0.0, 1.0)] for _ in range(300)]
    y = simulate(A0, B0, C0, D0, u, [0.5, -1.0])
    A, B, C, D, cov, s = n4sid(u, y, 4)
    assert len(A) == 2
    assert s[2] < 1e-12 * s[0]
    assert _eig_error(A, A0) < 1e-10
    assert abs(D[0][0] - 0.2) < 1e-10
    for g, g0 in zip(_markov(A, B, C, 12), _markov(A0, B0, C0, 12)):
        assert _close(g, g0, 1e-10)
    assert all(abs(v) < 1e-20 for row in cov for v in row)


def test_exact_mimo():
    A0 = [[0.5, 0.3, 0.0], [-0.3, 0.5, 0.2], [0.0, 0.0, -0.6]]
    B0 = [[1.0, 0.0], [0.0, 1.0], [1.0, -1.0]]
    C0 = [[1.0, 0.0, 1.0], [0.0, 1.0, 0.0]]
    D0 = [[0.0, 0.1], [0.0, 0.0]]
    rng = random.Random(11)
    u = [[rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0)] for _ in range(250)]
    y = simulate(A0, B0, C0, D0, u, [1.0, 0.0, -1.0])
    A, B, C, D, cov, s = n4sid(u, y, 4)
    assert len(A) == 3
    assert _eig_error(A, A0) < 1e-9
    assert _close(D, D0, 1e-9)
    for g, g0 in zip(_markov(A, B, C, 12), _markov(A0, B0, C0, 12)):
        assert _close(g, g0, 1e-9)


def test_innovation_noise():
    # measurement: innovation form with K = [0.5, 0.2]^T, e white with variance 0.01,
    # white input, N = 2000, i = 5
    A0 = [[0.7, 0.4], [-0.4, 0.7]]
    B0 = [[1.0], [0.5]]
    C0 = [[1.0, 0.0]]
    D0 = [[0.2]]
    K0 = [[0.5], [0.2]]
    for seed in (1, 2, 3):
        rng = random.Random(seed)
        u = [[rng.gauss(0.0, 1.0)] for _ in range(2000)]
        e = [[rng.gauss(0.0, 0.1)] for _ in range(2000)]
        y = simulate(A0, B0, C0, D0, u, [0.0, 0.0], K0, e)
        A, B, C, D, cov, s = n4sid(u, y, 5, n=2)
        assert s[1] > 50 * s[2]
        assert _eig_error(A, A0) < 0.01
        assert abs(D[0][0] - 0.2) < 0.02
        assert abs(cov[2][2] - 0.01) < 0.002


def test_too_few_samples_rejected():
    u = [[1.0]] * 20
    try:
        n4sid(u, u, 5)
    except ValueError:
        return
    assert False, "n4sid must reject too few samples"
