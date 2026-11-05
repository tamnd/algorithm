# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kadane-max-product/. The authors are listed in prov/8EPB4B.jsonl.

from typing import Union

Number = Union[int, float]


def max_product(a: list[Number]) -> Number:
    """Return the largest product of a non-empty subarray of a.

    Precondition: a is not empty (raises ValueError otherwise).
    Cost: O(n) arithmetic operations, O(1) extra space. Python integers are exact,
    so with integer items the numbers can grow to about n times the item size.
    """
    if not a:
        raise ValueError("the array must not be empty")
    hi = lo = best = a[0]  # @line L1
    for j in range(1, len(a)):  # @line L2
        x = a[j]
        if x < 0:  # @line L3
            hi, lo = lo, hi
        hi = max(x, hi * x)  # @line L4
        lo = min(x, lo * x)  # @line L5
        best = max(best, hi)  # @line L6
    return best  # @line L7


def max_product_subarray(a: list[Number]) -> tuple[Number, int, int]:
    """Return (best, i, j), 0-based and inclusive, with the product of a[i:j + 1] equal to best.

    Same precondition and cost as max_product.
    """
    if not a:
        raise ValueError("the array must not be empty")
    hi = lo = best = a[0]
    hs = ls = 0
    bi = bj = 0
    for j in range(1, len(a)):
        x = a[j]
        if x < 0:
            hi, lo = lo, hi
            hs, ls = ls, hs
        if hi * x > x:
            hi = hi * x
        else:
            hi, hs = x, j
        if lo * x < x:
            lo = lo * x
        else:
            lo, ls = x, j
        if hi > best:
            best, bi, bj = hi, hs, j
    return best, bi, bj
