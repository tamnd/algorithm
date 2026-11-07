# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/golub-kahan-svd-algorithm/. The authors are listed in prov/K72EMJ.jsonl.
import math
import random
from fractions import Fraction

from golub_kahan_svd_algorithm import U, bidiagonalize, svd


def check(a, c=10.0):
    """Run svd and assert residual and orthogonality bounds; return (sigma, steps)."""
    u, s, v, steps = svd(a)
    m, n = len(a), len(a[0])
    r = min(m, n)
    scale = max([abs(x) for row in a for x in row] + [1e-300])
    for i in range(m):
        for j in range(n):
            got = sum(u[i][k] * s[k] * v[j][k] for k in range(r))
            assert abs(a[i][j] - got) <= c * max(m, n) * U * scale * r
    for x, rows in ((u, m), (v, n)):
        for p in range(r):
            for q in range(r):
                dot = sum(x[i][p] * x[i][q] for i in range(rows))
                assert abs(dot - (p == q)) <= c * max(m, n) * U
    assert all(s[i] >= s[i + 1] for i in range(r - 1)) and s[-1] >= 0
    return s, steps


def det_exact(a):
    a = [[Fraction(x) for x in row] for row in a]
    n, d = len(a), Fraction(1)
    for k in range(n):
        p = next((i for i in range(k, n) if a[i][k] != 0), None)
        if p is None:
            return Fraction(0)
        if p != k:
            a[k], a[p] = a[p], a[k]
            d = -d
        d *= a[k][k]
        for i in range(k + 1, n):
            f = a[i][k] / a[k][k]
            for j in range(k, n):
                a[i][j] -= f * a[k][j]
    return d


def householder_matrix(n, seed):
    rnd = random.Random(seed)
    w = [rnd.gauss(0, 1) for _ in range(n)]
    ww = sum(t * t for t in w)
    return [[(i == j) - 2 * w[i] * w[j] / ww for j in range(n)] for i in range(n)]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def test_page_example():
    a = [[1, 2, 3], [4, 5, 6], [7, 8, 10], [1, 0, 1]]
    b, _, _ = bidiagonalize(a)
    assert abs(abs(b[0][0]) - 8.18535) < 1e-5 and abs(abs(b[0][1]) - 15.30194) < 1e-5
    assert abs(abs(b[1][2]) - 0.09756) < 1e-5 and abs(abs(b[2][2]) - 0.70867) < 1e-5
    trace = []
    u, s, v, steps = svd(a, trace=trace)
    assert steps == 4
    e2 = [t[1] for t in trace]
    assert e2[1] < 0.05 * e2[0] and e2[2] <= e2[1] ** 2  # at least quadratic, observed faster
    ata = [[sum(Fraction(a[k][i] * a[k][j]) for k in range(4)) for j in range(3)] for i in range(3)]
    assert abs(sum(x * x for x in s) - float(sum(ata[i][i] for i in range(3)))) < 1e-12 * 306
    prod = s[0] ** 2 * s[1] ** 2 * s[2] ** 2
    assert abs(prod - float(det_exact(ata))) < 1e-12 * abs(float(det_exact(ata)))
    assert abs(s[0] - 17.450895584636637) < 1e-12


def test_known_spectra():
    n = 10
    ones = [[1.0 if j in (i, i + 1) else 0.0 for j in range(n)] for i in range(n)]
    s, _ = check(ones)
    for k in range(1, n + 1):
        assert abs(s[k - 1] - 2 * math.cos(k * math.pi / (2 * n + 1))) < 20 * n * U
    n = 15
    toep = [[2.0 if i == j else (-1.0 if abs(i - j) == 1 else 0.0) for j in range(n)] for i in range(n)]
    s, _ = check(toep)
    exact = sorted((2 - 2 * math.cos(k * math.pi / (n + 1)) for k in range(1, n + 1)), reverse=True)
    assert max(abs(x - y) for x, y in zip(s, exact)) < 20 * n * U * 4


