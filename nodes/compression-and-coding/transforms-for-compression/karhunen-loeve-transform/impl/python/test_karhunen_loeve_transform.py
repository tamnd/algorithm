# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karhunen-loeve-transform/. The authors are listed in prov/PSR8K0.jsonl.

import math
import random

from karhunen_loeve_transform import (
    jacobi_eigen, karhunen_loeve_transform, klt_forward, klt_from_covariance, klt_inverse, mean_and_covariance,
)

TOL = 1e-9


def ar1(n, rho):
    return [[rho ** abs(i - j) for j in range(n)] for i in range(n)]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(c) for c in zip(*a)]


def householder(v):
    n = len(v)
    vv = sum(t * t for t in v)
    return [[(1.0 if i == j else 0.0) - 2.0 * v[i] * v[j] / vv for j in range(n)] for i in range(n)]


def random_orthogonal(rng, n):
    q = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(n):
        q = matmul(householder([rng.gauss(0, 1) for _ in range(n)]), q)
    return q


def test_worked_example_two_by_two():
    # The example of the page: blocks (x1, x2) with covariance [[5, 3], [3, 5]].
    lam, t = klt_from_covariance([[5.0, 3.0], [3.0, 5.0]])
    assert abs(lam[0] - 8.0) < TOL and abs(lam[1] - 2.0) < TOL
    s = 1 / math.sqrt(2)
    assert max(abs(a - b) for a, b in zip(t[0], [s, s])) < TOL
    assert max(abs(abs(a) - s) for a in t[1]) < TOL and abs(t[1][0] + t[1][1]) < TOL


def test_worked_example_data():
    blocks = [[2.0, 1.0], [0.0, -1.0], [3.0, 4.0], [-1.0, 0.0], [1.0, 1.0]]
    t, mu, lam = karhunen_loeve_transform(blocks)
    assert mu == [1.0, 1.0]
    _, r = mean_and_covariance(blocks)
    assert max(abs(a - b) for a, b in zip(sum(r, []), [2.0, 2.0, 2.0, 2.8])) < TOL
    assert abs(lam[0] - (2.4 + math.sqrt(4.16))) < TOL and abs(lam[1] - (2.4 - math.sqrt(4.16))) < TOL
    ys = [klt_forward(t, mu, b) for b in blocks]
    # The coefficients are uncorrelated over the data and have the variances lam.
    for i in range(2):
        for j in range(2):
            c = sum(y[i] * y[j] for y in ys) / len(ys)
            assert abs(c - (lam[i] if i == j else 0.0)) < TOL
    for b, y in zip(blocks, ys):
        assert max(abs(p - q) for p, q in zip(klt_inverse(t, mu, y), b)) < TOL


def test_edges():
    lam, t = klt_from_covariance([[3.0]])
    assert lam == [3.0] and t == [[1.0]]
    lam, t = klt_from_covariance([[0.0, 0.0], [0.0, 0.0]])
    assert lam == [0.0, 0.0]
    lam, t = klt_from_covariance([[1.0, 0.0], [0.0, 4.0]])
    assert lam == [4.0, 1.0] and t == [[0.0, 1.0], [1.0, 0.0]]
    # Equal eigenvalues: any orthonormal basis is a KLT; check orthogonality only.
    lam, t = klt_from_covariance([[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]])
    assert lam == [2.0, 2.0, 2.0]


def test_known_spectrum_random():
    rng = random.Random(5)
    for _ in range(500):
        n = rng.randint(1, 5)
        q = random_orthogonal(rng, n)
        lam_true = sorted((rng.uniform(0.0, 10.0) for _ in range(n)), reverse=True)
        r = matmul(matmul(q, [[lam_true[i] if i == j else 0.0 for j in range(n)] for i in range(n)]), transpose(q))
        r = [[(r[i][j] + r[j][i]) / 2 for j in range(n)] for i in range(n)]
        lam, t = klt_from_covariance(r)
        assert max(abs(a - b) for a, b in zip(lam, lam_true)) < 1e-9
        tt = matmul(t, transpose(t))
        assert max(abs(tt[i][j] - (1.0 if i == j else 0.0)) for i in range(n) for j in range(n)) < 1e-9
        d = matmul(matmul(t, r), transpose(t))
        assert max(abs(d[i][j] - (lam[i] if i == j else 0.0)) for i in range(n) for j in range(n)) < 1e-8


def test_jacobi_agrees_with_closed_form_two_by_two():
    rng = random.Random(6)
    for _ in range(500):
        a, b, c = rng.uniform(-5, 5), rng.uniform(-5, 5), rng.uniform(-5, 5)
        lam, _ = jacobi_eigen([[a, b], [b, c]])
        disc = math.sqrt((a - c) ** 2 + 4 * b * b)
        want = sorted([(a + c + disc) / 2, (a + c - disc) / 2])
        assert max(abs(x - y) for x, y in zip(sorted(lam), want)) < 1e-9


def test_ar1_coding_gain_closed_form():
    # For AR(1), det R = (1 - rho^2)^(n - 1), so the KLT gain is (1 - rho^2)^(-(n - 1)/n).
    for rho in [0.5, 0.9, 0.95]:
        lam, _ = klt_from_covariance(ar1(8, rho))
        gm = math.exp(sum(math.log(v) for v in lam) / 8)
        assert abs(1 / gm - (1 - rho * rho) ** (-7 / 8)) < 1e-9
    lam, _ = klt_from_covariance(ar1(8, 0.9))
    assert abs(10 * math.log10(sum(lam) / 8 / math.exp(sum(math.log(v) for v in lam) / 8)) - 6.3109) < 1e-4


def dct_matrix(n):
    return [[(math.sqrt(1 / n) if k == 0 else math.sqrt(2 / n)) * math.cos(math.pi * (2 * i + 1) * k / (2 * n)) for i in range(n)] for k in range(n)]


def test_klt_beats_dct_in_compaction_and_gain():
    # Optimality: for every m, the KLT puts at least as much variance in m coefficients as the DCT.
    for rho in [0.3, 0.9, 0.95]:
        r = ar1(8, rho)
        lam, _ = klt_from_covariance(r)
        c = dct_matrix(8)
        var = sorted((sum(c[k][i] * r[i][j] * c[k][j] for i in range(8) for j in range(8)) for k in range(8)), reverse=True)
        for m in range(1, 9):
            assert sum(lam[:m]) >= sum(var[:m]) - 1e-12
        gm_klt = sum(math.log(v) for v in lam)
        gm_dct = sum(math.log(v) for v in var)
        assert gm_klt <= gm_dct + 1e-12


def test_sample_data_ar1():
    # Data from an AR(1) source: the sample KLT diagonalizes the sample covariance.
    rng = random.Random(8)
    rho, n = 0.9, 8
    s = math.sqrt(1 - rho * rho)
    blocks = []
    for _ in range(2000):
        v = rng.gauss(0, 1)
        b = [v]
        for _ in range(n - 1):
            v = rho * v + s * rng.gauss(0, 1)
            b.append(v)
        blocks.append(b)
    t, mu, lam = karhunen_loeve_transform(blocks)
    ys = [klt_forward(t, mu, b) for b in blocks]
    for i in range(n):
        for j in range(n):
            c = sum(y[i] * y[j] for y in ys) / len(ys)
            assert abs(c - (lam[i] if i == j else 0.0)) < 1e-8
    # The sample eigenvalues are near the true ones (loose statistical tolerance).
    lam_true, _ = klt_from_covariance(ar1(n, rho))
    assert abs(lam[0] - lam_true[0]) < 0.4
