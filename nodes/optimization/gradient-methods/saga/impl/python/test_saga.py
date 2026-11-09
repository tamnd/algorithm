# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/saga/. The authors are listed in prov/GYY34P.jsonl.

import random

from saga import saga, soft_threshold

TOL = 1e-9


def solve(m: list[list[float]], r: list[float]) -> list[float]:
    d = len(r)
    a = [row[:] + [r[i]] for i, row in enumerate(m)]
    for c in range(d):
        p = max(range(c, d), key=lambda k: abs(a[k][c]))
        a[c], a[p] = a[p], a[c]
        for k in range(c + 1, d):
            f = a[k][c] / a[c][c]
            a[k] = [u - f * v for u, v in zip(a[k], a[c])]
    x = [0.0] * d
    for c in reversed(range(d)):
        x[c] = (a[c][d] - sum(a[c][j] * x[j] for j in range(c + 1, d))) / a[c][c]
    return x


def is_positive_definite(h: list[list[float]]) -> bool:
    d = len(h)
    low = [[0.0] * d for _ in range(d)]
    for i in range(d):
        for j in range(i + 1):
            s = h[i][j] - sum(low[i][k] * low[j][k] for k in range(j))
            if i == j:
                if s <= 0:
                    return False
                low[i][i] = s**0.5
            else:
                low[i][j] = s / low[j][j]
    return True


def smallest_eigenvalue_lower_bound(h: list[list[float]]) -> float:
    """Bisection on t with the Cholesky test: H - t I is positive definite for the returned t."""
    lo, hi = 0.0, max(h[i][i] for i in range(len(h)))
    for _ in range(60):
        mid = (lo + hi) / 2
        if is_positive_definite([[h[i][j] - (mid if i == j else 0.0) for j in range(len(h))] for i in range(len(h))]):
            lo = mid
        else:
            hi = mid
    return lo


def least_squares_problem(n: int, x_star: list[float], lam: float, signs: list[float], seed: int):
    """f_i(x) = (<a_i, x> - b_i)^2 / 2 with b built so that x* solves min F + lam |x|_1 (KKT by construction).

    grad F(x*) = -lam * signs, with signs = sign(x*_j) on the support and |signs_j| < 1 off it.
    A residual orthogonal to the columns makes the component gradients at x* nonzero.
    """
    d = len(x_star)
    r = random.Random(seed)
    a = [[r.uniform(-1, 1) for _ in range(d)] for _ in range(n)]
    ata = [[sum(a[i][j] * a[i][k] for i in range(n)) for k in range(d)] for j in range(d)]
    w = solve(ata, signs)
    e = [r.uniform(-1, 1) for _ in range(n)]
    coef = solve(ata, [sum(a[i][j] * e[i] for i in range(n)) for j in range(d)])
    e_perp = [e[i] - sum(a[i][j] * coef[j] for j in range(d)) for i in range(n)]
    res = [-n * lam * sum(a[i][j] * w[j] for j in range(d)) + e_perp[i] for i in range(n)]
    b = [sum(a[i][j] * x_star[j] for j in range(d)) - res[i] for i in range(n)]

    def grad(i: int, x: list[float]) -> list[float]:
        t = sum(p * q for p, q in zip(a[i], x)) - b[i]
        return [t * p for p in a[i]]

    big_l = max(sum(p * p for p in row) for row in a)
    mu = smallest_eigenvalue_lower_bound([[v / n for v in row] for row in ata])
    return grad, big_l, mu


LASSO_X = [1.5, 0.0, -0.8]
LASSO_SIGNS = [1.0, 0.3, -1.0]


def sq(u: list[float], v: list[float]) -> float:
    return sum((p - q) ** 2 for p, q in zip(u, v))


def lyapunov(x, table, x_star, grads_star, gamma, n):
    dist = sum(sq(g, gs) for g, gs in zip(table, grads_star)) / n
    return sq(x, x_star) + 4 * gamma * gamma * n * dist


def test_example_trace() -> None:
    c, b = [1.0, 2.0, 3.0], [0.0, 1.0, 5.0]
    grad = lambda i, x: [c[i] * (x[0] - b[i])]  # noqa: E731
    xs = saga(grad, 3, [0.0], 1 / 18, 6, random.Random(0), indices=[2, 0, 1, 2, 1, 0])
    want = [0.0, 0.31481, 0.61214, 0.85311, 0.99724, 1.19337, 1.36921]
    for x, w in zip(xs, want):
        assert abs(x[0] - w) <= 5e-6


