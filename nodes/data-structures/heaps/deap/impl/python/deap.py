# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deap/. The authors are listed in prov/5CWRB5.jsonl.

from collections.abc import Iterable
from typing import Any, Generic, Optional, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


T = TypeVar("T", bound=Ordered)


class Deap(Generic[T]):
    """A deap: a double-ended heap in one 1-based array with an empty root.

    The positions 2 .. n hold the keys. The subtree of 2 is a min-heap and
    the subtree of 3 is a max-heap. Each min node i has a partner j in the
    max-heap at the same level, or the parent of that place if it is past
    n, and A[i] <= A[j]. insert, extract_min and extract_max take
    O(log n) time; find_min and find_max take O(1) time. Keys need only "<".
    """

    def __init__(self, keys: Iterable[T] = ()) -> None:
        self.a: list[Optional[T]] = [None, None]
        for k in keys:
            self.insert(k)

    def __len__(self) -> int:
        return len(self.a) - 2

    @property
    def n(self) -> int:
        return len(self.a) - 1

    def _k(self, i: int) -> T:
        v = self.a[i]
        assert v is not None
        return v

    @staticmethod
    def is_max_node(i: int) -> bool:
        k = i.bit_length() - 1
        return (i >> (k - 1)) == 3

    @staticmethod
    def min_partner(j: int) -> int:
        return j - (1 << (j.bit_length() - 2))

    def max_partner(self, i: int) -> int:
        j = i + (1 << (i.bit_length() - 2))
        return j if j <= self.n else j // 2

    def _min_sift_up(self, i: int, x: T) -> None:
        a = self.a
        while i > 3 and x < self._k(i // 2):  # @line L6
            a[i] = a[i // 2]
            i //= 2
        a[i] = x  # @line L7

    def _max_sift_up(self, j: int, x: T) -> None:
        a = self.a
        while j > 3 and self._k(j // 2) < x:  # @line L8
            a[j] = a[j // 2]
            j //= 2
        a[j] = x  # @line L9

    def insert(self, x: T) -> None:
        a = self.a
        a.append(x)  # @line L1
        n = self.n
        if n == 2:
            return
        if self.is_max_node(n):  # @line L2
            i = self.min_partner(n)
            if x < self._k(i):  # @line L3
                a[n] = a[i]
                self._min_sift_up(i, x)
            else:
                self._max_sift_up(n, x)
        else:
            j = self.max_partner(n)  # @line L4
            if self._k(j) < x:  # @line L5
                a[n] = a[j]
                self._max_sift_up(j, x)
            else:
                self._min_sift_up(n, x)

    def find_min(self) -> T:
        if self.n < 2:
            raise IndexError("find_min from an empty deap")
        return self._k(2)

    def find_max(self) -> T:
        if self.n < 2:
            raise IndexError("find_max from an empty deap")
        return self._k(3) if self.n >= 3 else self._k(2)

    def extract_min(self) -> T:
        a = self.a
        if self.n < 2:  # @line L10
            raise IndexError("extract_min from an empty deap")
        r = self._k(2)
        x = self._k(self.n)
        a.pop()
        n = self.n
        if n < 2:  # @line L11
            return r
        if n == 2:
            a[2] = x
            return r
        i = 2
        while 2 * i <= n:  # @line L12
            c = 2 * i
            if c + 1 <= n and self._k(c + 1) < self._k(c):
                c += 1
            a[i] = a[c]
            i = c
        j = self.max_partner(i)  # @line L13
        if self._k(j) < x:  # @line L14
            a[i] = a[j]
            self._max_sift_up(j, x)
        else:
            self._min_sift_up(i, x)
        return r

    def extract_max(self) -> T:
        a = self.a
        if self.n < 2:  # @line L15
            raise IndexError("extract_max from an empty deap")
        if self.n == 2:
            v = a.pop()
            assert v is not None
            return v
        r = self._k(3)  # @line L16
        x = self._k(self.n)
        a.pop()
        n = self.n
        if n == 2:  # @line L17
            return r
        j = 3
        while 2 * j <= n:  # @line L18
            c = 2 * j
            if c + 1 <= n and self._k(c) < self._k(c + 1):
                c += 1
            a[j] = a[c]
            j = c
        i = self.min_partner(j)  # @line L19
        if 2 * i <= n:
            c = 2 * i
            if c + 1 <= n and self._k(c) < self._k(c + 1):
                c += 1
            i = c
        if x < self._k(i):  # @line L20
            a[j] = a[i]
            self._min_sift_up(i, x)
        else:
            self._max_sift_up(j, x)
        return r

    def keys(self) -> list[T]:
        return [self._k(i) for i in range(2, self.n + 1)]

    def check_invariant(self) -> None:
        n = self.n
        for i in range(4, n + 1):
            p = i // 2
            if self.is_max_node(i):
                assert not self._k(p) < self._k(i)
            else:
                assert not self._k(i) < self._k(p)
        for i in range(2, n + 1):
            if not self.is_max_node(i):
                j = self.max_partner(i)
                if j >= 3:
                    assert not self._k(j) < self._k(i)
