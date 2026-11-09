# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proximal-gradient-method/. The authors are listed in prov/QWQCF9.jsonl.

import random

from proximal_gradient_method import lasso_parts, proximal_gradient, soft_threshold

TOL = 1e-9


def solve(m: list[list[float]], v: list[float]) -> list[float]:
    """Solve m w = v by Gaussian elimination with partial pivoting."""
    n = len(v)
    a = [row[:] + [v[i]] for i, row in enumerate(m)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(a[r][c]))
        a[c], a[p] = a[p], a[c]
        for r in range(c + 1, n):
            f = a[r][c] / a[c][c]
            for k in range(c, n + 1):
                a[r][k] -= f * a[c][k]
    w = [0.0] * n
    for c in range(n - 1, -1, -1):
        w[c] = (a[c][n] - sum(a[c][k] * w[k] for k in range(c + 1, n))) / a[c][c]
    return w


def make_lasso(rng: random.Random, m: int, n: int, lam: float):
    """A lasso problem whose unique solution x* is known, built from the optimality condition."""
    a = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(m)]
    xs = [rng.choice([0.0, rng.uniform(-3, 3)]) for _ in range(n)]
    s = [(1.0 if x > 0 else -1.0) if x != 0 else rng.uniform(-0.9, 0.9) for x in xs]
    ata = [[sum(a[i][p] * a[i][q] for i in range(m)) for q in range(n)] for p in range(n)]
    w = solve(ata, s)
    r = [lam * sum(a[i][j] * w[j] for j in range(n)) for i in range(m)]
    b = [sum(a[i][j] * xs[j] for j in range(n)) + r[i] for i in range(m)]
    lf = sum(x * x for row in a for x in row)  # ||A||_F^2 >= the largest eigenvalue of A^T A
    return a, b, xs, lf


def dist2(x: list[float], y: list[float]) -> float:
    return sum((p - q) ** 2 for p, q in zip(x, y))


def test_soft_threshold() -> None:
    assert soft_threshold([3.0, -0.5, 1.2], 1.0) == [2.0, 0.0, 1.2 - 1.0]
    assert soft_threshold([-4.0, 1.0, -1.0], 1.0) == [-3.0, 0.0, 0.0]
    assert soft_threshold([0.3], 0.0) == [0.3]


def test_soft_threshold_is_the_prox() -> None:
    rng = random.Random(7)
    for _ in range(200):
        x, tau = rng.uniform(-5, 5), rng.uniform(0, 2)
        p = soft_threshold([x], tau)[0]
        best = min((abs(u) * tau + 0.5 * (u - x) ** 2, u) for u in [i / 1000 for i in range(-6000, 6001)])
        assert abs(tau * abs(p) + 0.5 * (p - x) ** 2 - best[0]) <= 1e-6


def test_rate_at_every_iterate_on_lasso() -> None:
    rng = random.Random(2024)
    for _ in range(15):
        m, n = rng.randint(6, 10), rng.randint(2, 5)
        lam = rng.uniform(0.1, 2.0)
        a, b, xs, lf = make_lasso(rng, m, n, lam)
        obj, grad_f, prox_h = lasso_parts(a, b, lam)
        fstar = obj(xs)
        x0 = [rng.uniform(-4, 4) for _ in range(n)]
        r2 = dist2(x0, xs)
        it = proximal_gradient(grad_f, prox_h, x0, 1.0 / lf, 300)
        for k in range(1, len(it)):
            gap = obj(it[k]) - fstar
            assert gap >= -TOL
            assert gap <= lf * r2 / (2 * k) + TOL
            assert obj(it[k]) <= obj(it[k - 1]) + TOL
            assert dist2(it[k], xs) <= dist2(it[k - 1], xs) + TOL


def test_linear_rate_when_strongly_convex() -> None:
    rng = random.Random(5)
    for _ in range(20):
        n = rng.randint(1, 6)
        d = [rng.uniform(0.5, 3.0) for _ in range(n)]
        a = [[d[i] if i == j else 0.0 for j in range(n)] for i in range(n)]
        b = [rng.uniform(-5, 5) for _ in range(n)]
        lam = rng.uniform(0.0, 3.0)
        # With a diagonal A, coordinate i solves min 0.5 (d x - b)^2 + lam |x|.
        xs = [soft_threshold([b[i] * d[i]], lam)[0] / (d[i] * d[i]) for i in range(n)]
        _, grad_f, prox_h = lasso_parts(a, b, lam)
        lf, mu = max(x * x for x in d), min(x * x for x in d)
        x0 = [rng.uniform(-5, 5) for _ in range(n)]
        it = proximal_gradient(grad_f, prox_h, x0, 1.0 / lf, 80)
        for k, x in enumerate(it):
            assert dist2(x, xs) <= (1 - mu / lf) ** k * dist2(x0, xs) + TOL


def test_box_indicator_gives_projected_gradient() -> None:
    def grad_f(x: list[float]) -> list[float]:
        return [2 * (x[0] - 3), 2 * (x[1] + 2)]

    def box(v: list[float], t: float) -> list[float]:
        return [min(max(c, -1.0), 1.0) for c in v]

    it = proximal_gradient(grad_f, box, [0.0, 0.0], 0.25, 30)
    assert it[-1] == [1.0, -1.0]


def test_zero_iterations() -> None:
    it = proximal_gradient(lambda x: x, lambda v, t: v, [1.0, 2.0], 0.5, 0)
    assert it == [[1.0, 2.0]]
