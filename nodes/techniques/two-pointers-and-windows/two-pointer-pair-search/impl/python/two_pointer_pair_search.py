# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-pointer-pair-search/. The authors are listed in prov/XYYCS4.jsonl.

from typing import Optional


def two_pointer_pair_search(a: list[int], t: int) -> Optional[tuple[int, int]]:
    """Return (i, j) with i < j and a[i] + a[j] == t, or None if no such pair exists.

    Precondition: a is sorted in non-decreasing order.
    Cost: at most len(a) - 1 iterations, O(n) time and O(1) extra space.
    """
    lo, hi = 0, len(a) - 1  # @line L1
    while lo < hi:  # @line L2
        s = a[lo] + a[hi]  # @line L3
        if s == t:  # @line L4
            return (lo, hi)
        if s < t:  # @line L5
            lo += 1
        else:  # @line L6
            hi -= 1
    return None  # @line L7


def count_pairs_with_sum(a: list[int], t: int) -> int:
    """Return the number of index pairs i < j with a[i] + a[j] == t.

    Precondition: a is sorted in non-decreasing order. Cost: O(n) time.
    """
    lo, hi = 0, len(a) - 1
    count = 0
    while lo < hi:
        s = a[lo] + a[hi]
        if s < t:
            lo += 1
        elif s > t:
            hi -= 1
        elif a[lo] == a[hi]:
            m = hi - lo + 1
            count += m * (m - 1) // 2
            break
        else:
            x, y = a[lo], a[hi]
            left = 0
            while a[lo] == x:
                lo += 1
                left += 1
            right = 0
            while a[hi] == y:
                hi -= 1
                right += 1
            count += left * right
    return count
