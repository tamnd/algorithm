# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cycle-sort/. The authors are listed in prov/FAY1AX.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def _position(a: list[T], s: int, x: T) -> int:
    p = s  # @line L13
    for i in range(s + 1, len(a)):  # @line L14
        if a[i] < x:  # @line L15
            p += 1
    return p  # @line L16


def _equal(x: T, y: T) -> bool:
    return not x < y and not y < x


def cycle_sort(a: list[T]) -> int:
    """Sort a in place, in non-decreasing order, and return the number of writes.

    Each start position s takes its item x, counts the items to its right that
    are smaller to find the final place of x, and follows the cycle of the
    permutation from there until an item lands at s. Each array write puts an
    item at its final place, so the number of writes is the number of
    positions whose item must change, which is the least possible.
    Cost: Θ(n²) comparisons on every input, Θ(1) extra space.
    """
    n = len(a)
    writes = 0  # @line L1
    for s in range(n - 1):  # @line L2
        x = a[s]  # @line L3
        p = _position(a, s, x)  # @line L4
        if p == s:  # @line L5
            continue
        while True:  # @line L6
            while _equal(x, a[p]):  # @line L7
                p += 1
            a[p], x = x, a[p]  # @line L8
            writes += 1  # @line L9
            if p == s:  # @line L10
                break
            p = _position(a, s, x)  # @line L11
    return writes  # @line L12
