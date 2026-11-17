# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mixed-model-association/. The authors are listed in prov/HRTZ5C.jsonl.
"""Mixed model association: variance components once under the null, then
generalized least squares for each SNP.

The model for n individuals is

    y = X beta + g_j b_j + u + e,   u ~ N(0, sigma_g^2 K),   e ~ N(0, sigma_e^2 I),

where X holds p fixed covariates (a column of ones first), g_j is the
dosage vector of the tested SNP and K is a genetic relationship matrix. So
Var(y) = sigma_g^2 (K + delta I) with delta = sigma_e^2 / sigma_g^2.

The variance components are estimated once, under the null model without
any SNP, by REML. With the eigendecomposition K = U diag(s) U^T, the rotated
data U^T y have the diagonal covariance sigma_g^2 diag(s + delta), so each
evaluation of the REML likelihood for a given delta costs O(n p^2). The
search over log(delta) is a grid followed by golden-section refinement, as
in EMMA (Kang et al. 2008). Each SNP is then tested by weighted least squares
on the rotated data with these components held fixed (Kang et al. 2010).
"""

from __future__ import annotations

import math
from typing import List, Sequence, Tuple

from biostoch import chi2_sf
from pg4lmm import eigh, inverse_small, solve_small, tmatvec

LOG_DELTA_RANGE = (-10.0, 10.0)
GRID_POINTS = 100


def weighted_ls(Z: Sequence[Sequence[float]], y: Sequence[float], w: Sequence[float]):
    """Weighted least squares: (coef, (Z^T W Z)^-1, residual sum sum w r^2)."""
    q = len(Z[0])
    A = [[0.0] * q for _ in range(q)]
    b = [0.0] * q
    for zi, yi, wi in zip(Z, y, w):
        for a in range(q):
            wz = wi * zi[a]
            b[a] += wz * yi
            Aa = A[a]
            for c in range(a, q):
                Aa[c] += wz * zi[c]
    for a in range(q):
        for c in range(a):
            A[a][c] = A[c][a]
    coef = solve_small(A, b)
    rss = 0.0
    for zi, yi, wi in zip(Z, y, w):
        r = yi - sum(zi[a] * coef[a] for a in range(q))
        rss += wi * r * r
    return coef, inverse_small(A), rss


def logdet_small(A: Sequence[Sequence[float]]) -> float:
    """log det of a small symmetric positive definite matrix."""
    n = len(A)
    M = [list(r) for r in A]
    s = 0.0
    for c in range(n):
        piv = M[c][c]
        if piv <= 0:
            raise ValueError("matrix is not positive definite")
        s += math.log(piv)
        for r in range(c + 1, n):
            f = M[r][c] / piv
            for k in range(c, n):
                M[r][k] -= f * M[c][k]
    return s


def reml_profile(s: Sequence[float], yt: Sequence[float], Xt, delta: float) -> float:
    """The REML log-likelihood at delta with sigma_g^2 profiled out.

    In rotated coordinates the covariance is sigma_g^2 diag(s + delta), and
      l_R(delta) = 1/2 [ (n - p) log((n - p) / (2 pi R)) - (n - p)
                         - sum log(s_i + delta) - log det(Xt^T W Xt) ],
    with W = diag(1 / (s_i + delta)) and R the weighted residual sum of
    squares of the regression of yt on Xt. The constant log det(X^T X) of
    the REML likelihood is left out.
    """
    n, p = len(yt), len(Xt[0])
    w = [1.0 / (si + delta) for si in s]
    _, inv, R = weighted_ls(Xt, yt, w)
    A = [[sum(Xt[i][a] * w[i] * Xt[i][c] for i in range(n)) for c in range(p)] for a in range(p)]
    df = n - p
    return 0.5 * (df * math.log(df / (2.0 * math.pi * R)) - df
                  - sum(math.log(si + delta) for si in s) - logdet_small(A))


def _golden(f, a: float, b: float, tol: float = 1e-10) -> float:
    """The maximizer of a unimodal f on [a, b] by golden-section search."""
    g = (math.sqrt(5.0) - 1.0) / 2.0
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = f(c), f(d)
    while b - a > tol:
        if fc >= fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = f(d)
    return (a + b) / 2.0


def fit_null(K, y: Sequence[float], X):
    """REML fit of the null model y = X beta + u + e.

    Returns a dict with delta, sigma_g2, sigma_e2, the eigenvalues s, the
    eigenvectors U (as columns), and the rotated yt and Xt.
    """
    n, p = len(y), len(X[0])
    if n <= p:
        raise ValueError("need more individuals than covariates")
    s, U = eigh(K)  # @line L1
    yt = tmatvec(U, y)  # @line L2
    Xt_cols = [tmatvec(U, [X[i][a] for i in range(n)]) for a in range(p)]
    Xt = [[Xt_cols[a][i] for a in range(p)] for i in range(n)]

    def f(t):
        return reml_profile(s, yt, Xt, math.exp(t))

    lo, hi = LOG_DELTA_RANGE
    if s[0] < 0.0:
        # The GRM of GCTA need not be positive semidefinite; keep K + delta I
        # positive definite.
        lo = max(lo, math.log(-s[0]) + 1e-6)
    step = (hi - lo) / (GRID_POINTS - 1)
    grid = [lo + k * step for k in range(GRID_POINTS)]
    vals = [f(t) for t in grid]
    k = max(range(GRID_POINTS), key=lambda i: vals[i])
    a, b = grid[max(k - 1, 0)], grid[min(k + 1, GRID_POINTS - 1)]
    t_best = _golden(f, a, b)
    if vals[k] > f(t_best):
        t_best = grid[k]
    delta = math.exp(t_best)  # @line L3
    w = [1.0 / (si + delta) for si in s]
    _, _, R = weighted_ls(Xt, yt, w)
    sigma_g2 = R / (n - p)  # @line L4
    return {"delta": delta, "sigma_g2": sigma_g2, "sigma_e2": delta * sigma_g2,
            "s": s, "U": U, "yt": yt, "Xt": Xt, "reml": f(t_best)}


def scan(fit, snps: Sequence[Sequence[float]]) -> List[Tuple[float, float, float, float]]:
    """Test each SNP (a dosage vector of length n) with the null components fixed.

    Returns (b, se, T, p) per SNP: the GLS effect, its standard error, the
    Wald statistic T = b^2 / se^2 and its chi-squared (1 df) p-value.
    """
    s, U, yt, Xt = fit["s"], fit["U"], fit["yt"], fit["Xt"]
    delta, sg2 = fit["delta"], fit["sigma_g2"]
    w = [1.0 / (sg2 * (si + delta)) for si in s]
    out = []
    for g in snps:
        gt = tmatvec(U, g)  # @line L5
        Z = [row + [gt[i]] for i, row in enumerate(Xt)]
        coef, inv, _ = weighted_ls(Z, yt, w)  # @line L6
        b = coef[-1]
        var = inv[-1][-1]
        T = b * b / var  # @line L7
        out.append((b, math.sqrt(var), T, chi2_sf(T, 1)))
    return out  # @line L8
