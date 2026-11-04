# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-array-trie/. The authors are listed in prov/8PV0JP.jsonl.

"""Static double-array trie (Aoe's base/check representation).

Each trie node is a cell index s. The child of s on symbol code a is the cell
t = base[s] + a, valid exactly when check[t] == s. Code 0 is the end-of-key
symbol: the cell base[s] + 0 of a node whose path is a key is a leaf cell,
whose base holds -(i + 1) for the index i of its value. The root is cell 0;
free cells have check == -1. This version builds the arrays from a key set;
lookups take O(1) per symbol.
"""

from collections import deque
from typing import Generic, TypeVar

V = TypeVar("V")

FREE = -1
ROOT_CHECK = -2


class DoubleArrayTrie(Generic[V]):
    """Read-only map from strings to values, stored in two integer arrays."""

    def __init__(self, items: dict[str, V]) -> None:
        symbols = sorted({c for k in items for c in k})
        self.code = {c: i + 1 for i, c in enumerate(symbols)}
        self.symbols = symbols
        self.values: list[V] = []
        self.base: list[int] = [0]
        self.check: list[int] = [ROOT_CHECK]
        self._build(items)

    def _next(self, s: int, a: int) -> int:
        """The child of cell s on code a, or -1."""
        t = self.base[s] + a  # @line L1
        if 0 <= t < len(self.check) and self.check[t] == s:  # @line L2
            return t
        return -1  # @line L3

    def get(self, key: str) -> V | None:
        """Return the value of key, or None."""
        s = 0
        for c in key:  # @line L4
            a = self.code.get(c)
            if a is None:
                return None
            s = self._next(s, a)
            if s < 0:
                return None
        t = self._next(s, 0)  # @line L5
        return self.values[-self.base[t] - 1] if t >= 0 else None  # @line L6

    def _grow(self, size: int) -> None:
        while len(self.check) < size:
            self.base.append(0)
            self.check.append(FREE)

    def _build(self, items: dict[str, V]) -> None:
        # The plain trie of the keys: a node is a dict from code to child, and
        # code 0 maps to the value index of the key that ends there.
        trie: dict[int, object] = {}
        for key in sorted(items):  # @line L7
            node = trie
            for c in key:
                node = node.setdefault(self.code[c], {})  # type: ignore[assignment]
            node[0] = len(self.values)
            self.values.append(items[key])
        queue: deque[tuple[dict[int, object], int]] = deque([(trie, 0)])
        while queue:  # @line L8
            node, s = queue.popleft()
            codes = sorted(node)  # @line L9
            if not codes:
                continue
            b = 1  # @line L10
            while True:
                self._grow(b + codes[-1] + 1)
                if all(self.check[b + a] == FREE for a in codes):
                    break
                b += 1
            self.base[s] = b  # @line L11
            for a in codes:
                self.check[b + a] = s
            for a in codes:  # @line L12
                if a == 0:
                    self.base[b] = -int(node[0]) - 1  # type: ignore[arg-type]
                else:
                    queue.append((node[a], b + a))  # type: ignore[arg-type]

    def keys_with_prefix(self, p: str) -> list[str]:
        """The keys that start with p, in lexicographic order."""
        s = 0
        for c in p:
            a = self.code.get(c)
            if a is None:
                return []
            s = self._next(s, a)
            if s < 0:
                return []
        out: list[str] = []
        stack: list[tuple[int, str]] = [(s, p)]
        while stack:
            s, path = stack.pop()
            if self._next(s, 0) >= 0:
                out.append(path)
            for a in range(len(self.symbols), 0, -1):
                t = self._next(s, a)
                if t >= 0:
                    stack.append((t, path + self.symbols[a - 1]))
        return out

    def prefixes_of(self, text: str) -> list[str]:
        """The keys that are prefixes of text, shortest first."""
        out: list[str] = []
        s = 0
        for d in range(len(text) + 1):
            if self._next(s, 0) >= 0:
                out.append(text[:d])
            if d == len(text):
                break
            a = self.code.get(text[d])
            s = self._next(s, a) if a is not None else -1
            if s < 0:
                break
        return out

    def check_invariant(self) -> None:
        assert len(self.base) == len(self.check) and self.check[0] == ROOT_CHECK
        leaves = 0
        seen = {0}
        stack = [0]
        while stack:
            s = stack.pop()
            for a in range(len(self.symbols) + 1):
                t = self._next(s, a)
                if t < 0:
                    continue
                assert t not in seen, "a cell has two parents"
                seen.add(t)
                if a == 0:
                    assert 0 <= -self.base[t] - 1 < len(self.values)
                    leaves += 1
                else:
                    assert self.base[t] >= 1
                    stack.append(t)
        assert leaves == len(self.values)
        assert all(self.check[t] == FREE for t in range(len(self.check)) if t not in seen)
