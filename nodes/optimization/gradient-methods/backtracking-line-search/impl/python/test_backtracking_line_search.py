# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backtracking-line-search/. The authors are listed in prov/G81MN3.jsonl.

import math
import random

import pytest

from backtracking_line_search import backtracking_line_search, dot, gradient_descent_backtracking, norm

TOL = 1e-9


def householder(v):
    """The orthogonal matrix I - 2 v v^T / (v^T v)."""
    s = sum(t * t for t in v)
    n = len(v)
    return [[(1.0 if i == j else 0.0) - 2.0 * v[i] * v[j] / s for j in range(n)] for i in range(n)]


class Quadratic:
    """f(x) = 1/2 (x - c)^T A (x - c) + fstar with A = Q diag(lam) Q^T, so the eigenvalues are known."""

    def __init__(self, lam, c, fstar, rng):
        n = len(lam)
        self.q = householder([rng.uniform(-1, 1) + (0.1 if i == 0 else 0.0) for i in range(n)])
        self.lam, self.c, self.fstar = list(lam), list(c), fstar
        q = self.q
        self.a = [[sum(q[i][t] * lam[t] * q[j][t] for t in range(n)) for j in range(n)] for i in range(n)]
        self.L = max(lam)
        self.mu = min(lam)

    def f(self, x):
        d = [xi - ci for xi, ci in zip(x, self.c)]
        return 0.5 * sum(d[i] * sum(self.a[i][j] * d[j] for j in range(len(d))) for i in range(len(d))) + self.fstar

    def grad(self, x):
        d = [xi - ci for xi, ci in zip(x, self.c)]
        return [sum(row[j] * d[j] for j in range(len(d))) for row in self.a]

    def nearest_minimizer_distance(self, x):
        d = [xi - ci for xi, ci in zip(x, self.c)]
        n = len(d)
        z = [sum(self.q[i][t] * d[i] for i in range(n)) for t in range(n)]
        return math.sqrt(sum(zt * zt for zt, l in zip(z, self.lam) if l > 0))


def random_quadratic(rng, n, singular=False):
    lam = [rng.uniform(0.1, 10.0) for _ in range(n)]
    if singular and n > 1:
        lam[rng.randrange(n)] = 0.0
    c = [rng.uniform(-5, 5) for _ in range(n)]
    return Quadratic(lam, c, rng.uniform(-3, 3), rng)


def armijo_holds(f, x, fx, g, d, alpha, c):
    xn = [xi + alpha * di for xi, di in zip(x, d)]
    return f(xn) <= fx + c * alpha * dot(g, d)


def test_worked_example():
    f = lambda x: 0.5 * (x[0] ** 2 + 10.0 * x[1] ** 2)
    x, g = [10.0, 1.0], [10.0, 10.0]
    d = [-10.0, -10.0]
    assert backtracking_line_search(f, x, 55.0, g, d, 1.0, 0.5, 1e-4) == (0.25, 3)
    assert backtracking_line_search(f, x, 55.0, g, d, 1.0, 0.5, 0.5) == (0.125, 4)
    grad = lambda x: [x[0], 10.0 * x[1]]
    path, steps = gradient_descent_backtracking(f, grad, [10.0, 1.0], 1000, tol=1e-6)
    assert len(steps) == 65 and steps[:4] == [0.25, 0.125, 0.5, 0.125]
    path, steps = gradient_descent_backtracking(f, grad, [10.0, 1.0], 1000, c=0.5, tol=1e-6)
    assert len(steps) == 55


def test_rejects_bad_input():
    f = lambda x: x[0] ** 2
    with pytest.raises(ValueError):
        backtracking_line_search(f, [1.0], 1.0, [2.0], [1.0])
    with pytest.raises(ValueError):
        backtracking_line_search(f, [1.0], 1.0, [2.0], [0.0])
    with pytest.raises(ValueError):
        backtracking_line_search(f, [1.0], 1.0, [2.0], [-1.0], rho=1.0)
    with pytest.raises(ValueError):
        backtracking_line_search(f, [1.0], 1.0, [2.0], [-1.0], c=1.0)


