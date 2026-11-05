# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/circular-kadane-algorithm/. The authors are listed in prov/00F99T.jsonl.

from typing import Union

Number = Union[int, float]


def circular_kadane(a: list[Number]) -> Number:
    """Return the largest sum of a non-empty circular subarray of a.

    A circular subarray may wrap from the end of a to its start; no item is used twice.
    Precondition: a is not empty (raises ValueError otherwise).
    Cost: O(n) time, O(1) extra space.
    """
    if not a:
        raise ValueError("the array must not be empty")
    hi = best = lo = worst = total = a[0]  # @line L1
    for j in range(1, len(a)):  # @line L2
        hi = a[j] + max(hi, 0)  # @line L3
        best = max(best, hi)
        lo = a[j] + min(lo, 0)  # @line L4
        worst = min(worst, lo)
        total += a[j]  # @line L5
    if best < 0:  # @line L6
        return best
    return max(best, total - worst)  # @line L7


def circular_kadane_arc(a: list[Number]) -> tuple[Number, int, int]:
    """Return (best, start, length): a best circular arc a[start], a[start + 1 mod n], ...

    Same precondition and cost as circular_kadane. Ties prefer a plain arc.
    """
    if not a:
        raise ValueError("the array must not be empty")
    n = len(a)
    hi = best = lo = worst = total = a[0]
    hs = ls = 0
    bi, bj = 0, 0
    wi, wj = 0, 0
    for j in range(1, n):
        if hi < 0:
            hi, hs = a[j], j
        else:
            hi += a[j]
        if hi > best:
            best, bi, bj = hi, hs, j
        if lo > 0:
            lo, ls = a[j], j
        else:
            lo += a[j]
        if lo < worst:
            worst, wi, wj = lo, ls, j
        total += a[j]
    if best < 0 or best >= total - worst or (wi, wj) == (0, n - 1):
        return best, bi, bj - bi + 1
    return total - worst, (wj + 1) % n, n - (wj - wi + 1)
