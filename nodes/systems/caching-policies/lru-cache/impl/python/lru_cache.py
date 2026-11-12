# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lru-cache/. The authors are listed in prov/DKPAX9.jsonl.

from collections.abc import Hashable
from typing import Any


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: Any = None, value: Any = None) -> None:
        self.key = key
        self.value = value
        self.prev: "_Node" = self
        self.next: "_Node" = self


class LRUCache:
    """A map of at most `capacity` entries that evicts the least recently used one.

    A dict maps each key to its node. The nodes form a circular doubly linked
    list with one sentinel: sentinel.next is the most recently used entry and
    sentinel.prev the least recently used one. get and put each take O(1)
    expected time.
    """

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.capacity = capacity
        self.map: dict[Hashable, _Node] = {}
        self.head = _Node()  # the sentinel

    def __len__(self) -> int:
        return len(self.map)

    def __contains__(self, key: Hashable) -> bool:
        return key in self.map

    def _unlink(self, x: _Node) -> None:
        x.prev.next = x.next
        x.next.prev = x.prev

    def _push_front(self, x: _Node) -> None:
        x.prev = self.head
        x.next = self.head.next
        self.head.next.prev = x
        self.head.next = x

    def get(self, key: Hashable, default: Any = None) -> Any:
        """Return the value of key and mark it most recently used, or default."""
        x = self.map.get(key)  # @line L1
        if x is None:  # @line L2
            return default
        self._unlink(x)  # @line L3
        self._push_front(x)  # @line L4
        return x.value  # @line L5

    def put(self, key: Hashable, value: Any) -> tuple[Hashable, Any] | None:
        """Set key to value and mark it most recently used.

        Return the evicted (key, value) pair, or None if nothing was evicted.
        """
        x = self.map.get(key)  # @line L6
        if x is not None:  # @line L7
            x.value = value  # @line L8
            self._unlink(x)  # @line L9
            self._push_front(x)
            return None
        evicted = None
        if len(self.map) == self.capacity:  # @line L10
            y = self.head.prev  # @line L11
            self._unlink(y)  # @line L12
            del self.map[y.key]  # @line L13
            evicted = (y.key, y.value)
        x = _Node(key, value)  # @line L14
        self._push_front(x)  # @line L15
        self.map[key] = x  # @line L16
        return evicted

    def delete(self, key: Hashable) -> bool:
        """Remove key if present. Return True if it was present."""
        x = self.map.pop(key, None)
        if x is None:
            return False
        self._unlink(x)
        return True

    def keys_mru_first(self) -> list[Hashable]:
        """The keys from the most to the least recently used."""
        out = []
        x = self.head.next
        while x is not self.head:
            out.append(x.key)
            x = x.next
        return out
