# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/next-fit-bin-packing/. The authors are listed in prov/G0STDP.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction]


def next_fit_bin_packing(sizes: Sequence[Number], capacity: Number = 1) -> list[list[int]]:
    """Pack the items in the given order with next fit.

    Return the bins as lists of 0-based item indices. Each size must be
    positive and at most the capacity. Use int or Fraction data, so that the
    test "load + size > capacity" is exact.
    """
    bins: list[list[int]] = []
    load: Number = 0  # @line L1
    for i, x in enumerate(sizes):  # @line L2
        if not 0 < x <= capacity:
            raise ValueError(f"item {i} has size {x}, outside (0, capacity]")
        if not bins or load + x > capacity:  # @line L3
            bins.append([])  # @line L4
            load = 0
        bins[-1].append(i)  # @line L5
        load += x
    return bins  # @line L6
