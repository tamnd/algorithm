# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/first-fit-bin-packing/. The authors are listed in prov/2VPCK0.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction]


def first_fit_bin_packing(sizes: Sequence[Number], capacity: Number = 1) -> list[list[int]]:
    """Pack the items in the given order with first fit.

    Return the bins as lists of 0-based item indices, in the order in which
    they were opened. A max tree over the free space of the bins finds the
    first bin with enough room in O(log n) steps. Bins that are not open yet
    have free space equal to the capacity, so the search always succeeds.
    Use int or Fraction data, so that the comparisons are exact.
    """
    n = len(sizes)
    size = 1
    while size < max(n, 1):
        size *= 2
    free = [capacity] * (2 * size)  # free[size + j] is the free space of bin j
    bins: list[list[int]] = []  # @line L1
    for i, x in enumerate(sizes):  # @line L2
        if not 0 < x <= capacity:
            raise ValueError(f"item {i} has size {x}, outside (0, capacity]")
        node = 1  # @line L3
        while node < size:
            node = 2 * node if free[2 * node] >= x else 2 * node + 1
        j = node - size
        if j == len(bins):  # @line L4
            bins.append([])
        bins[j].append(i)  # @line L5
        free[node] -= x
        node //= 2
        while node:
            free[node] = max(free[2 * node], free[2 * node + 1])
            node //= 2
    return bins  # @line L6
