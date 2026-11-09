# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fista/. The authors are listed in prov/KTPH6E.jsonl.

import random

from fista import fista, soft_threshold

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
    b = [sum(a[i][j] * (xs[j] + lam * w[j]) for j in range(n)) for i in range(m)]
    lf = sum(x * x for row in a for x in row)  # an upper bound on L_f

    def obj(x: list[float]) -> float:
        r = [sum(a[i][j] * x[j] for j in range(n)) - b[i] for i in range(m)]
        return 0.5 * sum(t * t for t in r) + lam * sum(abs(t) for t in x)

    def grad(x: list[float]) -> list[float]:
        r = [sum(a[i][j] * x[j] for j in range(n)) - b[i] for i in range(m)]
        return [sum(a[i][j] * r[i] for i in range(m)) for j in range(n)]

    def prox(v: list[float], t: float) -> list[float]:
        return soft_threshold(v, t * lam)

    return obj, grad, prox, xs, lf


def dist2(x: list[float], y: list[float]) -> float:
    return sum((p - q) ** 2 for p, q in zip(x, y))


def test_momentum_sequence() -> None:
    _, taus = fista(lambda x: x, lambda v, t: v, [1.0], 0.5, 200)
    assert taus[0] == 1.0
    for k in range(1, len(taus)):
        t, s = taus[k - 1], taus[k]
        assert abs(s * s - s - t * t) <= 1e-9 * s * s  # t_(k+1)^2 - t_(k+1) = t_k^2
        assert taus[k - 1] >= (k + 1) / 2 - 1e-12  # t_k >= (k + 1) / 2


def test_rate_and_lyapunov_on_lasso() -> None:
    rng = random.Random(31)
    for _ in range(15):
        m, n = rng.randint(6, 10), rng.randint(2, 5)
        lam = rng.uniform(0.1, 2.0)
        obj, grad, prox, xs, lf = make_lasso(rng, m, n, lam)
        fstar = obj(xs)
        x0 = [rng.uniform(-4, 4) for _ in range(n)]
        r2 = dist2(x0, xs)
        it, taus = fista(grad, prox, x0, 1.0 / lf, 300)
        energy_prev = None
        for k in range(1, len(it)):
            gap = obj(it[k]) - fstar
            assert gap >= -TOL
            assert gap <= 2 * lf * r2 / (k + 1) ** 2 + TOL
            t = taus[k - 1]
            u = [t * p - (t - 1) * q - z for p, q, z in zip(it[k], it[k - 1], xs)]
            energy = t * t * gap + lf / 2 * sum(c * c for c in u)
            assert energy <= lf / 2 * r2 + 1e-7 * (1 + lf * r2)
            if energy_prev is not None:
                assert energy <= energy_prev + 1e-7 * (1 + energy_prev)
            energy_prev = energy


def test_not_monotone() -> None:
    # A badly conditioned quadratic: the momentum overshoots, so F goes up at some step.
    def grad(x: list[float]) -> list[float]:
        return [100.0 * x[0], 1.0 * x[1]]

    def obj(x: list[float]) -> float:
        return 50.0 * x[0] ** 2 + 0.5 * x[1] ** 2

    it, _ = fista(grad, lambda v, t: v, [1.0, 1.0], 1.0 / 100.0, 200)
    values = [obj(x) for x in it]
    assert any(values[k + 1] > values[k] for k in range(len(values) - 1))
    for k in range(1, len(it)):
        assert values[k] <= 2 * 100.0 * 2.0 / (k + 1) ** 2 + TOL


def test_one_step_equals_proximal_gradient() -> None:
    rng = random.Random(3)
    obj, grad, prox, xs, lf = make_lasso(rng, 8, 4, 0.7)
    x0 = [1.0, -2.0, 0.5, 3.0]
    it, _ = fista(grad, prox, x0, 1.0 / lf, 1)
    g = grad(x0)
    step = 1.0 / lf
    assert it[1] == prox([a - step * b for a, b in zip(x0, g)], step)


def test_zero_iterations() -> None:
    it, taus = fista(lambda x: x, lambda v, t: v, [2.0], 0.1, 0)
    assert it == [[2.0]] and taus == [1.0]
