# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pareto-smoothed-importance-sampling-loo/. The authors are listed in prov/NR2Y7A.jsonl.
"""Pareto smoothed importance sampling (PSIS) and PSIS leave-one-out cross-validation.

The input of psis_loo and waic is a log-likelihood matrix: loglik[i][s] is
log p(y_i | theta^s) for observation i = 0, ..., n - 1 and posterior draw
s = 0, ..., S - 1. The draws must come from the full-data posterior.

The smoothing follows Algorithm 1 of Vehtari, Simpson, Gelman, Yao and Gabry
(2024): the tail length is M = floor(min(0.2 S, 3 sqrt(S))), the threshold is
the (S - M)-th smallest ratio, the M largest ratios are replaced by quantiles
of a fitted generalized Pareto law at (z - 1/2)/M, and no smoothed weight may
exceed the largest raw ratio. The shape estimate uses the method of Zhang and
Stephens (2009), followed by the shrinkage toward 0.5 with the weight of 10
observations that the paper describes in its Appendix G.
"""

import math
from typing import Sequence


def log_sum_exp(xs: Sequence[float]) -> float:
    """log(sum(exp(x))) without overflow: subtract the largest term first."""
    m = max(xs)
    if m == -math.inf:
        return -math.inf
    return m + math.log(math.fsum(math.exp(x - m) for x in xs))


def tail_length(s: int) -> int:
    """M = floor(min(0.2 S, 3 sqrt(S))), the number of ratios in the fitted tail."""
    return int(math.floor(min(0.2 * s, 3.0 * math.sqrt(s))))


def khat_threshold(s: int) -> float:
    """min(1 - 1/log10(S), 0.7): above it the PSIS estimate is flagged as unreliable."""
    return min(1.0 - 1.0 / math.log10(s), 0.7)


def gpd_fit(x: Sequence[float], min_grid: int = 30, prior: float = 3.0,
            shrink_n: float = 10.0, shrink_to: float = 0.5) -> tuple[float, float]:
    """Estimate (k, sigma) of a generalized Pareto law with location 0 from exceedances x >= 0.

    Zhang and Stephens (2009): the profile log-likelihood in theta = -k/sigma is
    n (log(-theta/k(theta)) - k(theta) - 1) with k(theta) = mean(log(1 - theta x)).
    It is averaged over a grid of theta values, weighted by the normalized profile
    likelihood, and k is recomputed at the averaged theta. Then k is shrunk toward
    shrink_to with the weight of shrink_n observations. Positive k is a heavy tail.
    """
    xs = sorted(float(v) for v in x)
    n = len(xs)
    if n == 0 or xs[-1] <= 0.0:
        raise ValueError("gpd_fit needs at least one positive exceedance")
    m = min_grid + int(math.floor(math.sqrt(n)))  # @line L13
    xstar = xs[int(math.floor(n / 4.0 + 0.5)) - 1]  # first quartile
    if xstar <= 0.0:
        xstar = next(v for v in xs if v > 0.0)
    thetas = [1.0 / xs[-1] + (1.0 - math.sqrt(m / (j - 0.5))) / (prior * xstar)  # @line L14
              for j in range(1, m + 1)]
    prof = []
    for th in thetas:
        k = math.fsum(math.log1p(-th * v) for v in xs) / n
        prof.append(n * (math.log(-th / k) - k - 1.0))  # @line L15
    top = log_sum_exp(prof)
    wts = [math.exp(p - top) for p in prof]  # @line L16
    th_hat = math.fsum(w * t for w, t in zip(wts, thetas))
    k_hat = math.fsum(math.log1p(-th_hat * v) for v in xs) / n  # @line L17
    sigma = -k_hat / th_hat
    k_hat = (n * k_hat + shrink_n * shrink_to) / (n + shrink_n)  # @line L18
    return k_hat, sigma


def gpd_quantile(p: float, k: float, sigma: float) -> float:
    """The p-quantile of the generalized Pareto law with location 0, shape k, scale sigma."""
    if abs(k) < 1e-12:
        return -sigma * math.log1p(-p)
    return sigma * math.expm1(-k * math.log1p(-p)) / k


