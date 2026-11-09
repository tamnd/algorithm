# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nonlinear-conjugate-gradient/. The authors are listed in prov/R5V6FZ.jsonl.

import math
import random

import pytest

from nonlinear_conjugate_gradient import dot, nonlinear_conjugate_gradient, norm, strong_wolfe

TOL = 1e-9


def matvec(a, v):
    return [dot(row, v) for row in a]


def householder(v):
    s = dot(v, v)
    n = len(v)
    return [[(1.0 if i == j else 0.0) - 2.0 * v[i] * v[j] / s for j in range(n)] for i in range(n)]


def quadratic(rng, lam):
    """f(x) = 1/2 x^T A x - b^T x with A = Q diag(lam) Q^T positive definite."""
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


def log_cosh_problem(rng, n):
    """f(x) = sum_i a_i z_i^2 / 2 + b_i log cosh(z_i - c_i), z = Q x: smooth and strongly convex."""
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


def check_strong_wolfe(f, grad, x, alpha, d, g, c1, c2):
    y = [xi + alpha * di for xi, di in zip(x, d)]
    slope0 = dot(g, d)
    scale = 1.0 + abs(f(x))
    assert slope0 < 0.0
    assert alpha > 0.0
    assert f(y) <= f(x) + c1 * alpha * slope0 + TOL * scale
    assert abs(dot(grad(y), d)) <= -c2 * slope0 + TOL * (1.0 + norm(grad(y)) * norm(d))


def linear_cg(a, b, x0, steps):
    """Hestenes-Stiefel linear conjugate gradient for A x = b."""
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
    for rule in ("FR", "PR+"):
        path, record = nonlinear_conjugate_gradient(f, grad, [10.0, 1.0], rule, tol=1e-6)
        assert len(path) == 3
        assert math.isclose(record[0][0], 2.0 / 11.0, rel_tol=1e-12)
        assert math.isclose(record[1][0], 0.55, rel_tol=1e-12)
        assert math.isclose(path[1][0], 90.0 / 11.0, rel_tol=1e-12)
        assert math.isclose(path[1][1], -9.0 / 11.0, rel_tol=1e-12)
        assert norm(path[2]) <= 1e-12
    expected = {("FR", 0.1): 305, ("PR+", 0.1): 19, ("FR", 0.45): 74, ("PR+", 0.45): 21}
    for (rule, c2), steps in expected.items():
        path, record = nonlinear_conjugate_gradient(rosenbrock, rosenbrock_grad, [-1.2, 1.0], rule, 100000, 1e-6, c2=c2)
        assert len(path) - 1 == steps
        assert math.dist(path[-1], [1.0, 1.0]) <= 1e-5


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        nonlinear_conjugate_gradient(rosenbrock, rosenbrock_grad, [0.0, 0.0], "HS")
    with pytest.raises(ValueError):
        strong_wolfe(rosenbrock, rosenbrock_grad, [0.0, 0.0], 1.0, [-2.0, 0.0], [-1.0, 0.0])
    with pytest.raises(ValueError):
        strong_wolfe(rosenbrock, rosenbrock_grad, [0.0, 0.0], 1.0, [-2.0, 0.0], [1.0, 0.0], 0.5, 0.4)


def test_line_search_returns_strong_wolfe_steps():
    rng = random.Random(9101)
    shapes = [
        (lambda t: (t - 3.0) ** 2, lambda t: 2.0 * (t - 3.0)),
        (lambda t: (t - 0.01) ** 2, lambda t: 2.0 * (t - 0.01)),
        (lambda t: math.sqrt(1.0 + (t - 50.0) ** 2), lambda t: (t - 50.0) / math.sqrt(1.0 + (t - 50.0) ** 2)),
        (lambda t: t ** 4 - 3.0 * t ** 2 + t, lambda t: 4.0 * t ** 3 - 6.0 * t + 1.0),
        (lambda t: math.cos(3.0 * t) + 0.1 * t * t, lambda t: -3.0 * math.sin(3.0 * t) + 0.2 * t),
    ]
    for h, dh in shapes:
        for _ in range(50):
            x0 = rng.uniform(-2.0, 2.0)
            if dh(x0) == 0.0:
                continue
            d = -math.copysign(rng.uniform(0.01, 10.0), dh(x0))
            f = lambda x: h(x[0])
            grad = lambda x: [dh(x[0])]
            c1 = rng.choice([1e-4, 0.01, 0.05])
            c2 = rng.choice([0.1, 0.4, 0.9])
            alpha, f_a, g_a = strong_wolfe(f, grad, [x0], h(x0), [dh(x0)], [d], c1, c2)
            assert f_a == f([x0 + alpha * d])
            check_strong_wolfe(f, grad, [x0], alpha, [d], [dh(x0)], c1, c2)


