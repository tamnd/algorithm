# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rayleigh-quotient-iteration/. The authors are listed in prov/DCQZQB.jsonl.

import math
import random
from fractions import Fraction

from rayleigh_quotient_iteration import matvec, norm2, rqi, shifted_solve

U = 2.0**-53


def householder_orthogonal(n, rng, k=3):
    """An exactly orthogonal rational matrix: a product of k reflectors."""
    q = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for _ in range(k):
        v = [Fraction(rng.randint(-5, 5)) for _ in range(n)]
        vv = sum(t * t for t in v)
        if vv == 0:
            continue
        qv = [sum(q[i][j] * v[j] for j in range(n)) for i in range(n)]
        q = [[q[i][j] - 2 * qv[i] * v[j] / vv for j in range(n)] for i in range(n)]
    return q


def rational_inverse(m):
    n = len(m)
    a = [list(r) + [Fraction(int(i == j)) for j in range(n)] for i, r in enumerate(m)]
    for c in range(n):
        p = next(i for i in range(c, n) if a[i][c] != 0)
        a[c], a[p] = a[p], a[c]
        piv = a[c][c]
        a[c] = [t / piv for t in a[c]]
        for i in range(n):
            if i != c and a[i][c] != 0:
                f = a[i][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[c])]
    return [r[n:] for r in a]


def similar(v, lam, vi):
    n = len(lam)
    return [[float(sum(v[i][k] * lam[k] * vi[k][j] for k in range(n))) for j in range(n)] for i in range(n)]


def known_symmetric(lam, rng):
    q = householder_orthogonal(len(lam), rng)
    qt = [list(r) for r in zip(*q)]
    return similar(q, [Fraction(x) for x in lam], qt)


