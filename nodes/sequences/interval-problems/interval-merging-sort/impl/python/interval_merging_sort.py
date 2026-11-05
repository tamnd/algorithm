# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-merging-sort/. The authors are listed in prov/ZVJBCZ.jsonl.

from typing import TypeVar

T = TypeVar("T", int, float)


def interval_merging_sort(
    intervals: list[tuple[T, T]], merge_touching: bool = True
) -> list[tuple[T, T]]:
    """Return the connected components of the union of the intervals, sorted.

    Each interval is a pair (l, r). With merge_touching=True (closed [l, r] with
    l <= r, or half-open [l, r) with l < r), two intervals that share an end
    point are merged. With merge_touching=False (open (l, r) with l < r), they
    are not. The input list is not changed. Time O(n log n), extra space O(n).
    """
    order = sorted(intervals)  # @line L1
    out: list[list[T]] = []  # @line L2
    for lo, hi in order:  # @line L3
        if not out or lo > out[-1][1] or (not merge_touching and lo == out[-1][1]):  # @line L4
            out.append([lo, hi])  # @line L5
        else:
            out[-1][1] = max(out[-1][1], hi)  # @line L6
    return [(a, b) for a, b in out]  # @line L7
