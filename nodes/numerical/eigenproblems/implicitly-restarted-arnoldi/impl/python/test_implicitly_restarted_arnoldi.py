# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/implicitly-restarted-arnoldi/. The authors are listed in prov/PAMN7C.jsonl.

import math
import random

import pytest

from implicitly_restarted_arnoldi import U, extend, iram, norm2, ritz_pairs, shifted_qr


def dense(a):
    return lambda x: [sum(r[j] * x[j] for j in range(len(x))) for r in a]


def bidiag(n):
    """Upper bidiagonal: diagonal 1..n, superdiagonal 1. Eigenvalues 1..n."""
    return lambda x: [(i + 1) * x[i] + (x[i + 1] if i + 1 < n else 0.0) for i in range(n)]


def householder_similarity(a, seed):
    rng = random.Random(seed)
    n = len(a)
    v = [rng.uniform(-1, 1) for _ in range(n)]
    nv = norm2(v)
    v = [x / nv for x in v]
    p = [[(1.0 if i == j else 0.0) - 2 * v[i] * v[j] for j in range(n)] for i in range(n)]
    pa = [[sum(p[i][t] * a[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
    return [[sum(pa[i][t] * p[t][j] for t in range(n)) for j in range(n)] for i in range(n)]


def diag(d):
    return [[d[i] if i == j else 0.0 for j in range(len(d))] for i in range(len(d))]


def close_to(found, expected, tol):
    pool = list(found)
    for lam in expected:
        best = min(range(len(pool)), key=lambda i: abs(pool[i] - lam))
        assert abs(pool[best] - lam) <= tol, (lam, pool[best])
        pool.pop(best)


def test_page_example():
    n = 100
    rng = random.Random(1)
    b = [rng.uniform(-1, 1) for _ in range(n)]
    seen = {}
    for k, m in ((1, 6), (3, 10), (4, 12), (4, 20)):
        th, x, est, restarts, matvecs, ok = iram(bidiag(n), b, k, m)
        assert ok
        close_to(th, [100, 99, 98, 97][:k], 1e-8)
        assert matvecs == k + restarts * (m - k) + (m - k)
        seen[(k, m)] = restarts
        for t, xv, e in zip(th, x, est):
            r = norm2([a - t * c for a, c in zip(bidiag(n)(xv), xv)])
            assert r == pytest.approx(e, rel=1e-4, abs=1e-12)
    assert seen[(4, 20)] < seen[(4, 12)]
    assert 40 <= seen[(1, 6)] <= 50 and 5 <= seen[(4, 20)] <= 9


def test_exact_shift_filter_and_relation():
    rng = random.Random(4)
    n, k, m = 30, 3, 10
    a = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)]
    mv = dense(a)
    b = [rng.gauss(0, 1) for _ in range(n)]
    counter = {"matvecs": 0, "scale": 0.0}
    v, h = [], [[0j] * m for _ in range(m)]
    f, j = extend(mv, v, h, [complex(x) for x in b], 0, m, counter)
    assert j == m
    pairs = ritz_pairs([row[:] for row in h], norm2(f))
    pairs.sort(key=lambda t: -abs(t[0]))
    shifts = [t[0] for t in pairs[k:]]
    q = [[1.0 + 0j if r == c else 0j for c in range(m)] for r in range(m)]
    for mu in shifts:
        shifted_qr(h, mu, q)
    v1 = [sum(v[c][i] * q[c][0] for c in range(m)) for i in range(n)]
    w = list(v[0])
    for mu in shifts:
        w = [s - mu * t for s, t in zip(mv(w), w)]
    nw = norm2(w)
    w = [t / nw for t in w]
    overlap = abs(sum(x.conjugate() * y for x, y in zip(v1, w)))
    assert overlap == pytest.approx(1.0, abs=1e-8)
    for c in range(k - 1):
        assert abs(q[m - 1][c]) <= 1e-12
    vk = [[sum(v[c][i] * q[c][col] for c in range(m)) for i in range(n)] for col in range(k + 1)]
    fk = [h[k][k - 1] * s + q[m - 1][k - 1] * t for s, t in zip(vk[k], f)]
    fro = math.sqrt(sum(x * x for row in a for x in row))
    for col in range(k):
        av = mv(vk[col])
        rhs = [sum(vk[r][i] * h[r][col] for r in range(k)) + (fk[i] if col == k - 1 else 0) for i in range(n)]
        assert norm2([s - t for s, t in zip(av, rhs)]) <= 1e3 * n * U * fro
    for r in range(k + 1):
        for c in range(k + 1):
            g = sum(x.conjugate() * y for x, y in zip(vk[r], vk[c]))
            assert abs(g - (1.0 if r == c else 0.0)) <= 100 * n * U
    assert all(abs(sum(x.conjugate() * y for x, y in zip(vk[r], fk))) <= 1e-12 * norm2(f) + 1e-13 for r in range(k))


def test_known_spectra():
    n = 40
    t = [[2.0 if i == j else (-1.0 if abs(i - j) == 1 else 0.0) for j in range(n)] for i in range(n)]
    th, _, _, _, _, ok = iram(dense(t), [1.0 + 0.01 * i for i in range(n)], 3, 12)
    assert ok
    close_to(th, [2 - 2 * math.cos(j * math.pi / (n + 1)) for j in (n, n - 1, n - 2)], 1e-8)
    a = householder_similarity(diag([float(i) for i in range(1, 31)]), 2)
    th, _, _, _, _, ok = iram(dense(a), [1.0] * 30, 2, 8)
    assert ok
    close_to(th, [30, 29], 1e-8)


def test_complex_pair_and_which():
    base = diag([float(i) for i in range(1, 21)] + [0.0, 0.0])
    base[20][20], base[20][21], base[21][20], base[21][21] = 15.0, 15.0, -15.0, 15.0
    a = householder_similarity(base, 9)
    rng = random.Random(3)
    b = [rng.uniform(-1, 1) for _ in range(22)]
    th, _, _, _, _, ok = iram(dense(a), b, 2, 8, which="LM")
    assert ok
    close_to(th, [15 + 15j, 15 - 15j], 1e-8)
    th, _, _, _, _, ok = iram(dense(a), b, 1, 8, which="LR")
    assert ok
    close_to(th, [20], 1e-8)
    d = [-10.0] + [float(i) for i in range(1, 10)]
    th, _, _, _, _, _ = iram(dense(householder_similarity(diag(d), 1)), [1.0] * 10, 1, 4, which="LM")
    close_to(th, [-10], 1e-8)
    th, _, _, _, _, _ = iram(dense(householder_similarity(diag(d), 1)), [1.0] * 10, 1, 4, which="LR")
    close_to(th, [9], 1e-8)


def test_breakdown_trivial_and_errors():
    d = [5.0, 4.0, 3.0, 2.0, 1.0, 0.5]
    th, _, est, restarts, _, ok = iram(dense(diag(d)), [1.0, 1.0, 1.0, 0, 0, 0], 2, 5)
    assert ok and restarts == 0
    close_to(th, [5, 4], 1e-13)
    th, _, _, _, _, ok = iram(dense(diag([0.0] * 4)), [1.0, 2.0, 3.0, 4.0], 1, 3)
    assert ok and abs(th[0]) == 0.0
    th, _, _, _, _, ok = iram(dense([[1.0, 2.0], [3.0, 4.0]]), [1.0, 0.0], 1, 2)
    assert ok
    close_to(th, [(5 + math.sqrt(33)) / 2], 1e-12)
    with pytest.raises(ValueError):
        iram(dense([[1.0]]), [1.0], 1, 2)
    with pytest.raises(ValueError):
        iram(dense(diag([1.0, 2.0, 3.0])), [0.0, 0.0, 0.0], 1, 2)
    with pytest.raises(ValueError):
        iram(dense(diag([1.0, 2.0, 3.0])), [1.0, 1.0, 1.0], 1, 3, which="SM")


def test_repeated_jordan_equal_modulus_nearly_equal():
    rng = random.Random(5)
    b = [rng.uniform(0.5, 1.5) for _ in range(12)]
    d = [3.0, 3.0] + [0.1 * i for i in range(1, 11)]
    th, _, _, _, _, ok = iram(dense(householder_similarity(diag(d), 4)), b, 1, 5)
    assert ok
    close_to(th, [3], 1e-9)
    j = diag([4.0, 4.0, 4.0] + [0.1 * i for i in range(1, 10)])
    j[0][1] = j[1][2] = 1.0
    # one wanted value inside a defective cluster: the shifts purge the cluster and it stalls
    th, _, _, restarts, _, ok = iram(dense(householder_similarity(j, 6)), b, 1, 6, max_restarts=50)
    assert not ok and restarts == 50
    # the whole cluster wanted: converges, with error about the cube root of the residual
    th, _, est, _, _, ok = iram(dense(householder_similarity(j, 6)), b, 3, 6)
    assert ok
    assert all(abs(t - 4.0) <= 1e-4 for t in th)
    assert all(e <= 1e-10 for e in est)
    d = [2.0, -2.0] + [0.1 * i for i in range(1, 11)]
    th, _, _, _, _, ok = iram(dense(householder_similarity(diag(d), 7)), b, 2, 6)
    assert ok
    close_to(th, [2, -2], 1e-9)
    d = [2.0, 2.0 + 1e-6] + [0.1 * i for i in range(1, 11)]
    th, _, _, _, _, ok = iram(dense(householder_similarity(diag(d), 8)), b, 2, 6)
    assert ok
    close_to(th, [2, 2 + 1e-6], 1e-9)
