# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tukey-hsd/. The authors are listed in prov/N35W2Z.jsonl.
"""Tukey's honestly significant difference test for all pairwise differences of k means.

For each pair (i, j) the statistic is q = |ybar_i - ybar_j| / sqrt((MSE / 2)(1/n_i + 1/n_j)),
with MSE the pooled within-group variance on nu = N - k degrees of freedom. The adjusted
p-value is P(Q > q) for the studentized range Q with k means and nu degrees of freedom, and
the simultaneous interval is ybar_i - ybar_j +- q_crit sqrt((MSE / 2)(1/n_i + 1/n_j)).
With equal group sizes this is Tukey's test, whose family-wise coverage is exactly 1 - alpha
under the normal model. With unequal sizes the same formula is the Tukey-Kramer method,
whose coverage is at least 1 - alpha (Hayter, 1984).
"""

import math
from collections.abc import Sequence
from typing import NamedTuple

from srange import srange_ppf, srange_sf


class Pair(NamedTuple):
    i: int
    j: int
    diff: float   # ybar_i - ybar_j
    se: float     # sqrt((MSE / 2)(1/n_i + 1/n_j))
    q: float      # |diff| / se
    p: float      # P(Q_(k, nu) > q), the adjusted p-value
    lo: float     # simultaneous interval for mu_i - mu_j
    hi: float


def means_and_mse(groups: Sequence[Sequence[float]]) -> tuple[list[float], float, int]:
    """Group means, the pooled within-group mean square (two-pass) and its degrees of freedom."""
    k = len(groups)
    big_n = sum(len(g) for g in groups)
    if k < 2 or any(len(g) == 0 for g in groups) or big_n <= k:
        raise ValueError("need k >= 2 nonempty groups and N > k")
    means = [math.fsum(g) / len(g) for g in groups]
    ssw = math.fsum((v - m) ** 2 for g, m in zip(groups, means) for v in g)
    if ssw == 0.0:
        raise ValueError("every group is constant, so MSE = 0")
    return means, ssw / (big_n - k), big_n - k


def tukey_hsd(groups: Sequence[Sequence[float]], alpha: float = 0.05) -> tuple[float, list[Pair]]:
    """(q_crit, pairs): the critical value of the studentized range and one record per pair i < j."""
    k = len(groups)
    means, mse, nu = means_and_mse(groups)  # @line L1
    q_crit = srange_ppf(1.0 - alpha, k, nu)  # @line L2
    pairs = []
    for i in range(k):  # @line L3
        for j in range(i + 1, k):
            diff = means[i] - means[j]  # @line L4
            se = math.sqrt(0.5 * mse * (1.0 / len(groups[i]) + 1.0 / len(groups[j])))
            q = abs(diff) / se  # @line L5
            p = srange_sf(q, k, nu)  # @line L6
            pairs.append(Pair(i, j, diff, se, q, p, diff - q_crit * se, diff + q_crit * se))  # @line L7
    return q_crit, pairs  # @line L8
