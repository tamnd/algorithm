# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/score-test/. The authors are listed in prov/6H761T.jsonl.
"""The score test (Rao score test, Lagrange multiplier test), general and for common models.

score_test fits the model under H_0 only, evaluates the score U and the
Fisher information J at the restricted estimate, and returns (S, p) with
S = U^T J^(-1) U and p the upper chi-squared tail with r degrees of
freedom (asymptotic). The linear system J y = U is solved by Gaussian
elimination with partial pivoting in the arithmetic of the inputs, so
Fraction inputs give an exact S. The model functions give S in closed form;
for a multinomial it is Pearson's X^2.
The code is in this file and not in score_test.py, because tools treat a
file whose name ends in _test.py as a test file.
"""

import math
from collections.abc import Callable, Sequence

from stdist import chi2_sf


def solve(a: Sequence[Sequence], b: Sequence) -> list:
    """Solve a y = b by Gaussian elimination with partial pivoting."""
    n = len(a)
    if n == 0 or any(len(row) != n for row in a) or len(b) != n:
        raise ValueError("need a square nonempty matrix and a vector of the same size")
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda i: abs(m[i][col]))
        if m[piv][col] == 0:
            raise ValueError("the information matrix is singular")
        m[col], m[piv] = m[piv], m[col]
        for i in range(col + 1, n):
            f = m[i][col] / m[col][col]
            if f:
                for j in range(col, n + 1):
                    m[i][j] -= f * m[col][j]
    y = [0] * n
    for i in range(n - 1, -1, -1):
        s = m[i][n] - sum(m[i][j] * y[j] for j in range(i + 1, n))
        y[i] = s / m[i][i]
    return y


def score_test(score: Callable[[object], Sequence], info: Callable[[object], Sequence[Sequence]],
               fit_null: Callable[[], object], r: int):
    """General score test: score(theta) and info(theta) are the full score vector and the
    Fisher information of the sample; fit_null returns the MLE under H_0. Returns (S, p)."""
    if r < 1:
        raise ValueError("r, the number of constraints, must be at least 1")
    theta0 = fit_null()  # @line L1
    u = list(score(theta0))  # @line L2
    j = info(theta0)  # @line L3
    y = solve(j, u)  # @line L4
    s = sum(u[i] * y[i] for i in range(len(u)))  # @line L5
    if s < 0:
        raise ValueError("the information matrix is not positive definite")
    p = chi2_sf(float(s), r)  # @line L6
    return s, p  # @line L7


def binomial_score(k: int, n: int, p0: float) -> tuple[float, float]:
    """S = (k - n p0)^2 / (n p0 (1 - p0)), the square of the one-proportion z statistic."""
    if n < 1 or not 0 <= k <= n or not 0.0 < p0 < 1.0:
        raise ValueError("need n >= 1, 0 <= k <= n and 0 < p0 < 1")
    s = (k - n * p0) ** 2 / (n * p0 * (1.0 - p0))
    return s, chi2_sf(s, 1)


def poisson_score(total: int, n: int, lam0: float) -> tuple[float, float]:
    """S = (total - n lam0)^2 / (n lam0) for n iid Poisson counts with sum total."""
    if n < 1 or total < 0 or lam0 <= 0.0:
        raise ValueError("need n >= 1, total >= 0 and lam0 > 0")
    s = (total - n * lam0) ** 2 / (n * lam0)
    return s, chi2_sf(s, 1)


def normal_mean_score(x: Sequence[float], mu0: float,
                      sigma: float | None = None) -> tuple[float, float]:
    """Score test of mu = mu0. With sigma unknown, S = n^2 (xbar - mu0)^2 / sum (x - mu0)^2,
    which is n T^2 / (n - 1 + T^2) for the t statistic T."""
    n = len(x)
    if n < 1 or (sigma is None and n < 2):
        raise ValueError("need n >= 1, and n >= 2 when sigma is unknown")
    mean = math.fsum(x) / n
    if sigma is None:
        ss0 = math.fsum((v - mu0) ** 2 for v in x)
        if ss0 == 0.0:
            raise ValueError("all observations equal mu0")
        s = n * n * (mean - mu0) ** 2 / ss0
    else:
        if sigma <= 0.0:
            raise ValueError("sigma must be positive")
        s = n * (mean - mu0) ** 2 / sigma ** 2
    return s, chi2_sf(s, 1)


def multinomial_score(counts: Sequence[int], probs: Sequence[float]) -> tuple[float, float]:
    """Score test of cell probabilities = probs; S is Pearson's X^2, with m - 1 degrees of freedom."""
    m, n = len(counts), sum(counts)
    if m < 2 or n < 1 or len(probs) != m or any(c < 0 for c in counts):
        raise ValueError("need at least 2 cells, nonnegative counts and one prob per cell")
    if any(q <= 0.0 for q in probs) or abs(math.fsum(probs) - 1.0) > 1e-12:
        raise ValueError("probs must be positive and sum to 1")
    s = math.fsum((c - n * q) ** 2 / (n * q) for c, q in zip(counts, probs))
    return s, chi2_sf(s, m - 1)
