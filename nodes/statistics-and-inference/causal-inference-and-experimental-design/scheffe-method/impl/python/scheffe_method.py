# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scheffe-method/. The authors are listed in prov/JFSS0K.jsonl.
"""Scheffe's method: simultaneous intervals and tests for all contrasts of k group means.

A contrast is c = (c_1, ..., c_k) with sum c_i = 0, and psi = sum c_i mu_i. Its estimate is
psi_hat = sum c_i ybar_i with standard error sqrt(MSE sum c_i^2 / n_i). Scheffe's interval is
psi_hat +- sqrt((k - 1) F_crit) se, where F_crit is the upper alpha point of F with
(k - 1, N - k) degrees of freedom. The intervals hold simultaneously for every contrast with
probability exactly 1 - alpha under the normal model, because the largest squared
standardized contrast is SSB / MSE = (k - 1) F, the one-way ANOVA statistic times k - 1.
"""

import math
from collections.abc import Sequence
from typing import NamedTuple

from stdist import f_ppf, f_sf


class Contrast(NamedTuple):
    estimate: float  # psi_hat
    se: float        # sqrt(MSE sum c_i^2 / n_i)
    f: float         # psi_hat^2 / ((k - 1) se^2), referred to F_(k-1, N-k)
    p: float         # the Scheffe adjusted p-value
    lo: float
    hi: float


def summary(groups: Sequence[Sequence[float]]) -> tuple[list[int], list[float], float, int]:
    """Group sizes, group means, MSE (two-pass) and its degrees of freedom N - k."""
    k = len(groups)
    n = [len(g) for g in groups]
    if k < 2 or min(n) == 0 or sum(n) <= k:
        raise ValueError("need k >= 2 nonempty groups and N > k")
    means = [math.fsum(g) / len(g) for g in groups]
    ssw = math.fsum((v - m) ** 2 for g, m in zip(groups, means) for v in g)
    if ssw == 0.0:
        raise ValueError("every group is constant, so MSE = 0")
    return n, means, ssw / (sum(n) - k), sum(n) - k


def scheffe(groups: Sequence[Sequence[float]], contrasts: Sequence[Sequence[float]],
            alpha: float = 0.05) -> list[Contrast]:
    """Scheffe intervals and adjusted p-values for the given contrasts."""
    k = len(groups)
    n, means, mse, nu = summary(groups)  # @line L1
    mult = math.sqrt((k - 1) * f_ppf(1.0 - alpha, k - 1, nu))  # @line L2
    out = []
    for c in contrasts:  # @line L3
        if len(c) != k or abs(math.fsum(c)) > 1e-9 * max(map(abs, c)) or not any(c):
            raise ValueError("a contrast needs k coefficients that sum to 0, not all 0")
        est = math.fsum(ci * m for ci, m in zip(c, means))  # @line L4
        se = math.sqrt(mse * math.fsum(ci * ci / ni for ci, ni in zip(c, n)))  # @line L5
        f = est * est / ((k - 1) * se * se)  # @line L6
        out.append(Contrast(est, se, f, f_sf(f, k - 1, nu), est - mult * se, est + mult * se))  # @line L7
    return out  # @line L8


def best_contrast(groups: Sequence[Sequence[float]]) -> list[float]:
    """The contrast with the largest psi_hat^2 / se^2: c_i = n_i (ybar_i - ybar), up to scale."""
    n, means, _, _ = summary(groups)
    grand = math.fsum(ni * m for ni, m in zip(n, means)) / sum(n)
    return [ni * (m - grand) for ni, m in zip(n, means)]
