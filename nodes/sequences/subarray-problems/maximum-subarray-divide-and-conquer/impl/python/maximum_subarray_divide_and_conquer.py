# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-subarray-divide-and-conquer/. The authors are listed in prov/NXBA0T.jsonl.

from typing import Union

Number = Union[int, float]


def _maxsub(a: list[Number], lo: int, hi: int) -> tuple[Number, int, int]:
    if lo == hi:  # @line L1
        return a[lo], lo, lo
    mid = (lo + hi) // 2  # @line L2
    s_left, i_left, j_left = _maxsub(a, lo, mid)  # @line L3
    s_right, i_right, j_right = _maxsub(a, mid + 1, hi)
    t: Number = 0  # @line L4
    left_sum: Number = a[mid]
    ci = mid
    for i in range(mid, lo - 1, -1):
        t += a[i]
        if t > left_sum or i == mid:
            left_sum = t
            ci = i
    t = 0  # @line L5
    right_sum: Number = a[mid + 1]
    cj = mid + 1
    for j in range(mid + 1, hi + 1):
        t += a[j]
        if t > right_sum or j == mid + 1:
            right_sum = t
            cj = j
    s_cross = left_sum + right_sum  # @line L6
    if s_left >= s_right and s_left >= s_cross:  # @line L7
        return s_left, i_left, j_left
    if s_right >= s_cross:  # @line L8
        return s_right, i_right, j_right
    return s_cross, ci, cj  # @line L9


def max_subarray_dc(a: list[Number]) -> tuple[Number, int, int]:
    """Return (best, i, j) with sum(a[i:j + 1]) == best, the largest sum of a non-empty subarray.

    Indices are 0-based and inclusive. Ties prefer the left half, then the right
    half, then the crossing subarray.
    Precondition: a is not empty (raises ValueError otherwise).
    Cost: Theta(n log n) time, Theta(log n) extra space for the recursion.
    """
    if not a:
        raise ValueError("the array must not be empty")
    return _maxsub(a, 0, len(a) - 1)


def max_subarray_linear_dc(a: list[Number]) -> Number:
    """Return the largest non-empty subarray sum with the four-value combine.

    Each part returns (total, best prefix, best suffix, best). Cost: Theta(n)
    time, Theta(log n) extra space. Precondition: a is not empty.
    """
    if not a:
        raise ValueError("the array must not be empty")

    def solve(lo: int, hi: int) -> tuple[Number, Number, Number, Number]:
        if lo == hi:
            x = a[lo]
            return x, x, x, x
        mid = (lo + hi) // 2
        lt, lp, ls, lb = solve(lo, mid)
        rt, rp, rs, rb = solve(mid + 1, hi)
        return lt + rt, max(lp, lt + rp), max(rs, rt + ls), max(lb, rb, ls + rp)

    return solve(0, len(a) - 1)[3]
