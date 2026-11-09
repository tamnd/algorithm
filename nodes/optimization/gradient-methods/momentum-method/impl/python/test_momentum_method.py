# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/momentum-method/. The authors are listed in prov/MHMX5D.jsonl.

import math
import random

import pytest

from momentum_method import heavy_ball, heavy_ball_velocity, tuned_parameters

TOL = 1e-9


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def householder(v):
    """The orthogonal matrix I - 2 v v^T / (v^T v)."""
    s = sum(t * t for t in v)
    n = len(v)
    return [[(1.0 if i == j else 0.0) - 2.0 * v[i] * v[j] / s for j in range(n)] for i in range(n)]


def matvec(a, v):
    return [dot(row, v) for row in a]


def quadratic(rng, n, lam):
    """f(x) = 1/2 (x - c)^T A (x - c) with A = Q diag(lam) Q^T. Returns (f, grad, c, q)."""
    q = householder([rng.uniform(-1, 1) + (0.1 if i == 0 else 0.0) for i in range(n)])
    a = [[sum(q[i][t] * lam[t] * q[j][t] for t in range(n)) for j in range(n)] for i in range(n)]
    c = [rng.uniform(-5, 5) for _ in range(n)]

    def f(x):
        e = [xi - ci for xi, ci in zip(x, c)]
        return 0.5 * dot(e, matvec(a, e))

    def grad(x):
        return matvec(a, [xi - ci for xi, ci in zip(x, c)])

    return f, grad, c, q


def test_worked_example():
    alpha, beta = tuned_parameters(1.0, 10.0)
    assert math.isclose(alpha, 4.0 / (math.sqrt(10.0) + 1.0) ** 2, rel_tol=1e-15)
    assert math.isclose(math.sqrt(beta), (math.sqrt(10.0) - 1.0) / (math.sqrt(10.0) + 1.0), rel_tol=1e-12)
    grad = lambda x: [x[0], 10.0 * x[1]]
    path = heavy_ball(grad, [10.0, 1.0], alpha, beta, 1000, tol=1e-6)
    assert len(path) - 1 == 31
    assert abs(path[1][0] - 7.6911) < 1e-4 and abs(path[1][1] + 1.3089) < 1e-4
    assert abs(path[2][0] - 5.2923) < 1e-4 and abs(path[2][1] - 1.0900) < 1e-4
    grad2 = lambda x: [x[0], 1000.0 * x[1]]
    a2, b2 = tuned_parameters(1.0, 1000.0)
    assert len(heavy_ball(grad2, [10.0, 1.0], a2, b2, 100000, tol=1e-6)) - 1 == 435


def test_velocity_form_is_the_same_method():
    rng = random.Random(8301)
    for _ in range(50):
        n = rng.randint(1, 4)
        f, grad, c, _ = quadratic(rng, n, [rng.uniform(0.1, 5) for _ in range(n)])
        x0 = [rng.uniform(-5, 5) for _ in range(n)]
        alpha, beta = rng.uniform(0.01, 0.3), rng.uniform(0, 0.9)
        p1 = heavy_ball(grad, x0, alpha, beta, 30)
        p2 = heavy_ball_velocity(grad, x0, alpha, beta, 30)
        for u, v in zip(p1, p2):
            assert all(abs(a - b) <= 1e-9 * (1 + abs(a)) for a, b in zip(u, v))


def test_beta_zero_is_gradient_descent():
    grad = lambda x: [2.0 * x[0], 6.0 * x[1]]
    path = heavy_ball(grad, [1.0, 1.0], 0.1, 0.0, 5)
    x = [1.0, 1.0]
    for k in range(1, 6):
        x = [x[0] - 0.1 * 2.0 * x[0], x[1] - 0.1 * 6.0 * x[1]]
        assert all(math.isclose(a, b, rel_tol=1e-12) for a, b in zip(path[k], x))


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        heavy_ball(lambda x: x, [1.0], 0.0, 0.5, 3)
    with pytest.raises(ValueError):
        heavy_ball(lambda x: x, [1.0], 0.1, 1.0, 3)
    with pytest.raises(ValueError):
        tuned_parameters(0.0, 1.0)


def test_quadratic_bound_every_iterate():
    """With Polyak's parameters for [mu, L] containing the spectrum of A:
    ||x_k - x*|| <= (1 + (1 + rho) k) rho^k ||x_0 - x*||, rho = (sqrt(kappa) - 1)/(sqrt(kappa) + 1)."""
    rng = random.Random(8302)
    for _ in range(200):
        n = rng.randint(1, 6)
        lmax = rng.choice([1.0, 10.0, 100.0, 1000.0])
        lam = [rng.uniform(0.1, lmax) for _ in range(n)]
        mu = min(lam) * rng.choice([1.0, 1.0, 0.5])
        big_l = max(lam) * rng.choice([1.0, 1.0, 1.5])
        f, grad, c, _ = quadratic(rng, n, lam)
        alpha, beta = tuned_parameters(mu, big_l)
        rho = math.sqrt(beta)
        x0 = [rng.uniform(-10, 10) for _ in range(n)]
        r0 = math.dist(x0, c)
        path = heavy_ball(grad, x0, alpha, beta, 400)
        for k, x in enumerate(path):
            bound = (1.0 + (1.0 + rho) * k) * rho ** k * r0
            assert math.dist(x, c) <= bound + 1e-12 * (1 + r0)


