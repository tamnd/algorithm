# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heap-construction-by-insertion/. The authors are listed in prov/0PQJ7X.jsonl.

from typing import Any, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def sift_up(a: list[T], j: int) -> None:
    """Move a[j] up in the max-heap a[0:j+1]; a[0:j] must be a max-heap."""
    i = j  # @line L2
    while i > 0 and a[(i - 1) // 2] < a[i]:  # @line L3
        p = (i - 1) // 2
        a[i], a[p] = a[p], a[i]  # @line L4
        i = p  # @line L5


def heap_construction_by_insertion(a: list[T]) -> None:
    """Rearrange a in place into a max-heap by inserting a[1], a[2], ... in turn.

    O(n log n) time in the worst case, O(n) expected time on a random order,
    O(1) extra space. After step j, a[0:j+1] is a max-heap.
    """
    for j in range(1, len(a)):  # @line L1
        sift_up(a, j)
