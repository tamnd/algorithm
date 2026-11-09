# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/svrg/. The authors are listed in prov/F7HP8J.jsonl.

import math
import random

from svrg import full_gradient, svrg, svrg_direction

TOL = 1e-10


def solve(m: list[list[float]], r: list[float]) -> list[float]:
    """Gaussian elimination with partial pivoting for a small dense system."""
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


def ridge(n: int, d: int, lam: float, seed: int):
    """f_i(x) = (<a_i, x> - b_i)^2 / 2 + lam |x|^2 / 2, with x* from the normal equations."""
    r = random.Random(seed)
    a = [[r.uniform(-1, 1) for _ in range(d)] for _ in range(n)]
    b = [r.uniform(-2, 2) for _ in range(n)]

    def grad(i: int, x: list[float]) -> list[float]:
        res = sum(p * q for p, q in zip(a[i], x)) - b[i]
        return [res * p + lam * q for p, q in zip(a[i], x)]

    def f(x: list[float]) -> float:
        return sum((sum(p * q for p, q in zip(a[i], x)) - b[i]) ** 2 for i in range(n)) / (2 * n) + lam * sum(q * q for q in x) / 2

    h = [[sum(a[i][j] * a[i][k] for i in range(n)) / n + (lam if j == k else 0.0) for k in range(d)] for j in range(d)]
    rhs = [sum(a[i][j] * b[i] for i in range(n)) / n for j in range(d)]
    x_star = solve(h, rhs)
    big_l = max(sum(p * p for p in row) for row in a) + lam
    return grad, f, x_star, big_l, lam


def sq(u: list[float], v: list[float]) -> float:
    return sum((p - q) ** 2 for p, q in zip(u, v))


def test_example_trace() -> None:
    c, b = [1.0, 2.0, 3.0], [0.0, 1.0, 5.0]
    grad = lambda i, x: [c[i] * (x[0] - b[i])]  # noqa: E731
    out = svrg(grad, 3, [0.0], 0.08, 6, 1, random.Random(0), option="last", indices=[2, 0, 1, 2, 1, 0])
    assert abs(out[1][0] - 1.91641) <= 5e-6


def test_direction_is_unbiased_and_variance_is_bounded() -> None:
    n, d = 15, 3
    grad, f, x_star, big_l, _ = ridge(n, d, 0.3, 11)
    f_star = f(x_star)
    assert max(abs(g) for g in full_gradient(grad, n, x_star)) <= 1e-12  # x* is the solution
    r = random.Random(12)
    for _ in range(50):
        x = [r.uniform(-3, 3) for _ in range(d)]
        snap = [r.uniform(-3, 3) for _ in range(d)]
        mu = full_gradient(grad, n, snap)
        g = full_gradient(grad, n, x)
        vs = [svrg_direction(grad, i, x, snap, mu) for i in range(n)]
        mean = [sum(v[j] for v in vs) / n for j in range(d)]
        assert sq(mean, g) <= TOL  # exact invariant: the average over i is grad F(x)
        # Lemma 1: (1/n) sum |grad f_i(x) - grad f_i(x*)|^2 <= 2 L (F(x) - F*).
        lem = sum(sq(grad(i, x), grad(i, x_star)) for i in range(n)) / n
        assert lem <= 2 * big_l * (f(x) - f_star) + TOL
        # Lemma 2: E|v|^2 <= 4 L (F(x) - F*) + 4 L (F(snapshot) - F*).
        second = sum(sum(t * t for t in v) for v in vs) / n
        assert second <= 4 * big_l * (f(x) - f_star + f(snap) - f_star) + TOL


def test_one_step_inequality_by_enumeration() -> None:
    n, d = 12, 3
    grad, f, x_star, big_l, _ = ridge(n, d, 0.5, 21)
    f_star = f(x_star)
    eta = 1 / (10 * big_l)
    r = random.Random(22)
    for _ in range(50):
        x = [r.uniform(-3, 3) for _ in range(d)]
        snap = [r.uniform(-3, 3) for _ in range(d)]
        mu = full_gradient(grad, n, snap)
        lhs = sum(sq([p - eta * q for p, q in zip(x, svrg_direction(grad, i, x, snap, mu))], x_star) for i in range(n)) / n
        rhs = sq(x, x_star) - 2 * eta * (1 - 2 * big_l * eta) * (f(x) - f_star) + 4 * big_l * eta * eta * (f(snap) - f_star)
        assert lhs <= rhs + TOL


def test_linear_rate_option_two_monte_carlo() -> None:
    n, d = 20, 3
    grad, f, x_star, big_l, mu = ridge(n, d, 0.5, 31)
    f_star = f(x_star)
    kappa = big_l / mu
    eta, m = 1 / (10 * big_l), math.ceil(50 * kappa)
    alpha = 1 / (mu * eta * (1 - 2 * big_l * eta) * m) + 2 * big_l * eta / (1 - 2 * big_l * eta)
    assert alpha <= 0.5 + 1e-12
    x0, epochs, seeds = [2.0, -2.0, 1.5], 4, 60
    gap0 = f(x0) - f_star
    total = [0.0] * (epochs + 1)
    for t in range(seeds):
        snaps = svrg(grad, n, x0, eta, m, epochs, random.Random(4000 + t))
        for s, x in enumerate(snaps):
            total[s] += f(x) - f_star
    for s in range(epochs + 1):
        # The theorem bounds the expectation by alpha^s gap0; the mean of 60 runs gets 10% slack.
        assert total[s] / seeds <= 1.1 * alpha**s * gap0 + 1e-12


def test_solution_is_a_fixed_point() -> None:
    # Unlike SGD, every step from x* with snapshot x* is zero: the estimator has no variance there.
    n, d = 10, 3
    grad, _, x_star, big_l, _ = ridge(n, d, 0.4, 41)
    for option in ("last", "random"):
        snaps = svrg(grad, n, x_star, 1 / (4 * big_l), 30, 3, random.Random(42), option=option)
        assert all(sq(s, x_star) <= 1e-20 for s in snaps)


def test_zero_epochs_and_zero_inner_steps() -> None:
    grad = lambda i, x: [x[0]]  # noqa: E731
    assert svrg(grad, 2, [1.0], 0.1, 5, 0, random.Random(0)) == [[1.0]]
    assert svrg(grad, 2, [1.0], 0.1, 0, 2, random.Random(0)) == [[1.0], [1.0], [1.0]]
