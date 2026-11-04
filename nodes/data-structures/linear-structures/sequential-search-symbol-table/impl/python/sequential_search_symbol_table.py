# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequential-search-symbol-table/. The authors are listed in prov/5G5MVH.jsonl.

from collections.abc import Iterator
from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class _Node(Generic[K, V]):
    __slots__ = ("key", "value", "next")

    def __init__(self, key: K, value: V, nxt: "_Node[K, V] | None") -> None:
        self.key = key
        self.value = value
        self.next = nxt


class SequentialSearchST(Generic[K, V]):
    """A symbol table stored as an unordered singly linked list of key-value pairs.

    Keys need only an equality test. get, put and delete make at most n key
    compares on n keys (n for a miss and for a new key); a hit at position i
    makes i. Space Theta(n). The attribute compares counts the key compares.
    """

    def __init__(self) -> None:
        self.first: _Node[K, V] | None = None
        self.n = 0
        self.compares = 0

    def get(self, k: K) -> V | None:
        """Return the value of k, or None if k is absent."""
        x = self.first  # @line L1
        while x is not None:  # @line L2
            self.compares += 1
            if x.key == k:  # @line L3
                return x.value
            x = x.next  # @line L4
        return None  # @line L5

    def put(self, k: K, v: V) -> None:
        """Map k to v, replacing an old value; a new key goes to the front."""
        x = self.first  # @line L6
        while x is not None:  # @line L7
            self.compares += 1
            if x.key == k:  # @line L8
                x.value = v
                return
            x = x.next  # @line L9
        self.first = _Node(k, v, self.first)  # @line L10
        self.n += 1

    def delete(self, k: K) -> None:
        """Remove k and its value, if present."""
        prev: _Node[K, V] | None = None
        x = self.first
        while x is not None:
            self.compares += 1
            if x.key == k:
                break
            prev, x = x, x.next
        if x is None:
            return
        if prev is None:
            self.first = x.next
        else:
            prev.next = x.next
        self.n -= 1

    def contains(self, k: K) -> bool:
        """Return True if k is in the table."""
        x = self.first
        while x is not None:
            if x.key == k:
                return True
            x = x.next
        return False

    def __len__(self) -> int:
        return self.n

    def keys(self) -> Iterator[K]:
        """The keys from the first node to the last."""
        x = self.first
        while x is not None:
            yield x.key
            x = x.next

    def check_invariant(self) -> None:
        """Assert (I1) and (I2): n nodes, no cycle, distinct keys."""
        seen: list[K] = []
        x, steps = self.first, 0
        while x is not None:
            assert steps < self.n, "cycle or wrong size"
            assert x.key not in seen, "duplicate key"
            seen.append(x.key)
            steps += 1
            x = x.next
        assert steps == self.n
