# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/insertion-sort/. The authors are listed in prov/3NS7RT.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def insertion_sort(a: list[T]) -> None:
    """Sort the list a in place, in non-decreasing order. The sort is stable."""
    for i in range(1, len(a)):  # @line L1
        key = a[i]  # @line L2
        j = i - 1  # @line L3
        while j >= 0 and key < a[j]:  # @line L4
            a[j + 1] = a[j]  # @line L5
            j -= 1  # @line L6
        a[j + 1] = key  # @line L7
