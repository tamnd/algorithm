# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-estimating-equations/. The authors are listed in prov/F7TMV3.jsonl.
"""Generalized estimating equations for clustered responses.

The mean model is mu_ij = g^{-1}(x_ij^T b) and Var y_ij = phi V(mu_ij). Within cluster i the working
covariance is V_i = phi S_i R(alpha) S_i with S_i = diag(sqrt V(mu_ij)). The estimate solves
    sum_i D_i^T V_i^{-1} (y_i - mu_i) = 0,   D_i = d mu_i / d b,
by Fisher scoring, and its covariance is the sandwich B^{-1} M B^{-1} with B = sum D_i^T V_i^{-1} D_i
and M = sum D_i^T V_i^{-1} (y_i - mu_i)(y_i - mu_i)^T V_i^{-1} D_i.

The Gaussian family uses only +, -, * and /, so with Fraction inputs and a fixed alpha the results
are exact.
"""

import math
from typing import NamedTuple

CORRELATIONS = ("independence", "exchangeable", "ar1")


def _expit(t):
    if t >= 0:
        return 1.0 / (1.0 + math.exp(-t))
    z = math.exp(t)
    return z / (1.0 + z)


# family -> (inverse link, d mu / d eta, variance function)
FAMILIES = {
    "gaussian": (lambda e: e, lambda e, m: 1, lambda m: 1),
    "poisson": (lambda e: math.exp(e), lambda e, m: m, lambda m: m),
    "binomial": (_expit, lambda e, m: m * (1 - m), lambda m: m * (1 - m)),
}


class GEEResult(NamedTuple):
    b: list            # coefficients
    cov: list          # sandwich covariance B^-1 M B^-1
    naive: list        # model-based covariance B^-1, valid only if the working covariance is right
    se: list           # square roots of the diagonal of cov
    phi: object        # dispersion estimate
    alpha: object      # working correlation parameter (0 for independence)
    iterations: int
    converged: bool


def solve_many(a: list, rhs: list) -> list:
    """Solve a X = rhs for X (rhs given as a list of rows, k x c). Gaussian elimination with
    partial pivoting; works with float and Fraction entries."""
    k = len(a)
    c = len(rhs[0]) if rhs else 0
    m = [list(a[i]) + list(rhs[i]) for i in range(k)]
    for col in range(k):
        piv = max(range(col, k), key=lambda r: abs(m[r][col]))
        if m[piv][col] == 0:
            raise ValueError("singular matrix")
        m[col], m[piv] = m[piv], m[col]
        for r in range(k):
            if r != col and m[r][col] != 0:
                f = m[r][col] / m[col][col]
                m[r] = [u - f * v for u, v in zip(m[r], m[col])]
    return [[m[i][k + j] / m[i][i] for j in range(c)] for i in range(k)]


def working_correlation(m: int, kind: str, alpha) -> list:
    """The m x m working correlation matrix R(alpha)."""
    one = alpha * 0 + 1
    if kind == "independence":
        return [[one if i == j else 0 * one for j in range(m)] for i in range(m)]
    if kind == "exchangeable":
        return [[one if i == j else alpha for j in range(m)] for i in range(m)]
    return [[alpha ** abs(i - j) for j in range(m)] for i in range(m)]


def _sqrt(v):
    return 1 if v == 1 else math.sqrt(v)


def _cluster_terms(cluster, b, fam, kind, alpha):
    """For one cluster, with V_i = S_i R S_i taken at phi = 1 (phi cancels from the update).
    Returns (resid, s, d, vinv_d, vinv_r): y_i - mu_i, the diagonal of S_i, D_i, V_i^-1 D_i and
    V_i^-1 (y_i - mu_i)."""
    inv_link, dmu, var = fam
    x, y = cluster
    eta = [sum(c * v for c, v in zip(b, row)) for row in x]
    mu = [inv_link(e) for e in eta]
    s = [_sqrt(var(m)) for m in mu]
    d = [[dmu(e, m) * v for v in row] for row, e, m in zip(x, eta, mu)]
    resid = [yi - m for yi, m in zip(y, mu)]
    r = working_correlation(len(y), kind, alpha)
    v = [[s[i] * r[i][j] * s[j] for j in range(len(y))] for i in range(len(y))]
    sol = solve_many(v, [dr + [e] for dr, e in zip(d, resid)])
    p = len(b)
    return resid, s, d, [row[:p] for row in sol], [row[p] for row in sol]


