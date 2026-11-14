# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/t-confidence-interval/. The authors are listed in prov/W2JAG5.jsonl.
"""The Student t confidence interval for a normal mean with unknown variance.

t_interval returns (lower, upper). side = "two-sided" gives
x-bar -+ t_(n-1, 1-alpha/2) S / sqrt(n); side = "lower" gives the lower
confidence bound [x-bar - t_(n-1, 1-alpha) S / sqrt(n), inf); side = "upper"
gives (-inf, x-bar + t_(n-1, 1-alpha) S / sqrt(n)]. S^2 has the divisor
n - 1 and is computed by two passes.
"""

import math
from collections.abc import Sequence
from functools import lru_cache

from stdist import t_ppf as _t_ppf

SIDES = ("two-sided", "lower", "upper")

# The quantile depends only on (p, n - 1); repeated calls, as in a simulation, reuse it.
t_ppf = lru_cache(maxsize=1024)(_t_ppf)


def t_interval(x: Sequence[float], confidence: float = 0.95,
               side: str = "two-sided") -> tuple[float, float]:
    """A confidence interval for the mean of iid normal data, exact coverage `confidence`."""
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must be in (0, 1)")
    if side not in SIDES:
        raise ValueError(f"side must be one of {SIDES}")
    n = len(x)  # @line L1
    if n < 2:
        raise ValueError("need at least 2 observations")
    mean = math.fsum(x) / n  # @line L2
    s2 = math.fsum((v - mean) ** 2 for v in x) / (n - 1)  # @line L3
    se = math.sqrt(s2 / n)  # @line L4
    if side == "two-sided":
        q = t_ppf(1.0 - (1.0 - confidence) / 2.0, n - 1)  # @line L5
        return mean - q * se, mean + q * se  # @line L6
    q = t_ppf(confidence, n - 1)  # @line L7
    if side == "lower":
        return mean - q * se, math.inf  # @line L8
    return -math.inf, mean + q * se  # @line L9
