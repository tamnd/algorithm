# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kaczmarz-method/. The authors are listed in prov/3ES5VF.jsonl.

import math
import random
from fractions import Fraction as F

from kaczmarz_method import CSR, kaczmarz, residual


def dot(u, v):
    return sum(p * q for p, q in zip(u, v))


def matvec(a, x):
    return [dot(r, x) for r in a]


def householder(rng, k):
    v = [rng.gauss(0, 1) for _ in range(k)]
    s = dot(v, v)
    return [[(1.0 if i == j else 0.0) - 2 * v[i] * v[j] / s for j in range(k)] for i in range(k)]


def with_singular_values(rng, m, sv):
    """A = H1[:, :n] diag(sv) H2, exactly orthogonal up to rounding."""
    n = len(sv)
    h1, h2 = householder(rng, m), householder(rng, n)
    return [[sum(h1[i][k] * sv[k] * h2[k][j] for k in range(n)) for j in range(n)] for i in range(m)]


def exact_solve(a, b):
    n = len(a)
    mat = [[F(v) for v in row] + [F(bi)] for row, bi in zip(a, b)]
    for k in range(n):
        p = next(i for i in range(k, n) if mat[i][k] != 0)
        mat[k], mat[p] = mat[p], mat[k]
        for i in range(n):
            if i != k and mat[i][k] != 0:
                l = mat[i][k] / mat[k][k]
                mat[i] = [u - l * w for u, w in zip(mat[i], mat[k])]
    return [mat[i][n] / mat[i][i] for i in range(n)]


def test_page_example():
    seen = []
    kaczmarz([[F(1), F(0)], [F(1), F(1)]], [F(1), F(2)], maxit=2, tol=0,
             trace=lambda k, i, x: seen.append(tuple(x)))
    assert seen[:4] == [(1, 0), (F(3, 2), F(1, 2)), (1, F(1, 2)), (F(5, 4), F(3, 4))]


def test_exact_pythagoras_identity_500():
    # ||e_new||^2 = ||e_old||^2 - w (2 - w) (b_i - a_i x)^2 / ||a_i||^2, exactly.
    rng = random.Random(2024)
    for t in range(500):
        m, n = rng.randint(1, 5), rng.randint(1, 5)
        a = [[F(rng.randint(-5, 5)) for _ in range(n)] for _ in range(m)]
        xs = [F(rng.randint(-4, 4)) for _ in range(n)]
        b = matvec(a, xs)
        w = rng.choice([F(1), F(1, 2), F(3, 2), F(2)])
        prev = [F(0)] * n

        def tr(k, i, x):
            e_old = [p - q for p, q in zip(prev, xs)]
            e_new = [p - q for p, q in zip(x, xs)]
            r_old = b[i] - dot(a[i], prev)
            nn = dot(a[i], a[i])
            assert dot(e_new, e_new) == dot(e_old, e_old) - w * (2 - w) * r_old * r_old / nn
            if w == 1:
                assert dot(a[i], x) == b[i]
            prev[:] = x

        kaczmarz(a, b, relax=w, maxit=3, tol=0, order=rng.choice(["cyclic", "random"]),
                 seed=t, trace=tr)


def test_orthogonal_rows_one_sweep():
    h = [[1, 1, 1, 1], [1, -1, 1, -1], [1, 1, -1, -1], [1, -1, -1, 1]]
    for a in (h, [[2, 0, 0], [0, 3, 0], [0, 0, 5]], [[7]]):
        a = [[F(v) for v in r] for r in a]
        xs = [F(i + 1, 3) for i in range(len(a))]
        res = kaczmarz(a, matvec(a, xs), tol=0)
        assert res.x == xs and res.sweeps == 1 and res.status == "converged"


def test_two_rows_rate_is_cos_squared():
    rng = random.Random(8)
    for t in range(100):
        a = [[rng.uniform(-1, 1) for _ in range(2)] for _ in range(2)]
        c2 = dot(a[0], a[1]) ** 2 / (dot(a[0], a[0]) * dot(a[1], a[1]))
        if c2 > 0.9:
            continue
        xs = [1.0, -2.0]
        errs = []
        kaczmarz(a, matvec(a, xs), maxit=6, tol=0,
                 trace=lambda k, i, x: errs.append(math.dist(x, xs)) if i == 1 else None)
        for s in range(1, 5):
            if errs[s] > 1e-9:
                assert abs(errs[s] / errs[s - 1] - c2) < 1e-6