def test_table_average_equals_full_gradient_at_stored_points() -> None:
    n, lam = 25, 0.1
    grad, big_l, _ = least_squares_problem(n, LASSO_X, lam, LASSO_SIGNS, 7)
    x0 = [0.5, 0.5, 0.5]
    stored = [list(x0) for _ in range(n)]

    def check(k: int, j: int, x: list[float], table: list[list[float]], avg: list[float]) -> None:
        stored[j] = list(x)
        for i in range(n):
            assert sq(table[i], grad(i, stored[i])) <= 1e-24
        full = [sum(grad(i, stored[i])[c] for i in range(n)) / n for c in range(3)]
        assert sq(avg, full) <= TOL * TOL  # the running average has no drift

    saga(grad, n, x0, 1 / (6 * big_l), 500, random.Random(8), soft_threshold(lam), observer=check)


def test_direction_is_unbiased() -> None:
    n = 20
    grad, _, _ = least_squares_problem(n, LASSO_X, 0.1, LASSO_SIGNS, 9)
    r = random.Random(10)
    for _ in range(20):
        x = [r.uniform(-2, 2) for _ in range(3)]
        table = [grad(i, [r.uniform(-2, 2) for _ in range(3)]) for i in range(n)]
        avg = [sum(g[c] for g in table) / n for c in range(3)]
        mean_v = [sum(grad(j, x)[c] - table[j][c] + avg[c] for j in range(n)) / n for c in range(3)]
        full = [sum(grad(j, x)[c] for j in range(n)) / n for c in range(3)]
        assert sq(mean_v, full) <= TOL * TOL


def test_lyapunov_contraction_by_enumeration() -> None:
    # E Psi_(k+1) <= (1 - min(gamma mu, 1 / (2n))) Psi_k at every state, for the lasso and the smooth case.
    for lam, seed in ((0.1, 11), (0.0, 12)):
        n = 20
        grad, big_l, mu = least_squares_problem(n, LASSO_X, lam, LASSO_SIGNS, seed)
        gamma = 1 / (6 * big_l)
        rho = 1 - min(gamma * mu, 1 / (2 * n))
        prox = soft_threshold(lam)
        grads_star = [grad(i, LASSO_X) for i in range(n)]
        r = random.Random(seed + 100)
        for _ in range(30):
            x = [r.uniform(-3, 3) for _ in range(3)]
            table = [grad(i, [r.uniform(-3, 3) for _ in range(3)]) for i in range(n)]
            avg = [sum(g[c] for g in table) / n for c in range(3)]
            psi = lyapunov(x, table, LASSO_X, grads_star, gamma, n)
            total = 0.0
            for j in range(n):
                u = grad(j, x)
                v = [p - q + s for p, q, s in zip(u, table[j], avg)]
                new_x = prox([p - gamma * q for p, q in zip(x, v)], gamma)
                new_table = table[:j] + [u] + table[j + 1 :]
                total += lyapunov(new_x, new_table, LASSO_X, grads_star, gamma, n)
            assert total / n <= rho * psi + TOL


def test_linear_rate_on_lasso_monte_carlo() -> None:
    n, lam = 20, 0.1
    grad, big_l, mu = least_squares_problem(n, LASSO_X, lam, LASSO_SIGNS, 13)
    gamma = 1 / (6 * big_l)
    rho = 1 - min(gamma * mu, 1 / (2 * n))
    x0 = [-1.0, 2.0, 1.0]
    grads_star = [grad(i, LASSO_X) for i in range(n)]
    psi0 = lyapunov(x0, [grad(i, x0) for i in range(n)], LASSO_X, grads_star, gamma, n)
    iters, seeds = 400, 60
    total = [0.0] * (iters + 1)
    for t in range(seeds):
        xs = saga(grad, n, x0, gamma, iters, random.Random(500 + t), soft_threshold(lam))
        for k, x in enumerate(xs):
            total[k] += sq(x, LASSO_X)
    for k in range(iters + 1):
        # The theorem bounds E|x_k - x*|^2 by rho^k Psi_0; the mean of 60 runs gets 10% slack.
        assert total[k] / seeds <= 1.1 * rho**k * psi0 + 1e-12
    assert total[iters] / seeds <= 1e-6  # well inside the bound at the end; x* is the known solution


def test_solution_is_a_fixed_point() -> None:
    n, lam = 15, 0.1
    grad, big_l, _ = least_squares_problem(n, LASSO_X, lam, LASSO_SIGNS, 14)
    xs = saga(grad, n, LASSO_X, 1 / (6 * big_l), 200, random.Random(15), soft_threshold(lam))
    assert all(sq(x, LASSO_X) <= 1e-20 for x in xs)


def test_zero_iterations() -> None:
    assert saga(lambda i, x: [x[0]], 2, [1.0], 0.1, 0, random.Random(0)) == [[1.0]]