def known_nonsymmetric(lam, rng):
    n = len(lam)
    v = [[Fraction(rng.randint(-3, 3)) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        v[i][i] += 7  # strictly diagonally dominant, so nonsingular
    return similar(v, [Fraction(x) for x in lam], rational_inverse(v))


def fro(a):
    return math.sqrt(sum(abs(t) ** 2 for row in a for t in row))


def charpoly(a):
    """Exact coefficients c[0..n] of det(x I - A) (c[0] = 1), by Faddeev-LeVerrier in Fractions."""
    n = len(a)
    a = [[Fraction(t) for t in row] for row in a]
    c = [Fraction(1)]
    m = [[Fraction(0)] * n for _ in range(n)]
    for k in range(1, n + 1):
        am = [[sum(a[i][t] * m[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
        m = [[am[i][j] + (c[-1] if i == j else 0) for j in range(n)] for i in range(n)]
        am = [[sum(a[i][t] * m[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
        c.append(-sum(am[i][i] for i in range(n)) / k)
    return c


def newton_distance(c, z):
    """|p(z) / p'(z)|, a first-order distance from z to a simple root of p."""
    n = len(c) - 1
    p = sum(float(c[i]) * z ** (n - i) for i in range(n + 1))
    dp = sum(float(c[i]) * (n - i) * z ** (n - i - 1) for i in range(n))
    return abs(p / dp)


def orders(errs, floor):
    """Observed convergence orders log(e_{k+1}/e_k) / log(e_k/e_{k-1})."""
    e = [t for t in errs if t > floor]
    return [math.log(e[k + 1] / e[k]) / math.log(e[k] / e[k - 1]) for k in range(1, len(e) - 1)]


def test_page_example():
    a = [[2.0, 1.0, 0.0], [1.0, 3.0, 1.0], [0.0, 1.0, 4.0]]
    res = rqi(a, [1.0, 1.0, 1.0], tol=1e-14)
    lam = 3 + math.sqrt(3)
    want_err = [3.987e-01, 2.463e-02, 4.535e-06]
    want_res = [9.428e-01, 2.219e-01, 2.869e-03, 7.251e-09]
    for k, w in enumerate(want_err):
        assert abs((lam - res.history[k][0]) - w) <= 1e-3 * w
    for k, w in enumerate(want_res):
        assert abs(res.history[k][1] - w) <= 1e-3 * w
    assert res.converged and res.iterations == 4 and abs(res.value - lam) <= 4 * U * lam


def test_backward_error_and_known_spectrum_symmetric():
    rng = random.Random(1)
    for _ in range(60):
        n = rng.randint(2, 8)
        lam = rng.sample(range(-20, 21), n)
        a = known_symmetric(lam, rng)
        x0 = [rng.uniform(-1, 1) for _ in range(n)]
        res = rqi(a, x0, tol=1e-12)
        assert res.converged
        x, rho = res.vector, res.value
        r = [p - rho * q for p, q in zip(matvec(a, x), x)]
        assert norm2(r) <= 1e-12 * fro(a) * 1.0000001
        assert abs(norm2(x) - 1.0) <= 10 * n * U
        # Weyl: some eigenvalue lies within ||r|| of rho (plus the rounding of A).
        assert min(abs(rho - t) for t in lam) <= norm2(r) + 50 * n * U * fro(a)


def test_cubic_rate_symmetric():
    rng = random.Random(2)
    seen = []
    for _ in range(80):
        n = rng.randint(3, 8)
        lam = rng.sample(range(-30, 31), n)
        a = known_symmetric(lam, rng)
        res = rqi(a, [rng.uniform(-1, 1) for _ in range(n)], tol=1e-14)
        rho = res.value
        target = min(lam, key=lambda t: abs(t - rho))
        errs = [abs(h[0] - target) for h in res.history]
        seen += [o for o in orders(errs, 1e-11) if errs[0] < 1.0]
    # Asymptotically cubic: the observed orders from close starts cluster near 3.
    assert len(seen) >= 10
    seen.sort()
    assert 2.6 <= seen[len(seen) // 2] <= 3.6


def test_monotone_residuals_symmetric():
    # Theorem: for Hermitian A, ||r_{k+1}|| <= ||r_k|| in exact arithmetic.
    rng = random.Random(3)
    for _ in range(60):
        n = rng.randint(2, 8)
        b = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        a = [[b[i][j] + b[j][i] for j in range(n)] for i in range(n)]
        res = rqi(a, [rng.uniform(-1, 1) for _ in range(n)], tol=1e-13)
        rs = [h[1] for h in res.history]
        for k in range(len(rs) - 1):
            assert rs[k + 1] <= rs[k] * (1 + 1e-8) + 100 * n * U * fro(a)


def test_complex_hermitian():
    a = [[2.0, 1j, 0.0], [-1j, 3.0, 1.0], [0.0, 1.0, 4.0]]
    res = rqi(a, [1.0, 0.5j, 1.0], tol=1e-13)
    assert res.converged
    assert abs(res.value.imag) <= 1e-14
    # The eigenvalues are 3 and 3 +- sqrt(3), as in the real example (a diagonal unitary similarity).
    assert min(abs(res.value - t) for t in (3.0, 3 - math.sqrt(3), 3 + math.sqrt(3))) <= 1e-12


def test_nonsymmetric_quadratic_rate():
    rng = random.Random(4)
    seen = []
    for _ in range(40):
        n = rng.randint(3, 6)
        lam = rng.sample(range(-12, 13), n)
        a = known_nonsymmetric(lam, rng)
        res = rqi(a, [rng.uniform(-1, 1) for _ in range(n)], tol=1e-13)
        if not res.converged:
            continue
        target = min(lam, key=lambda t: abs(t - res.value))
        assert abs(res.value - target) <= 1e-9 * max(1, abs(target))
        errs = [abs(h[0] - target) for h in res.history]
        seen += [o for o in orders(errs, 1e-9) if errs[0] < 0.5]
    assert len(seen) >= 5
    seen.sort()
    assert 1.6 <= seen[len(seen) // 2] <= 2.5


def test_exact_characteristic_polynomial_integer_matrices():
    rng = random.Random(5)
    for _ in range(30):
        n = rng.randint(2, 6)
        b = [[rng.randint(-5, 5) for _ in range(n)] for _ in range(n)]
        a = [[b[i][j] + b[j][i] for j in range(n)] for i in range(n)]
        c = charpoly(a)
        res = rqi([[float(t) for t in r] for r in a], [rng.uniform(-1, 1) for _ in range(n)], tol=1e-13)
        assert res.converged
        tr = sum(a[i][i] for i in range(n))
        assert c[1] == -tr  # the trace check of the exact coefficients
        assert newton_distance(c, res.value) <= 1e-9 * max(1.0, fro(a))


def test_eigenvector_start_and_trivial_cases():
    res = rqi([[5.0]], [3.0])
    assert res.converged and res.value == 5.0 and res.iterations == 0
    res = rqi([[0.0, 0.0], [0.0, 0.0]], [1.0, 1.0])
    assert res.converged and res.value == 0.0
    res = rqi([[1.0, 0.0], [0.0, 4.0]], [0.0, 2.0])
    assert res.converged and res.value == 4.0 and res.iterations == 0


def test_singular_shift_is_handled():
    # A shift equal to an eigenvalue: the zero pivot is replaced by u ||A||_F and the
    # huge solution points along the eigenvector, which is what the iteration wants.
    a = [[2.0, 1.0], [1.0, 2.0]]
    y = shifted_solve(a, 3.0, [1.0, 0.0], U * fro(a))
    ny = norm2(y)
    assert ny >= 1e14 and abs(abs(y[0] / ny) - math.sqrt(0.5)) <= 1e-12 and abs(y[0] - y[1]) <= 1e-12 * ny
    res = rqi(a, [1.0, 0.9], tol=1e-14)
    assert res.converged and abs(res.value - 3.0) <= 4 * U * 3.0 and res.iterations <= 3


def test_symmetric_stagnation_on_a_measure_zero_start():
    # diag(1, 3), x0 = (1, 1): rho = 2 is the midpoint, the solve maps x to (-1, 1), and in exact
    # arithmetic rho stays 2 forever. In floating point the rounding error grows by about 3 per
    # step, so the iteration escapes only after many steps.
    a = [[1.0, 0.0], [0.0, 3.0]]
    res = rqi(a, [1.0, 1.0], tol=1e-12, maxit=12)
    assert not res.converged and all(abs(h[0] - 2.0) <= 1e-8 for h in res.history)
    res = rqi(a, [1.0, 1.0], tol=1e-12, maxit=100)
    assert res.converged and res.iterations >= 20
    res = rqi(a, [1.0, 1.001], tol=1e-12, maxit=20)  # a perturbed start converges
    assert res.converged and min(abs(res.value - 1.0), abs(res.value - 3.0)) <= 1e-12


def test_real_start_cannot_reach_complex_eigenvalues():
    a = [[1.0, -2.0], [2.0, 1.0]]  # eigenvalues 1 +- 2i
    res = rqi(a, [1.0, 0.3], tol=1e-12, maxit=30)
    assert not res.converged and all(abs(h[0] - 1.0) <= 1e-15 for h in res.history)
    res = rqi(a, [1.0, 0.3 + 0.2j], tol=1e-13)
    assert res.converged and min(abs(res.value - 1 - 2j), abs(res.value - 1 + 2j)) <= 1e-12


def test_defective_eigenvalue_converges_linearly():
    # Jordan block J_2(2): the eigenvalue error halves at each step (the ratio t -> 2t + 1/t).
    a = [[2.0, 1.0], [0.0, 2.0]]
    res = rqi(a, [0.3, 1.0], tol=0.0, maxit=25)
    errs = [abs(h[0] - 2.0) for h in res.history]
    for k in range(10, 20):
        assert abs(errs[k + 1] / errs[k] - 0.5) <= 0.01


def test_few_solves_are_needed():
    # Observed, not proved: from a random start a few solves give a residual at roundoff level.
    rng = random.Random(6)
    counts = []
    for _ in range(50):
        n = rng.randint(2, 10)
        b = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        a = [[b[i][j] + b[j][i] for j in range(n)] for i in range(n)]
        res = rqi(a, [rng.uniform(-1, 1) for _ in range(n)], tol=1e-13)
        assert res.converged
        counts.append(res.iterations)
    assert max(counts) <= 12 and sum(counts) / len(counts) <= 6
