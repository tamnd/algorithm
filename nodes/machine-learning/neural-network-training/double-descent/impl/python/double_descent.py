# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-descent/. The authors are listed in prov/E223P3.jsonl.

"""Double descent of minimum norm least squares.

The learner is the minimum norm least squares fit w = X^+ y. When the number
of features p is at most the number of examples n, X has full column rank
(almost surely for Gaussian X) and w solves the p x p normal equations
X^T X w = X^T y. When p > n, X has full row rank and w = X^T alpha with
X X^T alpha = y, an n x n system. So each fit solves a system on the smaller
side of X.

The simulation follows the isotropic model of Hastie, Montanari, Rosset and
Tibshirani (2022): rows x_i ~ N(0, I_p), y_i = x_i . beta + noise with
variance sigma^2, and |beta| = r for every p. For a test point x ~ N(0, I_p)
the excess risk of w is exactly |w - beta|^2.
"""

import math
import random
from typing import List, Sequence

Matrix = List[List[float]]


def solve(a: Sequence[Sequence[float]], b: Sequence[float]) -> List[float]:
    """Solve a x = b by Gaussian elimination with partial pivoting."""
    n = len(a)
    m = [list(map(float, a[i])) + [float(b[i])] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        if m[piv][col] == 0.0:
            raise ValueError("singular matrix")
        m[col], m[piv] = m[piv], m[col]
        for r in range(col + 1, n):
            f = m[r][col] / m[col][col]
            if f != 0.0:
                row_r, row_c = m[r], m[col]
                for c in range(col, n + 1):
                    row_r[c] -= f * row_c[c]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = m[i][n] - sum(m[i][j] * x[j] for j in range(i + 1, n))
        x[i] = s / m[i][i]
    return x


def gram_rows(x: Sequence[Sequence[float]]) -> Matrix:
    """X X^T, the n x n matrix of inner products of the rows."""
    n = len(x)
    g = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            v = sum(a * b for a, b in zip(x[i], x[j]))
            g[i][j] = g[j][i] = v
    return g


def gram_cols(x: Sequence[Sequence[float]]) -> Matrix:
    """X^T X, the p x p matrix of inner products of the columns."""
    p = len(x[0])
    g = [[0.0] * p for _ in range(p)]
    for row in x:
        for i in range(p):
            ri = row[i]
            if ri != 0.0:
                gi = g[i]
                for j in range(p):
                    gi[j] += ri * row[j]
    return g


def min_norm_least_squares(x: Sequence[Sequence[float]], y: Sequence[float]) -> List[float]:
    """The minimum norm least squares solution X^+ y for a full rank X.

    If p <= n, solve X^T X w = X^T y. If p > n, solve X X^T alpha = y and
    return w = X^T alpha, which lies in the row space of X.
    """
    n, p = len(x), len(x[0])
    if p <= n:
        rhs = [sum(x[i][j] * y[i] for i in range(n)) for j in range(p)]
        return solve(gram_cols(x), rhs)
    alpha = solve(gram_rows(x), y)
    return [sum(alpha[i] * x[i][j] for i in range(n)) for j in range(p)]


def random_beta(p: int, r: float, rng: random.Random) -> List[float]:
    """A vector with a uniformly random direction and norm r."""
    v = [rng.gauss(0.0, 1.0) for _ in range(p)]
    s = math.sqrt(sum(t * t for t in v))
    return [r * t / s for t in v]


def excess_risk_trial(n: int, p: int, r: float, sigma: float, rng: random.Random) -> float:
    """One draw of the isotropic model; returns |w - beta|^2."""
    beta = random_beta(p, r, rng)
    x = [[rng.gauss(0.0, 1.0) for _ in range(p)] for _ in range(n)]
    y = [sum(a * b for a, b in zip(row, beta)) + rng.gauss(0.0, sigma) for row in x]
    w = min_norm_least_squares(x, y)
    return sum((a - b) ** 2 for a, b in zip(w, beta))


def simulate_curve(n: int, ps: Sequence[int], r: float, sigma: float, trials: int, seed: int) -> List[float]:
    """Mean excess risk over trials, for each p in ps, with one seeded generator."""
    rng = random.Random(seed)
    out = []
    for p in ps:
        out.append(sum(excess_risk_trial(n, p, r, sigma, rng) for _ in range(trials)) / trials)
    return out


def exact_expected_risk(n: int, p: int, r: float, sigma: float) -> float:
    """The exact finite sample expectation of |w - beta|^2 in the isotropic model.

    For p <= n - 2 it is sigma^2 p / (n - p - 1). For p >= n + 2 it is
    r^2 (1 - n/p) + sigma^2 n / (p - n - 1). For n - 1 <= p <= n + 1 it is
    infinite, because the mean of the inverse Wishart matrix does not exist.
    """
    if p <= n - 2:
        return sigma * sigma * p / (n - p - 1)
    if p >= n + 2:
        return r * r * (1.0 - n / p) + sigma * sigma * n / (p - n - 1)
    return math.inf


def asymptotic_risk(gamma: float, r: float, sigma: float) -> float:
    """The limit risk of Hastie et al. for p/n -> gamma (Theorem 1 there)."""
    if gamma < 1.0:
        return sigma * sigma * gamma / (1.0 - gamma)
    if gamma > 1.0:
        return r * r * (1.0 - 1.0 / gamma) + sigma * sigma / (gamma - 1.0)
    return math.inf
