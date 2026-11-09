# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coordinate-descent/. The authors are listed in prov/TFA12A.jsonl.

import random

from coordinate_descent import coordinate_descent, lasso_coordinate_descent

TOL = 1e-9


def dominant_quadratic(rng: random.Random, n: int):
    """f(x) = 0.5 x^T Q x - c^T x with Q strictly diagonally dominant.

    By Gershgorin, mu >= min_i (Q_ii - sum_{j != i} |Q_ij|), a valid strong convexity constant.
    """
    q = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            q[i][j] = q[j][i] = rng.uniform(-1, 1)
    margins = [rng.uniform(0.3, 2.0) for _ in range(n)]
    for i in range(n):
        q[i][i] = sum(abs(q[i][j]) for j in range(n) if j != i) + margins[i]
    c = [rng.uniform(-3, 3) for _ in range(n)]

    def f(x: list[float]) -> float:
        return 0.5 * sum(x[i] * q[i][j] * x[j] for i in range(n) for j in range(n)) - sum(a * b for a, b in zip(c, x))

    def partial(x: list[float], i: int) -> float:
        return sum(q[i][j] * x[j] for j in range(n)) - c[i]

    # The minimizer, from many cyclic sweeps (Gauss-Seidel converges for a dominant Q).
    xs, _ = coordinate_descent(partial, [q[i][i] for i in range(n)], [0.0] * n, 400 * n)
    return f, partial, q, min(margins), xs[-1]


def test_example_gauss_seidel() -> None:
    q, c = [[2.0, 1.0], [1.0, 2.0]], [3.0, -1.0]
    xs, chosen = coordinate_descent(lambda x, i: q[i][0] * x[0] + q[i][1] * x[1] - c[i], [2.0, 2.0], [0.0, 0.0], 4)
    assert chosen == [0, 1, 0, 1]
    assert xs[1] == [1.5, 0.0] and xs[2] == [1.5, -1.25]
    assert xs[3] == [2.125, -1.25] and xs[4] == [2.125, -1.5625]


def test_every_step_decreases_by_the_partial_squared() -> None:
    # For a quadratic and the step 1/Q_ii, f drops by exactly (d_i f)^2 / (2 Q_ii).
    rng = random.Random(41)
    for _ in range(20):
        n = rng.randint(1, 6)
        f, partial, q, _, _ = dominant_quadratic(rng, n)
        lips = [q[i][i] for i in range(n)]
        xs, chosen = coordinate_descent(partial, lips, [rng.uniform(-3, 3) for _ in range(n)], 60, random.Random(5))
        for k, i in enumerate(chosen):
            drop = partial(xs[k], i) ** 2 / (2 * lips[i])
            assert abs(f(xs[k]) - f(xs[k + 1]) - drop) <= 1e-9 * (1 + abs(f(xs[k])))


def test_expected_one_step_identity_by_enumeration() -> None:
    # E[f(x_(k+1)) | x_k] = f(x_k) - (1/n) sum_i (d_i f)^2 / (2 L_i) <= f(x_k) - ||grad f||^2 / (2 n L_max).
    rng = random.Random(42)
    for _ in range(30):
        n = rng.randint(1, 6)
        f, partial, q, _, _ = dominant_quadratic(rng, n)
        lips = [q[i][i] for i in range(n)]
        x = [rng.uniform(-3, 3) for _ in range(n)]
        after = []
        for i in range(n):
            y = list(x)
            y[i] -= partial(x, i) / lips[i]
            after.append(f(y))
        expected = sum(after) / n
        exact = f(x) - sum(partial(x, i) ** 2 / (2 * lips[i]) for i in range(n)) / n
        assert abs(expected - exact) <= 1e-9 * (1 + abs(exact))
        grad2 = sum(partial(x, i) ** 2 for i in range(n))
        assert expected <= f(x) - grad2 / (2 * n * max(lips)) + TOL