def test_random_seeded_and_steps():
    rnd = random.Random(3)
    for m, n in ((40, 30), (30, 40), (50, 50)):
        a = [[rnd.gauss(0, 1) for _ in range(n)] for _ in range(m)]
        s, steps = check(a)
        assert steps <= 3 * min(m, n)  # observed about 1.9 per singular value
    a = [[rnd.randint(-5, 5) for _ in range(6)] for _ in range(6)]
    s, _ = check(a)
    assert abs(math.prod(s) - abs(float(det_exact(a)))) <= 1e-12 * max(1.0, math.prod(s))


def test_trivial_shapes():
    assert check([[-3.0]])[0] == [3.0]
    s, _ = check([[3.0, 4.0]])
    assert abs(s[0] - 5) < 1e-15
    s, _ = check([[3.0], [0.0], [4.0]])
    assert abs(s[0] - 5) < 1e-15
    s, steps = check([[0.0] * 3 for _ in range(4)])
    assert s == [0.0, 0.0, 0.0] and steps == 0
    s, steps = check([[0.0, 0.0, -2.0], [0.0, 5.0, 0.0], [1.0, 0.0, 0.0]])
    assert s == [5.0, 2.0, 1.0]
    s, _ = check([[2.0, 7.0, 1.0], [0.0, -3.0, 4.0], [0.0, 0.0, 0.5]])  # triangular
    assert abs(s[0] * s[1] * s[2] - 3.0) < 1e-13


def test_zero_diagonal_paths():
    for d, e in (([1.0, 0.0, 2.0, 3.0], [1.0, 1.0, 1.0]),
                 ([1.0, 2.0, 3.0, 0.0], [1.0, 1.0, 1.0]),
                 ([0.0, 2.0, 3.0], [1.0, 1.0])):
        n = len(d)
        b = [[0.0] * n for _ in range(n)]
        for i in range(n):
            b[i][i] = d[i]
        for i in range(n - 1):
            b[i][i + 1] = e[i]
        s, _ = check(b)
        assert s[-1] == 0.0
    jordan = [[1.0 if j == i + 1 else 0.0 for j in range(5)] for i in range(5)]  # J_5(0)
    s, _ = check(jordan)
    assert s == [1.0, 1.0, 1.0, 1.0, 0.0]


def test_repeated_and_close_values():
    h = householder_matrix(6, 7)
    s, _ = check([[2 * x for x in row] for row in h])
    assert max(abs(x - 2) for x in s) < 30 * U
    s, _ = check([[0.0, -1.0], [1.0, 0.0]])  # complex eigenvalues, equal singular values
    assert max(abs(x - 1) for x in s) < 4 * U
    a = matmul(matmul(householder_matrix(4, 1), [[1.0, 0, 0, 0], [0, 1 + 1e-10, 0, 0], [0, 0, 3.0, 0], [0, 0, 0, 0]]),
               householder_matrix(4, 2))
    s, _ = check(a)
    assert abs(s[1] - (1 + 1e-10)) < 50 * U and abs(s[2] - 1) < 50 * U and s[3] < 50 * U
    rank1 = [[1.0, 2.0, 3.0], [2.0, 4.0, 6.0], [-1.0, -2.0, -3.0]]
    s, _ = check(rank1)
    assert abs(s[0] - math.sqrt(6 * 14)) < 1e-13 and s[1] < 1e-14 and s[2] < 1e-14


def test_bidiagonalization_shape():
    rnd = random.Random(11)
    a = [[rnd.uniform(-1, 1) for _ in range(5)] for _ in range(8)]
    b, uq, vq = bidiagonalize(a)
    for i in range(5):
        for j in range(5):
            if j != i and j != i + 1:
                assert b[i][j] == 0.0
    back = matmul(matmul(uq, b), [list(r) for r in zip(*vq)])
    assert max(abs(back[i][j] - a[i][j]) for i in range(8) for j in range(5)) < 100 * U
    assert all(vq[0][j] == (j == 0) for j in range(5))  # first column of V is e1
