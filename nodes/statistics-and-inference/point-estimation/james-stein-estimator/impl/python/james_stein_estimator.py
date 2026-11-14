# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/james-stein-estimator/. The authors are listed in prov/CYEN4M.jsonl.

import math
from typing import Optional, Sequence


def james_stein(
    x: Sequence[float],
    sigma2: float = 1.0,
    target: Optional[Sequence[float]] = None,
    positive_part: bool = False,
) -> list[float]:
    """Return the James-Stein estimate of theta from one draw x of N_p(theta, sigma2 I).

    The estimate is m + c (x - m) with c = 1 - (p - 2) sigma2 / ||x - m||^2,
    where m is the target (zero by default). With positive_part=True, c is
    replaced by max(c, 0). Needs p >= 3 and a known sigma2 > 0. If x equals
    the target (an event of probability zero), the target is returned.
    Cost: Theta(p) time, Theta(p) memory for the result.
    """
    p = len(x)  # @line L1
    if p < 3:
        raise ValueError("the James-Stein estimator needs p >= 3")
    if not sigma2 > 0.0:
        raise ValueError("sigma2 must be positive")
    m = [0.0] * p if target is None else [float(t) for t in target]
    if len(m) != p:
        raise ValueError("target must have the same length as x")
    d = [float(xi) - mi for xi, mi in zip(x, m)]
    s = math.fsum(t * t for t in d)  # @line L2
    if s == 0.0:  # @line L3
        return m
    k = (p - 2) * sigma2  # @line L4
    if positive_part and s <= k:  # @line L5
        return m
    theta = [mi + di - k * (di / s) for mi, di in zip(m, d)]  # @line L6
    return theta  # @line L7


def james_stein_toward_mean(
    x: Sequence[float], sigma2: float = 1.0, positive_part: bool = False
) -> list[float]:
    """Return Lindley's variant, which shrinks x toward its own mean.

    The estimate is xbar + c (x - xbar 1) with
    c = 1 - (p - 3) sigma2 / sum_i (x_i - xbar)^2. Needs p >= 4.
    """
    p = len(x)
    if p < 4:
        raise ValueError("shrinking toward the mean needs p >= 4")
    if not sigma2 > 0.0:
        raise ValueError("sigma2 must be positive")
    xbar = math.fsum(x) / p
    d = [float(xi) - xbar for xi in x]
    s = math.fsum(t * t for t in d)
    k = (p - 3) * sigma2
    if s == 0.0 or (positive_part and s <= k):
        return [xbar] * p
    return [xbar + di - k * (di / s) for di in d]


def stein_unbiased_risk_estimate(
    x: Sequence[float], sigma2: float = 1.0, target: Optional[Sequence[float]] = None
) -> float:
    """Return SURE for the plain James-Stein estimate: sigma2 (p - (p - 2)^2 sigma2 / ||x - m||^2).

    Its expectation under theta is the risk of james_stein at theta.
    """
    p = len(x)
    if p < 3:
        raise ValueError("needs p >= 3")
    m = [0.0] * p if target is None else [float(t) for t in target]
    s = math.fsum((float(xi) - mi) ** 2 for xi, mi in zip(x, m))
    if s == 0.0:
        return -math.inf
    return sigma2 * (p - (p - 2) ** 2 * sigma2 / s)


def inverse_moment_noncentral_chi2(p: int, lam: float) -> float:
    """Return E[1/W] for W ~ noncentral chi-squared with p >= 3 degrees of freedom and noncentrality lam.

    Uses the Poisson mixture: E[1/W] = sum_k Poisson(k; lam/2) / (p - 2 + 2k).
    Only the terms within 40 standard deviations of the Poisson mean are summed.
    """
    if p < 3:
        raise ValueError("E[1/W] is finite only for p >= 3")
    if lam < 0.0:
        raise ValueError("lam must be nonnegative")
    mu = lam / 2.0
    if mu == 0.0:
        return 1.0 / (p - 2)
    width = 40.0 * math.sqrt(mu) + 50.0
    lo = max(0, int(mu - width))
    hi = int(mu + width) + 1
    log_mu = math.log(mu)
    terms = []
    for k in range(lo, hi + 1):
        w = math.exp(-mu + k * log_mu - math.lgamma(k + 1))
        terms.append(w / (p - 2 + 2 * k))
    return math.fsum(terms)


def james_stein_risk(lam: float, p: int, sigma2: float = 1.0) -> float:
    """Return the exact risk E||JS(X) - theta||^2 of the plain James-Stein estimate.

    lam = ||theta - m||^2 is the squared distance from theta to the target.
    The risk is sigma2 (p - (p - 2)^2 E[1/W]) with W ~ chi-squared_p(lam / sigma2).
    """
    return sigma2 * (p - (p - 2) ** 2 * inverse_moment_noncentral_chi2(p, lam / sigma2))
