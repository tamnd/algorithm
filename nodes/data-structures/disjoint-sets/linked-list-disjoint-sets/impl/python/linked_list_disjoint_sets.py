# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linked-list-disjoint-sets/. The authors are listed in prov/JEF2AM.jsonl.

from collections.abc import Hashable, Iterator
from typing import Generic, TypeVar

T = TypeVar("T", bound=Hashable)


class LinkedListDisjointSets(Generic[T]):
    """Disjoint sets as linked lists with weighted union.

    Each set is a list of its members, named by its head. Each element stores
    the head of its set and the next element of its list. find takes O(1)
    time. union appends the shorter list to the longer one and renames its
    elements, so m operations on n elements take O(m + n log n) time.
    """

    def __init__(self) -> None:
        self.head: dict[T, T] = {}
        self.next: dict[T, T | None] = {}
        self.tail: dict[T, T] = {}
        self.length: dict[T, int] = {}

    def __contains__(self, x: object) -> bool:
        return x in self.head

    def make_set(self, x: T) -> None:
        """Add x as a set of its own. Raise ValueError if x is already present."""
        if x in self.head:
            raise ValueError("element already present")
        self.tail[x] = x  # @line L1
        self.length[x] = 1
        self.head[x] = x  # @line L2
        self.next[x] = None

    def find(self, x: T) -> T:
        """Return the head of the list of x, the representative of its set."""
        return self.head[x]  # @line L3

    def union(self, x: T, y: T) -> bool:
        """Merge the sets of x and y. Return False if they were already one set."""
        s, t = self.head[x], self.head[y]  # @line L4
        if s == t:  # @line L5
            return False
        if self.length[s] > self.length[t]:  # @line L6
            s, t = t, s
        z: T | None = s
        while z is not None:  # @line L7
            self.head[z] = t
            z = self.next[z]
        self.next[self.tail[t]] = s  # @line L8
        self.tail[t] = self.tail.pop(s)
        self.length[t] += self.length.pop(s)  # @line L9
        return True

    def connected(self, x: T, y: T) -> bool:
        """Return True if x and y are in the same set."""
        return self.head[x] == self.head[y]

    def size(self, x: T) -> int:
        """Return the number of elements in the set of x."""
        return self.length[self.head[x]]

    def members(self, x: T) -> Iterator[T]:
        """Yield the elements of the set of x, from the head to the tail."""
        z: T | None = self.head[x]
        while z is not None:
            yield z
            z = self.next[z]

    @property
    def count(self) -> int:
        """The number of sets."""
        return len(self.length)

    def check_invariant(self) -> None:
        """Check that each list has its size, its tail and the right heads, and covers each element once."""
        seen: set[T] = set()
        assert self.tail.keys() == self.length.keys()
        for h in self.length:
            assert self.head[h] == h
            z: T | None = h
            last = h
            k = 0
            while z is not None:
                assert z not in seen
                seen.add(z)
                assert self.head[z] == h
                last = z
                z = self.next[z]
                k += 1
            assert k == self.length[h]
            assert last == self.tail[h]
        assert seen == self.head.keys()
