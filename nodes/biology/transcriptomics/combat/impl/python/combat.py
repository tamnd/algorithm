# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/combat/. The authors are listed in prov/PBAHAY.jsonl.
"""ComBat batch correction with parametric empirical Bayes priors (Johnson, Li and Rabinovic 2007).

data[g][j] is the expression of gene g in sample j (for example log counts),
batch[j] is the batch of sample j, and covariates[j] is an optional list of
biological covariates of sample j that the correction must keep.

The model of the paper is Y_ijg = alpha_g + x_j beta_g + gamma_ig + delta_ig e_ijg
for sample j of batch i, with e_ijg of mean 0 and variance sigma_g^2. The steps
follow the R function ComBat of the sva package:

1. Least squares fit on the design [batch indicators | covariates]; alpha_g is
   the mean of the batch coefficients weighted by the batch sizes, and
   sigma_g^2 is the mean squared residual (divisor N).
2. Standardize: Z = (Y - alpha_g - x_j beta_g) / sigma_g.
3. gamma_hat_ig is the mean and delta_hat_ig^2 the variance (divisor n_i - 1)
   of Z over batch i.
4. Priors by the method of moments: gamma_ig ~ N(gamma_bar_i, tau_i^2) and
   delta_ig^2 ~ InvGamma(lambda_i, theta_i), from the values over all genes.
5. Iterate the two conditional posterior means until the relative change is
   below conv.
6. Y* = sigma_g / delta*_ig (Z - gamma*_ig) + alpha_g + x_j beta_g.

Left out: the non-parametric prior, the mean-only option, the reference batch
option and the handling of genes with zero variance inside a batch.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

from rq3lin import solve

Matrix = List[List[float]]


def mean(v: Sequence[float]) -> float:
    return sum(v) / len(v)


def var(v: Sequence[float]) -> float:
    """Sample variance with divisor len(v) - 1."""
    m = mean(v)
    return sum((x - m) ** 2 for x in v) / (len(v) - 1)


def design_matrix(batch: Sequence, covariates: Optional[Sequence[Sequence[float]]]) -> Tuple[Matrix, List]:
    levels = sorted(set(batch), key=lambda b: list(batch).index(b))
    rows = []
    for j, b in enumerate(batch):
        row = [1.0 if b == lv else 0.0 for lv in levels]
        if covariates is not None:
            row += [float(c) for c in covariates[j]]
        rows.append(row)
    return rows, levels


def least_squares(X: Matrix, y: Sequence[float]) -> List[float]:
    p = len(X[0])
    XtX = [[sum(r[a] * r[b] for r in X) for b in range(p)] for a in range(p)]
    Xty = [sum(r[a] * v for r, v in zip(X, y)) for a in range(p)]
    return solve(XtX, Xty)


def standardize(data: Sequence[Sequence[float]], batch: Sequence,
                covariates: Optional[Sequence[Sequence[float]]] = None):
    """(Z, stand_mean, sigma, levels): the standardized data and what is needed to undo it."""
    X, levels = design_matrix(batch, covariates)
    N, nb = len(batch), len(levels)
    sizes = [sum(1 for b in batch if b == lv) for lv in levels]
    Z, stand, sigma = [], [], []
    for y in data:
        coef = least_squares(X, y)  # @line L1
        alpha = sum(sizes[i] * coef[i] for i in range(nb)) / N
        cov_part = [sum(r[nb + a] * coef[nb + a] for a in range(len(coef) - nb)) for r in X]
        fit = [sum(r[a] * coef[a] for a in range(len(coef))) for r in X]
        s2 = sum((v - f) ** 2 for v, f in zip(y, fit)) / N  # @line L2
        if s2 <= 0:
            raise ValueError("a gene has no residual variance")
        s = s2 ** 0.5
        sm = [alpha + c for c in cov_part]
        Z.append([(v - m) / s for v, m in zip(y, sm)])  # @line L3
        stand.append(sm)
        sigma.append(s)
    return Z, stand, sigma, levels


def inverse_gamma_moments(d: Sequence[float]) -> Tuple[float, float]:
    """(lambda, theta) of the inverse gamma with the mean and variance of d."""
    D, S2 = mean(d), var(d)
    if S2 <= 0:
        raise ValueError("the batch variances do not vary over genes")
    return (D * D + 2 * S2) / S2, (D ** 3 + D * S2) / S2  # @line L6


def posterior(z: Sequence[float], g_hat: float, d_hat: float, g_bar: float, t2: float,
              lam: float, theta: float, conv: float = 1e-4, max_iter: int = 1000,
              history: Optional[list] = None) -> Tuple[float, float]:
    """The fixed point (gamma*, delta*^2) of the two conditional posterior means, for one gene and batch."""
    n = len(z)
    g_old, d_old = g_hat, d_hat
    for _ in range(max_iter):
        g_new = (t2 * n * g_hat + d_old * g_bar) / (t2 * n + d_old)  # @line L7
        ss = sum((x - g_new) ** 2 for x in z)
        d_new = (theta + 0.5 * ss) / (n / 2.0 + lam - 1.0)  # @line L8
        if history is not None:
            history.append((g_new, d_new))
        change = max(abs(g_new - g_old) / abs(g_old) if g_old != 0 else abs(g_new - g_old),
                     abs(d_new - d_old) / d_old)
        g_old, d_old = g_new, d_new
        if change < conv:  # @line L9
            break
    return g_old, d_old


def combat(data: Sequence[Sequence[float]], batch: Sequence,
           covariates: Optional[Sequence[Sequence[float]]] = None,
           shrink: bool = True, conv: float = 1e-4) -> Matrix:
    """The batch corrected data, genes by samples. With shrink=False the batch estimates are used as they are."""
    G = len(data)
    if G < 2:
        raise ValueError("ComBat needs at least two genes to estimate the priors")
    Z, stand, sigma, levels = standardize(data, batch, covariates)
    cols: Dict = {lv: [j for j, b in enumerate(batch) if b == lv] for lv in levels}
    if any(len(c) < 2 for c in cols.values()):
        raise ValueError("every batch needs at least two samples")
    out = [[0.0] * len(batch) for _ in range(G)]
    for lv in levels:
        idx = cols[lv]
        zs = [[Z[g][j] for j in idx] for g in range(G)]
        g_hat = [mean(z) for z in zs]  # @line L4
        d_hat = [var(z) for z in zs]
        if shrink:
            g_bar, t2 = mean(g_hat), var(g_hat)  # @line L5
            lam, theta = inverse_gamma_moments(d_hat)
            est = [posterior(zs[g], g_hat[g], d_hat[g], g_bar, t2, lam, theta, conv) for g in range(G)]
        else:
            est = list(zip(g_hat, d_hat))
        for g in range(G):
            gs, ds = est[g]
            for j in idx:
                out[g][j] = sigma[g] / ds ** 0.5 * (Z[g][j] - gs) + stand[g][j]  # @line L10
    return out
