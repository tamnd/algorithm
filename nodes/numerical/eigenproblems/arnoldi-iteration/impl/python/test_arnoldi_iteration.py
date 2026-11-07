# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arnoldi-iteration/. The authors are listed in prov/1X1DGA.jsonl.

import cmath
import math
import random
from fractions import Fraction

import pytest

from arnoldi_iteration import U, arnoldi, norm2, ritz


def dense(a):
    return lambda x: [sum(r[j] * x[j] for j in range(len(x))) for r in a]


def bidiag(n):
    """Upper bidiagonal: diagonal 1..n, superdiagonal 1. Eigenvalues 1..n."""
    return lambda x: [(i + 1) * x[i] + (x[i + 1] if i + 1 < n else 0.0) for i in range(n)]


def householder_similarity(a, seed):
    """P A P with P = I - 2 v v^T for a random unit v: same spectrum, structure hidden."""
    rng = random.Random(seed)
    n = len(a)
    v = [rng.uniform(-1, 1) for _ in range(n)]
    nv = norm2(v)
    v = [x / nv for x in v]
    p = [[(1.0 if i == j else 0.0) - 2 * v[i] * v[j] for j in range(n)] for i in range(n)]
    pa = [[sum(p[i][t] * a[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
    return [[sum(pa[i][t] * p[t][j] for t in range(n)) for j in range(n)] for i in range(n)]


def matches(found, expected, tol):
    """Every expected eigenvalue has a distinct found value within tol."""
    pool = list(found)
    for lam in expected:
        best = min(range(len(pool)), key=lambda i: abs(pool[i] - lam))
        assert abs(pool[best] - lam) <= tol, (lam, pool[best])
        pool.pop(best)


def test_page_example():
    n = 100
    mv = bidiag(n)
    expected = {5: 3.428396, 10: 0.4523255, 20: 0.009805770, 30: 1.602351e-4, 40: 5.681295e-7}
    errs = {}
    for k, err in expected.items():
        q, h, m = arnoldi(mv, [1.0] * n, k)
        assert m == k
        r = ritz(h, q, m)
        theta, x, est = r[0]
        errs[k] = abs(theta - 100)
        assert errs[k] == pytest.approx(err, rel=1e-4)
        ax = mv(x)
        res = norm2([a - theta * v for a, v in zip(ax, x)])
        assert est == pytest.approx(res, rel=1e-6, abs=1e-12)
        if k == 40:
            # the left eigenvector of 99 is orthogonal to b, so no Ritz value approaches 99
            assert min(abs(t[0] - 99) for t in r) > 0.5
    ks = sorted(errs)
    for k1, k2 in zip(ks, ks[1:]):
        assert errs[k2] < 0.2 * errs[k1]


def test_relation_and_orthogonality():
    rng = random.Random(7)
    n, k = 60, 30
    a = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)]
    mv = dense(a)
    b = [rng.gauss(0, 1) for _ in range(n)]
    fro = math.sqrt(sum(v * v for row in a for v in row))
    for reorth in (True, False):
        q, h, m = arnoldi(mv, b, k, reorth=reorth)
        assert m == k and len(q) == k + 1
        worst = 0.0
        for j in range(k):
            aq = mv(q[j])
            rhs = [sum(q[i][t] * h[i][j] for i in range(j + 2)) for t in range(n)]
            worst = max(worst, norm2([x - y for x, y in zip(aq, rhs)]))
        assert worst <= 10 * n * U * fro
        for i in range(k + 1):
            for j in range(k + 1):
                g = sum(x * y for x, y in zip(q[i], q[j]))
                target = 1.0 if i == j else 0.0
                bound = 10 * n * U if reorth else 1e3 * n * U
                assert abs(g - target) <= bound
        for i in range(k + 1):
            for j in range(k):
                if i > j + 1:
                    assert h[i][j] == 0.0


def unnormalized_arnoldi(a, b):
    """Lines L2 to L9 in exact arithmetic without the square root: q_j orthogonal, not unit."""
    n = len(a)
    q = [b[:]]
    hh = [[Fraction(0)] * n for _ in range(n)]
    for j in range(n):
        w = [sum(a[r][c] * q[j][c] for c in range(n)) for r in range(n)]
        for i in range(j + 1):
            c = sum(x * y for x, y in zip(q[i], w)) / sum(x * x for x in q[i])
            hh[i][j] = c
            w = [x - c * y for x, y in zip(w, q[i])]
        if j + 1 < n:
            hh[j + 1][j] = Fraction(1)
            q.append(w)
    return hh


def det_frac(m):
    m = [row[:] for row in m]
    n = len(m)
    d = Fraction(1)
    for c in range(n):
        p = next((r for r in range(c, n) if m[r][c] != 0), None)
        if p is None:
            return Fraction(0)
        if p != c:
            m[c], m[p] = m[p], m[c]
            d = -d
        d *= m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return d


def test_exact_fraction_similarity():
    a = [[Fraction(v) for v in row] for row in [[4, 1, -2, 2], [1, 2, 0, 1], [-2, 0, 3, -2], [2, 1, -2, -1]]]
    a[0][1] = Fraction(3)  # make it nonsymmetric
    b = [Fraction(1), Fraction(2), Fraction(-1), Fraction(1)]
    hh = unnormalized_arnoldi(a, b)
    for i in range(4):
        for j in range(4):
            if i > j + 1:
                assert hh[i][j] == 0
    assert sum(hh[i][i] for i in range(4)) == sum(a[i][i] for i in range(4))
    assert det_frac(hh) == det_frac(a)
    af = [[float(v) for v in row] for row in a]
    q, h, m = arnoldi(dense(af), [float(v) for v in b], 4)
    thetas = [t[0] for t in ritz(h, q, m)]
    assert abs(sum(thetas) - float(sum(a[i][i] for i in range(4)))) <= 1e-12
    prod = 1.0 + 0j
    for t in thetas:
        prod *= t
    assert abs(prod - float(det_frac(a))) <= 1e-11 * abs(float(det_frac(a)))


def test_full_steps_known_spectra():
    n = 12
    t = [[2.0 if i == j else (-1.0 if abs(i - j) == 1 else 0.0) for j in range(n)] for i in range(n)]
    q, h, m = arnoldi(dense(t), [1.0 + 0.1 * i for i in range(n)], n)
    for i in range(m):
        for j in range(i + 2, m):
            assert abs(h[i][j]) <= 100 * n * U
    exact = [2 - 2 * math.cos(k * math.pi / (n + 1)) for k in range(1, n + 1)]
    matches([x[0] for x in ritz(h, q, m)], exact, 1e-12)
    comp = [[0.0] * 5 for _ in range(5)]
    coeffs = [-15.0, 85.0, -225.0, 274.0, -120.0]  # (z-1)(z-2)(z-3)(z-4)(z-5)
    for i in range(4):
        comp[i + 1][i] = 1.0
    for i in range(5):
        comp[i][4] = -coeffs[4 - i]
    q, h, m = arnoldi(dense(comp), [1.0, 0.0, 0.0, 0.0, 0.0], 5)
    matches([x[0] for x in ritz(h, q, m)], [1, 2, 3, 4, 5], 1e-8)
    a = [[3.0, 1.0, -1.0], [-1.0, 5.0, 1.0], [-2.0, 2.0, 4.0]]  # S diag(2,4,6) S^-1
    q, h, m = arnoldi(dense(a), [1.0, 0.3, -0.2], 3)
    matches([x[0] for x in ritz(h, q, m)], [2, 4, 6], 1e-12)


def test_complex_pairs():
    base = [[0.0] * 6 for _ in range(6)]
    base[0][0], base[0][1], base[1][0], base[1][1] = 3.0, 4.0, -4.0, 3.0
    base[2][2], base[2][3], base[3][2], base[3][3] = 1.0, 1.0, -1.0, 1.0
    base[4][4], base[5][5] = 0.5, -2.0
    a = householder_similarity(base, 3)
    q, h, m = arnoldi(dense(a), [1.0, -1.0, 0.5, 0.25, 2.0, 1.0], 6)
    thetas = [x[0] for x in ritz(h, q, m)]
    matches(thetas, [3 + 4j, 3 - 4j, 1 + 1j, 1 - 1j, 0.5, -2.0], 1e-12)


def test_breakdown_and_trivial_cases():
    q, h, m = arnoldi(dense([[5.0]]), [2.0], 3)
    assert m == 1 and ritz(h, q, m)[0][0] == pytest.approx(5.0)
    q, h, m = arnoldi(dense([[0.0] * 3 for _ in range(3)]), [1.0, 2.0, 3.0], 3)
    assert m == 1 and abs(ritz(h, q, m)[0][0]) == 0.0
    d = [7.0, 5.0, 3.0, 2.0, 1.0]
    diag = [[d[i] if i == j else 0.0 for j in range(5)] for i in range(5)]
    q, h, m = arnoldi(dense(diag), [1.0, 1.0, 1.0, 0.0, 0.0], 5)
    assert m == 3
    th = [x[0] for x in ritz(h, q, m)]
    matches(th, [7, 5, 3], 1e-13)
    assert all(est <= 1e-13 for _, _, est in ritz(h, q, m))
    jb = [[2.0 if i == j else (1.0 if j == i + 1 else 0.0) for j in range(5)] for i in range(5)]
    q, h, m = arnoldi(dense(jb), [1.0, 0, 0, 0, 0], 5)
    assert m == 1 and ritz(h, q, m)[0][0] == pytest.approx(2.0)
    q, h, m = arnoldi(dense(jb), [0, 0, 0, 0, 1.0], 5)
    assert m == 5
    assert all(abs(x[0] - 2.0) <= 1e-2 for x in ritz(h, q, m))
    tri = [[4.0, 1.0, 2.0, 3.0], [0, -1.0, 5.0, 1.0], [0, 0, 2.5, 7.0], [0, 0, 0, 0.5]]
    q, h, m = arnoldi(dense(tri), [1.0, 1.0, 1.0, 1.0], 4)
    matches([x[0] for x in ritz(h, q, m)], [4, -1, 2.5, 0.5], 1e-11)


def test_repeated_equal_modulus_nearly_equal():
    rng = random.Random(11)
    b = [rng.uniform(0.5, 1.5) for _ in range(6)]
    d = [2.0, 2.0, 2.0, 1.0, 0.5, -1.0]
    a = householder_similarity([[d[i] if i == j else 0.0 for j in range(6)] for i in range(6)], 5)
    q, h, m = arnoldi(dense(a), b, 6)
    assert m == 4  # the Krylov space sees one copy of the triple eigenvalue
    matches([x[0] for x in ritz(h, q, m)], [2, 1, 0.5, -1], 1e-12)
    d = [3.0, -3.0, 1.0, 0.5]
    a = householder_similarity([[d[i] if i == j else 0.0 for j in range(4)] for i in range(4)], 6)
    q, h, m = arnoldi(dense(a), b[:4], 4)
    matches([x[0] for x in ritz(h, q, m)], d, 1e-12)
    d = [1.0, 1.0 + 1e-9, 0.5, 0.25]
    a = householder_similarity([[d[i] if i == j else 0.0 for j in range(4)] for i in range(4)], 8)
    q, h, m = arnoldi(dense(a), b[:4], 4)
    matches([x[0] for x in ritz(h, q, m)], d, 1e-12)


def test_errors_and_cap():
    with pytest.raises(ValueError):
        arnoldi(dense([[1.0, 0.0], [0.0, 1.0]]), [0.0, 0.0], 2)
    q, h, m = arnoldi(dense([[1.0, 2.0], [3.0, 4.0]]), [1.0, 0.0], 10)
    assert m == 2
    root = cmath.sqrt(33)
    matches([x[0] for x in ritz(h, q, m)], [(5 + root) / 2, (5 - root) / 2], 1e-13)
