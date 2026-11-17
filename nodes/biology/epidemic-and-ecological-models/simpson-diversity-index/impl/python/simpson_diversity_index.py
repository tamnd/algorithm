# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simpson-diversity-index/. The authors are listed in prov/2B5Z97.jsonl.
"""The forms of the Simpson index of a list of integer species counts.

Input: counts n_i >= 0 with a positive sum n. Output, as exact fractions:
the concentration lambda = sum (n_i / n)^2, the Gini-Simpson index
1 - lambda, the inverse Simpson index 1 / lambda, and the form without
replacement lambda_u = sum n_i (n_i - 1) / (n (n - 1)) with 1 - lambda_u
(both None when n < 2). Cost: Theta(k) arithmetic operations for k counts.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Optional, Sequence


@dataclass(frozen=True)
class Simpson:
    concentration: Fraction
    gini_simpson: Fraction
    inverse: Fraction
    unbiased: Optional[Fraction]
    gini_simpson_unbiased: Optional[Fraction]


def simpson(counts: Sequence[int]) -> Simpson:
    """Compute the Simpson forms from the counts."""
    if any(c < 0 for c in counts):
        raise ValueError("counts must be >= 0")
    n = sum(counts)  # @line L1
    if n <= 0:
        raise ValueError("counts must have a positive sum")
    lam = sum((Fraction(c, n) ** 2 for c in counts), Fraction(0))  # @line L2
    if n >= 2:
        lam_u = Fraction(sum(c * (c - 1) for c in counts), n * (n - 1))  # @line L3
        gs_u = 1 - lam_u
    else:
        lam_u = None
        gs_u = None
    return Simpson(lam, 1 - lam, 1 / lam, lam_u, gs_u)  # @line L4
