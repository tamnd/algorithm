# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bubble-sort/. The authors are listed in prov/JS56R4.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def bubble_sort(a: list[T]) -> int:
    """Sort a in place, in non-decreasing order, and return the number of passes.

    Each pass exchanges adjacent items that are out of order. The next pass
    stops at the place of the last exchange. The sort is stable.
    Cost: Theta(n + d) exchanges and O(n^2) comparisons, d = inversions.
    """
    passes = 0
    bound = len(a) - 1  # @line L1
    while bound > 0:  # @line L2
        passes += 1
        last = 0  # @line L3
        for j in range(bound):  # @line L4
            if a[j + 1] < a[j]:  # @line L5: a[j] > a[j + 1]
                a[j], a[j + 1] = a[j + 1], a[j]  # @line L6
                last = j  # @line L7
        bound = last  # @line L8
    return passes
