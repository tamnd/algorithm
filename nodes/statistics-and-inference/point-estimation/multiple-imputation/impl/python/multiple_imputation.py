# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiple-imputation/. The authors are listed in prov/W9KZM4.jsonl.

import math
import random
from collections.abc import Callable, Sequence
from fractions import Fraction
from typing import NamedTuple

from stdist import norm_ppf, t_ppf


class Pooled(NamedTuple):
    qbar: object       # mean of the m estimates
    w: object          # mean within-imputation variance
    b: object          # between-imputation variance, divisor m - 1
    t: object          # total variance W + (1 + 1/m) B
    r: object          # relative increase in variance (1 + 1/m) B / W
    lam: object        # (1 + 1/m) B / T, the fraction of variance due to missing data
    df: float          # degrees of freedom (Rubin 1987, or Barnard and Rubin 1999)


def rubin_pool(estimates: Sequence, variances: Sequence, df_com: float | None = None) -> Pooled:
    """Combine m >= 2 completed-data estimates of a scalar with Rubin's rules.

    variances are the completed-data variance estimates U_j. With df_com
    (the complete-data degrees of freedom) the Barnard-Rubin small-sample
    df is returned, otherwise Rubin's (m - 1)(1 + 1/r)^2. df is inf when B = 0.
    Exact for Fraction inputs except the df. Cost O(m).
    """
    m = len(estimates)
    if m < 2 or len(variances) != m:
        raise ValueError("need m >= 2 estimates and m variances")
    qbar = sum(estimates) / m  # @line L7
    w = sum(variances) / m
    b = sum((q - qbar) ** 2 for q in estimates) / (m - 1)
    inc = (1 + Fraction(1, m)) * b if isinstance(b, Fraction) else (1.0 + 1.0 / m) * b
    t = w + inc  # @line L8
    r = inc / w if w != 0 else math.inf
    lam = inc / t if t != 0 else 0
    if b == 0:
        df_m = math.inf
    else:
        df_m = (m - 1) / float(lam) ** 2
    if df_com is None:
        df = df_m
    else:
        df_obs = (df_com + 1) / (df_com + 3) * df_com * (1 - float(lam))
        df = 1.0 / (1.0 / df_m + 1.0 / df_obs)
    return Pooled(qbar, w, b, t, r, lam, df)


def pooled_interval(p: Pooled, level: float = 0.95) -> tuple[float, float]:
    """Qbar -/+ t_df quantile * sqrt(T); the normal quantile when df is inf."""
    a = 0.5 + level / 2
    c = norm_ppf(a) if math.isinf(p.df) else t_ppf(a, p.df)
    h = c * math.sqrt(float(p.t))
    return float(p.qbar) - h, float(p.qbar) + h  # @line L9


def _cholesky(a: list) -> list:
    k = len(a)
    low = [[0.0] * k for _ in range(k)]
    for i in range(k):
        for j in range(i + 1):
            s = a[i][j] - sum(low[i][t] * low[j][t] for t in range(j))
            low[i][j] = math.sqrt(s) if i == j else s / low[j][j]
    return low


def _inverse(a: list) -> list:
    k = len(a)
    m = [list(map(float, row)) + [1.0 if i == j else 0.0 for j in range(k)] for i, row in enumerate(a)]
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        m[c] = [v / piv for v in m[c]]
        for r in range(k):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [u - f * v for u, v in zip(m[r], m[c])]
    return [row[k:] for row in m]


def regression_posterior(x: Sequence[Sequence[float]], y: Sequence[float]) -> tuple[list, float, list, int]:
    """OLS on complete rows: (beta-hat, residual sum of squares, (X'X)^-1, n - p)."""
    p = len(x[0])
    xtx = [[sum(r[i] * r[j] for r in x) for j in range(p)] for i in range(p)]
    v = _inverse(xtx)
    xty = [sum(r[i] * yi for r, yi in zip(x, y)) for i in range(p)]
    beta = [sum(v[i][j] * xty[j] for j in range(p)) for i in range(p)]
    rss = sum((yi - sum(b * c for b, c in zip(beta, r))) ** 2 for r, yi in zip(x, y))
    return beta, rss, v, len(y) - p


def impute_normal_regression(
    y: Sequence[float | None], x: Sequence[Sequence[float]], rng: random.Random
) -> list:
    """One proper draw of the missing y from Bayesian normal linear regression.

    y holds None where missing; x is fully observed with a constant column.
    Draws sigma*^2 = RSS / chi2(n_obs - p), beta* ~ N(beta-hat, sigma*^2 (X'X)^-1)
    and y* = x' beta* + sigma* z. Observed y are returned unchanged.
    Precondition: n_obs - p >= 1 and X_obs of full rank. Cost O(n p^2 + p^3).
    """
    obs = [i for i, v in enumerate(y) if v is not None]
    beta, rss, v, dfr = regression_posterior([x[i] for i in obs], [y[i] for i in obs])  # @line L2
    sigma2 = rss / (2.0 * rng.gammavariate(dfr / 2.0, 1.0))  # @line L3
    low = _cholesky(v)
    z = [rng.gauss(0.0, 1.0) for _ in beta]
    p = len(beta)
    bstar = [beta[i] + math.sqrt(sigma2) * sum(low[i][j] * z[j] for j in range(p)) for i in range(p)]  # @line L4
    out = list(y)
    for i, yi in enumerate(y):
        if yi is None:
            out[i] = sum(b * c for b, c in zip(bstar, x[i])) + math.sqrt(sigma2) * rng.gauss(0.0, 1.0)  # @line L5
    return out


def multiple_imputation(
    y: Sequence[float | None],
    x: Sequence[Sequence[float]],
    analysis: Callable[[list, list], tuple[float, float]],
    m: int = 20,
    seed: int = 0,
    df_com: float | None = None,
) -> tuple[Pooled, list]:
    """Impute y m times, run analysis(x, y_completed) -> (estimate, variance), pool.

    Returns the pooled result and the m completed y vectors.
    Cost: m times (imputation + analysis).
    """
    rng = random.Random(seed)
    qs, us, sets = [], [], []
    for _ in range(m):  # @line L1
        yc = impute_normal_regression(y, x, rng)
        q, u = analysis(x, yc)  # @line L6
        qs.append(q)
        us.append(u)
        sets.append(yc)
    return rubin_pool(qs, us, df_com), sets
