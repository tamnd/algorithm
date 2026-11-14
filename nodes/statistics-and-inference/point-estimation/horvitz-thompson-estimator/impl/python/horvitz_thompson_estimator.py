# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/horvitz-thompson-estimator/. The authors are listed in prov/D95ZRB.jsonl.

"""The Horvitz-Thompson estimate of a population total and its variance estimates.

A sample is a sequence of distinct unit labels. y and pi map a label to its
value and its inclusion probability (a dict or a list). pij(i, j) returns the
probability that units i and j (i != j) are both in the sample. With Fraction
or int inputs the results are exact.
"""

import math
from collections.abc import Callable, Mapping, Sequence

from stdist import norm_ppf


def _check(sample: Sequence, pi) -> None:
    if len(set(sample)) != len(sample):
        raise ValueError("the sample must list distinct units")
    for i in sample:
        if pi[i] <= 0:
            raise ValueError(f"unit {i!r} has inclusion probability {pi[i]!r} <= 0")


def ht_total(sample: Sequence, y: Mapping | Sequence, pi: Mapping | Sequence):
    """Return sum over the sample of y[i] / pi[i]. Cost: 2 n operations."""
    _check(sample, pi)
    total = 0  # @line L1
    for i in sample:  # @line L2
        total = total + y[i] / pi[i]  # @line L3
    return total  # @line L4


def ht_variance(sample: Sequence, y, pi, pij: Callable) -> float:
    """The Horvitz-Thompson variance estimate; needs pij(i, j) > 0. Cost: Theta(n^2).

    The value can be negative.
    """
    _check(sample, pi)
    v = 0  # @line L5
    for i in sample:  # @line L6
        ci = y[i] / pi[i]
        v = v + (1 - pi[i]) * ci * ci  # @line L7
        for j in sample:  # @line L8
            if j == i:
                continue
            q = pij(i, j)
            if q <= 0:
                raise ValueError(f"pair {i!r}, {j!r} has joint probability {q!r} <= 0")
            v = v + (1 - pi[i] * pi[j] / q) * ci * (y[j] / pi[j])  # @line L9
    return v  # @line L10


def syg_variance(sample: Sequence, y, pi, pij: Callable) -> float:
    """The Sen-Yates-Grundy variance estimate, for fixed-size designs only. Cost: Theta(n^2)."""
    _check(sample, pi)
    v = 0  # @line L11
    for a in range(len(sample)):  # @line L12
        i = sample[a]
        for b in range(a + 1, len(sample)):
            j = sample[b]
            q = pij(i, j)
            if q <= 0:
                raise ValueError(f"pair {i!r}, {j!r} has joint probability {q!r} <= 0")
            d = y[i] / pi[i] - y[j] / pi[j]
            v = v + (pi[i] * pi[j] / q - 1) * d * d  # @line L13
    return v  # @line L14


def hajek_mean(sample: Sequence, y, pi):
    """The Hajek ratio: sum y[i]/pi[i] divided by sum 1/pi[i]. Biased, but shift equivariant."""
    _check(sample, pi)
    if not sample:
        raise ValueError("the Hajek ratio needs a nonempty sample")
    num = sum((y[i] / pi[i] for i in sample), 0)
    den = sum((1 / pi[i] for i in sample), 0)
    return num / den


def ht_interval(estimate: float, variance: float, level: float = 0.95) -> tuple[float, float]:
    """The approximate normal interval estimate +- z * sqrt(variance).

    Raises ValueError for a negative variance estimate. The coverage is
    approximate and depends on the design and the sample size.
    """
    if variance < 0:
        raise ValueError("negative variance estimate")
    half = norm_ppf(0.5 + level / 2) * math.sqrt(variance)
    return float(estimate) - half, float(estimate) + half
