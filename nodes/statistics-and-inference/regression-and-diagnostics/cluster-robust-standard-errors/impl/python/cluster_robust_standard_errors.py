# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cluster-robust-standard-errors/. The authors are listed in prov/X126D2.jsonl.
"""Cluster-robust covariance of the least squares estimate, CR0 and CR1, and the wild cluster bootstrap.

With X = Q1 R (thin QR) and s_g = sum over the rows i of cluster g of x_i e_i, the sandwich
(X^T X)^(-1) (sum_g s_g s_g^T) (X^T X)^(-1) equals R^(-1) (sum_g u_g u_g^T) R^(-T) with u_g = R^(-T) s_g.
  CR0: factor 1
  CR1: factor G/(G - 1) * (n - 1)/(n - p)
Inference uses t with G - 1 degrees of freedom. Nothing of size n x n is formed.
"""

import math
import random
from typing import NamedTuple

from stdist import t_ppf

RANK_TOL = 1e-12
KINDS = ("CR0", "CR1")


class CRFit(NamedTuple):
    b: list          # least squares coefficients
    cov: list        # the cluster-robust covariance estimate, p x p
    se: list         # square roots of its diagonal
    residuals: list  # e_i
    clusters: int    # G
    df: int          # G - 1, used for t intervals


def householder_r(a: list, y: list) -> tuple[list, list]:
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


def back_substitute(r: list, c: list) -> list:
    p = len(r)
    x = [0.0] * p
    for i in range(p - 1, -1, -1):
        x[i] = (c[i] - math.fsum(r[i][k] * x[k] for k in range(i + 1, p))) / r[i][i]
    return x


def forward_substitute_rt(r: list, c: list) -> list:
    """Solve R^T u = c for upper triangular R (R^T is lower triangular)."""
    p = len(r)
    u = [0.0] * p
    for i in range(p):
        u[i] = (c[i] - math.fsum(r[k][i] * u[k] for k in range(i))) / r[i][i]
    return u


def sandwich(r: list, u: list, factor: float) -> list:
    """factor * R^(-1) (sum_g u_g u_g^T) R^(-T) for upper triangular R."""
    p = len(r)
    m = [[factor * math.fsum(ug[a] * ug[b] for ug in u) for b in range(p)] for a in range(p)]
    t = [back_substitute(r, [m[a][b] for a in range(p)]) for b in range(p)]   # columns of R^(-1) M
    rows = [back_substitute(r, [t[b][a] for b in range(p)]) for a in range(p)]  # rows of (R^(-1) M) R^(-T)
    return [[rows[a][b] for b in range(p)] for a in range(p)]


def cluster_index(groups: list) -> list:
    """Lists of row indices, one per cluster, in the order of first appearance of each label."""
    where = {}
    for i, g in enumerate(groups):
        where.setdefault(g, []).append(i)
    return list(where.values())


def _cr_from_qr(x, y, r, c, members, kind):
    n, p = len(x), len(r)
    big_g = len(members)
    b = back_substitute(r, c[:p])  # @line L2
    e = [yi - math.fsum(a * bb for a, bb in zip(xi, b)) for xi, yi in zip(x, y)]  # @line L3
    s = [[math.fsum(x[i][j] * e[i] for i in rows) for j in range(p)] for rows in members]  # @line L4
    u = [forward_substitute_rt(r, sg) for sg in s]  # @line L4
    factor = 1.0 if kind == "CR0" else big_g / (big_g - 1) * (n - 1) / (n - p)  # @line L5
    cov = sandwich(r, u, factor)  # @line L6
    se = [math.sqrt(max(cov[j][j], 0.0)) for j in range(p)]  # @line L7
    return CRFit(b, cov, se, e, big_g, big_g - 1)  # @line L8


def cluster_covariance(x: list, y: list, groups: list, kind: str = "CR1") -> CRFit:
    """Least squares fit with the cluster-robust covariance; groups[i] is the cluster label of row i.

    Cost: Theta(n p^2) time, Theta(n p) space.
    """
    if kind not in KINDS:
        raise ValueError("kind must be one of " + ", ".join(KINDS))
    n = len(x)
    if len(y) != n or len(groups) != n:
        raise ValueError("x, y and groups must have the same length")
    members = cluster_index(groups)
    if len(members) < 2:
        raise ValueError("need at least two clusters")
    r, c = householder_r(x, y)  # @line L1
    if n <= len(r):
        raise ValueError("need n > p")
    return _cr_from_qr(x, y, r, c, members, kind)


def confidence_intervals(fit: CRFit, level: float = 0.95) -> list:
    """b_j +- t_(G-1, (1 + level)/2) se_j. The level is only approximate: the theory is asymptotic in G."""
    qt = t_ppf(0.5 + level / 2.0, fit.df)
    return [(bj - qt * s, bj + qt * s) for bj, s in zip(fit.b, fit.se)]


def wild_cluster_bootstrap(x: list, y: list, groups: list, j: int, value: float = 0.0,
                           reps: int = 999, seed: int = 1) -> tuple[float, float]:
    """Wild cluster bootstrap p-value for H0: b_j = value, with the null imposed and Rademacher weights.

    Returns (t, p) where t = (b_j - value)/se_j uses CR1 and p = (1 + #{|t*| >= |t|})/(1 + reps).
    """
    n, p = len(x), len(x[0])
    members = cluster_index(groups)
    r, c = householder_r(x, y)
    fit = _cr_from_qr(x, y, r, c, members, "CR1")
    t_obs = (fit.b[j] - value) / fit.se[j]
    # Restricted fit: drop column j and move value * x_j to the left side.
    xr = [[v for k, v in enumerate(row) if k != j] for row in x]
    yr = [yi - value * row[j] for yi, row in zip(y, x)]
    if p > 1:
        rr, cr = householder_r(xr, yr)
        br = back_substitute(rr, cr[:p - 1])
        fitted = [value * row[j] + math.fsum(a * bb for a, bb in zip(xrow, br)) for row, xrow in zip(x, xr)]
    else:
        fitted = [value * row[j] for row in x]
    er = [yi - fi for yi, fi in zip(y, fitted)]
    q = [forward_substitute_rt(r, xi) for xi in x]  # rows of Q1, so Q1^T y* = sum q_i y*_i
    rng = random.Random(seed)
    extreme = 0
    for _ in range(reps):
        ystar = list(fitted)
        for rows in members:
            sign = 1.0 if rng.random() < 0.5 else -1.0
            for i in rows:
                ystar[i] += sign * er[i]
        cstar = [math.fsum(qi[k] * yi for qi, yi in zip(q, ystar)) for k in range(p)]
        f = _cr_from_qr(x, ystar, r, cstar, members, "CR1")
        if abs((f.b[j] - value) / f.se[j]) >= abs(t_obs):
            extreme += 1
    return t_obs, (1 + extreme) / (1 + reps)
