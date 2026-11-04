# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/selection-sort/. The authors are listed in prov/6ADSAW.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def selection_sort(a: list[T]) -> None:
    """Sort a in place in non-decreasing order. Requires a total order; O(n²) time, O(1) extra space."""
    n = len(a)
    for i in range(0, n - 1):  # @line L1
        min_index = i  # @line L2
        for j in range(i + 1, n):  # @line L3
            if a[j] < a[min_index]:  # @line L4
                min_index = j  # @line L5
        a[i], a[min_index] = a[min_index], a[i]  # @line L6
