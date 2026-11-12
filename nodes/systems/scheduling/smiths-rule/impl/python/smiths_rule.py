# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smiths-rule/. The authors are listed in prov/51P9W7.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction]


def ratio_key(p: Number, w: Number) -> tuple:
    """The sort key of one job: p / w as an exact fraction.

    A job with weight 0 has an infinite ratio, so it goes after every job of
    positive weight. Its place among the other weight 0 jobs does not change the
    cost.
    """
    if w < 0 or p < 0:
        raise ValueError("processing times and weights must be nonnegative")
    if w == 0:
        return (1, Fraction(0))
    return (0, Fraction(p) / Fraction(w))


def smiths_rule(p: Sequence[Number], w: Sequence[Number]) -> list[int]:
    """Smith's rule (WSPT) for 1||sum w_j C_j.

    Return the job indices in order of nondecreasing p[j] / w[j], ties by index.
    The sort is stable, so equal ratios keep their input order.
    Cost: O(n log n) time for the sort and O(n) space.
    """
    if len(p) != len(w):
        raise ValueError("p and w must have the same length")
    return sorted(range(len(p)), key=lambda j: ratio_key(p[j], w[j]))  # @line L1


def weighted_completion_time(
    p: Sequence[Number], w: Sequence[Number], order: Sequence[int]
) -> Number:
    """The cost sum of w[j] * C[j] when the jobs run back to back from time 0."""
    t: Number = 0  # @line L2
    total: Number = 0
    for j in order:  # @line L3
        t += p[j]  # @line L4
        total += w[j] * t  # @line L5
    return total  # @line L6
