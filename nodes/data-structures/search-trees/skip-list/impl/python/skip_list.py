# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/skip-list/. The authors are listed in prov/XYVYKG.jsonl.

"""Skip list (Pugh 1990): an ordered map made of linked lists in levels."""

import random
from typing import Any, Iterator


class _Node:
    __slots__ = ("key", "value", "forward")

    def __init__(self, key: Any, value: Any, level: int) -> None:
        self.key = key
        self.value = value
        self.forward: list["_Node | None"] = [None] * level


class SkipList:
    """Ordered map with expected O(log n) search, insert and delete.

    Keys need only "<". Each node gets level l with probability p^(l-1)(1-p),
    capped at max_level. The header node has max_level forward pointers.
    """

    def __init__(self, p: float = 0.5, max_level: int = 32, seed: int | None = None) -> None:
        if not 0.0 < p < 1.0:
            raise ValueError("p must be in (0, 1)")
        self.p = p
        self.max_level = max_level
        self.level = 1  # number of levels in use
        self.header = _Node(None, None, max_level)
        self.n = 0
        self._rng = random.Random(seed)

    def __len__(self) -> int:
        return self.n

    def _random_level(self) -> int:
        lvl = 1
        while lvl < self.max_level and self._rng.random() < self.p:
            lvl += 1
        return lvl

    def _find_update(self, key: Any) -> list[_Node]:
        """For each level i, the last node with key < key (the header if none)."""
        update: list[_Node] = [self.header] * self.max_level
        x = self.header
        for i in range(self.level - 1, -1, -1):
            nxt = x.forward[i]
            while nxt is not None and nxt.key < key:
                x = nxt
                nxt = x.forward[i]
            update[i] = x
        return update

    def search(self, key: Any) -> Any:
        """Return the value of key, or None if key is absent."""
        x = self.header  # @line L1
        for i in range(self.level - 1, -1, -1):  # @line L2
            nxt = x.forward[i]
            while nxt is not None and nxt.key < key:  # @line L3
                x = nxt
                nxt = x.forward[i]
        x = x.forward[0]  # @line L4
        if x is not None and not (key < x.key):  # @line L5
            return x.value
        return None

    def __contains__(self, key: Any) -> bool:
        x = self._find_update(key)[0].forward[0]
        return x is not None and not (key < x.key)

    def insert(self, key: Any, value: Any = None) -> bool:
        """Map key to value. Return True if key was new."""
        update = self._find_update(key)  # @line L6
        x = update[0].forward[0]
        if x is not None and not (key < x.key):  # @line L7
            x.value = value
            return False
        lvl = self._random_level()  # @line L8
        if lvl > self.level:  # @line L9
            for i in range(self.level, lvl):
                update[i] = self.header
            self.level = lvl
        z = _Node(key, value, lvl)  # @line L10
        for i in range(lvl):  # @line L11
            z.forward[i] = update[i].forward[i]  # @line L12
            update[i].forward[i] = z  # @line L13
        self.n += 1
        return True

    def delete(self, key: Any) -> bool:
        """Remove key. Return True if it was present."""
        update = self._find_update(key)  # @line L14
        x = update[0].forward[0]
        if x is None or key < x.key:  # @line L15
            return False
        for i in range(len(x.forward)):  # @line L16
            if update[i].forward[i] is x:
                update[i].forward[i] = x.forward[i]  # @line L17
        while self.level > 1 and self.header.forward[self.level - 1] is None:  # @line L18
            self.level -= 1
        self.n -= 1
        return True

    def floor(self, key: Any) -> Any:
        """The largest key <= key, or None."""
        update = self._find_update(key)
        x = update[0].forward[0]
        if x is not None and not (key < x.key):
            return x.key
        y = update[0]
        return None if y is self.header else y.key

    def ceiling(self, key: Any) -> Any:
        """The smallest key >= key, or None."""
        x = self._find_update(key)[0].forward[0]
        return None if x is None else x.key

    def keys(self) -> Iterator[Any]:
        x = self.header.forward[0]
        while x is not None:
            yield x.key
            x = x.forward[0]

    def items(self) -> Iterator[tuple[Any, Any]]:
        x = self.header.forward[0]
        while x is not None:
            yield x.key, x.value
            x = x.forward[0]

    def level_sizes(self) -> list[int]:
        """The number of nodes in each level, from level 1 up."""
        sizes = []
        for i in range(self.level):
            c = 0
            x = self.header.forward[i]
            while x is not None:
                c += 1
                x = x.forward[i]
            sizes.append(c)
        return sizes

    def check_invariant(self) -> None:
        """Raise AssertionError if the structure is broken."""
        assert 1 <= self.level <= self.max_level
        for i in range(self.level, self.max_level):
            assert self.header.forward[i] is None
        bottom = []
        x = self.header.forward[0]
        while x is not None:
            assert 1 <= len(x.forward) <= self.max_level
            bottom.append(x)
            x = x.forward[0]
        assert len(bottom) == self.n
        for a, b in zip(bottom, bottom[1:]):
            assert a.key < b.key
        if self.level > 1:
            assert self.header.forward[self.level - 1] is not None
        for i in range(self.level):
            expected = [v for v in bottom if len(v.forward) > i]
            got = []
            x = self.header.forward[i]
            while x is not None:
                got.append(x)
                x = x.forward[i]
            assert got == expected, "level %d is not the sublist of tall nodes" % (i + 1)
