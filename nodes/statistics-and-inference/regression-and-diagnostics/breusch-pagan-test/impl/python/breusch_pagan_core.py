# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/breusch-pagan-test/. The authors are listed in prov/R9XRKX.jsonl.
"""The Breusch-Pagan test and Koenker's studentized form, by two Householder QR factorizations.

Fit y on X by least squares, set g_i = e_i^2 / sigma2 with sigma2 = sum e_i^2 / n, and regress g on
Z = [1, z_i] (q variables after the intercept). With d = Q_Z^T g, the explained sum of squares is
ESS = d[1]^2 + ... + d[q]^2 (0-based), and the total sum of squares about the mean 1 is
TSS = sum (g_i - 1)^2. Then
  Breusch-Pagan:  LM = ESS / 2
  Koenker:        LM = n ESS / TSS = n R^2
and both are referred to chi-square with q degrees of freedom. The code is in this file and not in
breusch_pagan_test.py, because tools treat a file whose name ends in _test.py as a test file.
"""

import math
import random
from typing import NamedTuple

from stdist import chi2_sf

RANK_TOL = 1e-12


class BPResult(NamedTuple):
    lm_bp: float      # ESS / 2, the original Breusch-Pagan statistic
    lm_koenker: float  # n R^2 of the auxiliary regression
    q: int            # degrees of freedom
    p_bp: float       # chi-square upper tail of lm_bp
    p_koenker: float  # chi-square upper tail of lm_koenker


def householder_qr(a: list, y: list) -> tuple[list, list]:
    """R of a Householder QR of the n x p matrix a, and Q^T y. Raises ValueError if rank < p."""
    n = len(a)
    p = len(a[0]) if n else 0
    if p == 0 or n < p:
        raise ValueError("need a design with n >= p >= 1")
    a = [[float(v) for v in row] for row in a]
    c = [float(v) for v in y]
    col = [math.sqrt(math.fsum(a[i][j] ** 2 for i in range(n))) for j in range(p)]
    for j in range(p):
        norm = math.sqrt(math.fsum(a[i][j] ** 2 for i in range(j, n)))
        if norm == 0.0 or norm <= RANK_TOL * col[j]:
            raise ValueError("the design has rank below its number of columns")
        alpha = -norm if a[j][j] >= 0.0 else norm
        v = [a[j][j] - alpha] + [a[i][j] for i in range(j + 1, n)]
        vv = math.fsum(t * t for t in v)
        for k in range(j, p):
            s = 2.0 * math.fsum(v[i - j] * a[i][k] for i in range(j, n)) / vv
            for i in range(j, n):
                a[i][k] -= s * v[i - j]
        s = 2.0 * math.fsum(v[i - j] * c[i] for i in range(j, n)) / vv
        for i in range(j, n):
            c[i] -= s * v[i - j]
    return [[a[i][k] if k >= i else 0.0 for k in range(p)] for i in range(p)], c


def residuals(x: list, y: list) -> list:
    """Least squares residuals of y on the columns of x."""
    r, c = householder_qr(x, y)
    p = len(r)
    b = [0.0] * p
    for i in range(p - 1, -1, -1):
        b[i] = (c[i] - math.fsum(r[i][k] * b[k] for k in range(i + 1, p))) / r[i][i]
    return [yi - math.fsum(a * bb for a, bb in zip(xi, b)) for xi, yi in zip(x, y)]


def statistics_from_residuals(e: list, z: list) -> tuple[float, float]:
    """(LM_BP, LM_Koenker) from the residuals e and the variables z (rows without the intercept)."""
    n = len(e)
    q = len(z[0])
    sigma2 = math.fsum(t * t for t in e) / n  # @line L2
    if sigma2 == 0.0:
        raise ValueError("all residuals are 0")
    g = [t * t / sigma2 for t in e]  # @line L2
    _, d = householder_qr([[1.0] + list(zi) for zi in z], g)  # @line L3
    ess = math.fsum(d[j] ** 2 for j in range(1, q + 1))  # @line L4
    tss = math.fsum((gi - 1.0) ** 2 for gi in g)  # @line L4
    if tss == 0.0:
        raise ValueError("all squared residuals are equal")
    return ess / 2.0, n * ess / tss  # @line L5 @line L6


def breusch_pagan(x: list, y: list, z: list | None = None) -> BPResult:
    """Breusch-Pagan and Koenker tests of constant variance against variance depending on z.

    x: rows of the design (with an intercept column); z: rows of the variance variables, without
    an intercept. If z is None, the columns of x other than a constant column are used.
    Cost: Theta(n (p^2 + q^2)) time, Theta(n (p + q)) space.
    """
    n = len(x)
    if len(y) != n:
        raise ValueError("x and y must have the same length")
    if z is None:
        keep = [j for j in range(len(x[0])) if len({row[j] for row in x}) > 1]
        z = [[row[j] for j in keep] for row in x]
    if len(z) != n or not z or len(z[0]) == 0:
        raise ValueError("z must have n rows and at least one column")
    q = len(z[0])
    if n <= q + 1 or n <= len(x[0]):
        raise ValueError("too few observations")
    e = residuals(x, y)  # @line L1
    lm_bp, lm_k = statistics_from_residuals(e, z)
    return BPResult(lm_bp, lm_k, q, chi2_sf(lm_bp, q), chi2_sf(lm_k, q))  # @line L7 @line L8


def monte_carlo_p_values(x: list, y: list, z: list, reps: int = 999, seed: int = 1) -> tuple[float, float]:
    """Monte Carlo p-values (1 + #{T* >= T}) / (1 + reps) for both statistics under normal errors.

    Under H0 with normal errors the residuals are (I - H) eps and both statistics are unchanged by
    scaling, so their law depends only on X and Z: the Monte Carlo test has exact size.
    """
    obs = statistics_from_residuals(residuals(x, y), z)
    rng = random.Random(seed)
    n = len(x)
    count = [0, 0]
    for _ in range(reps):
        sim = statistics_from_residuals(residuals(x, [rng.gauss(0.0, 1.0) for _ in range(n)]), z)
        for k in range(2):
            count[k] += sim[k] >= obs[k] - 1e-12 * abs(obs[k])
    return (1 + count[0]) / (1 + reps), (1 + count[1]) / (1 + reps)
