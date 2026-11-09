# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bfgs/. The authors are listed in prov/54MPPW.jsonl.

import math
import random

import pytest

from bfgs import bfgs, bfgs_update, dot, matvec, norm, strong_wolfe

TOL = 1e-9


def identity(n):
    return [[float(i == j) for j in range(n)] for i in range(n)]


def householder(v):
    s = dot(v, v)
    n = len(v)
    return [[(1.0 if i == j else 0.0) - 2.0 * v[i] * v[j] / s for j in range(n)] for i in range(n)]


def cholesky_ok(a):
    """True if the symmetric matrix a has a Cholesky factor with positive pivots."""
    n = len(a)
    l = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            t = a[i][j] - sum(l[i][k] * l[j][k] for k in range(j))
            if i == j:
                if not t > 0.0:
                    return False
                l[i][i] = math.sqrt(t)
            else:
                l[i][j] = t / l[j][j]
    return True


def quadratic(rng, lam):
    """f(x) = 1/2 x^T A x - b^T x with A = Q diag(lam) Q^T positive definite."""
    n = len(lam)
    q = householder([rng.uniform(-1, 1) + (0.1 if i == 0 else 0.0) for i in range(n)])
    a = [[sum(q[i][t] * lam[t] * q[j][t] for t in range(n)) for j in range(n)] for i in range(n)]
    a_inv = [[sum(q[i][t] / lam[t] * q[j][t] for t in range(n)) for j in range(n)] for i in range(n)]
    b = [rng.uniform(-5, 5) for _ in range(n)]
    f = lambda x: 0.5 * dot(x, matvec(a, x)) - dot(b, x)
    grad = lambda x: [u - v for u, v in zip(matvec(a, x), b)]
    exact = lambda x, g, d: -dot(g, d) / dot(d, matvec(a, d))
    return a, a_inv, b, f, grad, exact


def rosenbrock(x):
    return 100.0 * (x[1] - x[0] ** 2) ** 2 + (1.0 - x[0]) ** 2


def rosenbrock_grad(x):
    return [-400.0 * x[0] * (x[1] - x[0] ** 2) - 2.0 * (1.0 - x[0]), 200.0 * (x[1] - x[0] ** 2)]


def log_cosh_problem(rng, n, shift=True):
    """f(x) = sum_i a_i z_i^2 / 2 + b_i log cosh(z_i - c_i), z = Q x: smooth and strongly convex.
    With shift=False, c = 0 and the minimizer is x* = 0."""
    q = householder([rng.uniform(-1, 1) + (0.1 if i == 0 else 0.0) for i in range(n)])
    av = [rng.uniform(0.1, 3.0) for _ in range(n)]
    bv = [rng.uniform(0.0, 20.0) for _ in range(n)]
    cv = [rng.uniform(-3, 3) if shift else 0.0 for _ in range(n)]

    def f(x):
        z = matvec(q, x)
        return sum(a * zi * zi / 2 + b * math.log1p(2.0 * math.sinh((zi - c) / 2) ** 2) for a, b, c, zi in zip(av, bv, cv, z))

    def grad(x):
        z = matvec(q, x)
        w = [a * zi + b * math.tanh(zi - c) for a, b, c, zi in zip(av, bv, cv, z)]
        return [sum(q[t][i] * w[t] for t in range(n)) for i in range(n)]

    return f, grad


def linear_cg(a, b, x0, steps):
    x = list(x0)
    r = [u - v for u, v in zip(matvec(a, x), b)]
    p = [-t for t in r]
    path = [list(x)]
    for _ in range(steps):
        ap = matvec(a, p)
        alpha = dot(r, r) / dot(p, ap)
        x = [xi + alpha * pi for xi, pi in zip(x, p)]
        r_new = [ri + alpha * t for ri, t in zip(r, ap)]
        beta = dot(r_new, r_new) / dot(r, r)
        p = [-u + beta * v for u, v in zip(r_new, p)]
        r = r_new
        path.append(list(x))
    return path


