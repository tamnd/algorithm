# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robust-pca/. The authors are listed in prov/4W6RMP.jsonl.

import math
import random

import pytest

from robust_pca import add, fro, one_sided_jacobi, rpca, shrink, singular_values, svt


def planted(rng, n1, n2, r, frac, mag):
    u = [[rng.gauss(0, 1) for _ in range(r)] for _ in range(n1)]
    v = [[rng.gauss(0, 1) for _ in range(r)] for _ in range(n2)]
    l0 = [[sum(a * b for a, b in zip(u[i], v[j])) for j in range(n2)] for i in range(n1)]
    cells = rng.sample([(i, j) for i in range(n1) for j in range(n2)], int(frac * n1 * n2))
    s0 = [[0.0] * n2 for _ in range(n1)]
    for i, j in cells:
        s0[i][j] = rng.choice((-1, 1)) * mag
    return l0, s0


@pytest.fixture(scope="module")
def solved():
    l0, s0 = planted(random.Random(0), 20, 20, 2, 0.05, 10.0)
    m = add(l0, s0)
    trace = []
    l, s, y, it, _ = rpca(m, trace=trace)
    return l0, s0, m, l, s, y, trace


def test_jacobi_svd_reconstructs():
    rng = random.Random(1)
    m = [[rng.gauss(0, 1) for _ in range(5)] for _ in range(7)]
    a, s, v = one_sided_jacobi(m)
    back = [[sum(a[j][i] * v[j][k] for j in range(5)) for k in range(5)] for i in range(7)]
    assert fro(add(back, m, -1.0)) < 1e-12
    for p in range(5):
        for q in range(p + 1, 5):
            assert abs(sum(x * y for x, y in zip(a[p], a[q]))) < 1e-12 * (1 + s[p] * s[q])


def test_proximal_operators():
    rng = random.Random(2)
    m = [[rng.gauss(0, 1) for _ in range(6)] for _ in range(6)]
    tau = 0.8
    out, rank = svt(m, tau)
    before = singular_values(m)
    after = singular_values(out)
    assert rank == sum(1 for x in before if x > tau)
    for x, y in zip(before, after):
        assert abs(max(x - tau, 0.0) - y) < 1e-9
    assert shrink([[3.0, -0.5, -2.0]], 1.0) == [[2.0, 0.0, -1.0]]


def test_planted_recovery(solved):
    l0, s0, m, l, s, y, trace = solved
    assert fro(add(l, l0, -1.0)) <= 1e-5 * fro(l0)
    assert fro(add(s, s0, -1.0)) <= 1e-5 * fro(s0)
    assert trace[-1][0] == 2  # the rank of L
    assert {(i, j) for i in range(20) for j in range(20) if abs(s[i][j]) > 1e-3} == \
        {(i, j) for i in range(20) for j in range(20) if s0[i][j] != 0.0}
    # plain PCA of rank 2 is far off on the same data
    a, sv, v = one_sided_jacobi(m)
    top = sorted(range(20), key=lambda j: -sv[j])[:2]
    t2 = [[sum(a[j][i] * v[j][k] for j in top) for k in range(20)] for i in range(20)]
    assert fro(add(t2, l0, -1.0)) > 0.5 * fro(l0)


def test_dual_certificate(solved):
    # Y approximates a dual certificate: ||Y||_inf <= lam, Y = lam sign(S) on the support, ||Y||_2 ~ 1
    _, _, _, l, s, y, _ = solved
    lam = 1 / math.sqrt(20)
    assert max(abs(x) for row in y for x in row) <= lam * (1 + 1e-12)
    for yr, sr in zip(y, s):
        for yv, sv in zip(yr, sr):
            if sv != 0.0:
                assert abs(yv - math.copysign(lam, sv)) < 1e-9
    assert abs(singular_values(y)[0] - 1.0) < 1e-3


def test_residual_decreases_to_tolerance(solved):
    trace = solved[-1]
    assert trace[-1][2] <= 1e-7
    assert trace[-1][2] < trace[0][2]


def test_clean_low_rank_matrix():
    l0, _ = planted(random.Random(3), 12, 10, 1, 0.0, 0.0)
    l, s, _, _, _ = rpca(l0)
    assert fro(add(l, l0, -1.0)) <= 1e-5 * fro(l0)
    assert fro(s) <= 1e-5 * fro(l0)
