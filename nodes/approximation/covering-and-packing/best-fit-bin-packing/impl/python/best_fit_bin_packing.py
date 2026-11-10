# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/best-fit-bin-packing/. The authors are listed in prov/Z0DHY7.jsonl.

from bisect import bisect_left, insort
from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction]


def best_fit_bin_packing(sizes: Sequence[Number], capacity: Number = 1) -> list[list[int]]:
    """Pack the items in the given order with best fit.

    Each item goes into the open bin with the least free space that is still
    at least the item size; ties go to the bin opened first. Return the bins
    as lists of 0-based item indices, in the order in which they were opened.
    The open bins are kept as a sorted list of (free space, index) pairs. Use
    int or Fraction data, so that the comparisons are exact.
    """
    bins: list[list[int]] = []  # @line L1
    by_free: list[tuple[Number, int]] = []
    for i, x in enumerate(sizes):  # @line L2
        if not 0 < x <= capacity:
            raise ValueError(f"item {i} has size {x}, outside (0, capacity]")
        pos = bisect_left(by_free, (x, -1))  # @line L3
        if pos == len(by_free):  # @line L4
            j, free = len(bins), capacity
            bins.append([])
        else:
            free, j = by_free.pop(pos)
        bins[j].append(i)  # @line L5
        insort(by_free, (free - x, j))
    return bins  # @line L6
