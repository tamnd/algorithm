# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gospers-hack/. The authors are listed in prov/EEBZ0F.jsonl.

from collections.abc import Iterator


def gospers_hack(x: int, w: int = 64) -> int:
    """Return the next larger w-bit word with the same number of 1-bits as x.

    Precondition: 0 < x < 2**w. The arithmetic wraps modulo 2**w, as on a
    machine. If x is the largest w-bit word with its number of ones, the
    result wraps and is smaller than x, so the caller must stop first.
    Cost: O(1) word operations.
    """
    if not 0 < x < (1 << w):
        raise ValueError("x must satisfy 0 < x < 2**w")
    mask = (1 << w) - 1
    smallest = x & (-x & mask)  # @line L1
    ripple = (x + smallest) & mask  # @line L2
    ones = x ^ ripple  # @line L3
    ones = (ones >> 2) // smallest  # @line L4
    return ripple | ones  # @line L5


def k_subsets(n: int, k: int) -> Iterator[int]:
    """Yield the masks of all k-subsets of {0, ..., n-1} in increasing order.

    Uses Python integers, so there is no word-size limit. Cost: O(1) word
    operations for each mask, C(n, k) masks in all.
    """
    if k < 0 or k > n:
        return
    if k == 0:
        yield 0
        return
    x = (1 << k) - 1
    while x < (1 << n):
        yield x
        x = gospers_hack(x, n + 1)
