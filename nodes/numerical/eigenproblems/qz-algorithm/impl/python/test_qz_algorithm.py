# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/qz-algorithm/. The authors are listed in prov/WCHJ4Y.jsonl.

import math
import random
from fractions import Fraction

import pytest

from qz_algorithm import eigenvalues, frob, qz

U = 2.0**-53


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def ctrans(a):
    return [[a[j][i].conjugate() for j in range(len(a))] for i in range(len(a[0]))]


def rel_residual(a, q, s, z):
    r = mm(mm(q, s), ctrans(z))
    n = len(a)
    return math.sqrt(sum(abs(r[i][j] - a[i][j]) ** 2 for i in range(n) for j in range(n))) / max(frob(a), 1e-300)


def unitarity(q):
    g = mm(ctrans(q), q)
    n = len(q)
    return max(abs(g[i][j] - (i == j)) for i in range(n) for j in range(n))


def det_fraction(m):
    """Exact determinant by fraction Gaussian elimination."""
    a = [[Fraction(x) for x in row] for row in m]
    n = len(a)
    det = Fraction(1)
    for j in range(n):
        piv = next((i for i in range(j, n) if a[i][j] != 0), None)
        if piv is None:
            return Fraction(0)
        if piv != j:
            a[j], a[piv] = a[piv], a[j]
            det = -det
        det *= a[j][j]
        for i in range(j + 1, n):
            f = a[i][j] / a[j][j]
            for k in range(j, n):
                a[i][k] -= f * a[j][k]
    return det


def pencil_poly(a, b):
    """Exact coefficients c_0..c_n of p(x) = det(A - x B), by interpolation at x = 0..n."""
    n = len(a)
    af = [[Fraction(x) for x in row] for row in a]
    bf = [[Fraction(x) for x in row] for row in b]
    xs = list(range(n + 1))
    ys = [det_fraction([[af[i][j] - x * bf[i][j] for j in range(n)] for i in range(n)]) for x in xs]
    coeffs = [Fraction(0)] * (n + 1)
    for k, xk in enumerate(xs):  # Lagrange basis polynomials, expanded
        basis = [Fraction(1)]
        denom = Fraction(1)
        for m, xm in enumerate(xs):
            if m == k:
                continue
            basis = [Fraction(0)] + basis
            for i in range(len(basis) - 1):
                basis[i] -= xm * basis[i + 1]
            denom *= xk - xm
        for i in range(n + 1):
            coeffs[i] += ys[k] * basis[i] / denom
    return coeffs


def poly_from_roots(roots):
    """Coefficients c_0..c_d of prod (x - r), lowest first."""
    c = [1 + 0j]
    for r in roots:
        c = [0j] + c
        for i in range(len(c) - 1):
            c[i] -= r * c[i + 1]
    return c


def orthogonal_rational(n, rng, k=3):
    q = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for _ in range(k):
        v = [Fraction(rng.randint(-4, 4)) for _ in range(n)]
        if all(t == 0 for t in v):
            v[0] = Fraction(1)
        vv = sum(t * t for t in v)
        for row in q:
            s = sum(r * t for r, t in zip(row, v)) * 2 / vv
            for j in range(n):
                row[j] -= s * v[j]
    return q


def check_schur(a, b, r, c=10):
    n = len(a)
    assert r.converged
    assert rel_residual(a, r.q, r.s, r.z) <= c * max(n, 1) * U
    if frob(b) > 0:
        assert rel_residual(b, r.q, r.t, r.z) <= c * max(n, 1) * U
    assert unitarity(r.q) <= c * max(n, 1) * U
    assert unitarity(r.z) <= c * max(n, 1) * U
    for i in range(n):
        for j in range(i):
            assert r.s[i][j] == 0 and r.t[i][j] == 0


def test_backward_stability_many_seeds():
    for seed in range(40):
        rng = random.Random(seed)
        n = rng.randint(1, 9)
        a = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        b = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        if seed % 4 == 0:
            for i in range(n):
                b[i][0] = 0.0  # B singular: at least one infinite eigenvalue
        check_schur(a, b, qz(a, b))


def test_exact_pencil_polynomial_and_determinants():
    for seed in range(16):
        rng = random.Random(500 + seed)
        n = rng.randint(2, 6)
        a = [[float(rng.randint(-5, 5)) for _ in range(n)] for _ in range(n)]
        b = [[float(rng.randint(-5, 5)) for _ in range(n)] for _ in range(n)]
        if seed % 3 == 0:
            b[n - 1] = [0.0] * n  # rank-deficient B
        c = pencil_poly(a, b)
        if all(x == 0 for x in c):
            continue  # a singular pencil; covered separately
        deg = max(i for i, x in enumerate(c) if x != 0)
        r = qz(a, b)
        check_schur(a, b, r)
        scale_b = max(abs(x) for x in r.beta)
        finite = [x for x, beta in zip(eigenvalues(r), r.beta) if abs(beta) > 1e-12 * scale_b]
        assert len(finite) == deg  # n - deg infinite eigenvalues
        mine = poly_from_roots(finite)
        lead = c[deg]
        exact = [complex(float(x / lead)) for x in c[: deg + 1]]
        size = max(abs(x) for x in exact)
        for u_, v_ in zip(mine, exact):
            assert abs(u_ - v_) <= 1e-8 * size
        # |det A| = |prod alpha| and |det B| = |prod beta|, since Q and Z are unitary
        da, db = det_fraction(a), det_fraction(b)
        pa = abs(math.prod(r.alpha))
        pb = abs(math.prod(r.beta))
        assert abs(pa - abs(float(da))) <= 1e-10 * max(1.0, abs(float(da)))
        assert abs(pb - abs(float(db))) <= 1e-10 * max(1.0, abs(float(db)))


