# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mirror-descent/. The authors are listed in prov/41N7NJ.jsonl.

import math
import random

from mirror_descent import entropy_simplex, euclidean, kl, mirror_descent, weighted_average

TOL = 1e-9


def random_simplex(rng: random.Random, n: int) -> list[float]:
    w = [rng.expovariate(1.0) + 1e-12 for _ in range(n)]
    s = sum(w)
    return [a / s for a in w]


def matrix_game(rng: random.Random, n: int, m: int):
    """f(x) = max_j (A^T x)_j on the simplex: convex, nonsmooth, and ||subgradient||_inf <= max |A|."""
    a = [[rng.uniform(-1, 1) for _ in range(m)] for _ in range(n)]

    def f(x: list[float]) -> float:
        return max(sum(a[i][j] * x[i] for i in range(n)) for j in range(m))

    def sub(x: list[float]) -> list[float]:
        j = max(range(m), key=lambda c: sum(a[i][c] * x[i] for i in range(n)))
        return [a[i][j] for i in range(n)]

    g = max(abs(v) for row in a for v in row)
    return f, sub, g


def test_example_closed_form() -> None:
    c = [0.0, 1.0, 2.0]
    xs = mirror_descent(lambda x: c, *entropy_simplex(), [1 / 3] * 3, 0.5, 5)
    for k, x in enumerate(xs):
        w = [math.exp(-0.5 * k * ci) for ci in c]
        z = sum(w)
        assert all(abs(a - b / z) <= 1e-12 for a, b in zip(x, w))
    assert abs(xs[1][0] - 0.50648) <= 1e-5


def test_regret_bound_entropy_every_k_every_u() -> None:
    rng = random.Random(21)
    for trial in range(20):
        n, m = rng.randint(2, 6), rng.randint(2, 5)
        f, sub, g = matrix_game(rng, n, m)
        x0 = [1.0 / n] * n
        if trial % 2 == 0:
            steps = [math.sqrt(2 * math.log(n) / (g * g * 200))] * 200
        else:
            steps = [0.5 / math.sqrt(k + 1) for k in range(200)]
        xs = mirror_descent(sub, *entropy_simplex(), x0, lambda k: steps[k], 200)
        us = [[1.0 if i == j else 0.0 for i in range(n)] for j in range(n)]
        us += [random_simplex(rng, n) for _ in range(5)]
        for u in us:
            fu, d0 = f(u), kl(u, x0)
            assert d0 <= math.log(n) + TOL
            lhs, quad = 0.0, 0.0
            for k in range(200):
                lhs += steps[k] * (f(xs[k]) - fu)
                quad += steps[k] ** 2 * g * g / 2  # sigma = 1 for the entropy in the l1 norm
                assert lhs <= d0 + quad + TOL
                if k % 20 == 19:
                    avg = weighted_average(xs[: k + 1], steps[: k + 1])
                    assert f(avg) - fu <= (d0 + quad) / sum(steps[: k + 1]) + TOL


def test_entropic_step_minimizes_the_model() -> None:
    rng = random.Random(22)
    for _ in range(50):
        n = rng.randint(2, 6)
        x = random_simplex(rng, n)
        g = [rng.uniform(-2, 2) for _ in range(n)]
        eta = rng.uniform(0.05, 2.0)
        nxt = mirror_descent(lambda _: g, *entropy_simplex(), x, eta, 1)[1]
        assert abs(sum(nxt) - 1) <= 1e-12 and min(nxt) > 0

        def model(z: list[float], g=g, eta=eta, x=x) -> float:
            return eta * sum(a * b for a, b in zip(g, z)) + kl(z, x)

        best = model(nxt)
        for _ in range(30):
            assert best <= model(random_simplex(rng, n)) + TOL


def test_three_point_identity() -> None:
    rng = random.Random(23)
    for _ in range(100):
        n = rng.randint(2, 5)
        x, y, z = (random_simplex(rng, n) for _ in range(3))
        lhs = kl(x, y) + kl(y, z) - kl(x, z)
        rhs = sum((math.log(c) - math.log(b)) * (a - b) for a, b, c in zip(x, y, z))
        assert abs(lhs - rhs) <= 1e-9


def test_euclidean_geometry_is_projected_subgradient() -> None:
    rng = random.Random(24)
    clip = lambda v: [min(max(a, 0.0), 1.0) for a in v]  # noqa: E731
    p = [rng.uniform(-1, 2) for _ in range(4)]

    def sub(x: list[float]) -> list[float]:
        return [1.0 if a > b else -1.0 if a < b else 0.0 for a, b in zip(x, p)]

    xs = mirror_descent(sub, *euclidean(clip), [0.5] * 4, 0.05, 40)
    x = [0.5] * 4
    for k in range(40):
        x = clip([a - 0.05 * b for a, b in zip(x, sub(x))])
        assert xs[k + 1] == x


def test_zero_iterations() -> None:
    assert mirror_descent(lambda x: x, *entropy_simplex(), [0.5, 0.5], 0.1, 0) == [[0.5, 0.5]]
