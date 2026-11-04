# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gnome-sort/. The authors are listed in prov/6HS4Z7.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def gnome_sort(a: list[T]) -> int:
    """Sort a in place, in non-decreasing order, and return the number of steps.

    One index walks forward while its item is in order with the item to its
    left, and otherwise exchanges the two and steps back. The sort is stable.
    Cost: exactly n + 2d steps and d exchanges, d = inversions.
    """
    n = len(a)
    steps = 0
    i = 0  # @line L1
    while i < n:  # @line L2
        steps += 1
        if i == 0 or not a[i] < a[i - 1]:  # @line L3: i = 0 or a[i - 1] <= a[i]
            i += 1  # @line L4
        else:  # @line L5
            a[i - 1], a[i] = a[i], a[i - 1]  # @line L6
            i -= 1  # @line L7
    return steps
