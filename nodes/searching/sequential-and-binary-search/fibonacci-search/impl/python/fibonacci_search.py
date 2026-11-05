# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fibonacci-search/. The authors are listed in prov/8R17S9.jsonl.

from collections.abc import Sequence
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def fibonacci_search(a: Sequence[T], x: T) -> int:
    """Return the smallest index i with a[i] == x, or -1 when x is not in a.

    The list a must be sorted in non-decreasing order. The range of f - 1
    positions, with f a Fibonacci number, is cut after its first g - 1
    positions, where g is the Fibonacci number before f. Index arithmetic uses
    only addition and subtraction.
    """
    n = len(a)
    g, f = 0, 1  # @line L1
    while f - 1 < n:  # @line L2
        g, f = f, f + g
    lo = 0  # @line L3
    while f > 1:  # @line L4
        mid = lo + g - 1  # @line L5
        if mid < n and a[mid] < x:  # @line L6
            lo = mid + 1  # @line L7
            f, g = f - g, 2 * g - f
        else:  # @line L8
            f, g = g, f - g
    if lo < n and a[lo] == x:  # @line L9
        return lo
    return -1  # @line L10