def test_known_spectra_with_infinite_eigenvalues():
    for seed in range(10):
        rng = random.Random(900 + seed)
        n = rng.randint(2, 7)
        uq, vq = orthogonal_rational(n, rng), orthogonal_rational(n, rng)
        da = [Fraction(rng.randint(1, 9)) * rng.choice((-1, 1)) for _ in range(n)]
        db = [Fraction(rng.randint(1, 5)) for _ in range(n)]
        ninf = rng.randint(0, 2)
        for i in range(min(ninf, n)):
            db[i] = Fraction(0)
        sa = [[da[i] if i == j else (Fraction(rng.randint(-3, 3)) if j > i else Fraction(0)) for j in range(n)] for i in range(n)]
        sb = [[db[i] if i == j else (Fraction(rng.randint(-3, 3)) if j > i else Fraction(0)) for j in range(n)] for i in range(n)]
        a = [[float(x) for x in row] for row in mm(mm(uq, sa), vq)]
        b = [[float(x) for x in row] for row in mm(mm(uq, sb), vq)]
        r = qz(a, b)
        check_schur(a, b, r)
        scale = max(abs(x) for x in r.beta)
        got_inf = sum(1 for x in r.beta if abs(x) <= 1e-12 * scale)
        assert got_inf == min(ninf, n)
        want = sorted(float(x / y) for x, y in zip(da, db) if y != 0)
        got = sorted(x.real for x, beta in zip(eigenvalues(r), r.beta) if abs(beta) > 1e-12 * scale)
        assert got == pytest.approx(want, abs=1e-8 * max(abs(w) for w in want))


def test_identity_b_gives_ordinary_eigenvalues():
    a = [[0.0, -1.0], [1.0, 0.0]]
    r = qz(a, [[1.0, 0.0], [0.0, 1.0]])
    ev = sorted(eigenvalues(r), key=lambda z: z.imag)
    assert ev == [pytest.approx(-1j, abs=1e-14), pytest.approx(1j, abs=1e-14)]
    rng = random.Random(3)
    n = 6
    q = orthogonal_rational(n, rng)
    lam = [Fraction(k) for k in (5, 3, 2, -1, -4, 7)]
    a = [[float(sum(q[i][k] * lam[k] * q[j][k] for k in range(n))) for j in range(n)] for i in range(n)]
    r = qz(a, [[float(i == j) for j in range(n)] for i in range(n)])
    assert sorted(x.real for x in eigenvalues(r)) == pytest.approx(sorted(float(x) for x in lam), abs=1e-12)


def test_quadratic_convergence_of_the_subdiagonal():
    ratios = []
    steps = []
    for seed in range(30):
        rng = random.Random(seed)
        n = rng.randint(4, 9)
        a = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        b = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        r = qz(a, b)
        steps.append(r.iterations / n)
        h = r.history
        for (k1, e1), (k2, e2) in zip(h, h[1:]):
            if k1 == k2 and 1e-12 <= e1 <= 1e-4:
                ratios.append(e2 / e1**2)
    assert ratios
    ratios.sort()
    assert ratios[len(ratios) // 2] <= 10.0  # e_(k+1) = O(e_k^2): quadratic in the typical case
    assert sum(steps) / len(steps) <= 4.0  # typically 2 to 3 QZ steps per eigenvalue


def test_page_example():
    a = [[1.0, 2, 3], [4, 5, 6], [7, 8, 10]]
    b = [[1.0, 0, 0], [0, 1.0, 0], [0, 0, 0.0]]
    assert pencil_poly(a, b) == [-3, 9, 10, 0]
    r = qz(a, b)
    check_schur(a, b, r)
    ev = eigenvalues(r)
    assert math.isinf(ev[0].real)
    finite = sorted(x.real for x in ev[1:])
    assert finite == pytest.approx([(-9 - 201**0.5) / 20, (-9 + 201**0.5) / 20], abs=1e-14)
    assert r.iterations == 1
    rng = random.Random(1)
    n = 6
    a = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    b = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    r = qz(a, b)
    assert r.iterations == 16
    tail = [e for k, e in r.history if k == 5][3:]
    assert [float("%.1e" % e) for e in tail] == [4.1e-04, 9.7e-09, 1.5e-18]


def test_edge_cases():
    r = qz([[3.0]], [[2.0]])
    assert r.alpha[0] / r.beta[0] == 1.5 and r.iterations == 0
    tri_a = [[1.0, 2.0, 3.0], [0.0, 4.0, 5.0], [0.0, 0.0, 6.0]]
    tri_b = [[1.0, 1.0, 1.0], [0.0, 2.0, 1.0], [0.0, 0.0, 3.0]]
    r = qz(tri_a, tri_b)
    assert r.iterations == 0 and [x.real for x in eigenvalues(r)] == [1.0, 2.0, 2.0]
    r = qz([[1.0, 2.0], [3.0, 4.0]], [[0.0, 0.0], [0.0, 0.0]])
    assert all(x == 0 for x in r.beta)  # B = 0 and det A != 0: two infinite eigenvalues
    r = qz([[1.0, 0.0], [0.0, 0.0]], [[1.0, 0.0], [0.0, 0.0]])
    assert any(abs(x) <= 1e-15 and abs(y) <= 1e-15 for x, y in zip(r.alpha, r.beta))  # singular pencil
    with pytest.raises(ValueError):
        qz([[1.0, 2.0]], [[1.0]])
