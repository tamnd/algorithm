# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heaps-algorithm/. The authors are listed in prov/AEJSBV.jsonl.

from collections.abc import Callable, Iterator
from typing import TypeVar

T = TypeVar("T")


def heaps_algorithm(a: list[T], visit: Callable[[list[T]], None]) -> None:
    """Call visit(a) once for each arrangement of a, by the recursive form.

    Consecutive visits differ by one exchange of two positions. The array
    is changed in place; visit must copy it if it keeps it. The recursion
    depth is len(a).
    """

    def heap(k: int) -> None:
        if k <= 1:  # @line L1
            visit(a)  # @line L2
            return  # @line L3
        heap(k - 1)  # @line L4
        for i in range(k - 1):  # @line L5
            if k % 2 == 0:
                a[i], a[k - 1] = a[k - 1], a[i]  # @line L6
            else:
                a[0], a[k - 1] = a[k - 1], a[0]  # @line L7
            heap(k - 1)  # @line L8

    heap(len(a))


def heap_permutations(items: list[T]) -> Iterator[list[T]]:
    """Yield a copy of each arrangement of items in Heap's order, without recursion."""
    a = list(items)
    n = len(a)
    c = [0] * n  # @line I1
    yield list(a)  # @line I2
    k = 1  # @line I3
    while k < n:  # @line I4
        if c[k] < k:  # @line I5
            if k % 2 == 1:
                a[c[k]], a[k] = a[k], a[c[k]]  # @line I6
            else:
                a[0], a[k] = a[k], a[0]  # @line I7
            yield list(a)  # @line I8
            c[k] += 1  # @line I9
            k = 1
        else:
            c[k] = 0  # @line I11
            k += 1
