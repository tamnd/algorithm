# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/durbin-watson-test/. The authors are listed in prov/TBDQN3.jsonl.
"""The Durbin-Watson test of serial correlation in regression residuals.

d = sum_{t>=2} (e_t - e_{t-1})^2 / sum_t e_t^2, with e the least squares residuals of y on X.
Under H0 with independent normal errors, e = M eps with M = I - H, so the law of d depends only on
X: simulating standard normal y for the given X gives a Monte Carlo p-value with exact size.
The bounds d_L and d_U use the eigenvalues 2 - 2 cos(pi j / n) of the matrix A of the quadratic
form in the numerator. The code is in this file and not in durbin_watson_test.py, because tools
treat a file whose name ends in _test.py as a test file.
"""

import math
import random
from typing import NamedTuple

RANK_TOL = 1e-12


class DWResult(NamedTuple):
    d: float        # the Durbin-Watson statistic
    r1: float       # the lag-1 residual autocorrelation sum e_t e_(t-1) / sum e_t^2
    p_value: float  # Monte Carlo p-value for the chosen alternative
    reps: int       # number of simulated samples


def householder_q1(a: list) -> list:
    """Rows of Q1 (n x p, orthonormal columns spanning the columns of a), by Householder QR."""
    n = len(a)
    p = len(a[0]) if n else 0
    if p == 0 or n <= p:
        raise ValueError("need a design with n > p >= 1")
    a = [[float(v) for v in row] for row in a]
    col = [math.sqrt(math.fsum(a[i][j] ** 2 for i in range(n))) for j in range(p)]
    vs = []
    for j in range(p):
        norm = math.sqrt(math.fsum(a[i][j] ** 2 for i in range(j, n)))
        if norm == 0.0 or norm <= RANK_TOL * col[j]:
            raise ValueError("the design has rank below its number of columns")
        alpha = -norm if a[j][j] >= 0.0 else norm
        v = [0.0] * j + [a[j][j] - alpha] + [a[i][j] for i in range(j + 1, n)]
        vv = math.fsum(t * t for t in v)
        for k in range(j, p):
            s = 2.0 * math.fsum(v[i] * a[i][k] for i in range(j, n)) / vv
            for i in range(j, n):
                a[i][k] -= s * v[i]
        vs.append((v, vv))
    # Q1 = H_1 ... H_p applied to the first p unit vectors.
    q = [[1.0 if i == k else 0.0 for k in range(p)] for i in range(n)]
    for j in range(p - 1, -1, -1):
        v, vv = vs[j]
        for k in range(p):
            s = 2.0 * math.fsum(v[i] * q[i][k] for i in range(j, n)) / vv
            for i in range(j, n):
                q[i][k] -= s * v[i]
    return q


def project_out(q: list, y: list) -> list:
    """Residuals y - Q1 Q1^T y."""
    p = len(q[0])
    c = [math.fsum(q[i][k] * y[i] for i in range(len(y))) for k in range(p)]
    return [yi - math.fsum(qi[k] * c[k] for k in range(p)) for qi, yi in zip(q, y)]


def dw_statistic(e: list) -> tuple[float, float]:
    """(d, r1) for a residual vector e."""
    s = math.fsum(t * t for t in e)  # @line L2
    if s == 0.0:
        raise ValueError("all residuals are 0")
    num = math.fsum((e[t] - e[t - 1]) ** 2 for t in range(1, len(e)))  # @line L3
    r1 = math.fsum(e[t] * e[t - 1] for t in range(1, len(e))) / s
    return num / s, r1  # @line L4


def durbin_watson(x: list, y: list, alternative: str = "positive", reps: int = 999,
                  seed: int = 1) -> DWResult:
    """Durbin-Watson statistic and Monte Carlo p-value for the given design.

    alternative: "positive" (small d is extreme), "negative" (large d) or "two-sided".
    Cost: Theta(n p^2 + B n p) time, Theta(n p) space.
    """
    if alternative not in ("positive", "negative", "two-sided"):
        raise ValueError("alternative must be positive, negative or two-sided")
    n = len(x)
    if len(y) != n:
        raise ValueError("x and y must have the same length")
    q = householder_q1(x)  # @line L1
    e = project_out(q, y)  # @line L1
    if math.fsum(t * t for t in e) <= 1e-24 * math.fsum(float(v) ** 2 for v in y):
        raise ValueError("y is fitted exactly by X, so d is undefined")
    d, r1 = dw_statistic(e)
    rng = random.Random(seed)
    below = above = 0
    tol = 1e-12 * max(d, 1.0)
    for _ in range(reps):  # @line L5
        dstar = dw_statistic(project_out(q, [rng.gauss(0.0, 1.0) for _ in range(n)]))[0]  # @line L6
        below += dstar <= d + tol
        above += dstar >= d - tol
    if alternative == "positive":  # @line L7
        p = (1 + below) / (1 + reps)
    elif alternative == "negative":
        p = (1 + above) / (1 + reps)
    else:
        p = min(1.0, 2.0 * (1 + min(below, above)) / (1 + reps))
    return DWResult(d, r1, p, reps)  # @line L8


def bound_eigenvalues(n: int) -> list:
    """Eigenvalues 2 - 2 cos(pi j / n), j = 0..n-1, of the matrix A with d = e^T A e / e^T e."""
    return [2.0 - 2.0 * math.cos(math.pi * j / n) for j in range(n)]


def bounds_p_values(d: float, n: int, p: int, reps: int = 9999, seed: int = 1) -> tuple[float, float]:
    """Monte Carlo P(d_L <= d) and P(d_U <= d) for a design with an intercept and p columns.

    d_L = sum lam_i xi_i^2 / sum xi_i^2 over i = 1..n-p, and d_U the same with lam_(i+p-1).
    Since d_L <= d <= d_U for the same xi, the exact p-value P(d* <= d) lies between the two.
    Against positive correlation: if P(d_L <= d) < alpha, reject; if P(d_U <= d) > alpha, do not
    reject; otherwise the bounds test is inconclusive.
    """
    lam = bound_eigenvalues(n)
    m = n - p
    low, high = lam[1:m + 1], lam[p:p + m]
    rng = random.Random(seed)
    cl = cu = 0
    for _ in range(reps):
        xi2 = [rng.gauss(0.0, 1.0) ** 2 for _ in range(m)]
        s = math.fsum(xi2)
        cl += math.fsum(a * b for a, b in zip(low, xi2)) / s <= d
        cu += math.fsum(a * b for a, b in zip(high, xi2)) / s <= d
    return cl / reps, cu / reps
