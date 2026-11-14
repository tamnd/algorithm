# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wilson-score-interval/. The authors are listed in prov/H3CD21.jsonl.

import math
from statistics import NormalDist


def wilson_score_interval(x: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """The Wilson score interval [L, U] for a binomial p at nominal level 1 - alpha.

    [L, U] is the set of p with (x - n p)^2 <= z^2 n p (1 - p), where z is the
    upper alpha/2 point of the standard normal: the values that the two-sided
    score test does not reject. The upper root is computed as center plus
    half-width, and the lower root as (x^2 / n) / ((n + z^2) U), the product of
    the roots divided by U, which avoids cancellation when x is small.
    """
    if not (isinstance(x, int) and isinstance(n, int)) or n < 1 or not 0 <= x <= n:
        raise ValueError("need integers with 0 <= x <= n and n >= 1")
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be in (0, 1)")
    z = NormalDist().inv_cdf(1.0 - alpha / 2)  # @line L1
    z2 = z * z
    center = (x + z2 / 2) / (n + z2)  # @line L2
    half = z / (n + z2) * math.sqrt(x * (n - x) / n + z2 / 4)  # @line L3
    # p = 1 is a root exactly when x = n; set it exactly instead of 1 +- rounding.
    upper = 1.0 if x == n else min(1.0, center + half)  # @line L4
    lower = (x * x / n) / ((n + z2) * upper)  # @line L5
    return lower, upper  # @line L6
