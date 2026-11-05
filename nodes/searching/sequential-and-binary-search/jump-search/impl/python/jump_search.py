# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jump-search/. The authors are listed in prov/FX08EH.jsonl.

import math
from collections.abc import Sequence
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def jump_search(a: Sequence[T], x: T) -> int:
    """Return the smallest index i with a[i] == x, or -1 when x is not in a.

    The list a must be sorted in non-decreasing order. The search jumps in
    blocks of max(1, isqrt(n)) items, then scans one block, so it makes at most
    ceil(n / m) + m comparisons, about 2 * sqrt(n), and uses O(1) extra space.
    """
    n = len(a)
    m = max(1, math.isqrt(n))  # @line L1
    lo, hi = 0, min(m, n)  # @line L2
    while hi < n and a[hi - 1] < x:  # @line L3
        lo, hi = hi, min(hi + m, n)  # @line L4
    i = lo  # @line L5
    while i < hi and a[i] < x:  # @line L6
        i += 1  # @line L7
    if i < n and a[i] == x:  # @line L8
        return i
    return -1  # @line L9