def test_expected_linear_rate_over_seeds() -> None:
    # The mean over 300 seeds must lie below (1 - mu/(n L_max))^k (f(x_0) - f*), with 10% slack for sampling.
    rng = random.Random(43)
    n = 4
    f, partial, q, mu, xstar = dominant_quadratic(rng, n)
    lips = [q[i][i] for i in range(n)]
    fstar = f(xstar)
    x0 = [3.0, -2.0, 1.0, 4.0]
    seeds, iters = 300, 40
    total = [0.0] * (iters + 1)
    for s in range(seeds):
        xs, _ = coordinate_descent(partial, lips, x0, iters, random.Random(1000 + s))
        for k, x in enumerate(xs):
            total[k] += f(x) - fstar
    rho = 1 - mu / (n * max(lips))
    for k in range(iters + 1):
        assert total[k] / seeds <= 1.1 * rho**k * (f(x0) - fstar) + 1e-9


def make_lasso(rng: random.Random, m: int, n: int, lam: float):
    """A lasso problem with a known unique solution, built from the optimality conditions."""
    a = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(m)]
    xs = [rng.choice([0.0, rng.uniform(-3, 3)]) for _ in range(n)]
    s = [(1.0 if x > 0 else -1.0) if x != 0 else rng.uniform(-0.9, 0.9) for x in xs]
    ata = [[sum(a[i][p] * a[i][q] for i in range(m)) for q in range(n)] for p in range(n)]
    # Solve A^T A w = s by Gaussian elimination.
    aug = [row[:] + [s[i]] for i, row in enumerate(ata)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(aug[r][col]))
        aug[col], aug[piv] = aug[piv], aug[col]
        for r in range(col + 1, n):
            t = aug[r][col] / aug[col][col]
            for k in range(col, n + 1):
                aug[r][k] -= t * aug[col][k]
    w = [0.0] * n
    for col in range(n - 1, -1, -1):
        w[col] = (aug[col][n] - sum(aug[col][k] * w[k] for k in range(col + 1, n))) / aug[col][col]
    b = [sum(a[i][j] * (xs[j] + lam * w[j]) for j in range(n)) for i in range(m)]

    def obj(x: list[float]) -> float:
        r = [sum(a[i][j] * x[j] for j in range(n)) - b[i] for i in range(m)]
        return 0.5 * sum(t * t for t in r) + lam * sum(abs(t) for t in x)

    return a, b, obj, xs


def test_lasso_monotone_coordinatewise_optimal_and_convergent() -> None:
    rng = random.Random(44)
    for _ in range(15):
        m, n = rng.randint(6, 10), rng.randint(2, 5)
        lam = rng.uniform(0.1, 2.0)
        a, b, obj, xstar = make_lasso(rng, m, n, lam)
        it = lasso_coordinate_descent(a, b, lam, [rng.uniform(-3, 3) for _ in range(n)], 300)
        for k in range(1, len(it)):
            assert obj(it[k]) <= obj(it[k - 1]) + TOL
        # Each update is the exact minimizer along its coordinate.
        for k in range(1, min(len(it), 4 * n)):
            j = (k - 1) % n
            base = obj(it[k])
            for t in (-0.3, -1e-3, 1e-3, 0.3):
                y = list(it[k])
                y[j] += t
                assert base <= obj(y) + TOL
        # After 300 sweeps the iterate is within 1e-6 of the known solution.
        assert max(abs(p - q) for p, q in zip(it[-1], xstar)) <= 1e-6


def test_nonsmooth_nonseparable_gets_stuck() -> None:
    def f(x: float, y: float) -> float:
        return x * x + y * y + 2 * abs(x - y)

    for k in range(-200, 201):
        t = k / 50
        assert f(1 + t, 1) >= f(1, 1) and f(1, 1 + t) >= f(1, 1)
    assert f(0, 0) < f(1, 1)


def test_zero_iterations() -> None:
    xs, chosen = coordinate_descent(lambda x, i: x[i], [1.0], [2.0], 0)
    assert xs == [[2.0]] and chosen == []
