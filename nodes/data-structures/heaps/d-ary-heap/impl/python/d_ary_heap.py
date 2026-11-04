# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/d-ary-heap/. The authors are listed in prov/Y99BAR.jsonl.

from collections.abc import Iterable
from typing import Any, Generic, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


T = TypeVar("T", bound=Ordered)


class DaryHeap(Generic[T]):
    """A d-ary min-heap in a 0-based list.

    The parent of i is (i - 1) // d and its children are d*i + 1 .. d*i + d.
    insert and decrease_key take O(log_d n) time; extract_min takes
    O(d log_d n) time; build takes O(n) time. Keys need only "<".
    """

    def __init__(self, d: int = 4) -> None:
        if d < 2:
            raise ValueError("d must be at least 2")
        self.d = d
        self.a: list[T] = []

    def __len__(self) -> int:
        return len(self.a)

    def _parent(self, i: int) -> int:
        return (i - 1) // self.d  # @line L1

    def _child(self, i: int, j: int) -> int:
        return self.d * i + j  # @line L2: j = 1 .. d

    def _sift_up(self, i: int) -> None:
        a = self.a
        while i > 0 and a[i] < a[self._parent(i)]:  # @line L3
            p = self._parent(i)
            a[i], a[p] = a[p], a[i]  # @line L4
            i = p  # @line L5

    def _sift_down(self, i: int) -> None:
        a, n = self.a, len(self.a)
        while True:  # @line L6
            m = i  # @line L7
            for j in range(1, self.d + 1):  # @line L8
                c = self._child(i, j)  # @line L9
                if c >= n:
                    break
                if a[c] < a[m]:  # @line L10
                    m = c
            if m == i:  # @line L11
                return
            a[i], a[m] = a[m], a[i]  # @line L12
            i = m

    def insert(self, key: T) -> None:
        """Add a key. O(log_d n) time."""
        self.a.append(key)  # @line L13
        self._sift_up(len(self.a) - 1)  # @line L14

    def find_min(self) -> T:
        if not self.a:
            raise IndexError("heap underflow")
        return self.a[0]

    def extract_min(self) -> T:
        """Remove and return a smallest key. O(d log_d n) time."""
        if not self.a:  # @line L15
            raise IndexError("heap underflow")
        top = self.a[0]  # @line L16
        last = self.a.pop()
        if self.a:
            self.a[0] = last
            self._sift_down(0)  # @line L17
        return top  # @line L18

    def decrease_key(self, i: int, key: T) -> None:
        """Lower the key at index i to key. O(log_d n) time."""
        if not 0 <= i < len(self.a):
            raise IndexError("index out of range")
        if self.a[i] < key:  # @line L19
            raise ValueError("new key is larger than the current key")
        self.a[i] = key  # @line L20
        self._sift_up(i)

    def build(self, items: Iterable[T]) -> None:
        """Replace the contents by the given keys, in O(n) time."""
        self.a = list(items)  # @line L21
        n = len(self.a)
        for i in range(self._parent(n - 1) if n > 1 else -1, -1, -1):  # @line L22
            self._sift_down(i)

    def check_invariant(self) -> None:
        a = self.a
        for i in range(1, len(a)):
            assert not a[i] < a[self._parent(i)]
