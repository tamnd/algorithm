# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sample-size-determination/. The authors are listed in prov/43QS5G.jsonl.
"""Sample size for the z-test and the t-test of a mean or of two means.

The z-test sizes use the closed form and an exact power search. The t-test
power needs the noncentral t distribution, which the helper does not have, so
t_power computes it as a one-dimensional integral over the chi distribution
of the scaled standard deviation, by the composite Simpson rule.

Conventions: delta is the true difference mu - mu_0 (one sample) or
mu_1 - mu_2 (two samples), sigma the common standard deviation, alpha the
level, power the target power 1 - beta, sides 1 or 2, groups 1 (one-sample or
paired test, n observations) or 2 (two independent samples, n in each group).
For sides = 1 the test rejects in the direction of delta.
"""

import math

from stdist import norm_cdf, norm_ppf, t_ppf

_SIMPSON_INTERVALS = 800  # per piece, even; the error at lambda = 0 is below 1e-8 for nu >= 1


def _check(delta: float, sigma: float, alpha: float, sides: int, groups: int) -> None:
    if sigma <= 0.0 or delta == 0.0:
        raise ValueError("need sigma > 0 and delta != 0")
    if not 0.0 < alpha < 1.0 or sides not in (1, 2) or groups not in (1, 2):
        raise ValueError("need 0 < alpha < 1, sides in (1, 2) and groups in (1, 2)")


def _noncentrality(n: int, delta: float, sigma: float, groups: int) -> float:
    """lambda = |delta| / sigma divided by the standard error factor of the mean (difference)."""
    return abs(delta) / sigma * math.sqrt(n / groups)


def z_sample_size_formula(delta: float, sigma: float, alpha: float = 0.05,
                          power: float = 0.8, sides: int = 2, groups: int = 1) -> int:
    """ceil(groups * ((z_(1 - alpha/sides) + z_power) sigma / delta)^2).

    For sides = 2 this ignores the far rejection tail, so it can be 1 too
    large when the exact power at n - 1 already reaches the target.
    """
    _check(delta, sigma, alpha, sides, groups)
    if not 0.0 < power < 1.0:
        raise ValueError("need 0 < power < 1")
    z = norm_ppf(1.0 - alpha / sides) + norm_ppf(power)
    return max(1, math.ceil(groups * (z * sigma / delta) ** 2))


def z_power(n: int, delta: float, sigma: float, alpha: float = 0.05,
            sides: int = 2, groups: int = 1) -> float:
    """Exact power of the z-test with known sigma, both tails counted."""
    _check(delta, sigma, alpha, sides, groups)
    lam = _noncentrality(n, delta, sigma, groups)
    c = norm_ppf(1.0 - alpha / sides)
    if sides == 1:
        return norm_cdf(lam - c)
    return norm_cdf(lam - c) + norm_cdf(-lam - c)


def z_sample_size(delta: float, sigma: float, alpha: float = 0.05, power: float = 0.8,
                  sides: int = 2, groups: int = 1) -> int:
    """The smallest n with z_power(n) >= power (n per group when groups = 2).

    z_power increases with n, and the closed form n already reaches the
    target with the near tail alone, so the search steps down from it.
    """
    n = z_sample_size_formula(delta, sigma, alpha, power, sides, groups)
    while n > 1 and z_power(n - 1, delta, sigma, alpha, sides, groups) >= power:
        n -= 1
    return n


def _log_chi_density(s: float, nu: int) -> float:
    """log of the density of S = sqrt(V) for V chi-square with nu degrees of freedom."""
    return ((nu - 1) * math.log(s) - 0.5 * s * s
            - (0.5 * nu - 1.0) * math.log(2.0) - math.lgamma(0.5 * nu))


def t_power(n: int, delta: float, sigma: float, alpha: float = 0.05,
            sides: int = 2, groups: int = 1) -> float:
    """Power of the t-test at the true difference delta, by numerical integration.

    T = (Z + lambda) / (S / sqrt(nu)) with Z standard normal and S a chi
    variable with nu degrees of freedom, independent. Given S = s, the test
    rejects with probability Phi(lambda - c s / sqrt(nu)) (plus the far tail
    Phi(-lambda - c s / sqrt(nu)) for sides = 2), where c is the t critical
    value. The function integrates this against the chi density by Simpson.
    """
    _check(delta, sigma, alpha, sides, groups)
    nu = groups * (n - 1)
    if nu < 1:
        raise ValueError("need at least 1 degree of freedom")
    lam = _noncentrality(n, delta, sigma, groups)
    c = t_ppf(1.0 - alpha / sides, nu)
    root = math.sqrt(nu)

    def integrand(s: float) -> float:
        g = norm_cdf(lam - c * s / root)
        if sides == 2:
            g += norm_cdf(-lam - c * s / root)
        if s <= 0.0:
            # The chi density at 0 is sqrt(2/pi) for nu = 1 and 0 for nu >= 2.
            return g * math.sqrt(2.0 / math.pi) if nu == 1 else 0.0
        return g * math.exp(_log_chi_density(s, nu))

    mode = math.sqrt(max(nu - 1.0, 0.0))
    lo, hi = max(0.0, mode - 12.0), mode + 12.0  # the chi sd is below 0.8
    # The rejection probability falls from 1 to 0 within about 10 root / c of
    # lambda root / c (near tail) and of 0 (far tail); split the range there.
    w = 10.0 * root / c
    centre = lam * root / c
    cuts = sorted({lo, hi, *(min(max(v, lo), hi) for v in (centre - w, centre + w, w))})
    m = _SIMPSON_INTERVALS
    total = 0.0
    for a, b in zip(cuts, cuts[1:]):
        h = (b - a) / m
        part = integrand(a) + integrand(b)
        for i in range(1, m):
            part += (4.0 if i % 2 else 2.0) * integrand(a + i * h)
        total += part * h / 3.0
    return total


def t_sample_size(delta: float, sigma: float, alpha: float = 0.05, power: float = 0.8,
                  sides: int = 2, groups: int = 1) -> int:
    """The smallest n with t_power(n) >= power (n per group when groups = 2).

    At every n the t-test has at most the power of the z-test (the z-test is
    most powerful, or most powerful unbiased, when sigma is known), so no n
    below z_sample_size can work, and the search starts there.
    """
    n = max(z_sample_size(delta, sigma, alpha, power, sides, groups), 2)
    while t_power(n, delta, sigma, alpha, sides, groups) < power:
        n += 1
    return n


def z_width_sample_size(half_width: float, sigma: float, alpha: float = 0.05) -> int:
    """The smallest n for which the z interval X-bar +- z_(1 - alpha/2) sigma / sqrt(n) has half-width <= half_width."""
    if half_width <= 0.0 or sigma <= 0.0 or not 0.0 < alpha < 1.0:
        raise ValueError("need half_width > 0, sigma > 0 and 0 < alpha < 1")
    z = norm_ppf(1.0 - alpha / 2.0)
    n = max(1, math.ceil((z * sigma / half_width) ** 2))
    while n > 1 and z * sigma / math.sqrt(n - 1) <= half_width:
        n -= 1  # guard against rounding in the square
    return n
