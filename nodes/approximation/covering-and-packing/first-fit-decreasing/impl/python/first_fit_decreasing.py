# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/first-fit-decreasing/. The authors are listed in prov/Q1QQRH.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction]


def first_fit_decreasing(sizes: Sequence[Number], capacity: Number = 1) -> list[list[int]]:
    """Sort the items by decreasing size, then pack them with first fit.

    Return the bins as lists of 0-based indices into the input list. Items of
    equal size keep their input order. A max tree over the free space of the
    bins finds the first bin with room in O(log n) steps. Use int or Fraction
    data, so that the comparisons are exact.
    """
    n = len(sizes)
    for i, x in enumerate(sizes):
        if not 0 < x <= capacity:
            raise ValueError(f"item {i} has size {x}, outside (0, capacity]")
    order = sorted(range(n), key=lambda i: -sizes[i])  # @line L1
    size = 1
    while size < max(n, 1):
        size *= 2
    free = [capacity] * (2 * size)
    bins: list[list[int]] = []  # @line L2
    for i in order:  # @line L3
        x = sizes[i]
        node = 1  # @line L4
        while node < size:
            node = 2 * node if free[2 * node] >= x else 2 * node + 1
        j = node - size
        if j == len(bins):  # @line L5
            bins.append([])
        bins[j].append(i)  # @line L6
        free[node] -= x
        node //= 2
        while node:
            free[node] = max(free[2 * node], free[2 * node + 1])
            node //= 2
    return bins  # @line L7