def test_randomized_expected_rate():
    # Strohmer and Vershynin: E||e_k||^2 <= (1 - sigma_min^2/||A||_F^2)^k ||e_0||^2.
    rng = random.Random(42)
    sv = [2.0, 1.5, 1.0, 0.7, 0.5]
    a = with_singular_values(rng, 20, sv)
    q = 1 - min(sv) ** 2 / sum(s * s for s in sv)
    xs = [rng.uniform(-1, 1) for _ in range(5)]
    b = matvec(a, xs)
    e0 = dot(xs, xs)
    ks = (20, 60, 100)
    sums = {k: 0.0 for k in ks}
    runs = 200
    for seed in range(runs):
        def tr(k, i, x):
            if k in sums:
                d = [p - q for p, q in zip(x, xs)]
                sums[k] += dot(d, d)
        kaczmarz(a, b, order="random", seed=seed, maxit=5, tol=0, trace=tr)
    for k in ks:
        assert sums[k] / runs <= q ** k * e0
    # iteration count against theory: k* = ceil(ln(1/eps)/ln(1/q)) steps
    eps = 1e-6
    kstar = math.ceil(math.log(1 / eps) / math.log(1 / q))
    res_steps = []
    for seed in range(50):
        r = kaczmarz(a, b, order="random", seed=seed, tol=1e-6, maxit=200)
        assert r.converged
        res_steps.append(r.steps)
    assert sum(res_steps) / len(res_steps) <= 2 * kstar


def test_noisy_system_converges_to_a_ball():
    # Needell (2010): E||x_k - x*|| <= (1 - 1/R)^(k/2) ||x0 - x*|| + sqrt(R) gamma.
    rng = random.Random(5)
    sv = [1.5, 1.0, 0.8]
    a = with_singular_values(rng, 30, sv)
    xs = [0.3, -0.7, 1.1]
    noise = [rng.uniform(-1e-3, 1e-3) for _ in range(30)]
    b = [v + e for v, e in zip(matvec(a, xs), noise)]
    R = sum(s * s for s in sv) / min(sv) ** 2
    gamma = max(abs(e) / math.sqrt(dot(r, r)) for e, r in zip(noise, a))
    tot = 0.0
    for seed in range(100):
        r = kaczmarz(a, b, order="random", seed=seed, maxit=20, tol=0)
        tot += math.dist(r.x, xs)
    assert tot / 100 <= math.sqrt(R) * gamma + 1e-9


def test_inconsistent_stagnates_and_relaxed_limit():
    r = kaczmarz([[1.0], [1.0]], [0.0, 2.0], maxit=50, tol=1e-8)
    assert r.status == "maxit" and not r.converged
    assert r.x == [2.0] and abs(r.history[-1] - 1.0) < 1e-15  # least squares x would be 1
    for w in (0.5, 0.1, 0.02):
        r = kaczmarz([[1.0], [1.0]], [0.0, 2.0], relax=w, maxit=5000, tol=0)
        assert abs(r.x[0] - 2 / (2 - w)) < 1e-9


def test_underdetermined_gives_minimum_norm():
    rng = random.Random(17)
    for t in range(40):
        m, n = rng.randint(1, 3), rng.randint(4, 6)
        a = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(m)]
        if any(all(v == 0 for v in row) for row in a):
            continue
        aat = [[dot(p, q) for q in a] for p in a]
        try:
            y = exact_solve(aat, [F(1)] * m)
        except StopIteration:
            continue
        b = [1.0] * m
        xmin = [float(sum(a[i][j] * y[i] for i in range(m))) for j in range(n)]
        r = kaczmarz([[float(v) for v in row] for row in a], b, tol=1e-13, maxit=20000)
        assert r.converged and math.dist(r.x, xmin) < 1e-8


def test_singular_systems():
    r = kaczmarz([[F(1), F(1)], [F(2), F(2)]], [F(1), F(2)], tol=0)
    assert r.converged and r.x == [F(1, 2), F(1, 2)]
    r = kaczmarz([[1.0, 1.0], [2.0, 2.0]], [1.0, 3.0], maxit=100)
    assert r.status == "maxit"


def test_hilbert_slow_but_monotone_error():
    n = 8
    a = [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]
    xs = [1.0] * n
    b = matvec(a, xs)
    errs = []
    r = kaczmarz(a, b, maxit=200, tol=1e-10, trace=lambda k, i, x: errs.append(math.dist(x, xs)))
    assert r.status == "maxit" and r.history[-1] > 1e-10
    assert all(errs[k + 1] <= errs[k] * (1 + 1e-12) + 1e-15 for k in range(len(errs) - 1))
    assert r.history[-1] < r.history[0]


def test_well_conditioned_float_backward_error_and_csr():
    rng = random.Random(99)
    for t in range(60):
        n = rng.randint(2, 8)
        a = [[rng.uniform(-1, 1) + (4 if i == j else 0) for j in range(n)] for i in range(n)]
        xs = [rng.uniform(-1, 1) for _ in range(n)]
        b = matvec(a, xs)
        r = kaczmarz(CSR.from_dense(a), b, tol=1e-13, maxit=5000)
        assert r.converged
        res = residual(a, b, r.x)
        eta = max(map(abs, res)) / (max(sum(map(abs, row)) for row in a) * max(map(abs, r.x)) + max(map(abs, b)))
        assert eta < 1e-12


def test_edge_cases():
    r = kaczmarz([[F(3)]], [F(6)], tol=0)
    assert r.x == [2] and r.sweeps == 1
    r = kaczmarz([[F(0), F(0)], [F(1), F(1)]], [F(0), F(4)], tol=0)
    assert r.converged and r.x == [2, 2]
    r = kaczmarz([[1.0, 2.0]], [0.0])
    assert r.converged and r.x == [0.0, 0.0]
