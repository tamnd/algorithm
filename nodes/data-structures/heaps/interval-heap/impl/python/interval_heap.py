# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-heap/. The authors are listed in prov/XN8WFN.jsonl.

from collections.abc import Iterable
from typing import Any, Generic, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


T = TypeVar("T", bound=Ordered)


class IntervalHeap(Generic[T]):
    """A double-ended priority queue in one 0-based list.

    The node j holds the keys a[2j] (low) and a[2j + 1] (high); the last
    node may hold only a low key. The parent of the node j is (j - 1) // 2.
    Each node has low <= high, and the keys of a node lie in the interval of
    its parent. insert, extract_min and extract_max take O(log n) time;
    find_min and find_max take O(1) time. Keys need only "<".
    """

    def __init__(self, keys: Iterable[T] = ()) -> None:
        self.a: list[T] = []
        for k in keys:
            self.insert(k)

    def __len__(self) -> int:
        return len(self.a)

    def _hi(self, j: int) -> int:
        return 2 * j + 1 if 2 * j + 1 < len(self.a) else 2 * j

    def _sift_up_min(self, j: int) -> None:
        a = self.a
        while j > 0 and a[2 * j] < a[2 * ((j - 1) // 2)]:  # @line L4
            p = (j - 1) // 2
            a[2 * j], a[2 * p] = a[2 * p], a[2 * j]  # @line L5
            j = p

    def _sift_up_max(self, j: int) -> None:
        a = self.a
        while j > 0 and a[2 * ((j - 1) // 2) + 1] < a[self._hi(j)]:  # @line L6
            p = (j - 1) // 2
            h = self._hi(j)
            a[h], a[2 * p + 1] = a[2 * p + 1], a[h]  # @line L7
            j = p

    def insert(self, x: T) -> None:
        a = self.a
        a.append(x)  # @line L1
        k = len(a) - 1
        j = k // 2
        if k % 2 == 1 and a[k] < a[k - 1]:  # @line L2
            a[k], a[k - 1] = a[k - 1], a[k]
        self._sift_up_min(j)  # @line L3
        self._sift_up_max(j)

    def find_min(self) -> T:
        if not self.a:
            raise IndexError("find_min from an empty heap")
        return self.a[0]

    def find_max(self) -> T:
        if not self.a:
            raise IndexError("find_max from an empty heap")
        return self.a[1] if len(self.a) > 1 else self.a[0]

    def _children(self, j: int) -> list[int]:
        return [c for c in (2 * j + 1, 2 * j + 2) if 2 * c < len(self.a)]

    def extract_min(self) -> T:
        a = self.a
        if not a:  # @line L8
            raise IndexError("extract_min from an empty heap")
        r = a[0]  # @line L9
        x = a.pop()
        if not a:
            return r
        a[0] = x  # @line L10
        j = 0
        while True:
            cs = self._children(j)  # @line L11
            if not cs:
                return r
            c = cs[0]
            if len(cs) == 2 and a[2 * cs[1]] < a[2 * cs[0]]:
                c = cs[1]
            if not a[2 * c] < a[2 * j]:  # @line L12
                return r
            a[2 * j], a[2 * c] = a[2 * c], a[2 * j]  # @line L13
            h = self._hi(c)
            if a[h] < a[2 * c]:
                a[h], a[2 * c] = a[2 * c], a[h]
            j = c  # @line L14

    def extract_max(self) -> T:
        a = self.a
        if not a:  # @line L15
            raise IndexError("extract_max from an empty heap")
        if len(a) <= 2:  # @line L16
            return a.pop()
        r = a[1]  # @line L17
        a[1] = a.pop()
        j = 0
        while True:
            cs = self._children(j)  # @line L18
            if not cs:
                return r
            c = cs[0]
            if len(cs) == 2 and a[self._hi(cs[0])] < a[self._hi(cs[1])]:
                c = cs[1]
            if not a[2 * j + 1] < a[self._hi(c)]:  # @line L19
                return r
            h = self._hi(c)
            a[2 * j + 1], a[h] = a[h], a[2 * j + 1]  # @line L20
            if a[h] < a[2 * c]:
                a[h], a[2 * c] = a[2 * c], a[h]
            j = c  # @line L21

    def nodes(self) -> list[tuple[T, ...]]:
        return [tuple(self.a[2 * j : 2 * j + 2]) for j in range((len(self.a) + 1) // 2)]

    def check_invariant(self) -> None:
        a = self.a
        for j in range((len(a) + 1) // 2):
            lo, hi = a[2 * j], a[self._hi(j)]
            assert not hi < lo
            if j > 0:
                p = (j - 1) // 2
                assert not lo < a[2 * p]
                assert not a[2 * p + 1] < hi
