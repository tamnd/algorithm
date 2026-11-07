# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minres/. The authors are listed in prov/NAYDFS.jsonl.

import math
import random
from fractions import Fraction

from minres import from_dense, interval_bound, matvec, minres, residual_norm

U = 2.0 ** -53


def diagop(d):
    return lambda v: [a * b for a, b in zip(d, v)]


def random_symmetric(rng, n, indefinite=True):
    """Q diag(d) Q^T with Q a product of random Givens rotations, so the spectrum is known."""
    d = [rng.uniform(1.0, 10.0) * (rng.choice([-1, 1]) if indefinite else 1) for _ in range(n)]
    a = [[d[i] if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(3 * n):
        p, q = rng.sample(range(n), 2)
        t = rng.uniform(0, 2 * math.pi)
        c, s = math.cos(t), math.sin(t)
        for row in a:  # a <- a G
            row[p], row[q] = c * row[p] - s * row[q], s * row[p] + c * row[q]
        a[p], a[q] = ([c * x - s * y for x, y in zip(a[p], a[q])],
                      [s * x + c * y for x, y in zip(a[p], a[q])])
    for i in range(n):  # symmetrize the rounding
        for j in range(i):
            a[i][j] = a[j][i] = (a[i][j] + a[j][i]) / 2
    return a, d


def exact_min_residual(a, b, k):
    """min ||b - A y||_2 over y in K_k(A, b), in exact rational arithmetic (x0 = 0)."""
    A = [[Fraction(v) for v in row] for row in a]
    r0 = [Fraction(v) for v in b]
    mv = lambda v: [sum(x * y for x, y in zip(row, v)) for row in A]
    K, v = [], r0
    for _ in range(k):
        K.append(v)
        v = mv(v)
    M = [mv(col) for col in K]  # columns A K
    g = [[sum(x * y for x, y in zip(M[i], M[j])) for j in range(k)] + [sum(x * y for x, y in zip(M[i], r0))]
         for i in range(k)]
    for c in range(k):  # Gauss-Jordan on the normal equations (M^T M is SPD here)
        piv = g[c][c]
        g[c] = [v / piv for v in g[c]]
        for i in range(k):
            if i != c and g[i][c] != 0:
                f = g[i][c]
                g[i] = [x - f * y for x, y in zip(g[i], g[c])]
    y = [g[i][k] for i in range(k)]
    rr = sum(v * v for v in r0) - sum(y[i] * sum(x * z for x, z in zip(M[i], r0)) for i in range(k))
    return math.sqrt(rr)


def test_one_by_one():
    x, k, conv = minres(from_dense([[-2.0]]), [4.0])
    assert conv and k == 1 and abs(x[0] + 2.0) <= 4 * U


def test_zero_rhs():
    x, k, conv = minres(from_dense([[1.0, 2.0], [2.0, -1.0]]), [0.0, 0.0])
    assert conv and k == 0 and x == [0.0, 0.0]


def test_hand_example_stagnates_then_solves():
    # A = [[0,1],[1,0]], b = e1: A b is orthogonal to b, so step 1 makes no progress.
    h = []
    x, k, conv = minres(from_dense([[0.0, 1.0], [1.0, 0.0]]), [1.0, 0.0], history=h)
    assert conv and k == 2
    assert h[0] == 1.0 and h[1] == 0.0
    assert x == [0.0, 1.0]


def test_matches_exact_minimal_residual():
    rng = random.Random(11)
    for trial in range(25):
        n = rng.randint(3, 7)
        a, _ = random_symmetric(rng, n)
        b = [rng.uniform(-1, 1) for _ in range(n)]
        h = []
        minres(from_dense(a), b, tol=0.0, maxiter=n - 1, history=h)
        nb = math.sqrt(sum(v * v for v in b))
        for k in range(1, len(h) + 1):
            ref = exact_min_residual(a, b, k)
            assert abs(h[k - 1] - ref) <= 1e-8 * nb, (trial, k)


def test_random_converges_and_error_bound():
    rng = random.Random(5)
    for trial in range(30):
        n = rng.randint(2, 25)
        a, d = random_symmetric(rng, n)
        xs = [rng.uniform(-1, 1) for _ in range(n)]
        b = matvec(from_dense(a), xs)
        h = []
        x, k, conv = minres(from_dense(a), b, tol=1e-10, history=h)
        assert conv
        assert all(h[i + 1] <= h[i] * (1 + 1e-12) for i in range(len(h) - 1))  # monotone
        nb = math.sqrt(sum(v * v for v in b))
        rel = residual_norm(from_dense(a), b, x) / nb
        assert rel <= 1e-9
        kappa = max(map(abs, d)) / min(map(abs, d))
        err = math.sqrt(sum((p - q) ** 2 for p, q in zip(x, xs))) / math.sqrt(sum(q * q for q in xs))
        assert err <= kappa * rel * 1.01 + 1e-14


def test_finite_termination_with_few_distinct_eigenvalues():
    vals = [-3.0, -1.0, 0.5, 2.0, 7.0]
    d = [vals[i % 5] for i in range(60)]
    rng = random.Random(2)
    b = [rng.uniform(0.5, 1.5) for _ in range(60)]
    x, k, conv = minres(diagop(d), b, tol=1e-12)
    assert conv and k <= 6


def test_iteration_counts_against_interval_bounds():
    # spectrum [c, d] (SPD) or [-d, -c] U [c, d], uniformly filled; b = ones
    for kap in (10.0, 100.0):
        N = 300
        spd = [1 + (kap - 1) * i / (N - 1) for i in range(N)]
        ind = [-v for v in spd] + spd
        for d, bound_k in ((spd, None), (ind, None)):
            b = [1.0] * len(d)
            h = []
            minres(diagop(d), b, tol=1e-8, history=h, maxiter=5000)
            r0 = math.sqrt(len(d))
            for k, rk in enumerate(h, start=1):
                if d is spd:
                    q = (math.sqrt(kap) - 1) / (math.sqrt(kap) + 1)
                    assert rk / r0 <= 2 * q ** k + 1e-12
                else:
                    assert rk / r0 <= interval_bound(1.0, kap, k) + 1e-12
        # the indefinite problem takes many more steps than the definite one
        k_spd = minres(diagop(spd), [1.0] * N, tol=1e-8)[1]
        k_ind = minres(diagop(ind), [1.0] * (2 * N), tol=1e-8, maxiter=5000)[1]
        assert k_ind > 3 * k_spd


def test_odd_steps_stagnate_for_symmetric_spectrum():
    d = [-(i + 1.0) for i in range(20)] + [i + 1.0 for i in range(20)]
    h = []
    minres(diagop(d), [1.0] * 40, tol=1e-10, history=h)
    r0 = math.sqrt(40)
    assert abs(h[0] - r0) <= 1e-12 * r0
    for j in range(1, 8):
        assert abs(h[2 * j] - h[2 * j - 1]) <= 1e-10 * r0


def test_singular_inconsistent_never_below_least_squares_residual():
    h = []
    x, k, conv = minres(from_dense([[1.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 0.0]]),
                        [1.0, 1.0, 1.0], maxiter=30, history=h)
    assert not conv and k == 2
    assert min(h) >= 1.0 - 1e-12  # dist(b, range A) = 1
    assert abs(residual_norm(from_dense([[1.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 0.0]]),
                             [1.0, 1.0, 1.0], x) - 1.0) <= 1e-12


def test_nonsymmetric_is_not_minimal():
    # GMRES solves this in 2 steps; MINRES assumes symmetry and does not.
    h = []
    x, k, conv = minres(from_dense([[1.0, 1.0], [0.0, 1.0]]), [0.0, 1.0], maxiter=10, history=h)
    assert not conv and h[1] > 0.5


def test_recurrence_residual_runs_below_true_residual():
    rng = random.Random(9)
    a, _ = random_symmetric(rng, 30)
    b = [rng.uniform(-1, 1) for _ in range(30)]
    h = []
    x, k, conv = minres(from_dense(a), b, tol=1e-22, maxiter=200, history=h)
    nb = math.sqrt(sum(v * v for v in b))
    true = residual_norm(from_dense(a), b, x) / nb
    assert min(h) / nb < 1e-18
    assert 1e-18 < true < 1e-11