def test_worked_example():
    f = lambda x: 0.5 * (x[0] ** 2 + 10.0 * x[1] ** 2)
    grad = lambda x: [x[0], 10.0 * x[1]]
    path, record = bfgs(f, grad, [10.0, 1.0], tol=1e-6)
    assert len(path) == 4
    assert math.isclose(record[0][0], 2.0 / 11.0, rel_tol=1e-12)
    assert record[1][0] == 1.0 and record[2][0] == 1.0
    h2 = record[2][3]
    for i, row in enumerate([[1.0, 0.0], [0.0, 0.1]]):
        for j, v in enumerate(row):
            assert abs(h2[i][j] - v) <= 1e-12
    assert norm(path[3]) <= 1e-12
    path, _ = bfgs(f, grad, [10.0, 1.0], tol=1e-12, step=lambda x, g, d: -dot(g, d) / (d[0] ** 2 + 10.0 * d[1] ** 2))
    assert len(path) == 3 and norm(path[2]) <= 1e-12
    count = [0]

    def counted(x):
        count[0] += 1
        return rosenbrock(x)

    path, record = bfgs(counted, rosenbrock_grad, [-1.2, 1.0], tol=1e-8)
    assert len(path) - 1 == 37
    assert count[0] - 1 == 62
    assert sum(1 for r in record if r[0] == 1.0) == 27
    assert math.dist(path[-1], [1.0, 1.0]) <= 1e-11


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        bfgs_update(identity(2), [1.0, 0.0], [-1.0, 0.0])
    with pytest.raises(ValueError):
        strong_wolfe(rosenbrock, rosenbrock_grad, [0.0, 0.0], 1.0, [-2.0, 0.0], [-1.0, 0.0])


