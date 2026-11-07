# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subspace-iteration/. The authors are listed in prov/1HMDCT.jsonl.

import math
import random
from fractions import Fraction

import pytest

from subspace_iteration import dot, jacobi_eig, matvec, norm2, subspace_iteration

U = 2.0**-53


def orthogonal_rational(n, rng, k=3):
    """An exactly orthogonal rational matrix: a product of k reflectors I - 2 v v^T / v^T v."""
    q = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for _ in range(k):
        v = [Fraction(rng.randint(-5, 5)) for _ in range(n)]
        if all(t == 0 for t in v):
            v[0] = Fraction(1)
        vv = sum(t * t for t in v)
        for row in q:
            s = sum(r * t for r, t in zip(row, v)) * 2 / vv
            for j in range(n):
                row[j] -= s * v[j]
    return q


def build(lams, rng):
    """A = Q diag(lams) Q^T computed exactly, rounded once. Returns (A, exact eigenvector columns)."""
    n = len(lams)
    q = orthogonal_rational(n, rng)
    lf = [Fraction(t) for t in lams]
    a = [[float(sum(q[i][k] * lf[k] * q[j][k] for k in range(n))) for j in range(n)] for i in range(n)]
    vecs = [[float(q[i][k]) for i in range(n)] for k in range(n)]
    return a, vecs


