# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gradient-descent/. The authors are listed in prov/WZ9ATZ.jsonl.

import math
import random

from gradient_descent import gradient_descent, norm

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

    def f(self, x):
        d = [xi - ci for xi, ci in zip(x, self.c)]
        return 0.5 * sum(d[i] * sum(self.a[i][j] * d[j] for j in range(len(d))) for i in range(len(d))) + self.fstar

    def grad(self, x):
        d = [xi - ci for xi, ci in zip(x, self.c)]
        return [sum(row[j] * d[j] for j in range(len(d))) for row in self.a]

    def coords(self, x):
        """The coordinates of x - c in the eigenvector basis."""
        d = [xi - ci for xi, ci in zip(x, self.c)]
        n = len(d)
        return [sum(self.q[i][t] * d[i] for i in range(n)) for t in range(n)]

    def nearest_minimizer_distance(self, x):
        z = self.coords(x)
        return math.sqrt(sum(zt * zt for zt, l in zip(z, self.lam) if l > 0))


def random_quadratic(rng, n, singular=False):
    lam = [rng.uniform(0.1, 10.0) for _ in range(n)]
    if singular and n > 1:
        lam[rng.randrange(n)] = 0.0
    c = [rng.uniform(-5, 5) for _ in range(n)]
    return Quadratic(lam, c, rng.uniform(-3, 3), rng)


def test_worked_example():
    grad = lambda x: [x[0], 10.0 * x[1]]
    f = lambda x: 0.5 * (x[0] ** 2 + 10.0 * x[1] ** 2)
    path = gradient_descent(grad, [10.0, 1.0], 0.1, 3)
    assert [round(f(x), 6) for x in path] == [55.0, 40.5, 32.805, 26.57205]
    path = gradient_descent(grad, [10.0, 1.0], 0.18, 2)
    assert abs(path[1][0] - 8.2) < TOL and abs(path[1][1] + 0.8) < TOL
    path = gradient_descent(grad, [10.0, 1.0], 0.21, 20)
    assert abs(path[-1][1]) > 1.0  # step above 2/L: the second coordinate grows by 1.1 per step


def test_stops_on_small_gradient():
    grad = lambda x: [2.0 * x[0]]
    assert gradient_descent(grad, [0.0], 0.1, 50, tol=1e-12) == [[0.0]]
    path = gradient_descent(grad, [1.0], 0.25, 100, tol=1e-6)
    assert len(path) < 101 and abs(2.0 * path[-1][0]) <= 1e-6
    assert gradient_descent(grad, [3.0], 0.1, 0) == [[3.0]]


def test_against_closed_form():
    rng = random.Random(7101)
    for _ in range(500):
        n = rng.randint(1, 5)
        q = random_quadratic(rng, n, singular=rng.random() < 0.3)
        x0 = [rng.uniform(-10, 10) for _ in range(n)]
        lmax = max(q.lam)
        alpha = rng.uniform(0.05, 1.9) / lmax
        k = rng.randint(0, 25)
        xk = gradient_descent(q.grad, x0, alpha, k)[-1]
        z0, zk = q.coords(x0), q.coords(xk)
        for t in range(n):
            expected = (1.0 - alpha * q.lam[t]) ** k * z0[t]
            assert abs(zk[t] - expected) <= 1e-7 * (1.0 + abs(z0[t]))


def test_convex_bound_every_iterate():
    rng = random.Random(7102)
    for _ in range(200):
        n = rng.randint(1, 6)
        q = random_quadratic(rng, n, singular=rng.random() < 0.5)
        x0 = [rng.uniform(-10, 10) for _ in range(n)]
        lip = max(q.lam)
        alpha = 1.0 / lip if rng.random() < 0.5 else rng.uniform(0.1, 1.0) / lip
        r = q.nearest_minimizer_distance(x0)
        path = gradient_descent(q.grad, x0, alpha, 60)
        gaps = [q.f(x) - q.fstar for x in path]
        dists = [q.nearest_minimizer_distance(x) for x in path]
        for k in range(1, len(path)):
            assert gaps[k] <= r * r / (2.0 * alpha * k) + TOL
            assert gaps[k] <= gaps[k - 1] + TOL
            assert dists[k] <= dists[k - 1] + TOL


def test_strongly_convex_bounds_every_iterate():
    rng = random.Random(7103)
    for _ in range(200):
        n = rng.randint(1, 6)
        q = random_quadratic(rng, n)
        mu, lip = min(q.lam), max(q.lam)
        x0 = [rng.uniform(-10, 10) for _ in range(n)]
        xstar = q.c
        r = norm([a - b for a, b in zip(x0, xstar)])
        path = gradient_descent(q.grad, x0, 1.0 / lip, 60)
        gap0 = q.f(x0) - q.fstar
        for k, x in enumerate(path):
            factor = (1.0 - mu / lip) ** k
            assert q.f(x) - q.fstar <= factor * gap0 + TOL
            assert norm([a - b for a, b in zip(x, xstar)]) ** 2 <= factor * r * r + TOL
        kappa = lip / mu
        path = gradient_descent(q.grad, x0, 2.0 / (mu + lip), 60)
        for k, x in enumerate(path):
            assert norm([a - b for a, b in zip(x, xstar)]) <= ((kappa - 1) / (kappa + 1)) ** k * r + TOL


def test_nonconvex_stationarity_bound():
    # f(x) = sum of x_i^2 + 3 sin^2 x_i is not convex, its second derivative lies in [-4, 8], so L = 8, and f* = 0.
    f = lambda x: sum(t * t + 3.0 * math.sin(t) ** 2 for t in x)
    grad = lambda x: [2.0 * t + 3.0 * math.sin(2.0 * t) for t in x]
    rng = random.Random(7104)
    for _ in range(100):
        x0 = [rng.uniform(-20, 20) for _ in range(rng.randint(1, 4))]
        path = gradient_descent(grad, x0, 1.0 / 8.0, 40)
        best = float("inf")
        for k in range(1, len(path)):
            best = min(best, norm(grad(path[k - 1])) ** 2)
            assert best <= 2.0 * 8.0 * (f(x0) - 0.0) / k + TOL
            assert f(path[k]) <= f(path[k - 1]) + TOL