def test_every_step_satisfies_strong_wolfe_and_descent():
    rng = random.Random(9102)
    for trial in range(60):
        n = rng.randint(1, 6)
        rule = rng.choice(["FR", "PR+"])
        c2 = rng.choice([0.1, 0.3, 0.45])
        if trial % 3 == 0:
            f, grad = rosenbrock, rosenbrock_grad
            x0 = [rng.uniform(-2, 2), rng.uniform(-1, 3)]
        elif trial % 3 == 1:
            lam = [rng.uniform(0.1, 100.0) for _ in range(n)]
            _, _, f, grad, _ = quadratic(rng, lam)
            x0 = [rng.uniform(-10, 10) for _ in range(n)]
        else:
            f, grad = log_cosh_problem(rng, n)
            x0 = [rng.uniform(-10, 10) for _ in range(n)]
        path, record = nonlinear_conjugate_gradient(f, grad, x0, rule, 3000, 1e-6, c2=c2)
        assert norm(grad(path[-1])) <= 1e-6
        for k, (alpha, d, g) in enumerate(record):
            assert dot(g, d) < 0.0
            check_strong_wolfe(f, grad, path[k], alpha, d, g, 1e-4, c2)
            assert f(path[k + 1]) <= f(path[k])


def test_fletcher_reeves_sufficient_descent_bound():
    """Al-Baali: with strong Wolfe steps and c2 < 1/2, every Fletcher-Reeves direction satisfies
    -1/(1 - c2) <= g_k^T d_k / ||g_k||^2 <= (2 c2 - 1)/(1 - c2)."""
    rng = random.Random(9103)
    for trial in range(60):
        n = rng.randint(2, 6)
        c2 = rng.choice([0.1, 0.25, 0.4, 0.49])
        if trial % 2 == 0:
            f, grad = rosenbrock, rosenbrock_grad
            x0 = [rng.uniform(-2, 2), rng.uniform(-1, 3)]
        else:
            f, grad = log_cosh_problem(rng, n)
            x0 = [rng.uniform(-10, 10) for _ in range(n)]
        path, record = nonlinear_conjugate_gradient(f, grad, x0, "FR", 500, 1e-8, c2=c2)
        for alpha, d, g in record:
            ratio = dot(g, d) / dot(g, g)
            assert -1.0 / (1.0 - c2) - 1e-9 <= ratio <= (2.0 * c2 - 1.0) / (1.0 - c2) + 1e-9


def test_quadratic_with_exact_steps_is_linear_cg():
    rng = random.Random(9104)
    for _ in range(100):
        n = rng.randint(1, 6)
        lam = [rng.uniform(1.0, 50.0) for _ in range(n)]
        a, b, f, grad, exact = quadratic(rng, lam)
        x0 = [rng.uniform(-10, 10) for _ in range(n)]
        reference = linear_cg(a, b, x0, n)
        g0 = norm(grad(x0))
        for rule in ("FR", "PR+"):
            path, record = nonlinear_conjugate_gradient(f, grad, x0, rule, n, 0.0, step=exact)
            for k in range(len(path)):
                assert math.dist(path[k], reference[k]) <= 1e-7 * (1.0 + norm(reference[k]))
            assert norm(grad(path[-1])) <= 1e-8 * g0
            for i in range(len(record)):
                for j in range(i):
                    di, dj = record[i][1], record[j][1]
                    gi, gj = record[i][2], record[j][2]
                    assert abs(dot(di, matvec(a, dj))) <= 1e-7 * norm(di) * norm(matvec(a, dj))
                    assert abs(dot(gi, gj)) <= 1e-7 * norm(gi) * norm(gj)


def test_terminates_in_number_of_distinct_eigenvalues():
    rng = random.Random(9105)
    for _ in range(60):
        n = rng.randint(3, 8)
        m = rng.randint(1, 3)
        values = [rng.uniform(1.0, 20.0) for _ in range(m)]
        lam = [values[i % m] for i in range(n)]
        _, _, f, grad, exact = quadratic(rng, lam)
        x0 = [rng.uniform(-10, 10) for _ in range(n)]
        g0 = norm(grad(x0))
        for rule in ("FR", "PR+"):
            path, _ = nonlinear_conjugate_gradient(f, grad, x0, rule, m, 0.0, step=exact)
            assert len(path) - 1 <= m
            assert norm(grad(path[-1])) <= 1e-8 * g0
