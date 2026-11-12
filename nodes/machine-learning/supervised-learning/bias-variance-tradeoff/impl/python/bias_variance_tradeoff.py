# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bias-variance-tradeoff/. The authors are listed in prov/BSBWN0.jsonl.
"""The bias-variance decomposition of the expected squared error, computed by simulation.

The data model: x is drawn from a distribution on [0, 1], y = f(x) + noise, the noise has mean 0 and
variance sigma^2 and is independent of x. A learner maps a training set to a predictor. For a fixed test
point x0, the expected squared error over training sets and over the noise of the test label is

    E[(y0 - g_S(x0))^2] = sigma^2 + (f(x0) - E_S[g_S(x0)])^2 + Var_S[g_S(x0)].

The simulation draws `reps` training sets, so the mean and variance below are the empirical ones over
those sets. With the empirical mean and variance (divide by reps), the identity holds exactly for the
expected error given the drawn training sets.
"""

import math
import random
from typing import Callable

Predictor = Callable[[float], float]
Learner = Callable[[list[float], list[float]], Predictor]


def solve(a: list[list[float]], b: list[float]) -> list[float]:
    """Solve a x = b by Gaussian elimination with partial pivoting (a is square and nonsingular)."""
    n = len(a)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        for r in range(c + 1, n):
            t = m[r][c] / m[c][c]
            for k in range(c, n + 1):
                m[r][k] -= t * m[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (m[r][n] - sum(m[r][k] * x[k] for k in range(r + 1, n))) / m[r][r]
    return x


def polynomial_learner(degree: int) -> Learner:
    """Least squares polynomial of the given degree, with the input mapped from [0, 1] to [-1, 1]."""

    def fit(xs: list[float], ys: list[float]) -> Predictor:
        p = degree + 1
        rows = [[(2 * x - 1) ** j for j in range(p)] for x in xs]
        ata = [[sum(r[i] * r[j] for r in rows) for j in range(p)] for i in range(p)]
        aty = [sum(r[i] * y for r, y in zip(rows, ys)) for i in range(p)]
        w = solve(ata, aty)
        return lambda x: sum(w[j] * (2 * x - 1) ** j for j in range(p))

    return fit


def knn_learner(k: int) -> Learner:
    """k-nearest-neighbor regression on the line: the mean label of the k closest training inputs."""

    def fit(xs: list[float], ys: list[float]) -> Predictor:
        pts = list(zip(xs, ys))

        def predict(x: float) -> float:
            near = sorted(range(len(pts)), key=lambda i: (abs(pts[i][0] - x), i))[:k]
            return sum(pts[i][1] for i in near) / k

        return predict

    return fit


def decompose(learner: Learner, f: Callable[[float], float], sigma: float, x0s: list[float],
              draw_xs: Callable[[random.Random], list[float]], reps: int, rng: random.Random) -> dict:
    """Simulate `reps` training sets and return the terms, averaged over the test points x0s.

    Keys: noise, bias2, variance, expected (the expected error given the drawn sets, sigma^2 + mean
    (f - g)^2), monte_carlo (the mean of (y0 - g(x0))^2 with a fresh noisy y0 for each set and point).
    """
    preds = [[0.0] * reps for _ in x0s]
    mc = 0.0
    for r in range(reps):
        xs = draw_xs(rng)
        ys = [f(x) + rng.gauss(0.0, sigma) for x in xs]
        g = learner(xs, ys)
        for j, x0 in enumerate(x0s):
            v = g(x0)
            preds[j][r] = v
            y0 = f(x0) + rng.gauss(0.0, sigma)
            mc += (y0 - v) ** 2
    bias2 = var = exp = 0.0
    for j, x0 in enumerate(x0s):
        mean = sum(preds[j]) / reps
        bias2 += (f(x0) - mean) ** 2
        var += sum((v - mean) ** 2 for v in preds[j]) / reps
        exp += sigma ** 2 + sum((f(x0) - v) ** 2 for v in preds[j]) / reps
    q = len(x0s)
    return {"noise": sigma ** 2, "bias2": bias2 / q, "variance": var / q, "expected": exp / q,
            "monte_carlo": mc / (q * reps)}


def target(x: float) -> float:
    return math.sin(2 * math.pi * x)


def uniform_inputs(n: int) -> Callable[[random.Random], list[float]]:
    return lambda rng: [rng.random() for _ in range(n)]


if __name__ == "__main__":
    grid = [(i + 0.5) / 20 for i in range(20)]
    for deg in (0, 1, 3, 5, 7, 9):
        t = decompose(polynomial_learner(deg), target, 0.3, grid, uniform_inputs(20), 2000, random.Random(1))
        print(deg, {k: round(v, 4) for k, v in t.items()})
