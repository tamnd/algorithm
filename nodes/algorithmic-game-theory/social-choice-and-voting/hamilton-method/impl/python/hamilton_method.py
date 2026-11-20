# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hamilton-method/. The authors are listed in prov/S01MQ4.jsonl.

from fractions import Fraction
from typing import Sequence


def quotas(populations: Sequence[int], h: int) -> list[Fraction]:
    """Return the exact quotas h p_i / P."""
    total = sum(populations)
    return [Fraction(h * p, total) for p in populations]


def hamilton_method(populations: Sequence[int], h: int) -> list[int]:
    """Apportion h seats by Hamilton's method (largest remainders).

    populations are nonnegative integers with a positive sum. Each state gets the integer
    part of its quota h p_i / P, and the s seats that are left go to the s states with the
    largest remainders, the smallest index among ties. All arithmetic is on integers: the
    remainder of state i is h p_i mod P, which is P times the fractional part of its quota.
    """
    if h < 0 or any(p < 0 for p in populations) or sum(populations) <= 0:
        raise ValueError("need h >= 0, populations >= 0 and a positive total")
    n = len(populations)
    total = sum(populations)  # @line L1
    a = [h * p // total for p in populations]  # @line L2
    r = [h * p % total for p in populations]
    s = h - sum(a)  # @line L3
    order = sorted(range(n), key=lambda i: (-r[i], i))  # @line L4
    for i in order[:s]:  # @line L5
        a[i] += 1  # @line L6
    return a  # @line L7
