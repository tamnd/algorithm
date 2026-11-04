# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/min-max-heap/. The authors are listed in prov/HGEHQG.jsonl.

from typing import Any, Generic, Iterable, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)


def is_min_level(i: int) -> bool:
    """True if index i (0-based) is on a min level: levels 0, 2, 4, ..."""
    return ((i + 1).bit_length() - 1) % 2 == 0


class MinMaxHeap(Generic[K]):
    """A double-ended priority queue in one array, after Atkinson et al. (1986).

    The root is on level 0. Nodes on even levels are smaller than or equal to
    all their descendants; nodes on odd levels are larger than or equal to them.
    """

    def __init__(self, items: Iterable[K] = ()) -> None:
        """Build a heap from items in O(n) time, bottom up."""
        self.a: list[K] = list(items)
        for i in range(len(self.a) // 2 - 1, -1, -1):
            self._push_down(i)

    def __len__(self) -> int:
        return len(self.a)

    def is_empty(self) -> bool:
        """Return True if the heap holds no item."""
        return not self.a

    def _better(self, x: K, y: K, min_level: bool) -> bool:
        """True if x should be above y on a level of the given kind."""
        return x < y if min_level else y < x

    def _push_down(self, i: int) -> None:
        """Move a[i] down until the min-max order holds in the subtree of i."""
        a, n = self.a, len(self.a)
        mn = is_min_level(i)
        while 2 * i + 1 < n:  # @line L1
            m = 2 * i + 1  # @line L2
            for j in (2 * i + 2, 4 * i + 3, 4 * i + 4, 4 * i + 5, 4 * i + 6):
                if j < n and self._better(a[j], a[m], mn):
                    m = j
            if m <= 2 * i + 2:  # @line L3
                if self._better(a[m], a[i], mn):  # @line L4
                    a[m], a[i] = a[i], a[m]
                return  # @line L5
            if not self._better(a[m], a[i], mn):  # @line L6
                return
            a[m], a[i] = a[i], a[m]  # @line L7
            p = (m - 1) // 2
            if self._better(a[p], a[m], mn):  # @line L8
                a[m], a[p] = a[p], a[m]
            i = m  # @line L9

    def _push_up(self, i: int) -> None:
        """Move a[i] up until the min-max order holds on the path to the root."""
        a = self.a
        if i == 0:  # @line L10
            return
        p = (i - 1) // 2  # @line L11
        mn = is_min_level(i)
        if self._better(a[i], a[p], not mn):  # @line L12
            a[i], a[p] = a[p], a[i]  # @line L13
            i, mn = p, not mn
        while i >= 3 and self._better(a[i], a[(i - 3) // 4], mn):  # @line L14
            g = (i - 3) // 4
            a[i], a[g] = a[g], a[i]  # @line L15
            i = g

    def insert(self, x: K) -> None:
        """Add x to the heap in O(log n) time."""
        self.a.append(x)  # @line L20
        self._push_up(len(self.a) - 1)

    def find_min(self) -> K:
        """Return a smallest item; the heap must not be empty."""
        if not self.a:
            raise IndexError("find_min on an empty heap")
        return self.a[0]

    def _max_index(self) -> int:
        a = self.a
        if len(a) <= 2:
            return len(a) - 1
        return 1 if not a[1] < a[2] else 2

    def find_max(self) -> K:
        """Return a largest item; the heap must not be empty."""
        if not self.a:
            raise IndexError("find_max on an empty heap")
        return self.a[self._max_index()]

    def delete_min(self) -> K:
        """Remove and return a smallest item in O(log n) time."""
        return self._delete_at(0)  # @line L16

    def delete_max(self) -> K:
        """Remove and return a largest item in O(log n) time."""
        if not self.a:
            raise IndexError("delete_max on an empty heap")
        return self._delete_at(self._max_index())  # @line L18

    def _delete_at(self, m: int) -> K:
        a = self.a
        if not a:
            raise IndexError("delete on an empty heap")
        x = a[m]  # @line L19
        last = a.pop()
        if m < len(a):
            a[m] = last
            self._push_down(m)
        return x  # @line L17

    def check_invariant(self) -> None:
        """Check that each node is on the correct side of all its descendants."""
        a, n = self.a, len(self.a)
        for i in range(1, n):
            j = (i - 1) // 2
            while True:  # every ancestor j of i
                if is_min_level(j):
                    assert not (a[i] < a[j]), f"min order at {j}, {i}"
                else:
                    assert not (a[j] < a[i]), f"max order at {j}, {i}"
                if j == 0:
                    break
                j = (j - 1) // 2
