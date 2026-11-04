# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pigeonhole-sort/. The authors are listed in prov/Y6SQW0.jsonl.

from collections import deque
from typing import Callable, TypeVar

T = TypeVar("T")


def pigeonhole_sort(a: list[T], key: Callable[[T], int] = lambda x: x) -> None:  # type: ignore[assignment,return-value]
    """Sort the list a in place by its integer keys. The sort is stable.

    The cost is Theta(n + k) time and Theta(n + k) extra space, where k is
    max(key) - min(key) + 1. The caller must make sure that k is small.
    """
    n = len(a)
    if n == 0:  # @line L1
        return
    keys = [key(x) for x in a]
    lo, hi = min(keys), max(keys)  # @line L2
    k = hi - lo + 1  # @line L3
    holes: list[deque[T]] = [deque() for _ in range(k)]  # @line L4
    for i in range(n):  # @line L5
        holes[keys[i] - lo].append(a[i])  # @line L6
    j = 0  # @line L7
    for h in range(k):  # @line L8
        for x in holes[h]:  # @line L9
            a[j] = x  # @line L10
            j += 1
