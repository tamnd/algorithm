# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/indexed-priority-queue/. The authors are listed in prov/QQ610A.jsonl.

from typing import Any, Generic, Optional, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


T = TypeVar("T", bound=Ordered)


class IndexedMinPQ(Generic[T]):
    """A binary min-heap of item indices 0 .. m - 1, ordered by their keys.

    pq is the heap, a 0-based list of indices; qp[i] is the position of the
    index i in pq, or -1 if i is not in the queue; key[i] is the key of i.
    So pq[qp[i]] == i for each i in the queue. insert, extract_min,
    decrease_key, change_key and delete take O(log n) time; contains and
    key_of take O(1) time. Keys need only "<".
    """

    def __init__(self, m: int) -> None:
        if m < 0:
            raise ValueError("capacity must be at least 0")
        self.m = m
        self.pq: list[int] = []
        self.qp: list[int] = [-1] * m
        self.key: list[Optional[T]] = [None] * m

    def __len__(self) -> int:
        return len(self.pq)

    def _check_index(self, i: int) -> None:
        if not 0 <= i < self.m:
            raise IndexError("index out of range")

    def contains(self, i: int) -> bool:
        self._check_index(i)
        return self.qp[i] != -1

    def key_of(self, i: int) -> T:
        if not self.contains(i):
            raise KeyError("index not in the queue")
        k = self.key[i]
        assert k is not None
        return k

    def _less(self, a: int, b: int) -> bool:
        ka, kb = self.key[self.pq[a]], self.key[self.pq[b]]
        assert ka is not None and kb is not None
        return ka < kb

    def _exch(self, a: int, b: int) -> None:
        pq = self.pq
        pq[a], pq[b] = pq[b], pq[a]  # @line L13
        self.qp[pq[a]] = a
        self.qp[pq[b]] = b

    def _swim(self, j: int) -> None:
        while j > 0 and self._less(j, (j - 1) // 2):  # @line L14
            self._exch(j, (j - 1) // 2)  # @line L15
            j = (j - 1) // 2

    def _sink(self, j: int) -> None:
        n = len(self.pq)
        while 2 * j + 1 < n:  # @line L16
            c = 2 * j + 1  # @line L17
            if c + 1 < n and self._less(c + 1, c):
                c += 1
            if not self._less(c, j):  # @line L18
                return
            self._exch(j, c)  # @line L19
            j = c

    def insert(self, i: int, k: T) -> None:
        if self.contains(i):  # @line L1
            raise KeyError("index already in the queue")
        self.qp[i] = len(self.pq)  # @line L2
        self.pq.append(i)
        self.key[i] = k
        self._swim(self.qp[i])  # @line L3

    def min_index(self) -> int:
        if not self.pq:
            raise IndexError("min_index from an empty queue")
        return self.pq[0]

    def extract_min(self) -> tuple[int, T]:
        if not self.pq:  # @line L4
            raise IndexError("extract_min from an empty queue")
        i = self.pq[0]  # @line L5
        k = self.key_of(i)
        self._exch(0, len(self.pq) - 1)
        self.pq.pop()
        self._sink(0)  # @line L6
        self.qp[i] = -1
        self.key[i] = None
        return i, k  # @line L7

    def decrease_key(self, i: int, k: T) -> None:
        if self.key_of(i) < k:  # @line L8
            raise ValueError("new key is larger than the current key")
        self.key[i] = k  # @line L9
        self._swim(self.qp[i])

    def change_key(self, i: int, k: T) -> None:
        old = self.key_of(i)
        self.key[i] = k
        if k < old:
            self._swim(self.qp[i])
        else:
            self._sink(self.qp[i])

    def delete(self, i: int) -> T:
        k = self.key_of(i)
        j = self.qp[i]  # @line L10
        self._exch(j, len(self.pq) - 1)
        self.pq.pop()
        if j < len(self.pq):  # @line L11
            self._swim(j)
            self._sink(j)
        self.qp[i] = -1  # @line L12
        self.key[i] = None
        return k

    def check_invariant(self) -> None:
        n = len(self.pq)
        for j, i in enumerate(self.pq):
            assert self.qp[i] == j
            assert self.key[i] is not None
            if j > 0:
                assert not self._less(j, (j - 1) // 2)
        assert sum(1 for p in self.qp if p != -1) == n
        for i in range(self.m):
            if self.qp[i] == -1:
                assert self.key[i] is None
