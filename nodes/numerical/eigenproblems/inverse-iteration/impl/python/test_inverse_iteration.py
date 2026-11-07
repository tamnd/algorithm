# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverse-iteration/. The authors are listed in prov/GR2E1P.jsonl.

import cmath
import math
import random
from fractions import Fraction

from inverse_iteration import U, inverse_iteration, matvec, norm2, norm_frobenius


def charpoly(a):
    """Exact characteristic polynomial (Faddeev-LeVerrier in Fraction), leading coefficient first."""
    n = len(a)
    a = [[Fraction(t) for t in row] for row in a]
    m = [[Fraction(0)] * n for _ in range(n)]
    c = [Fraction(1)]
    for k in range(1, n + 1):
        am = [[sum(a[i][l] * m[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
        m = [[am[i][j] + (c[-1] if i == j else 0) for j in range(n)] for i in range(n)]
        am = [[sum(a[i][l] * m[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
        c.append(-sum(am[i][i] for i in range(n)) / k)
    return c


def poly_roots(c):
    """All roots of a polynomial by the Durand-Kerner iteration, then Newton polishing."""
    n = len(c) - 1
    c = [complex(t) / complex(c[0]) for t in c]
    z = [(0.4 + 0.9j) ** k for k in range(n)]
    for _ in range(400):
        for i in range(n):
            p = 0j
            for t in c:
                p = p * z[i] + t
            q = 1 + 0j
            for j in range(n):
                if j != i:
                    q *= z[i] - z[j]
            z[i] -= p / q
    return z


def random_orthogonal(n, rng):
    """A product of n Householder reflectors: orthogonal to rounding level."""
    q = [[float(i == j) for j in range(n)] for i in range(n)]
    for _ in range(n):
        v = [rng.gauss(0, 1) for _ in range(n)]
        vv = sum(t * t for t in v)
        q = [[q[i][j] - 2 * v[j] * sum(q[i][k] * v[k] for k in range(n)) / vv for j in range(n)] for i in range(n)]
    return q


def sym_from_spectrum(d, q):
    n = len(d)
    return [[sum(q[i][k] * d[k] * q[j][k] for k in range(n)) for j in range(n)] for i in range(n)]


def residual(a, theta, x):
    return norm2([t - theta * xi for t, xi in zip(matvec(a, x), x)])


def test_one_by_one():
    theta, x, k, ok = inverse_iteration([[3.5]], 1.0)
    assert ok and theta == 3.5 and abs(abs(x[0]) - 1) < 1e-15


def test_page_example():
    a = [[2.0, -1, 0, 0], [-1, 2, -1, 0], [0, -1, 2, -1], [0, 0, -1, 2]]
    theta, x, k, ok = inverse_iteration(a, 1.3, x0=[1.0, 0, 0, 0])
    lam = 2 - 2 * math.cos(2 * math.pi / 5)
    assert ok and abs(theta - lam) < 1e-14
    v = [math.sin(j * 2 * math.pi / 5) for j in range(1, 5)]
    c = abs(sum(p * q for p, q in zip(x, v))) / norm2(v)
    assert 1 - c < 1e-14


def test_toeplitz_every_eigenvalue():
    n = 12
    a = [[2.0 if i == j else (-1.0 if abs(i - j) == 1 else 0.0) for j in range(n)] for i in range(n)]
    for k in range(1, n + 1):
        lam = 2 - 2 * math.cos(k * math.pi / (n + 1))
        theta, x, _, ok = inverse_iteration(a, lam + 1e-3)
        assert ok and abs(theta - lam) < 1e-13
        assert residual(a, theta, x) <= 10 * n * U * norm_frobenius(a)


def test_diagonal_and_triangular():
    theta, x, _, ok = inverse_iteration([[1.0, 0, 0], [0, 2, 0], [0, 0, 3]], 2.9)
    assert ok and abs(theta - 3) < 1e-15 and abs(abs(x[2]) - 1) < 1e-12
    t = [[1.0, 5, -2], [0, 4, 7], [0, 0, -3]]
    theta, x, _, ok = inverse_iteration(t, 3.5)
    assert ok and abs(theta - 4) < 1e-13


def test_shift_equal_to_eigenvalue():
    theta, x, k, ok = inverse_iteration([[1.0, 0, 0], [0, 2, 0], [0, 0, 3]], 2.0)
    assert ok and abs(theta - 2) < 1e-15 and k <= 2


def test_zero_matrix():
    theta, x, k, ok = inverse_iteration([[0.0] * 3 for _ in range(3)], 0.5)
    assert ok and theta == 0 and k == 1


def test_random_symmetric_known_spectrum_and_rate():
    rng = random.Random(7101)
    for trial in range(20):
        n = rng.randint(2, 9)
        d = sorted(rng.uniform(-5, 5) for _ in range(n))
        q = random_orthogonal(n, rng)
        a = sym_from_spectrum(d, q)
        j = rng.randrange(n)
        sigma = d[j] + rng.uniform(-0.2, 0.2) * min([abs(d[j] - d[i]) for i in range(n) if i != j] + [1.0])
        theta, x, _, ok = inverse_iteration(a, sigma)
        assert ok, trial
        assert abs(theta - d[j]) < 1e-12 * max(1.0, max(abs(t) for t in d)), (trial, theta, d[j])
        assert residual(a, theta, x) <= 10 * n * U * norm_frobenius(a)


def test_observed_rate_matches_ratio():
    rng = random.Random(55)
    d = [1.0, 2.0, 4.0, 7.0]
    q = random_orthogonal(4, rng)
    a = sym_from_spectrum(d, q)
    v = [q[i][1] for i in range(4)]
    sigma = 2.3  # nearest eigenvalue 2, next 1: ratio 0.3 / 1.3
    x = [1.0, 1.0, 1.0, 1.0]
    sines = []
    for _ in range(6):
        _, x, _, _ = inverse_iteration(a, sigma, x0=x, kmax=1, tol=0.0)
        c = abs(sum(p * t for p, t in zip(x, v)))
        sines.append(math.sqrt(max(0.0, 1 - c * c)))
    ratio = 0.3 / 1.3
    for s0, s1 in zip(sines[1:4], sines[2:5]):
        assert abs(s1 / s0 - ratio) < 0.05


def test_random_nonsymmetric_against_charpoly():
    rng = random.Random(2024)
    for trial in range(15):
        n = rng.randint(2, 6)
        a = [[float(rng.randint(-5, 5)) for _ in range(n)] for _ in range(n)]
        roots = poly_roots(charpoly(a))
        for lam in roots:
            others = [abs(lam - mu) for mu in roots if mu is not lam]
            gap = min(others) if others else 1.0
            if gap < 1e-3:
                continue
            sigma = lam + 0.01 * gap * (1 + 1j) / math.sqrt(2)
            theta, x, _, ok = inverse_iteration([[complex(t) for t in row] for row in a], sigma, x0=[complex(1, 0.3 * k) for k in range(n)])
            assert ok, (trial, lam)
            assert abs(theta - lam) < 1e-9 * max(1.0, abs(lam)) / min(1.0, gap), (trial, theta, lam)


def test_complex_pair_needs_complex_shift():
    a = [[1.0, -2.0], [2.0, 1.0]]  # eigenvalues 1 +- 2i
    theta, x, _, ok = inverse_iteration([[complex(t) for t in row] for row in a], 1 + 1.9j, x0=[1 + 0j, 0j])
    assert ok and abs(theta - (1 + 2j)) < 1e-14
    theta, x, k, ok = inverse_iteration(a, 1.0, x0=[1.0, 0.0], kmax=50)
    assert not ok and k == 50  # a real shift is equally far from both: no convergence


def test_equal_distance_does_not_converge():
    a = [[1.0, 0.0], [0.0, 3.0]]
    theta, x, k, ok = inverse_iteration(a, 2.0, x0=[1.0, 1.0], kmax=30)
    assert not ok


def test_defective_jordan_block():
    a = [[2.0, 1.0], [0.0, 2.0]]
    theta, x, _, ok = inverse_iteration(a, 2.0 + 1e-8, x0=[0.6, 0.8])
    assert ok and abs(theta - 2) < 1e-7 and abs(x[1]) < 1e-6


def test_nearly_equal_eigenvalues():
    rng = random.Random(9)
    d = [1.0, 1.0 + 1e-6, 5.0]
    q = random_orthogonal(3, rng)
    a = sym_from_spectrum(d, q)
    theta, x, _, ok = inverse_iteration(a, 1.0 + 0.9e-6)
    assert ok and abs(theta - (1.0 + 1e-6)) < 1e-12
    v = [q[i][1] for i in range(3)]
    c = abs(sum(p * t for p, t in zip(x, v)))
    assert 1 - c < 1e-8
