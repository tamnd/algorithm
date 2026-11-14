# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/likelihood-ratio-test/. The authors are listed in prov/04CJ2P.jsonl.
"""The likelihood ratio test, in general form and for common models.

likelihood_ratio_test takes a log-likelihood and two maximizers and returns
(Lambda, p) with Lambda = 2 (l(theta_hat) - l(theta0_hat)) and p the upper
chi-squared tail with r degrees of freedom (Wilks' theorem, so p is only
asymptotic). The model functions compute Lambda in closed form, as a sum of
deviance terms x log(x / y) - x + y, which do not cancel when x is near y.
most_powerful_test builds the randomized Neyman-Pearson test of a simple
null against a simple alternative on a finite sample space.
The code is in this file and not in likelihood_ratio_test.py, because tools
treat a file whose name ends in _test.py as a test file.
"""

import math
from collections.abc import Callable, Sequence
from fractions import Fraction

from stdist import chi2_sf


def likelihood_ratio_test(loglik: Callable[[object], float],
                          fit_full: Callable[[], object],
                          fit_null: Callable[[], object],
                          r: int) -> tuple[float, float]:
    """General LRT: fit_full and fit_null return maximizers of loglik over Theta and Theta_0."""
    if r < 1:
        raise ValueError("r, the number of constraints, must be at least 1")
    theta_hat = fit_full()  # @line L1
    theta0_hat = fit_null()  # @line L2
    lam = 2.0 * (loglik(theta_hat) - loglik(theta0_hat))  # @line L3
    lam = max(lam, 0.0)  # @line L4
    p = chi2_sf(lam, r)  # @line L5
    return lam, p  # @line L6


def deviance_term(x: float, y: float) -> float:
    """x log(x / y) - x + y for x >= 0 and y > 0, without cancellation near x = y."""
    if y <= 0.0 or x < 0.0:
        raise ValueError("need x >= 0 and y > 0")
    if x == 0.0:
        return y
    d = (x - y) / y
    if abs(d) < 0.1:
        # y h(1 + d) with h(1 + d) = sum_{j >= 2} (-1)^j d^j / (j (j - 1)).
        term, total, j = d * d, 0.0, 2
        while True:
            add = term / (j * (j - 1))
            total += add
            if abs(add) <= 1e-17 * total:
                break
            term *= -d
            j += 1
        return y * total
    return x * math.log(x / y) - x + y


def binomial_lrt(k: int, n: int, p0: float) -> tuple[float, float]:
    """LRT of H_0: p = p0 from k successes in n trials; r = 1."""
    if n < 1 or not 0 <= k <= n or not 0.0 < p0 < 1.0:
        raise ValueError("need n >= 1, 0 <= k <= n and 0 < p0 < 1")
    lam = 2.0 * (deviance_term(k, n * p0) + deviance_term(n - k, n * (1.0 - p0)))
    return lam, chi2_sf(lam, 1)


def poisson_lrt(total: int, n: int, lam0: float) -> tuple[float, float]:
    """LRT of H_0: lambda = lam0 from n iid Poisson counts with sum total; r = 1."""
    if n < 1 or total < 0 or lam0 <= 0.0:
        raise ValueError("need n >= 1, total >= 0 and lam0 > 0")
    lam = 2.0 * deviance_term(total, n * lam0)
    return lam, chi2_sf(lam, 1)


def normal_mean_lrt(x: Sequence[float], mu0: float,
                    sigma: float | None = None) -> tuple[float, float]:
    """LRT of H_0: mu = mu0 for iid normal data; r = 1.

    With sigma known, Lambda = n (xbar - mu0)^2 / sigma^2. With sigma unknown
    (sigma=None), Lambda = n log(1 + n (xbar - mu0)^2 / SS), SS = sum (x - xbar)^2,
    which equals n log(1 + T^2 / (n - 1)) for the t statistic T.
    """
    n = len(x)
    mean = math.fsum(x) / n if n else 0.0
    if sigma is not None:
        if n < 1 or sigma <= 0.0:
            raise ValueError("need n >= 1 and sigma > 0")
        lam = n * (mean - mu0) ** 2 / sigma ** 2
    else:
        if n < 2:
            raise ValueError("need n >= 2 when sigma is unknown")
        ss = math.fsum((v - mean) ** 2 for v in x)
        if ss == 0.0:
            raise ValueError("all observations are equal")
        lam = n * math.log1p(n * (mean - mu0) ** 2 / ss)
    return lam, chi2_sf(lam, 1)


def multinomial_lrt(counts: Sequence[int], probs: Sequence[float]) -> tuple[float, float]:
    """G-test of H_0: cell probabilities = probs; r = m - 1 for m cells."""
    m, n = len(counts), sum(counts)
    if m < 2 or n < 1 or len(probs) != m or any(c < 0 for c in counts):
        raise ValueError("need at least 2 cells, nonnegative counts and one prob per cell")
    if any(q <= 0.0 for q in probs) or abs(math.fsum(probs) - 1.0) > 1e-12:
        raise ValueError("probs must be positive and sum to 1")
    lam = 2.0 * math.fsum(deviance_term(c, n * q) for c, q in zip(counts, probs))
    return lam, chi2_sf(lam, m - 1)


def most_powerful_test(f0: Sequence[Fraction], f1: Sequence[Fraction],
                       alpha: Fraction) -> list[Fraction]:
    """The Neyman-Pearson test phi on a finite sample space, with E_0 phi = alpha.

    Points are taken in decreasing order of f1 / f0 (points with f0 = 0 first)
    until the size budget alpha is spent; the last point is randomized.
    Ties in the ratio share the remaining budget in proportion to f0.
    """
    m = len(f0)
    if len(f1) != m or not 0 <= alpha <= 1:
        raise ValueError("need f0, f1 of equal length and 0 <= alpha <= 1")
    phi = [Fraction(0)] * m
    for i in range(m):
        if f0[i] == 0 and f1[i] > 0:
            phi[i] = Fraction(1)
    ratio = {i: Fraction(f1[i]) / f0[i] for i in range(m) if f0[i] > 0}
    budget = Fraction(alpha)
    for k in sorted(set(ratio.values()), reverse=True):
        level = [i for i in ratio if ratio[i] == k]
        mass = sum(Fraction(f0[i]) for i in level)
        share = min(Fraction(1), budget / mass)
        for i in level:
            phi[i] = share
        budget -= share * mass
        if budget == 0:
            break
    return phi
