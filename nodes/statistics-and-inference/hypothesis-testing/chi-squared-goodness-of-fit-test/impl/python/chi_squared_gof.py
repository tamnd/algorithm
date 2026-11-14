# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chi-squared-goodness-of-fit-test/. The authors are listed in prov/B43M8J.jsonl.

import math
from collections.abc import Sequence

from stdist import chi2_sf


def chi_squared_gof(
    observed: Sequence[int],
    probs: Sequence[float] | None = None,
    fitted: int = 0,
    statistic: str = "pearson",
) -> tuple[float, int, float]:
    """Pearson's chi-squared goodness-of-fit test.

    observed holds the counts of k categories; probs holds the null cell
    probabilities (equal cells when None). fitted is the number s of
    parameters estimated by maximum likelihood from these grouped counts,
    which lowers the degrees of freedom to k - 1 - s. statistic "pearson"
    gives X^2 = sum (O - E)^2 / E; "g" gives the likelihood-ratio statistic
    G = 2 sum O log(O / E). Returns (statistic, degrees of freedom, p-value),
    where the p-value is the upper tail of the chi-square law.
    """
    k = len(observed)
    if k < 2 or any(not isinstance(o, int) or o < 0 for o in observed):
        raise ValueError("need at least two non-negative integer counts")
    if probs is None:
        probs = [1.0 / k] * k
    if len(probs) != k or any(not p > 0 for p in probs) or abs(math.fsum(probs) - 1.0) > 1e-9:
        raise ValueError("probs must be k positive numbers that sum to 1")
    if statistic not in ("pearson", "g"):
        raise ValueError("unknown statistic")
    n = sum(observed)  # @line L1
    if n == 0:
        raise ValueError("need at least one observation")
    expected = [n * p for p in probs]  # @line L2
    if statistic == "pearson":  # @line L3
        x2 = math.fsum((o - e) ** 2 / e for o, e in zip(observed, expected))
    else:
        x2 = 2.0 * math.fsum(o * math.log(o / e) for o, e in zip(observed, expected) if o > 0)
    df = k - 1 - fitted  # @line L4
    if df < 1:
        raise ValueError("need k - 1 - fitted >= 1")
    return x2, df, chi2_sf(x2, df)  # @line L5