def charpoly(a):
    """Exact characteristic polynomial det(tI - A) by Faddeev-LeVerrier, coefficients highest first."""
    n = len(a)
    af = [[Fraction(x) for x in row] for row in a]
    m = [[Fraction(0)] * n for _ in range(n)]
    coeffs = [Fraction(1)]
    for k in range(1, n + 1):
        am = [[sum(af[i][t] * m[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
        m = [[am[i][j] + (coeffs[-1] if i == j else 0) for j in range(n)] for i in range(n)]
        am = [[sum(af[i][t] * m[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
        coeffs.append(-sum(am[i][i] for i in range(n)) / k)
    return coeffs


def peval(c, x):
    s = Fraction(0)
    for t in c:
        s = s * x + t
    return s


def sin_angle_to(vecs_out, q):
    """sin of the largest principal angle between span(q) and the orthogonal complement
    of span(vecs_out): the 2-norm of M = V_out^T Q, from the eigenvalues of M^T M."""
    m = [[dot(v, c) for c in q] for v in vecs_out]
    p = len(q)
    g = [[sum(row[i] * row[j] for row in m) for j in range(p)] for i in range(p)]
    vals, _ = jacobi_eig(g)
    return math.sqrt(max(0.0, max(vals)))


def check_result(a, r, tol):
    n = len(a)
    scale = max(abs(t) for t in r.values)
    for x, t, res in zip(r.vectors, r.values, r.residuals):
        ax = matvec(a, x)
        rr = norm2([u - t * v for u, v in zip(ax, x)])
        assert abs(rr - res) <= 1e-13 * max(1.0, scale)
        assert res <= tol * scale
    for i, x in enumerate(r.vectors):
        for j, y in enumerate(r.vectors):
            assert abs(dot(x, y) - (i == j)) <= 4 * n * U


def test_known_spectra_many_seeds():
    for seed in range(25):
        rng = random.Random(seed)
        n = rng.randint(4, 10)
        p = rng.randint(1, min(4, n - 1))
        mags = sorted((rng.uniform(1.0, 10.0) for _ in range(n)), reverse=True)
        lams = [m * rng.choice((-1, 1)) for m in mags]
        if abs(lams[p]) > 0.9 * abs(lams[p - 1]):
            lams[p] = 0.9 * lams[p] * abs(lams[p - 1]) / abs(lams[p])
        a, _ = build(lams, rng)
        r = subspace_iteration(a, p, tol=1e-12, seed=seed)
        assert r.converged
        check_result(a, r, 1e-12)
        for t, lam in zip(r.values, lams[:p]):
            assert abs(t - lam) <= 1e-10 * abs(lams[0])
        assert r.matvecs == p * r.iterations


def test_exact_characteristic_polynomial():
    rng = random.Random(7)
    mats = [[[2, 1, 0], [1, 3, 1], [0, 1, 4]]]
    for _ in range(4):
        n = 5
        m = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                m[i][j] = m[j][i] = rng.randint(-4, 4)
        mats.append(m)
    for m in mats:
        a = [[float(x) for x in row] for row in m]
        c = charpoly(m)
        r = subspace_iteration(a, 2, tol=1e-13, maxit=20000)
        if not r.converged:
            continue  # a tie in modulus; covered by test_equal_modulus
        for t in r.values:
            d = 1e-7 * max(1.0, abs(t))
            lo, hi = peval(c, Fraction(t - d)), peval(c, Fraction(t + d))
            assert lo * hi <= 0  # a root of the exact characteristic polynomial lies within d


def test_backward_error_is_residual():
    rng = random.Random(3)
    a, _ = build([9.0, -7.0, 4.0, 2.0, 1.0, 0.5], rng)
    r = subspace_iteration(a, 3, tol=1e-10)
    n = len(a)
    x = r.vectors
    res = [[u - t * v for u, v in zip(matvec(a, xc), xc)] for xc, t in zip(x, r.values)]
    # E = -(R X^T + X R^T) makes (A + E) X = X Theta, up to X^T R, which is tiny.
    for i in range(3):
        for j in range(3):
            assert abs(dot(x[i], res[j])) <= 50 * n * U * 9.0
    e = [[-sum(res[k][i] * x[k][j] + x[k][i] * res[k][j] for k in range(3)) for j in range(n)] for i in range(n)]
    ae = [[a[i][j] + e[i][j] for j in range(n)] for i in range(n)]
    for xc, t in zip(x, r.values):
        y = matvec(ae, xc)
        assert norm2([u - t * v for u, v in zip(y, xc)]) <= 1e-12 * 9.0


def test_subspace_angle_rate_matches_ratio():
    for ratio in (0.5, 0.8):
        rng = random.Random(11)
        p = 2
        lams = [10.0, 6.0, 6.0 * ratio, 1.0, 0.5, -0.25]
        a, vecs = build(lams, rng)
        out = vecs[p:]
        tans = []

        def mon(k, q):
            s = sin_angle_to(out, q)
            tans.append(s / math.sqrt(1.0 - s * s))

        subspace_iteration(a, p, tol=1e-13, seed=5, monitor=mon)
        for k, t in enumerate(tans):
            assert t <= ratio**k * tans[0] * (1 + 1e-6) + 1e-14
        late = [tans[k + 1] / tans[k] for k in range(len(tans) - 1) if 1e-10 < tans[k + 1] < 1e-4]
        assert late
        observed = late[-1]
        assert abs(observed - ratio) <= 0.03 * ratio


def test_ritz_value_rate_is_squared():
    rng = random.Random(12)
    lams = [8.0, 4.0, 2.0, 0.5, 0.25]
    a, _ = build(lams, rng)
    r = subspace_iteration(a, 2, tol=1e-14, seed=1)
    err = [abs(h[1] - lams[1]) for h in r.history]
    pairs = [err[k + 1] / err[k] for k in range(len(err) - 1) if 1e-12 < err[k + 1] and err[k] < 1e-3]
    assert pairs
    expected = (lams[2] / lams[1]) ** 2
    assert abs(pairs[-1] - expected) <= 0.05 * expected


def test_full_block_gives_trace_and_determinant():
    m = [[4, 1, -2, 2], [1, 2, 0, 1], [-2, 0, 3, -2], [2, 1, -2, -1]]
    a = [[float(x) for x in row] for row in m]
    c = charpoly(m)
    r = subspace_iteration(a, 4, tol=1e-12)
    assert r.converged and r.iterations == 1
    assert abs(sum(r.values) - float(-c[1])) <= 1e-12
    det = float(c[4])  # det(-A) = det(A) for n = 4
    prod = math.prod(r.values)
    assert abs(prod - det) <= 1e-11 * max(1.0, abs(det))


def test_equal_modulus_needs_a_larger_block():
    a = [[3.0, 0, 0], [0, -3.0, 0], [0, 0, 1.0]]
    r1 = subspace_iteration(a, 1, x0=[[1.0, 1.0, 1.0]], maxit=200)
    assert not r1.converged
    r2 = subspace_iteration(a, 2, x0=[[1.0, 1.0, 1.0], [1.0, -1.0, 0.5]], tol=1e-12)
    assert r2.converged
    assert sorted(r2.values) == pytest.approx([-3.0, 3.0], abs=1e-11)


def test_zero_and_rank_deficient_matrices():
    z = [[0.0] * 4 for _ in range(4)]
    r = subspace_iteration(z, 2)
    assert r.converged and r.iterations == 1 and r.values == [0.0, 0.0]
    d = [[5.0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    r = subspace_iteration(d, 2, tol=1e-12)
    assert r.converged
    assert r.values[0] == pytest.approx(5.0, abs=1e-12)
    assert abs(r.values[1]) <= 1e-12


def test_invariant_start_converges_at_once():
    rng = random.Random(4)
    a, vecs = build([5.0, 3.0, 1.0, 0.5], rng)
    r = subspace_iteration(a, 2, x0=[vecs[0], vecs[1]], tol=1e-12)
    assert r.converged and r.iterations == 1


def test_page_example():
    a = [[2.0, 1, 0], [1, 3, 1], [0, 1, 4]]
    r = subspace_iteration(a, 2, x0=[[1.0, 0, 0], [0, 1.0, 0]], tol=1e-12)
    assert r.history[0] == pytest.approx([(5 + 5**0.5) / 2, (5 - 5**0.5) / 2], abs=1e-12)
    assert r.history[1] == pytest.approx([4.095445, 1.904555], abs=1e-6)
    assert r.converged and r.iterations == 34
    assert r.values == pytest.approx([3 + 3**0.5, 3.0], abs=1e-11)


def test_bad_arguments():
    with pytest.raises(ValueError):
        subspace_iteration([[1.0]], 0)
    with pytest.raises(ValueError):
        subspace_iteration([[1.0]], 2)
    with pytest.raises(ValueError):
        subspace_iteration([[1.0, 0], [0, 1.0]], 1, maxit=0)
