# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/z-test/. The authors are listed in prov/PZWGTN.jsonl.
"""The one-sample, two-sample and one-proportion z-tests.

Each function returns (z, p): the statistic and its p-value for the chosen
alternative, "two-sided", "greater" (H_1: parameter > null value) or "less".
Upper tails come from erfc, not from 1 - cdf, so small p-values keep their
relative accuracy. The code is in this file and not in z_test.py, because
tools treat a file whose name ends in _test.py as a test file.
"""

import math
from collections.abc import Sequence

from stdist import norm_cdf, norm_sf

ALTERNATIVES = ("two-sided", "greater", "less")


def normal_p_value(z: float, alternative: str = "two-sided") -> float:
    """The p-value of an observed z when Z is standard normal under H_0."""
    if alternative == "two-sided":
        return min(1.0, 2.0 * norm_sf(abs(z)))  # @line L6
    if alternative == "greater":
        return norm_sf(z)  # @line L7
    if alternative == "less":
        return norm_cdf(z)  # @line L8
    raise ValueError(f"alternative must be one of {ALTERNATIVES}")


def z_test(x: Sequence[float], mu0: float, sigma: float,
           alternative: str = "two-sided") -> tuple[float, float]:
    """Test H_0: mu = mu0 for iid N(mu, sigma^2) data with sigma known."""
    n = len(x)  # @line L1
    if n < 1 or sigma <= 0.0:
        raise ValueError("need at least one observation and sigma > 0")
    s = math.fsum(x)  # @line L2
    mean = s / n  # @line L3
    z = (mean - mu0) / (sigma / math.sqrt(n))  # @line L4
    return z, normal_p_value(z, alternative)  # @line L5


def two_sample_z_test(x: Sequence[float], y: Sequence[float], sigma_x: float, sigma_y: float,
                      delta0: float = 0.0, alternative: str = "two-sided") -> tuple[float, float]:
    """Test H_0: mu_x - mu_y = delta0 for two independent normal samples with known sigmas."""
    m, n = len(x), len(y)
    if m < 1 or n < 1 or sigma_x <= 0.0 or sigma_y <= 0.0:
        raise ValueError("need non-empty samples and positive sigmas")
    diff = math.fsum(x) / m - math.fsum(y) / n
    se = math.sqrt(sigma_x * sigma_x / m + sigma_y * sigma_y / n)
    z = (diff - delta0) / se
    return z, normal_p_value(z, alternative)


def proportion_z_test(k: int, n: int, p0: float,
                      alternative: str = "two-sided") -> tuple[float, float]:
    """Large-sample test of H_0: p = p0 from k successes in n Bernoulli trials.

    The standard error uses p0, the value under H_0. The null distribution
    is standard normal only in the limit n -> infinity.
    """
    if n < 1 or not 0 <= k <= n or not 0.0 < p0 < 1.0:
        raise ValueError("need n >= 1, 0 <= k <= n and 0 < p0 < 1")
    z = (k - n * p0) / math.sqrt(n * p0 * (1.0 - p0))
    return z, normal_p_value(z, alternative)
