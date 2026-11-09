# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/limited-memory-bfgs/. The authors are listed in prov/AJV6AP.jsonl.

import math
import random

import pytest

from limited_memory_bfgs import dot, limited_memory_bfgs, norm, strong_wolfe, two_loop

TOL = 1e-9


def matvec(a, v):
    return [dot(row, v) for row in a]


def householder(v):
    s = dot(v, v)
    n = len(v)
    return [[(1.0 if i == j else 0.0) - 2.0 * v[i] * v[j] / s for j in range(n)] for i in range(n)]


def dense_matrix(pairs, n):
    """The BFGS recursion H <- (I - rho s y^T) H (I - rho y s^T) + rho s s^T, oldest pair first,
    from H = gamma I with gamma = s^T y / y^T y for the newest pair."""
    if pairs:
        s, y = pairs[-1]
        gamma = dot(s, y) / dot(y, y)
    else:
        gamma = 1.0
    h = [[gamma * float(i == j) for j in range(n)] for i in range(n)]
    for s, y in pairs:
        rho = 1.0 / dot(y, s)
        v = [[float(i == j) - rho * y[i] * s[j] for j in range(n)] for i in range(n)]
        hv = [[sum(h[i][t] * v[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
        h = [[sum(v[t][i] * hv[t][j] for t in range(n)) + rho * s[i] * s[j] for j in range(n)] for i in range(n)]
    return h


def cholesky_ok(a):
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
    n = len(lam)
    q = householder([rng.uniform(-1, 1) + (0.1 if i == 0 else 0.0) for i in range(n)])
    a = [[sum(q[i][t] * lam[t] * q[j][t] for t in range(n)) for j in range(n)] for i in range(n)]
    b = [rng.uniform(-5, 5) for _ in range(n)]
    f = lambda x: 0.5 * dot(x, matvec(a, x)) - dot(b, x)
    grad = lambda x: [u - v for u, v in zip(matvec(a, x), b)]
    exact = lambda x, g, d: -dot(g, d) / dot(d, matvec(a, d))
    return a, b, f, grad, exact


def rosenbrock(x):
    return 100.0 * (x[1] - x[0] ** 2) ** 2 + (1.0 - x[0]) ** 2


def rosenbrock_grad(x):
    return [-400.0 * x[0] * (x[1] - x[0] ** 2) - 2.0 * (1.0 - x[0]), 200.0 * (x[1] - x[0] ** 2)]


def extended_rosenbrock(x):
    return sum(100.0 * (x[2 * i + 1] - x[2 * i] ** 2) ** 2 + (1.0 - x[2 * i]) ** 2 for i in range(len(x) // 2))


def extended_rosenbrock_grad(x):
    g = [0.0] * len(x)
    for i in range(len(x) // 2):
        a, b = x[2 * i], x[2 * i + 1]
        g[2 * i] = -400.0 * a * (b - a * a) - 2.0 * (1.0 - a)
        g[2 * i + 1] = 200.0 * (b - a * a)
    return g


def log_cosh_problem(rng, n):
    q = householder([rng.uniform(-1, 1) + (0.1 if i == 0 else 0.0) for i in range(n)])
    av = [rng.uniform(0.1, 3.0) for _ in range(n)]
    bv = [rng.uniform(0.0, 20.0) for _ in range(n)]
    cv = [rng.uniform(-3, 3) for _ in range(n)]

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
    pairs = [([1.0, 0.0], [2.0, 1.0]), ([0.0, 1.0], [1.0, 4.0])]
    r = two_loop([1.0, 1.0], pairs)
    assert math.isclose(r[0], 57.0 / 136.0, rel_tol=1e-12)
    assert math.isclose(r[1], 79.0 / 544.0, rel_tol=1e-12)
    assert two_loop([1.0, 4.0], pairs) == pytest.approx([0.0, 1.0], abs=1e-15)
    r = two_loop([2.0, 1.0], pairs)
    assert math.dist(r, [1.0, 0.0]) > 0.02
    expected = {1: (45, 106), 3: (40, 75), 5: (39, 68), 10: (37, 64)}
    for memory, (steps, values) in expected.items():
        count = [0]

        def counted(x):
            count[0] += 1
            return rosenbrock(x)

        path, _ = limited_memory_bfgs(counted, rosenbrock_grad, [-1.2, 1.0], memory, tol=1e-6)
        assert (len(path) - 1, count[0] - 1) == (steps, values)
    rng = random.Random(5)
    x0 = [v + rng.uniform(-0.5, 0.5) for v in [-1.2, 1.0] * 50]
    for memory, steps in ((1, 139), (5, 239), (20, 145)):
        path, _ = limited_memory_bfgs(extended_rosenbrock, extended_rosenbrock_grad, x0, memory, 5000, 1e-6)
        assert len(path) - 1 == steps
        assert all(abs(v - 1.0) <= 1e-5 for v in path[-1])


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        limited_memory_bfgs(rosenbrock, rosenbrock_grad, [0.0, 0.0], 0)
    with pytest.raises(ValueError):
        strong_wolfe(rosenbrock, rosenbrock_grad, [0.0, 0.0], 1.0, [-2.0, 0.0], [-1.0, 0.0])


def test_two_loop_equals_dense_recursion():
    rng = random.Random(6301)
    assert two_loop([3.0, -1.0], []) == [3.0, -1.0]
    for _ in range(300):
        n = rng.randint(1, 6)
        ell = rng.randint(1, 6)
        pairs = []
        while len(pairs) < ell:
            s = [rng.uniform(-1, 1) for _ in range(n)]
            y = [rng.uniform(-1, 1) for _ in range(n)]
            if dot(y, s) < 0.0:
                y = [-t for t in y]
            if dot(y, s) > 0.05 * norm(y) * norm(s):
                pairs.append((s, y))
        q = [rng.uniform(-5, 5) for _ in range(n)]
        h = dense_matrix(pairs, n)
        r = two_loop(q, pairs)
        hq = matvec(h, q)
        scale = max(abs(v) for row in h for v in row) * norm(q)
        assert all(abs(u - v) <= 1e-9 * scale for u, v in zip(r, hq))
        assert cholesky_ok(h)
        s, y = pairs[-1]
        assert math.dist(two_loop(y, pairs), s) <= 1e-9 * (norm(s) + scale)


def test_every_step_wolfe_descent_and_memory():
    rng = random.Random(6302)
    for trial in range(60):
        n = rng.randint(1, 6)
        memory = rng.randint(1, 7)
        c2 = rng.choice([0.9, 0.5, 0.1])
        if trial % 3 == 0:
            f, grad = rosenbrock, rosenbrock_grad
            x0 = [rng.uniform(-2, 2), rng.uniform(-1, 3)]
            n = 2
        elif trial % 3 == 1:
            lam = [math.exp(rng.uniform(-2, 4)) for _ in range(n)]
            _, _, f, grad, _ = quadratic(rng, lam)
            x0 = [rng.uniform(-10, 10) for _ in range(n)]
        else:
            f, grad = log_cosh_problem(rng, n)
            x0 = [rng.uniform(-10, 10) for _ in range(n)]
        tol = 1e-7 * (1.0 + norm(grad(x0)))
        path, record = limited_memory_bfgs(f, grad, x0, memory, 2000, tol, c2=c2)
        assert norm(grad(path[-1])) <= tol
        for k, (alpha, d, g, pairs) in enumerate(record):
            assert len(pairs) <= memory
            assert all(dot(y, s) > 0.0 for s, y in pairs)
            assert cholesky_ok(dense_matrix(pairs, n))
            x, x_next = path[k], path[k + 1]
            slope0 = dot(g, d)
            assert slope0 < 0.0 and alpha > 0.0
            assert f(x_next) <= f(x) + 1e-4 * alpha * slope0 + TOL * (1.0 + abs(f(x)))
            g_next = grad(x_next)
            assert abs(dot(g_next, d)) <= -c2 * slope0 + TOL * (1.0 + norm(g_next) * norm(d))
            if k + 1 < len(record):
                newest = record[k + 1][3][-1]
                assert math.dist(newest[0], [u - v for u, v in zip(x_next, x)]) <= 1e-12 * (1.0 + norm(x_next))


def test_quadratic_exact_steps_match_linear_cg_for_every_memory():
    rng = random.Random(6303)
    for _ in range(60):
        n = rng.randint(1, 7)
        lam = [rng.uniform(1.0, 30.0) for _ in range(n)]
        a, b, f, grad, exact = quadratic(rng, lam)
        x0 = [rng.uniform(-10, 10) for _ in range(n)]
        reference = linear_cg(a, b, x0, n)
        g0 = norm(grad(x0))
        for memory in (1, 2, 5):
            path, _ = limited_memory_bfgs(f, grad, x0, memory, n, 0.0, step=exact)
            assert len(path) - 1 <= n
            for k in range(len(path)):
                assert math.dist(path[k], reference[k]) <= 1e-7 * (1.0 + norm(reference[k]))
            assert norm(grad(path[-1])) <= 1e-8 * g0
