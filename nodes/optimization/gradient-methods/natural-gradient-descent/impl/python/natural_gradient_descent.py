# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/natural-gradient-descent/. The authors are listed in prov/R1B2TS.jsonl.

"""Natural gradient descent: theta <- theta - eta (F(theta) + lambda I)^(-1) grad L(theta).

Vectors are lists of floats and matrices are lists of rows. The Fisher matrix is given
by a function; the step solves one linear system by Gaussian elimination.
"""

import math
from collections.abc import Callable

Vector = list[float]
Matrix = list[list[float]]


def solve(m: Matrix, v: Vector) -> Vector:
    """Solve m w = v by Gaussian elimination with partial pivoting (m must be invertible)."""
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


def natural_gradient_descent(
    grad: Callable[[Vector], Vector],
    fisher: Callable[[Vector], Matrix],
    theta0: Vector,
    step: float,
    iters: int,
    damping: float = 0.0,
) -> list[Vector]:
    """Return [theta_0, ..., theta_iters]. damping adds lambda I to the Fisher matrix."""
    theta = list(theta0)  # @line L1
    out = [theta]
    for _ in range(iters):  # @line L2
        g = grad(theta)  # @line L3
        f = fisher(theta)  # @line L4
        n = len(theta)
        f = [[f[i][j] + (damping if i == j else 0.0) for j in range(n)] for i in range(n)]
        d = solve(f, g)  # @line L5
        theta = [t - step * di for t, di in zip(theta, d)]  # @line L6
        out.append(theta)
    return out  # @line L7


def sigmoid(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def logistic_model(xs: list[Vector], ys: list[int]):
    """Mean negative log-likelihood of logistic regression, its gradient, and its Fisher matrix.

    For this model the Fisher matrix (1/N) sum s_i (1 - s_i) x_i x_i^T equals the Hessian.
    """
    n_obs, d = len(xs), len(xs[0])

    def loss(theta: Vector) -> float:
        total = 0.0
        for x, y in zip(xs, ys):
            z = sum(a * b for a, b in zip(theta, x))
            # log(1 + e^z) - y z, computed without overflow
            total += max(z, 0.0) + math.log1p(math.exp(-abs(z))) - y * z
        return total / n_obs

    def grad(theta: Vector) -> Vector:
        g = [0.0] * d
        for x, y in zip(xs, ys):
            r = sigmoid(sum(a * b for a, b in zip(theta, x))) - y
            for j in range(d):
                g[j] += r * x[j] / n_obs
        return g

    def fisher(theta: Vector) -> Matrix:
        f = [[0.0] * d for _ in range(d)]
        for x in xs:
            s = sigmoid(sum(a * b for a, b in zip(theta, x)))
            w = s * (1 - s) / n_obs
            for i in range(d):
                for j in range(d):
                    f[i][j] += w * x[i] * x[j]
        return f

    return loss, grad, fisher