def psis_smooth(log_ratios: Sequence[float]) -> tuple[list[float], float]:
    """Pareto smooth the importance ratios exp(log_ratios).

    Returns the smoothed log weights (shifted so that the largest raw log ratio is
    0, not normalized) and the shape estimate k-hat. If the tail has fewer than 5
    draws, or all its exceedances are 0, the weights are returned unchanged and
    k-hat is reported as infinity, as the reference implementations do.
    """
    s = len(log_ratios)
    m = tail_length(s)  # @line L1
    top = max(log_ratios)
    lw = [v - top for v in log_ratios]  # @line L3
    order = sorted(range(s), key=lambda j: lw[j])  # @line L4
    if m < 5:
        return lw, math.inf
    u = math.exp(lw[order[s - m - 1]])
    tail = [math.exp(lw[j]) - u for j in order[s - m:]]
    if tail[-1] <= 0.0:
        return lw, math.inf
    k, sigma = gpd_fit(tail)  # @line L5
    if not math.isfinite(k):
        return lw, math.inf
    for z in range(1, m + 1):  # @line L6
        w = min(u + gpd_quantile((z - 0.5) / m, k, sigma), 1.0)
        lw[order[s - m + z - 1]] = math.log(w)
    return lw, k  # @line L7


def _variance(xs: Sequence[float]) -> float:
    """Sample variance with divisor len(xs) - 1."""
    n = len(xs)
    mean = math.fsum(xs) / n
    return math.fsum((v - mean) ** 2 for v in xs) / (n - 1)


def psis_loo(loglik: Sequence[Sequence[float]]) -> dict:
    """PSIS-LOO estimate of the expected log pointwise predictive density.

    Returns a dict with elpd_loo, se_elpd_loo (sqrt(n) times the sample standard
    deviation of the pointwise values), p_loo = lppd - elpd_loo, looic = -2 elpd_loo,
    the pointwise elpd values, the k-hat values, and the indices whose k-hat is
    above min(1 - 1/log10(S), 0.7).
    Cost: Theta(n S log S) time for the sorts, Theta(S) extra memory per row.
    """
    n = len(loglik)
    s = len(loglik[0])
    limit = khat_threshold(s)
    pointwise, khats, lppd_i = [], [], []
    for row in loglik:  # @line L2
        if len(row) != s:
            raise ValueError("every row needs the same number of draws")
        lw, k = psis_smooth([-v for v in row])
        num = log_sum_exp([a + b for a, b in zip(lw, row)])  # @line L8
        pointwise.append(num - log_sum_exp(lw))
        khats.append(k)
        lppd_i.append(log_sum_exp(row) - math.log(s))
    elpd = math.fsum(pointwise)  # @line L10
    lppd = math.fsum(lppd_i)
    se = math.sqrt(n * _variance(pointwise)) if n > 1 else math.nan  # @line L11
    return {  # @line L12
        "elpd_loo": elpd,
        "se_elpd_loo": se,
        "p_loo": lppd - elpd,
        "looic": -2.0 * elpd,
        "pointwise": pointwise,
        "k_hat": khats,
        "flagged": [i for i, k in enumerate(khats) if k > limit],  # @line L9
    }


def is_loo_raw(loglik: Sequence[Sequence[float]]) -> list[float]:
    """Plain importance sampling LOO: elpd_i = -log((1/S) sum_s 1/p(y_i | theta^s))."""
    out = []
    for row in loglik:
        out.append(math.log(len(row)) - log_sum_exp([-v for v in row]))
    return out


def waic(loglik: Sequence[Sequence[float]]) -> dict:
    """WAIC from draws: lppd - p_waic, with p_waic the sum of sample variances (divisor S - 1)."""
    n = len(loglik)
    s = len(loglik[0])
    pts, pen, lp = [], [], []
    for row in loglik:
        a = log_sum_exp(row) - math.log(s)
        v = _variance(row)
        lp.append(a)
        pen.append(v)
        pts.append(a - v)
    elpd = math.fsum(pts)
    return {
        "lppd": math.fsum(lp),
        "p_waic": math.fsum(pen),
        "elpd_waic": elpd,
        "waic": -2.0 * elpd,
        "se_elpd_waic": math.sqrt(n * _variance(pts)) if n > 1 else math.nan,
        "pointwise": pts,
    }
