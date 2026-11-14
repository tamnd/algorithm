# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiple-imputation-by-chained-equations/. The authors are listed in prov/XHM517.jsonl.

import math
import random
from collections.abc import Sequence
from typing import NamedTuple

Row = list
Table = list


def _inverse(a: list) -> list:
    """Gauss-Jordan inverse with partial pivoting. Cost O(p^3)."""
    k = len(a)
    m = [list(map(float, row)) + [1.0 if i == j else 0.0 for j in range(k)] for i, row in enumerate(a)]
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0:
            raise ZeroDivisionError("predictors are collinear")
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        m[c] = [v / piv for v in m[c]]
        for r in range(k):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [u - f * v for u, v in zip(m[r], m[c])]
    return [row[k:] for row in m]


def _cholesky(a: list) -> list:
    k = len(a)
    low = [[0.0] * k for _ in range(k)]
    for i in range(k):
        for j in range(i + 1):
            s = a[i][j] - sum(low[i][t] * low[j][t] for t in range(j))
            low[i][j] = math.sqrt(max(s, 0.0)) if i == j else s / low[j][j]
    return low


def bayes_regression_draw(
    x: Sequence[Sequence[float]], y: Sequence[float], rng: random.Random
) -> tuple[list, list, float]:
    """Fit OLS and draw (beta*, sigma*) from the posterior under p(beta, log sigma) = const.

    Returns (beta-hat, beta*, sigma*). sigma*^2 = RSS / chi2(n - p) and
    beta* ~ N(beta-hat, sigma*^2 (X'X)^-1). Precondition: n > p and X of full
    column rank. Cost O(n p^2 + p^3).
    """
    p = len(x[0])
    xtx = [[sum(r[i] * r[j] for r in x) for j in range(p)] for i in range(p)]
    v = _inverse(xtx)
    xty = [sum(r[i] * yi for r, yi in zip(x, y)) for i in range(p)]
    beta = [sum(v[i][j] * xty[j] for j in range(p)) for i in range(p)]
    rss = sum((yi - sum(b * c for b, c in zip(beta, r))) ** 2 for r, yi in zip(x, y))
    sigma2 = rss / (2.0 * rng.gammavariate((len(y) - p) / 2.0, 1.0))
    low = _cholesky(v)
    z = [rng.gauss(0.0, 1.0) for _ in range(p)]
    s = math.sqrt(sigma2)
    bstar = [beta[i] + s * sum(low[i][j] * z[j] for j in range(i + 1)) for i in range(p)]
    return beta, bstar, s


class MiceResult(NamedTuple):
    imputations: list   # m completed tables (lists of rows)
    chain_means: list   # chain_means[l][t][j]: mean of the imputed values of column j after sweep t


def mice(
    data: Sequence[Sequence[float | None]],
    m: int = 5,
    iters: int = 10,
    seed: int = 0,
    method: str = "norm",
    donors: int = 5,
) -> MiceResult:
    """Multiple imputation by chained equations for numeric columns.

    data is a table of n rows and p columns with None for a missing value.
    Each incomplete column, from left to right, is imputed from a Bayesian
    linear regression on all other columns (with an intercept), using their
    current values. method "norm" draws y* = x'beta* + sigma* z; method "pmm"
    takes the observed value of one of the `donors` observed rows whose
    predicted mean x'beta-hat is closest to x'beta*. Observed values never change.
    Precondition: every column has more than p observed values and the
    regressions have full rank. Cost: O(m iters q (n p^2 + p^3)) for q incomplete columns.
    """
    rng = random.Random(seed)
    n, p = len(data), len(data[0])
    miss = [[i for i in range(n) if data[i][j] is None] for j in range(p)]
    obs = [[i for i in range(n) if data[i][j] is not None] for j in range(p)]
    todo = [j for j in range(p) if miss[j]]
    sets, traces = [], []
    for _ in range(m):  # @line L1
        cur = [list(r) for r in data]
        for j in todo:  # @line L2
            pool = [data[i][j] for i in obs[j]]
            for i in miss[j]:
                cur[i][j] = rng.choice(pool)
        trace = []
        for _t in range(iters):  # @line L3
            for j in todo:  # @line L4
                design = [[1.0] + [cur[i][k] for k in range(p) if k != j] for i in range(n)]
                xo = [design[i] for i in obs[j]]
                yo = [data[i][j] for i in obs[j]]
                beta, bstar, s = bayes_regression_draw(xo, yo, rng)  # @line L5
                if method == "norm":
                    for i in miss[j]:
                        cur[i][j] = sum(b * c for b, c in zip(bstar, design[i])) + s * rng.gauss(0.0, 1.0)  # @line L6
                elif method == "pmm":
                    pred_obs = [sum(b * c for b, c in zip(beta, r)) for r in xo]
                    for i in miss[j]:
                        target = sum(b * c for b, c in zip(bstar, design[i]))
                        near = sorted(range(len(yo)), key=lambda k: (abs(pred_obs[k] - target), k))[:donors]
                        cur[i][j] = yo[rng.choice(near)]
                else:
                    raise ValueError("method must be 'norm' or 'pmm'")
            trace.append([sum(cur[i][j] for i in miss[j]) / len(miss[j]) if miss[j] else None for j in range(p)])
        sets.append(cur)  # @line L7
        traces.append(trace)
    return MiceResult(sets, traces)  # @line L8
