# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/one-way-anova/. The authors are listed in prov/QHQ1W6.jsonl.
"""One-way analysis of variance, and Welch's heteroscedastic version.

one_way_anova splits the total sum of squares into the part between the group
means and the part within the groups, and refers the ratio of their mean
squares to the F distribution with (k - 1, N - k) degrees of freedom. Each
group sum of squares uses the two-pass formula (subtract the group mean
first), which does not cancel like sum y^2 - n ybar^2. The p-value comes from
the upper tail f_sf directly, not from 1 - cdf.

welch_anova is Welch's (1951) test, which weights each group by n_i / s_i^2
and does not assume equal variances. With two groups its statistic is the
square of the Welch t statistic.
"""

import math
from collections.abc import Sequence
from typing import NamedTuple

from stdist import f_sf


class AnovaResult(NamedTuple):
    f: float          # the F statistic
    df1: int          # k - 1
    df2: int          # N - k
    p: float          # P(F_(df1, df2) > f)
    ssb: float        # sum of squares between groups
    ssw: float        # sum of squares within groups
    means: list[float]


def one_way_anova(groups: Sequence[Sequence[float]]) -> AnovaResult:
    """Test H_0: all k group means are equal, for normal groups with a common variance."""
    k = len(groups)
    if k < 2 or any(len(g) == 0 for g in groups):
        raise ValueError("need at least two nonempty groups")
    n = [len(g) for g in groups]
    big_n = sum(n)  # @line L1
    if big_n <= k:
        raise ValueError("need N > k, so that some group has two or more values")
    means = [math.fsum(g) / len(g) for g in groups]  # @line L2
    grand = math.fsum(ni * m for ni, m in zip(n, means)) / big_n  # @line L3
    ssb = math.fsum(ni * (m - grand) ** 2 for ni, m in zip(n, means))  # @line L4
    ssw = math.fsum((v - m) ** 2 for g, m in zip(groups, means) for v in g)  # @line L5
    if ssw == 0.0:
        raise ValueError("every group is constant, so the within mean square is 0")
    df1, df2 = k - 1, big_n - k
    f = (ssb / df1) / (ssw / df2)  # @line L6
    p = f_sf(f, df1, df2)  # @line L7
    return AnovaResult(f, df1, df2, p, ssb, ssw, means)  # @line L8


def welch_anova(groups: Sequence[Sequence[float]]) -> tuple[float, float, float, float]:
    """Welch's test of equal means without equal variances: (F*, df1, df2, p)."""
    k = len(groups)
    if k < 2 or any(len(g) < 2 for g in groups):
        raise ValueError("need at least two groups of two or more values")
    n = [len(g) for g in groups]
    means = [math.fsum(g) / len(g) for g in groups]
    var = [math.fsum((v - m) ** 2 for v in g) / (len(g) - 1) for g, m in zip(groups, means)]
    if any(v == 0.0 for v in var):
        raise ValueError("a group is constant, so its weight n / s^2 is infinite")
    w = [ni / v for ni, v in zip(n, var)]
    total_w = math.fsum(w)
    mw = math.fsum(wi * m for wi, m in zip(w, means)) / total_w
    a = math.fsum(wi * (m - mw) ** 2 for wi, m in zip(w, means)) / (k - 1)
    lam = math.fsum((1.0 - wi / total_w) ** 2 / (ni - 1) for wi, ni in zip(w, n))
    f = a / (1.0 + 2.0 * (k - 2) / (k * k - 1) * lam)
    df2 = (k * k - 1) / (3.0 * lam)
    return f, k - 1, df2, f_sf(f, k - 1, df2)
