# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-search/. The authors are listed in prov/GDCGR7.jsonl.

from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def linear_search(a: Sequence[T], x: T) -> int:
    """Return the smallest index i with a[i] == x, or -1 when x is not in a.

    The items need no order, only an equality test. The cost is at most
    len(a) equality tests and O(1) extra space.
    """
    for i in range(len(a)):  # @line L1
        if a[i] == x:  # @line L2
            return i
    return -1  # @line L3
