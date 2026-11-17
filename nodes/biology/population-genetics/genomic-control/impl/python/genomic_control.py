# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/genomic-control/. The authors are listed in prov/MQGC1J.jsonl.
"""Genomic control for a case-control association scan.

Each SNP is tested with the Cochran-Armitage trend test, which equals
N r^2, where N is the number of individuals and r is the Pearson
correlation of the allele dosage (0, 1 or 2) with the case status (1 for a
case, 0 for a control). Under the null of no association and no
confounding, each statistic is approximately chi-squared with 1 degree of
freedom. Genomic control estimates the inflation factor lambda as the
median of the M statistics divided by the median of the chi-squared law
with 1 degree of freedom, and divides every statistic by lambda
(Devlin and Roeder 1999).
"""

from __future__ import annotations

from fractions import Fraction
from statistics import NormalDist
from typing import List, Sequence, Tuple

from biostoch import chi2_sf

# The median of the chi-squared law with 1 df is the square of the 0.75
# quantile of the standard normal law: 0.454936...
CHI2_1_MEDIAN = NormalDist().inv_cdf(0.75) ** 2


def trend_statistic(dosage: Sequence[int], status: Sequence[int], exact: bool = False):
    """The Cochran-Armitage trend statistic N r^2 for one SNP.

    It is computed from integer sums, as
    N (N Sxy - Sx Sy)^2 / ((N Sxx - Sx^2) (N Sy - Sy^2)),
    so with exact=True the result is a Fraction. A SNP without variation, or
    a sample with only cases or only controls, gives 0.
    """
    n = len(dosage)
    if n != len(status):
        raise ValueError("dosage and status need the same length")
    sx = sxx = sy = sxy = 0
    for x, y in zip(dosage, status):
        sx += x
        sxx += x * x
        sy += y
        sxy += x * y
    vx = n * sxx - sx * sx
    vy = n * sy - sy * sy
    if vx == 0 or vy == 0:
        return Fraction(0) if exact else 0.0
    num = n * (n * sxy - sx * sy) ** 2
    den = vx * vy
    return Fraction(num, den) if exact else num / den


def median(xs: Sequence[float]) -> float:
    """The sample median (the mean of the two middle values for an even count)."""
    s = sorted(xs)
    k = len(s)
    if k == 0:
        raise ValueError("empty sample")
    mid = k // 2
    return s[mid] if k % 2 else (s[mid - 1] + s[mid]) / 2


def inflation_factor(stats: Sequence[float]) -> float:
    """lambda = median(stats) / 0.454936, without the floor at 1."""
    return median(stats) / CHI2_1_MEDIAN


def genomic_control(stats: Sequence[float]) -> Tuple[float, List[float], List[float]]:
    """Apply genomic control to 1-df association statistics.

    Returns (lam, adjusted, pvalues): lam = max(1, median / 0.454936), the
    statistics divided by lam, and their chi-squared (1 df) p-values.
    """
    m = median(stats)  # @line L2
    lam = max(1.0, m / CHI2_1_MEDIAN)  # @line L3
    adjusted = [t / lam for t in stats]  # @line L4
    pvalues = [chi2_sf(t, 1) for t in adjusted]  # @line L5
    return lam, adjusted, pvalues  # @line L6


def association_scan(genotypes: Sequence[Sequence[int]], status: Sequence[int]):
    """Trend test at every SNP, then genomic control.

    genotypes[i][j] is the dosage of individual i at SNP j. Returns the raw
    statistics followed by the result of genomic_control.
    """
    m = len(genotypes[0])
    stats = []
    for j in range(m):  # @line L1
        stats.append(trend_statistic([row[j] for row in genotypes], status))
    lam, adjusted, pvalues = genomic_control(stats)
    return stats, lam, adjusted, pvalues
