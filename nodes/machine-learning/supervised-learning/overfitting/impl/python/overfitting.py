# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/overfitting/. The authors are listed in prov/3J0J4Q.jsonl.
"""Overfitting of least squares polynomials, and its detection with a validation set.

The data model: x uniform on [0, 1], y = sin(2 pi x) + Gaussian noise of standard deviation sigma.
The learner fits a polynomial of degree p by least squares. The polynomial is written in the Legendre
basis on [-1, 1] and the least squares problem is solved by a QR factorization with modified Gram-Schmidt
(two passes), so that high degrees stay well conditioned.
"""

import math
import random


def legendre_row(x: float, p: int) -> list[float]:
    """P_0(t), ..., P_p(t) at t = 2x - 1, by the three-term recurrence."""
    t = 2 * x - 1
    row = [1.0, t][: p + 1]
    for j in range(2, p + 1):
        row.append(((2 * j - 1) * t * row[j - 1] - (j - 1) * row[j - 2]) / j)
    return row


def least_squares(rows: list[list[float]], ys: list[float]) -> list[float]:
    """Minimize ||A w - y|| for A with full column rank, by QR (modified Gram-Schmidt, twice)."""
    n, p = len(rows), len(rows[0])
    q = [[rows[i][j] for i in range(n)] for j in range(p)]  # columns
    r = [[0.0] * p for _ in range(p)]
    for j in range(p):
        for _ in range(2):
            for k in range(j):
                c = sum(q[k][i] * q[j][i] for i in range(n))
                r[k][j] += c
                q[j] = [q[j][i] - c * q[k][i] for i in range(n)]
        norm = math.sqrt(sum(v * v for v in q[j]))
        r[j][j] = norm
        q[j] = [v / norm for v in q[j]]
    qty = [sum(q[j][i] * ys[i] for i in range(n)) for j in range(p)]
    w = [0.0] * p
    for j in range(p - 1, -1, -1):
        w[j] = (qty[j] - sum(r[j][k] * w[k] for k in range(j + 1, p))) / r[j][j]
    return w


def fit_polynomial(xs: list[float], ys: list[float], degree: int):
    w = least_squares([legendre_row(x, degree) for x in xs], ys)
    return lambda x: sum(a * b for a, b in zip(w, legendre_row(x, degree)))


def mse(g, xs: list[float], ys: list[float]) -> float:
    return sum((g(x) - y) ** 2 for x, y in zip(xs, ys)) / len(xs)


def target(x: float) -> float:
    return math.sin(2 * math.pi * x)


def true_risk(g, sigma: float, grid: int = 2000) -> float:
    """sigma^2 plus the mean of (f - g)^2 over a midpoint grid of [0, 1] (the integral, up to grid error)."""
    return sigma ** 2 + sum((target((i + 0.5) / grid) - g((i + 0.5) / grid)) ** 2 for i in range(grid)) / grid


def draw(n: int, sigma: float, rng: random.Random) -> tuple[list[float], list[float]]:
    xs = [rng.random() for _ in range(n)]
    return xs, [target(x) + rng.gauss(0.0, sigma) for x in xs]


def curves(n_train: int, n_val: int, sigma: float, degrees: list[int], rng: random.Random) -> list[tuple]:
    """For each degree: (degree, training MSE, validation MSE, true risk)."""
    xt, yt = draw(n_train, sigma, rng)
    xv, yv = draw(n_val, sigma, rng)
    out = []
    for p in degrees:
        g = fit_polynomial(xt, yt, p)
        out.append((p, mse(g, xt, yt), mse(g, xv, yv), true_risk(g, sigma)))
    return out


def select_by_validation(table: list[tuple]) -> int:
    """The degree with the smallest validation error (the first one on a tie)."""
    return min(table, key=lambda row: (row[2], row[0]))[0]


if __name__ == "__main__":
    t = curves(12, 50, 0.3, list(range(12)), random.Random(4))
    for row in t:
        print("%2d  train %.4f  val %.4f  true %.4f" % row)
    print("chosen", select_by_validation(t))