def smooth_abs_function(rng, n):
    """f(x) = sum_i w_i h(z_i - c_i), z = Q x, h(t) = sqrt(1 + t^2) - 1.
    f is convex and L-smooth with L = max w_i (h'' <= 1), not strongly convex, and f* = 0 at x* = Q^T c."""
    q = householder([rng.uniform(-1, 1) + (0.1 if i == 0 else 0.0) for i in range(n)])
    w = [rng.uniform(0.2, 5.0) for _ in range(n)]
    c = [rng.uniform(-3, 3) for _ in range(n)]

    def f(x):
        z = matvec(q, x)
        return sum(wi * (math.sqrt(1.0 + (zi - ci) ** 2) - 1.0) for wi, zi, ci in zip(w, z, c))

    def grad(x):
        z = matvec(q, x)
        t = [wi * (zi - ci) / math.sqrt(1.0 + (zi - ci) ** 2) for wi, zi, ci in zip(w, z, c)]
        return [sum(q[s][i] * t[s] for s in range(n)) for i in range(n)]

    xstar = [sum(q[s][i] * c[s] for s in range(n)) for i in range(n)]
    return f, grad, max(w), xstar


def test_convex_average_bound_every_iterate():
    """For convex L-smooth f, 0 <= beta < 1 and 0 < alpha <= (1 - beta)/L:
    f(average of x_0..x_T) - f* <= ((1 - beta) R^2 / (2 alpha) + beta (f(x_0) - f*) / (1 - beta)) / (T + 1),
    and the same bound holds for min over k <= T of f(x_k) - f*."""
    rng = random.Random(8303)
    for trial in range(200):
        n = rng.randint(1, 5)
        if trial % 2 == 0:
            lam = [rng.uniform(0.1, 10.0) for _ in range(n)]
            if n > 1 and rng.random() < 0.5:
                lam[0] = 0.0
            f, grad, c, q = quadratic(rng, n, lam)
            big_l, fstar = max(lam), 0.0

            def dist_to_minimizers(x, c=c, q=q, lam=lam):
                e = [xi - ci for xi, ci in zip(x, c)]
                z = [sum(q[i][t] * e[i] for i in range(len(e))) for t in range(len(e))]
                return math.sqrt(sum(zt * zt for zt, l in zip(z, lam) if l > 0))

        else:
            f, grad, big_l, xstar = smooth_abs_function(rng, n)
            fstar = 0.0
            dist_to_minimizers = lambda x, xstar=xstar: math.dist(x, xstar)
        beta = rng.choice([0.0, 0.5, 0.9, rng.uniform(0, 0.99)])
        alpha = (1.0 - beta) / big_l * rng.choice([1.0, rng.uniform(0.1, 1.0)])
        x0 = [rng.uniform(-10, 10) for _ in range(n)]
        r2 = dist_to_minimizers(x0) ** 2
        gap0 = f(x0) - fstar
        path = heavy_ball(grad, x0, alpha, beta, 150)
        total = [0.0] * n
        best = float("inf")
        for t, x in enumerate(path):
            total = [s + xi for s, xi in zip(total, x)]
            avg = [s / (t + 1) for s in total]
            best = min(best, f(x) - fstar)
            bound = ((1.0 - beta) * r2 / (2.0 * alpha) + beta * gap0 / (1.0 - beta)) / (t + 1)
            assert f(avg) - fstar <= bound + TOL * (1 + bound)
            assert best <= bound + TOL * (1 + bound)


def test_lessard_recht_packard_cycle():
    """The function of Lessard, Recht and Packard (2016): mu = 1, L = 25, f* = 0 at x = 0.
    With alpha = 1/9 and beta = 4/9 (Polyak's parameters for [1, 25]) and x_0 = 3.3,
    the observed iterates end in a cycle of period 3 and do not converge."""

    def grad(x):
        t = x[0]
        if t < 1.0:
            return [25.0 * t]
        if t < 2.0:
            return [t + 24.0]
        return [25.0 * t - 24.0]

    alpha, beta = tuned_parameters(1.0, 25.0)
    assert math.isclose(alpha, 1.0 / 9.0) and math.isclose(beta, 4.0 / 9.0)
    path = heavy_ball(grad, [3.3], alpha, beta, 600)
    tail = [x[0] for x in path[-30:]]
    assert max(abs(t) for t in tail) > 2.0
    for i in range(len(tail) - 3):
        assert abs(tail[i] - tail[i + 3]) < 1e-9
    cycle = sorted(tail[-3:])
    assert [round(t, 4) for t in cycle] == [-1.8024, 0.6465, 2.1159]
    # From a start near the minimizer, where f is the quadratic 25 x^2 / 2, the method converges.
    assert abs(heavy_ball(grad, [0.5], alpha, beta, 600)[-1][0]) < 1e-12