def _moments(clusters, b, fam, kind, n_obs, p):
    """Dispersion and correlation from Pearson residuals r_ij = (y_ij - mu_ij) / sqrt V(mu_ij)."""
    inv_link, _, var = fam
    ss = 0
    pair_sum = 0
    pairs = 0
    for x, y in clusters:
        mu = [inv_link(sum(c * v for c, v in zip(b, row))) for row in x]
        r = [(yi - m) / _sqrt(var(m)) for yi, m in zip(y, mu)]
        ss += sum(t * t for t in r)
        if kind == "exchangeable":
            for j in range(len(r)):
                for k in range(j + 1, len(r)):
                    pair_sum += r[j] * r[k]
            pairs += len(r) * (len(r) - 1) // 2
        elif kind == "ar1":
            pair_sum += sum(r[j] * r[j + 1] for j in range(len(r) - 1))
            pairs += len(r) - 1
    phi = ss / (n_obs - p)
    if kind == "independence" or pairs == 0 or phi == 0:
        return phi, 0
    alpha = pair_sum / (pairs * phi)
    m_max = max(len(y) for _, y in clusters)
    lo = -1.0 / (m_max - 1) + 1e-3 if kind == "exchangeable" else -0.99
    return phi, min(0.99, max(lo, float(alpha)))


def gee(clusters: list, family: str = "gaussian", corr: str = "exchangeable", alpha=None,
        b0: list | None = None, tol: float = 1e-10, max_iter: int = 100) -> GEEResult:
    """Fit generalized estimating equations.

    clusters: list of (x_i, y_i), x_i a list of m_i rows of length p, y_i a list of m_i responses,
    in time order within the cluster for corr="ar1". If alpha is given it is held fixed;
    otherwise it is re-estimated from Pearson residuals at each step.
    Cost per step: Theta(sum_i (m_i^3 + m_i^2 p + m_i p^2) + p^3).
    """
    if family not in FAMILIES or corr not in CORRELATIONS:  # @line L1
        raise ValueError("unknown family or working correlation")
    if not clusters:
        raise ValueError("need at least one cluster")
    p = len(clusters[0][0][0])
    n_obs = 0
    for x, y in clusters:
        if len(x) != len(y) or not y or any(len(row) != p for row in x):
            raise ValueError("each cluster needs rows of length p and one response per row")
        n_obs += len(y)
    if n_obs <= p:
        raise ValueError("need more observations than coefficients")
    fam = FAMILIES[family]
    b = list(b0) if b0 is not None else [0 * clusters[0][1][0] for _ in range(p)]  # @line L2
    fixed = alpha is not None
    a = alpha if fixed else 0
    phi = 1
    converged = False
    it = 0
    for it in range(1, max_iter + 1):  # @line L3
        if not fixed and corr != "independence":
            phi, a = _moments(clusters, b, fam, corr, n_obs, p)  # @line L4
        big_b = [[0] * p for _ in range(p)]
        u = [0] * p
        for cl in clusters:
            resid, _, d, vinv_d, vinv_r = _cluster_terms(cl, b, fam, corr, a)  # @line L5
            for j in range(p):
                u[j] += sum(d[t][j] * vinv_r[t] for t in range(len(resid)))
                for k in range(p):
                    big_b[j][k] += sum(d[t][j] * vinv_d[t][k] for t in range(len(resid)))
        step = [row[0] for row in solve_many(big_b, [[v] for v in u])]
        b = [bj + sj for bj, sj in zip(b, step)]  # @line L6
        if max(abs(s) for s in step) <= tol * (1 + max(abs(v) for v in b)):  # @line L7
            converged = True
            break
    phi_final, a_final = _moments(clusters, b, fam, corr, n_obs, p)
    if fixed:
        a_final = alpha
    big_b = [[0] * p for _ in range(p)]
    meat = [[0] * p for _ in range(p)]
    for cl in clusters:
        resid, _, d, vinv_d, vinv_r = _cluster_terms(cl, b, fam, corr, a_final)
        score = [sum(d[t][j] * vinv_r[t] for t in range(len(resid))) for j in range(p)]
        for j in range(p):
            for k in range(p):
                big_b[j][k] += sum(d[t][j] * vinv_d[t][k] for t in range(len(resid)))
                meat[j][k] += score[j] * score[k]
    eye = [[1 if i == j else 0 for j in range(p)] for i in range(p)]
    binv = solve_many(big_b, eye)
    left = [[sum(binv[i][t] * meat[t][j] for t in range(p)) for j in range(p)] for i in range(p)]
    cov = [[sum(left[i][t] * binv[t][j] for t in range(p)) for j in range(p)] for i in range(p)]  # @line L8
    naive = [[phi_final * v for v in row] for row in binv]
    se = [math.sqrt(float(cov[i][i])) for i in range(p)]
    return GEEResult(b, cov, naive, se, phi_final, a_final, it, converged)  # @line L8


def glm_independence_score(clusters: list, b: list, family: str) -> list:
    """The GLM score sum_ij x_ij (dmu/deta) (y_ij - mu_ij) / V(mu_ij) at b, for checks."""
    inv_link, dmu, var = FAMILIES[family]
    p = len(b)
    out = [0.0] * p
    for x, y in clusters:
        for row, yi in zip(x, y):
            e = sum(c * v for c, v in zip(b, row))
            m = inv_link(e)
            f = dmu(e, m) * (yi - m) / var(m)
            for j in range(p):
                out[j] += row[j] * f
    return out
