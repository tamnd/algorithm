# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smith-rule/. The authors are listed in prov/5N4EPA.jsonl.

from fractions import Fraction
from functools import cmp_to_key
from typing import Sequence, Union

Number = Union[int, float, Fraction]


def smith_rule(jobs: Sequence[tuple[Number, Number]]) -> tuple[list[int], Number]:
    """Order jobs on one machine to minimize the sum of weight times completion time.

    Each job is a pair (p, w) with processing time p > 0 and a real weight w.
    The jobs are sorted by nonincreasing ratio w / p, compared through the cross
    products w_a * p_b and w_b * p_a, with ties kept in input order. The result
    is the order (0-based job indices) and its cost sum(w_j * C_j).

    Cost: O(n log n) comparisons for the sort and O(n) for the cost.
    """
    if any(p <= 0 for p, _ in jobs):
        raise ValueError("every processing time must be positive")

    def before(a: int, b: int) -> int:
        (pa, wa), (pb, wb) = jobs[a], jobs[b]
        left, right = wa * pb, wb * pa
        return -1 if left > right else (1 if left < right else 0)

    order = sorted(range(len(jobs)), key=cmp_to_key(before))  # @line L1
    t: Number = 0  # @line L2
    total: Number = 0
    for j in order:  # @line L3
        p, w = jobs[j]
        t = t + p  # @line L4
        total = total + w * t  # @line L5
    return order, total  # @line L6
