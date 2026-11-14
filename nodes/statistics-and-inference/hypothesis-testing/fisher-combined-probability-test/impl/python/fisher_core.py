# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fisher-combined-probability-test/. The authors are listed in prov/SR875B.jsonl.
"""Fisher's method for combining independent p-values.

X = -2 sum ln p_i. When the k p-values are independent and uniform on (0, 1)
under the global null, X has the chi-squared law with 2k degrees of freedom
exactly, and the combined p-value is its upper tail. For even degrees of
freedom the tail is a finite Poisson sum,
    P(chi2_2k >= x) = exp(-x/2) sum_{j < k} (x/2)^j / j!,
which the code evaluates term by term in log space, so that neither the
product of the p-values nor exp(-x/2) underflows.
The code is in this file and not in fisher_combined_probability_test.py,
because tools treat a file whose name ends in _test.py as a test file.
"""

import math
from collections.abc import Sequence


def fisher_method(p: Sequence[float]) -> tuple[float, float]:
    """Combine independent p-values; returns (X, P) with X = -2 sum ln p_i and P = P(chi2_2k >= X)."""
    k = len(p)
    if k == 0:
        raise ValueError("need at least one p-value")
    if any(not 0.0 <= v <= 1.0 for v in p):  # also rejects NaN
        raise ValueError("p-values must lie in [0, 1]")
    if any(v == 0.0 for v in p):  # @line L1
        return math.inf, 0.0
    h = -math.fsum(math.log(v) for v in p)  # @line L2
    x = 2.0 * h  # @line L3
    if h == 0.0:  # all p-values are 1
        return 0.0, 1.0
    log_h = math.log(h)  # @line L4
    terms = [math.exp(-h + j * log_h - math.lgamma(j + 1)) for j in range(k)]
    total = math.fsum(terms)  # @line L5
    return x, min(total, 1.0)  # @line L6