def test_update_secant_symmetry_and_positive_definiteness():
    rng = random.Random(7201)
    for _ in range(300):
        n = rng.randint(1, 6)
        q = householder([rng.uniform(-1, 1) + 0.1 for _ in range(n)])
        lam = [math.exp(rng.uniform(-3, 3)) for _ in range(n)]
        h = [[sum(q[i][t] * lam[t] * q[j][t] for t in range(n)) for j in range(n)] for i in range(n)]
        s = [rng.uniform(-1, 1) for _ in range(n)]
        y = [rng.uniform(-1, 1) for _ in range(n)]
        if dot(y, s) <= 1e-3 * norm(y) * norm(s):
            y = [-t for t in y]
        if dot(y, s) <= 1e-3 * norm(y) * norm(s):
            continue
        hp = bfgs_update(h, s, y)
        hy = matvec(hp, y)
        assert all(abs(u - v) <= 1e-9 * (1.0 + norm(s)) * max(lam) / min(lam) for u, v in zip(hy, s))
        assert all(abs(hp[i][j] - hp[j][i]) <= 1e-12 * (1.0 + abs(hp[i][j])) for i in range(n) for j in range(n))
        assert cholesky_ok(hp)
        rho = 1.0 / dot(y, s)
        left = [[float(i == j) - rho * s[i] * y[j] for j in range(n)] for i in range(n)]
        mid = [[sum(left[i][t] * h[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
        full = [[sum(mid[i][t] * left[j][t] for t in range(n)) + rho * s[i] * s[j] for j in range(n)] for i in range(n)]
        scale = max(abs(v) for row in full for v in row)
        assert all(abs(hp[i][j] - full[i][j]) <= 1e-10 * scale for i in range(n) for j in range(n))


def test_every_step_wolfe_curvature_and_positive_definite():
    rng = random.Random(7202)
    for trial in range(60):
        n = rng.randint(1, 6)
        c2 = rng.choice([0.9, 0.5, 0.1])
        if trial % 3 == 0:
            f, grad = rosenbrock, rosenbrock_grad
            x0 = [rng.uniform(-2, 2), rng.uniform(-1, 3)]
        elif trial % 3 == 1:
            lam = [math.exp(rng.uniform(-2, 4)) for _ in range(n)]
            _, _, _, f, grad, _ = quadratic(rng, lam)
            x0 = [rng.uniform(-10, 10) for _ in range(n)]
        else:
            f, grad = log_cosh_problem(rng, n)
            x0 = [rng.uniform(-10, 10) for _ in range(n)]
        path, record = bfgs(f, grad, x0, iterations=500, tol=1e-6, c2=c2)
        assert norm(grad(path[-1])) <= 1e-6
        for k, (alpha, d, g, h) in enumerate(record):
            x, x_next = path[k], path[k + 1]
            slope0 = dot(g, d)
            assert slope0 < 0.0 and alpha > 0.0
            assert cholesky_ok(h)
            assert f(x_next) <= f(x) + 1e-4 * alpha * slope0 + TOL * (1.0 + abs(f(x)))
            g_next = grad(x_next)
            assert abs(dot(g_next, d)) <= -c2 * slope0 + TOL * (1.0 + norm(g_next) * norm(d))
            s = [u - v for u, v in zip(x_next, x)]
            y = [u - v for u, v in zip(g_next, g)]
            assert dot(y, s) > 0.0
            if k + 1 < len(record):
                hy = matvec(record[k + 1][3], y)
                assert math.dist(hy, s) <= 1e-6 * (norm(s) + norm(hy))


def test_quadratic_exact_steps_terminate_with_inverse_hessian():
    rng = random.Random(7203)
    for _ in range(100):
        n = rng.randint(1, 6)
        lam = [rng.uniform(1.0, 30.0) for _ in range(n)]
        a, a_inv, b, f, grad, exact = quadratic(rng, lam)
        x0 = [rng.uniform(-10, 10) for _ in range(n)]
        g0 = norm(grad(x0))
        path, record = bfgs(f, grad, x0, iterations=n, tol=0.0, step=exact)
        assert len(path) - 1 <= n
        assert norm(grad(path[-1])) <= 1e-8 * g0
        steps = [[u - v for u, v in zip(path[k + 1], path[k])] for k in range(len(path) - 1)]
        for i in range(len(steps)):
            for j in range(i):
                si, sj = steps[i], steps[j]
                assert abs(dot(si, matvec(a, sj))) <= 1e-7 * norm(si) * norm(matvec(a, sj))
        if len(steps) == n:
            s = steps[-1]
            y = [u - v for u, v in zip(grad(path[-1]), grad(path[-2]))]
            if dot(y, s) > 0.0:
                h_n = bfgs_update(record[-1][3], s, y)
                scale = max(abs(v) for row in a_inv for v in row)
                assert all(abs(h_n[i][j] - a_inv[i][j]) <= 1e-6 * scale for i in range(n) for j in range(n))


def test_identity_start_with_exact_steps_matches_linear_cg():
    rng = random.Random(7204)
    for _ in range(100):
        n = rng.randint(1, 6)
        lam = [rng.uniform(1.0, 30.0) for _ in range(n)]
        a, _, b, f, grad, exact = quadratic(rng, lam)
        x0 = [rng.uniform(-10, 10) for _ in range(n)]
        reference = linear_cg(a, b, x0, n)
        path, _ = bfgs(f, grad, x0, h0=identity(n), iterations=n, tol=0.0, step=exact)
        for k in range(len(path)):
            assert math.dist(path[k], reference[k]) <= 1e-7 * (1.0 + norm(reference[k]))


def test_superlinear_rate_observed_on_strongly_convex_function():
    """Observed behaviour: on these strongly convex smooth functions with x* = 0 the last error ratios
    ||x_{k+1} - x*|| / ||x_k - x*|| are far below any fixed linear factor."""
    rng = random.Random(7205)
    for _ in range(30):
        n = rng.randint(2, 6)
        f, grad = log_cosh_problem(rng, n, shift=False)
        x0 = [rng.uniform(-3, 3) for _ in range(n)]
        path, _ = bfgs(f, grad, x0, iterations=500, tol=1e-10)
        errors = [norm(x) for x in path]
        tail = [errors[k + 1] / errors[k] for k in range(len(errors) - 1) if errors[k] < 1e-3 and errors[k + 1] > 0.0]
        assert tail and min(tail) <= 0.05
