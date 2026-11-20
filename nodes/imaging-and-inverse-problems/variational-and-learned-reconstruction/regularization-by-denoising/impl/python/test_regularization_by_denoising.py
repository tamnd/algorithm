# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regularization-by-denoising/. The authors are listed in prov/K86DXS.jsonl.

import math
import random

from regularization_by_denoising import (
    matvec,
    red_fixed_point,
    red_gradient_descent,
    red_regularizer,
    red_regularizer_gradient,
    rmatvec,
    solve,
)

EYE2 = [[1.0, 0.0], [0.0, 1.0]]


def close(u, v, tol):
    return max(abs(p - q) for p, q in zip(u, v)) < tol


def fd_gradient(fun, x, h=1e-6):
    out = []
    for j in range(len(x)):
        xp, xm = list(x), list(x)
        xp[j] += h
        xm[j] -= h
        out.append((fun(xp) - fun(xm)) / (2 * h))
    return out


def seeded_problem(seed, n=6, m=4):
    rng = random.Random(seed)
    a = [[rng.gauss(0.0, 1.0) for _ in range(n)] for _ in range(m)]
    y = [rng.gauss(0.0, 1.0) for _ in range(m)]
    b = [[rng.gauss(0.0, 1.0) for _ in range(n)] for _ in range(n)]
    return rng, a, y, b


def test_hand_example_symmetric():
    w = [[0.5, 0.5], [0.5, 0.5]]
    d = lambda x: matvec(w, x)
    assert red_gradient_descent(EYE2, [1.0, 0.0], d, 1.0, 0.5, [0.0, 0.0], 1) == [0.5, 0.0]
    assert close(red_gradient_descent(EYE2, [1.0, 0.0], d, 1.0, 0.5, [0.0, 0.0], 3), [0.6875, 0.1875], 1e-15)
    assert close(red_gradient_descent(EYE2, [1.0, 0.0], d, 1.0, 0.5, [0.0, 0.0], 60), [0.75, 0.25], 1e-12)


def test_symmetric_linear_denoiser_gives_the_exact_gradient():
    rng, a, y, b = seeded_problem(1)
    n = 6
    # W = I - c B^T B is symmetric; the gradient of R is (I - W) x.
    btb = [[sum(b[k][i] * b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    w = [[(1.0 if i == j else 0.0) - 0.02 * btb[i][j] for j in range(n)] for i in range(n)]
    d = lambda x: matvec(w, x)
    x = [rng.gauss(0.0, 1.0) for _ in range(n)]
    g = fd_gradient(lambda z: red_regularizer(z, d), x)
    assert close(g, [xi - di for xi, di in zip(x, d(x))], 1e-7)
    # RED converges to the minimizer: (A^T A + lam (I - W)) x = A^T y.
    lam = 2.0
    m = [[sum(a[r][i] * a[r][j] for r in range(4)) + lam * 0.02 * btb[i][j]
          for j in range(n)] for i in range(n)]
    exact = solve(m, rmatvec(a, y))
    x_fp = red_fixed_point(a, y, d, lam, [0.0] * n, 3000)
    assert close(x_fp, exact, 1e-8)


def test_nonsymmetric_denoiser_does_not_minimize_the_red_objective():
    w = [[0.0, 1.0], [0.0, 1.0]]
    d = lambda x: matvec(w, x)
    y = [1.0, 0.0]
    x_gd = red_gradient_descent(EYE2, y, d, 1.0, 0.5, [0.0, 0.0], 50)
    x_fp = red_fixed_point(EYE2, y, d, 1.0, [0.0, 0.0], 50)
    assert close(x_gd, [0.5, 0.0], 1e-12) and close(x_fp, [0.5, 0.0], 1e-12)

    def objective(x):
        return 0.5 * ((x[0] - 1.0) ** 2 + x[1] ** 2) + red_regularizer(x, d)

    # The true minimizer solves (2I - (W + W^T)/2) x = y.
    best = [4.0 / 7.0, 2.0 / 7.0]
    assert close(fd_gradient(objective, best), [0.0, 0.0], 1e-8)
    assert abs(objective(x_gd) - 0.25) < 1e-12 and abs(objective(best) - 3.0 / 14.0) < 1e-12
    # The residual x - W x is not the gradient of R.
    x = [0.3, -0.8]
    g = fd_gradient(lambda z: red_regularizer(z, d), x)
    assert not close(g, [p - q for p, q in zip(x, d(x))], 0.1)


def test_general_gradient_formula_for_a_nonlinear_denoiser():
    rng, _, _, b = seeded_problem(2)
    n = 6

    def d(x):
        return [math.tanh(sum(bij * xj for bij, xj in zip(row, x))) for row in b]

    def d_vjp(x, v):
        t = d(x)
        return rmatvec(b, [vi * (1.0 - ti * ti) for vi, ti in zip(v, t)])

    x = [rng.gauss(0.0, 0.5) for _ in range(n)]
    g = fd_gradient(lambda z: red_regularizer(z, d), x)
    assert close(g, red_regularizer_gradient(x, d, d_vjp), 1e-7)
    assert not close(g, [xi - di for xi, di in zip(x, d(x))], 0.05)
