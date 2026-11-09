# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/projected-gradient-descent/. The authors are listed in prov/XQJ388.jsonl.

import math
import random

from projected_gradient_descent import project_ball, project_box, project_simplex, projected_gradient_descent

TOL = 1e-9


def dot(x: list[float], y: list[float]) -> float:
    return sum(a * b for a, b in zip(x, y))


def dist2(x: list[float], y: list[float]) -> float:
    return sum((a - b) ** 2 for a, b in zip(x, y))


def random_spd(rng: random.Random, n: int) -> list[list[float]]:
    b = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)]
    return [[sum(b[k][i] * b[k][j] for k in range(n)) + (0.5 if i == j else 0.0) for j in range(n)] for i in range(n)]


def box_qp(rng: random.Random, n: int):
    """f(x) = 0.5 x^T Q x - c^T x on [0, 1]^n, with a known minimizer from the KKT conditions."""
    q = random_spd(rng, n)
    xs, g = [], []
    for _ in range(n):
        kind = rng.randrange(3)
        if kind == 0:
            xs.append(0.0)
            g.append(rng.uniform(0.1, 2.0))  # at the lower bound the gradient points up
        elif kind == 1:
            xs.append(1.0)
            g.append(-rng.uniform(0.1, 2.0))
        else:
            xs.append(rng.uniform(0.1, 0.9))
            g.append(0.0)
    c = [dot(q[i], xs) - g[i] for i in range(n)]

    def f(x: list[float]) -> float:
        return 0.5 * sum(x[i] * dot(q[i], x) for i in range(n)) - dot(c, x)

    def grad(x: list[float]) -> list[float]:
        return [dot(q[i], x) - c[i] for i in range(n)]

    lf = sum(v * v for row in q for v in row) ** 0.5  # Frobenius norm >= the largest eigenvalue
    return f, grad, xs, lf, q


def test_example() -> None:
    q, c = [[2.0, 1.0], [1.0, 2.0]], [3.0, -1.0]

    def grad(x: list[float]) -> list[float]:
        return [dot(q[i], x) - c[i] for i in range(2)]

    it = projected_gradient_descent(grad, project_box([0.0, 0.0], [1.0, 1.0]), [0.0, 1.0], 1.0 / 3.0, 3)
    assert all(abs(a - b) <= 1e-12 for a, b in zip(it[1], [2.0 / 3.0, 0.0]))
    assert it[2] == [1.0, 0.0] and it[3] == [1.0, 0.0]


def test_rate_monotone_and_fejer_on_box_qp() -> None:
    rng = random.Random(11)
    for _ in range(25):
        n = rng.randint(1, 6)
        f, grad, xs, lf, _ = box_qp(rng, n)
        box = project_box([0.0] * n, [1.0] * n)
        fstar = f(xs)
        x0 = [rng.uniform(0, 1) for _ in range(n)]
        r2 = dist2(x0, xs)
        it = projected_gradient_descent(grad, box, x0, 1.0 / lf, 200)
        for k in range(1, len(it)):
            assert all(0.0 <= v <= 1.0 for v in it[k])
            gap = f(it[k]) - fstar
            assert -TOL <= gap <= lf * r2 / (2 * k) + TOL
            assert f(it[k]) <= f(it[k - 1]) + TOL
            assert dist2(it[k], xs) <= dist2(it[k - 1], xs) + TOL


def test_linear_rate_with_strong_convexity() -> None:
    rng = random.Random(12)
    for _ in range(25):
        n = rng.randint(1, 5)
        d = [rng.uniform(0.5, 4.0) for _ in range(n)]
        target = [rng.uniform(-2, 2) for _ in range(n)]
        center, radius = [0.0] * n, 1.0

        def grad(x: list[float], d=d, target=target) -> list[float]:
            return [di * (xi - ti) for di, xi, ti in zip(d, x, target)]

        ball = project_ball(center, radius)
        lf, mu = max(d), min(d)
        # The minimizer over the ball, from a long run (the bound below is then checked at every k).
        xs = projected_gradient_descent(grad, ball, center, 1.0 / lf, 4000)[-1]
        x0 = ball([rng.uniform(-1, 1) for _ in range(n)])
        it = projected_gradient_descent(grad, ball, x0, 1.0 / lf, 60)
        for k, x in enumerate(it):
            assert dist2(x, xs) <= (1 - mu / lf) ** k * dist2(x0, xs) + 1e-12


def test_projected_subgradient_bound() -> None:
    # f(x) = ||x - p||_1 over the box [0, 1]^n; p may lie outside, so the minimizer is clip(p).
    rng = random.Random(13)
    for _ in range(20):
        n = rng.randint(1, 5)
        p = [rng.uniform(-1, 2) for _ in range(n)]
        box = project_box([0.0] * n, [1.0] * n)
        xs = box(p)
        fstar = sum(abs(a - b) for a, b in zip(xs, p))
        x0 = [rng.uniform(0, 1) for _ in range(n)]
        g_bound = math.sqrt(n)  # each subgradient has entries in [-1, 1]
        r = math.sqrt(dist2(x0, xs))
        k_total = 400
        eta = max(r, 1e-3) / (g_bound * math.sqrt(k_total))

        def sub(x: list[float], p=p) -> list[float]:
            return [1.0 if a > b else -1.0 if a < b else 0.0 for a, b in zip(x, p)]

        it = projected_gradient_descent(sub, box, x0, eta, k_total)
        best = min(sum(abs(a - b) for a, b in zip(x, p)) for x in it[:k_total])
        assert best - fstar <= (r * r + g_bound**2 * eta * eta * k_total) / (2 * eta * k_total) + TOL


def test_projection_properties() -> None:
    rng = random.Random(14)
    for _ in range(300):
        n = rng.randint(1, 6)
        v, w = [rng.uniform(-3, 3) for _ in range(n)], [rng.uniform(-3, 3) for _ in range(n)]
        lo = [rng.uniform(-2, 0) for _ in range(n)]
        hi = [a + rng.uniform(0, 2) for a in lo]
        sets = [
            (project_box(lo, hi), lambda: [rng.uniform(a, b) for a, b in zip(lo, hi)]),
            (project_ball(lo, 1.5), lambda: project_ball(lo, 1.5)([rng.uniform(-4, 4) for _ in range(n)])),
            (project_simplex, lambda: project_simplex([rng.uniform(-2, 2) for _ in range(n)])),
        ]
        for proj, sample in sets:
            p, q = proj(v), proj(w)
            assert dist2(p, q) <= dot([a - b for a, b in zip(p, q)], [a - b for a, b in zip(v, w)]) + TOL
            for _ in range(5):
                z = sample()  # a point of the set
                assert dot([a - b for a, b in zip(v, p)], [a - b for a, b in zip(z, p)]) <= 1e-9
            assert dist2(proj(p), p) <= TOL  # a projection is idempotent


def test_simplex_projection() -> None:
    assert all(abs(a - b) <= 1e-12 for a, b in zip(project_simplex([0.5, 1.2, -0.3]), [0.15, 0.85, 0.0]))
    p = project_simplex([0.2, 0.3, 0.1])
    assert abs(sum(p) - 1) <= 1e-12 and min(p) >= 0
    assert project_simplex([5.0]) == [1.0]


def test_zero_iterations_projects_the_start() -> None:
    it = projected_gradient_descent(lambda x: x, project_box([0.0], [1.0]), [3.0], 0.1, 0)
    assert it == [[1.0]]
