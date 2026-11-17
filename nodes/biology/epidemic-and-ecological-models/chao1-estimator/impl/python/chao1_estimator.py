# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chao1-estimator/. The authors are listed in prov/A0Z4WE.jsonl.
"""The Chao1 lower estimate of species richness.

Input: the species labels of the n individuals of one sample. The estimate
uses the number of observed species S_obs, the singletons f1 and the
doubletons f2. All estimates are exact fractions.Fraction values.

Cost: Theta(n) expected time with the hash map of line L1, and Theta(s)
extra space for s observed species.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import comb
from typing import Dict, Hashable, Iterable, Optional, Sequence


@dataclass(frozen=True)
class Chao1Result:
    """The frequency counts and the estimates of one sample."""

    n: int
    s_obs: int
    f1: int
    f2: int
    classic: Optional[Fraction]
    bias_corrected: Fraction
    variance: Optional[Fraction]


def frequency_counts(counts: Iterable[int]) -> Dict[int, int]:
    """Map k -> f_k, the number of species with k individuals (k >= 1)."""
    out: Dict[int, int] = {}
    for k in counts:
        if k < 1:
            raise ValueError("species counts must be >= 1")
        out[k] = out.get(k, 0) + 1
    return out


def chao1_classic(s_obs: int, f1: int, f2: int, n: Optional[int] = None) -> Optional[Fraction]:
    """S_obs + f1^2 / (2 f2), or None when f2 = 0. With n, the factor
    (n - 1) / n of multinomial sampling is applied to the correction."""
    if f2 == 0:
        return None
    extra = Fraction(f1 * f1, 2 * f2)
    if n is not None:
        extra *= Fraction(n - 1, n)
    return s_obs + extra


def chao1_bias_corrected(s_obs: int, f1: int, f2: int, n: Optional[int] = None) -> Fraction:
    """S_obs + f1 (f1 - 1) / (2 (f2 + 1)), with the optional factor (n - 1) / n."""
    extra = Fraction(f1 * (f1 - 1), 2 * (f2 + 1))
    if n is not None:
        extra *= Fraction(n - 1, n)
    return s_obs + extra


def chao1_variance(f1: int, f2: int) -> Optional[Fraction]:
    """Chao's (1987) variance estimate f2 (q^4 / 4 + q^3 + q^2 / 2) with
    q = f1 / f2, or None when f2 = 0."""
    if f2 == 0:
        return None
    q = Fraction(f1, f2)
    return f2 * (q ** 4 / 4 + q ** 3 + q ** 2 / 2)


def chao1(sample: Sequence[Hashable]) -> Chao1Result:
    """Compute the Chao1 estimates from the species labels of a sample."""
    count: Dict[Hashable, int] = {}
    for x in sample:
        count[x] = count.get(x, 0) + 1  # @line L1
    n = len(sample)  # @line L2
    s_obs = len(count)
    freq = frequency_counts(count.values())
    f1 = freq.get(1, 0)  # @line L3
    f2 = freq.get(2, 0)
    s_bc = chao1_bias_corrected(s_obs, f1, f2)  # @line L4
    if f2 == 0:  # @line L5
        s_classic = None
        v = None
    else:
        s_classic = chao1_classic(s_obs, f1, f2)  # @line L6
        v = chao1_variance(f1, f2)
    return Chao1Result(n, s_obs, f1, f2, s_classic, s_bc, v)  # @line L7


def expected_frequency(p: Sequence[Fraction], n: int, k: int) -> Fraction:
    """E[f_k] = sum over species of C(n, k) p^k (1 - p)^(n - k) for
    multinomial sampling of n individuals with abundances p."""
    return sum((comb(n, k) * q ** k * (1 - q) ** (n - k) for q in p), Fraction(0))
