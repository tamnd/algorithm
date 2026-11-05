# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kadane-algorithm/. The authors are listed in prov/W9Q826.jsonl.

from typing import Union

Number = Union[int, float]


def kadane(a: list[Number]) -> tuple[Number, int, int]:
    """Return (best, i, j) with sum(a[i:j + 1]) == best, the largest sum of a non-empty subarray.

    Indices are 0-based and inclusive. Among the best subarrays, the one with the
    earliest end is returned, and for that end the earliest start.
    Precondition: a is not empty (raises ValueError otherwise).
    Cost: O(n) time, O(1) extra space.
    """
    if not a:
        raise ValueError("the array must not be empty")
    cur = a[0]  # @line L1
    c = 0
    best = a[0]
    bi, bj = 0, 0
    for j in range(1, len(a)):  # @line L2
        if cur < 0:  # @line L3
            cur = a[j]
            c = j
        else:  # @line L4
            cur = cur + a[j]
        if cur > best:  # @line L5
            best = cur
            bi, bj = c, j
    return best, bi, bj  # @line L6


def kadane_allow_empty(a: list[Number]) -> Number:
    """Return the largest subarray sum when the empty subarray (sum 0) is allowed.

    Cost: O(n) time, O(1) extra space. Returns 0 for an empty array.
    """
    cur: Number = 0
    best: Number = 0
    for x in a:
        cur = max(cur, 0) + x
        best = max(best, cur)
    return best
