# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radix-select/. The authors are listed in prov/ZPSQHH.jsonl.

from typing import Optional, Sequence


def radix_select(a: Sequence[int], k: int, r: int = 8, w: Optional[int] = None) -> int:
    """Return the item of rank k (1-based) of a list of nonnegative integers.

    Looks at the keys r bits at a time, from the most significant digit of a
    w-bit key down, and keeps only the bucket that holds rank k. If w is not
    given, it is the bit length of the largest key. Uses no comparisons
    between keys.
    """
    n = len(a)
    if not 1 <= k <= n:
        raise ValueError("k must be between 1 and len(a)")
    if r < 1:
        raise ValueError("r must be at least 1")
    if any(x < 0 for x in a):
        raise ValueError("keys must be nonnegative")
    if w is None:
        w = max(max(a).bit_length(), 1)
    mask = (1 << r) - 1
    s = list(a)  # @line L1
    d = -(-w // r)  # @line L1
    for j in range(d - 1, -1, -1):  # @line L2
        if len(s) == 1:  # @line L3
            return s[0]  # @line L3
        shift = r * j
        count = [0] * (mask + 1)  # @line L4
        for x in s:  # @line L5
            count[(x >> shift) & mask] += 1  # @line L5
        b = 0  # @line L6
        while k > count[b]:  # @line L7
            k -= count[b]  # @line L7
            b += 1  # @line L7
        s = [x for x in s if (x >> shift) & mask == b]  # @line L8
    return s[0]  # @line L9
