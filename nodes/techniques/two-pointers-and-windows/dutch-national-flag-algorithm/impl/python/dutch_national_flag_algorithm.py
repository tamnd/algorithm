# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dutch-national-flag-algorithm/. The authors are listed in prov/302WGD.jsonl.

from typing import Any


def three_way_partition(a: list[Any], pivot: Any) -> tuple[int, int]:
    """Rearrange a in place around pivot and return (lt, gt).

    On return a[:lt] < pivot, a[lt:gt] == pivot and a[gt:] > pivot.
    Cost: exactly len(a) iterations, at most len(a) swaps, O(1) extra space.
    """
    lo, mid, hi = 0, 0, len(a) - 1  # @line L1
    while mid <= hi:  # @line L2
        if a[mid] < pivot:  # @line L3
            a[lo], a[mid] = a[mid], a[lo]  # @line L4
            lo += 1
            mid += 1
        elif a[mid] > pivot:  # @line L5
            a[mid], a[hi] = a[hi], a[mid]  # @line L6
            hi -= 1
        else:  # @line L7
            mid += 1
    return lo, hi + 1  # @line L8


def sort_colors(a: list[int]) -> None:
    """Sort a list of values in {0, 1, 2} in place in one pass."""
    three_way_partition(a, 1)