def test_accepted_step_conditions():
    """Each accepted step meets the Armijo condition, the step before it fails it,
    the step is at least min(alpha0, 2 rho (1 - c) |g^T d| / (L ||d||^2)),
    and the number of trials is within the bound of the page."""
    rng = random.Random(8101)
    for _ in range(1000):
        n = rng.randint(1, 5)
        q = random_quadratic(rng, n, singular=rng.random() < 0.3)
        x = [rng.uniform(-10, 10) for _ in range(n)]
        g = q.grad(x)
        if norm(g) < 1e-8:
            continue
        d = [rng.gauss(0, 1) for _ in range(n)]
        if dot(g, d) > 0:
            d = [-t for t in d]
        if dot(g, d) > -1e-6 * norm(g) * norm(d):
            d = [-t for t in g]
        alpha0 = rng.choice([1.0, 0.3, 5.0, 100.0])
        rho = rng.choice([0.5, 0.1, 0.8])
        c = rng.choice([1e-4, 0.1, 0.5, 0.9])
        fx = q.f(x)
        alpha, trials = backtracking_line_search(q.f, x, fx, g, d, alpha0, rho, c)
        assert armijo_holds(q.f, x, fx, g, d, alpha, c)
        assert math.isclose(alpha, alpha0 * rho ** (trials - 1), rel_tol=1e-12)
        if trials > 1:
            assert not armijo_holds(q.f, x, fx, g, d, alpha / rho, c)
        slope, dd = -dot(g, d), dot(d, d)
        bound = 2.0 * (1.0 - c) * slope / (q.L * dd)
        assert alpha >= min(alpha0, rho * bound) * (1 - TOL)
        max_trials = 1 + max(0, math.ceil(math.log(alpha0 / bound) / math.log(1 / rho) - TOL))
        assert trials <= max_trials


def test_gradient_descent_convex_bound():
    """With c = 1/2 on convex quadratics: f(x_k) - f* <= R^2 / (2 sum of the first k steps)
    at every iterate, f does not increase, and the distance to the minimizer set does not increase."""
    rng = random.Random(8102)
    for _ in range(150):
        n = rng.randint(1, 5)
        q = random_quadratic(rng, n, singular=rng.random() < 0.4)
        x0 = [rng.uniform(-10, 10) for _ in range(n)]
        alpha0 = rng.choice([1.0, 10.0, 0.05])
        # Stop at a gradient norm of 1e-6, before the values of f reach the rounding level.
        path, steps = gradient_descent_backtracking(q.f, q.grad, x0, 60, alpha0=alpha0, rho=0.5, c=0.5, tol=1e-6)
        r2 = q.nearest_minimizer_distance(x0) ** 2
        alpha_min = min(alpha0, 0.5 / q.L)
        total = 0.0
        for k in range(1, len(path)):
            total += steps[k - 1]
            assert steps[k - 1] >= alpha_min * (1 - TOL)
            gap = q.f(path[k]) - q.fstar
            assert gap <= r2 / (2.0 * total) + TOL * (1 + abs(q.fstar))
            assert gap <= r2 / (2.0 * k * alpha_min) + TOL * (1 + abs(q.fstar))
            assert q.f(path[k]) <= q.f(path[k - 1]) + TOL * (1 + abs(q.fstar))
            assert q.nearest_minimizer_distance(path[k]) <= q.nearest_minimizer_distance(path[k - 1]) + TOL


def test_gradient_descent_strongly_convex_bound():
    """For every c: f(x_{k+1}) - f* <= (1 - 2 mu c alpha_k)(f(x_k) - f*) at every step."""
    rng = random.Random(8103)
    for _ in range(150):
        n = rng.randint(1, 5)
        q = random_quadratic(rng, n)
        x0 = [rng.uniform(-10, 10) for _ in range(n)]
        c = rng.choice([1e-4, 0.1, 0.5, 0.9])
        path, steps = gradient_descent_backtracking(q.f, q.grad, x0, 40, alpha0=1.0, rho=0.5, c=c, tol=1e-6)
        for k in range(1, len(path)):
            factor = 1.0 - 2.0 * q.mu * c * steps[k - 1]
            assert factor >= -TOL
            previous = q.f(path[k - 1]) - q.fstar
            assert q.f(path[k]) - q.fstar <= factor * previous + TOL * (1 + abs(q.fstar))


def test_nonconvex_stationarity():
    """f(x) = sum x_i^2 + 3 sin^2 x_i is 8-smooth and not convex, with f* = 0.
    Then min over i < k of ||grad f(x_i)||^2 <= (f(x_0) - f*) / (c * sum of steps)."""
    f = lambda x: sum(t * t + 3.0 * math.sin(t) ** 2 for t in x)
    grad = lambda x: [2.0 * t + 3.0 * math.sin(2.0 * t) for t in x]
    rng = random.Random(8104)
    for _ in range(100):
        n = rng.randint(1, 4)
        x0 = [rng.uniform(-6, 6) for _ in range(n)]
        c = rng.choice([1e-4, 0.3, 0.5])
        path, steps = gradient_descent_backtracking(f, grad, x0, 50, alpha0=1.0, rho=0.5, c=c)
        best, total = float("inf"), 0.0
        for k in range(1, len(path)):
            best = min(best, dot(grad(path[k - 1]), grad(path[k - 1])))
            total += steps[k - 1]
            assert steps[k - 1] >= min(1.0, 0.5 * 2.0 * (1 - c) / 8.0) * (1 - TOL)
            assert f(path[k]) <= f(path[k - 1]) + TOL
            assert best <= f(x0) / (c * total) + TOL
