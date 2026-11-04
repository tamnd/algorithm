# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-heap/. The authors are listed in prov/1QKQ6A.jsonl.

from collections.abc import Iterable
from typing import Any, Generic, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


T = TypeVar("T", bound=Ordered)


class BinaryHeap(Generic[T]):
    """A binary min-heap of keys in a 0-based Python list.

    The parent of index i is (i - 1) // 2 and its children are 2i + 1 and
    2i + 2. insert, extract_min and decrease_key take O(log n) time (insert
    is amortized, because the list grows), find_min takes O(1) time and
    build takes O(n) time. Keys need only "<".
    """

    def __init__(self) -> None:
        self.a: list[T] = []

    def __len__(self) -> int:
        return len(self.a)

    def _sift_up(self, i: int) -> None:
        a = self.a
        while i > 0 and a[i] < a[(i - 1) // 2]:  # @line L1
            p = (i - 1) // 2
            a[i], a[p] = a[p], a[i]  # @line L2
            i = p  # @line L3

    def _sift_down(self, n: int, i: int) -> None:
        a = self.a
        while True:  # @line L4
            m = i  # @line L5
            left, right = 2 * i + 1, 2 * i + 2
            if left < n and a[left] < a[m]:  # @line L6
                m = left
            if right < n and a[right] < a[m]:  # @line L7
                m = right
            if m == i:  # @line L8
                return
            a[i], a[m] = a[m], a[i]  # @line L9
            i = m  # @line L10

    def insert(self, k: T) -> None:
        """Add the key k. O(log n) amortized time."""
        self.a.append(k)  # @line L11 @line L12
        self._sift_up(len(self.a) - 1)  # @line L13

    def find_min(self) -> T:
        """Return a minimum key. Raise IndexError on an empty heap."""
        if not self.a:  # @line L14
            raise IndexError("heap underflow")
        return self.a[0]  # @line L15

    def extract_min(self) -> T:
        """Remove and return a minimum key. Raise IndexError on an empty heap."""
        a = self.a
        if not a:  # @line L16
            raise IndexError("heap underflow")
        smallest = a[0]  # @line L17
        last = a.pop()  # @line L19
        if a:
            a[0] = last  # @line L18
            self._sift_down(len(a), 0)  # @line L20
        return smallest  # @line L21

    def decrease_key(self, i: int, k: T) -> None:
        """Lower the key at the 0-based index i to k. Raise ValueError if k is larger."""
        if not 0 <= i < len(self.a):
            raise IndexError("index out of range")
        if self.a[i] < k:  # @line L22
            raise ValueError("new key is larger than the current key")
        self.a[i] = k  # @line L23
        self._sift_up(i)  # @line L24

    def build(self, items: Iterable[T]) -> None:
        """Replace the contents by the given keys and make a heap in O(n) time."""
        self.a = list(items)  # @line L25
        n = len(self.a)
        for i in range(n // 2 - 1, -1, -1):  # @line L26
            self._sift_down(n, i)

    def check_invariant(self) -> None:
        """Raise AssertionError if a key is smaller than its parent."""
        a = self.a
        for i in range(1, len(a)):
            assert not a[i] < a[(i - 1) // 2], f"heap order fails at index {i}"
