# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hyperquicksort/. The authors are listed in prov/J95TFF.jsonl.

"""Hyperquicksort on a simulated hypercube of p = 2^d processors.

The processors of one round are handled one pair at a time. Each pair
touches only its own two lists, so this gives the same result as running
all pairs at the same time.
"""

import heapq
from bisect import bisect_right
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def hyperquicksort(lists: list[list[T]]) -> list[list[T]]:
    """Sort the keys held by p = 2^d processors. Processor q ends with a
    sorted list, and every key on q is at most every key on q + 1."""
    p = len(lists)
    if p == 0 or p & (p - 1):
        raise ValueError("the number of processors must be a power of 2")
    d = p.bit_length() - 1
    lists = [sorted(x) for x in lists]  # @line L1
    for i in range(d - 1, -1, -1):  # @line L2: one round per dimension
        bit = 1 << i
        for root in range(0, p, 2 * bit):  # each subcube of dimension i + 1
            members = range(root, root + 2 * bit)
            own = lists[root]  # @line L3: the root's list gives the pivot
            if own:
                pivot = own[(len(own) - 1) // 2]
            else:
                pivot = next((lists[q][(len(lists[q]) - 1) // 2] for q in members if lists[q]), None)
            if pivot is None:
                continue
            for low in members:  # @line L4: pairs across dimension i
                if low & bit:
                    continue
                high = low | bit
                a, b = lists[low], lists[high]
                ca, cb = bisect_right(a, pivot), bisect_right(b, pivot)  # @line L5
                lists[low] = list(heapq.merge(a[:ca], b[:cb]))  # @line L6
                lists[high] = list(heapq.merge(a[ca:], b[cb:]))  # @line L7
    return lists


def flatten(lists: list[list[T]]) -> list[T]:
    return [x for lst in lists for x in lst]
