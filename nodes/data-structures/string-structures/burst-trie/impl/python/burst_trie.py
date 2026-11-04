# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burst-trie/. The authors are listed in prov/4A6NMB.jsonl.

"""Burst trie: a trie of access nodes whose leaves are small containers of strings.

An access node has one slot per symbol and a value for the key that ends at the
node. A slot holds either another access node or a container: a sorted list of
(suffix, value) pairs for the keys that continue through that slot, with the
symbols of the path removed. When a container holds more than `limit` pairs it
bursts: it is replaced by an access node, and its pairs are spread over new
containers by their first symbol (the limit heuristic).
"""

from bisect import bisect_left
from typing import Generic, TypeVar

V = TypeVar("V")


class _Container(Generic[V]):
    __slots__ = ("suffixes", "vals")

    def __init__(self) -> None:
        self.suffixes: list[str] = []
        self.vals: list[V] = []

    def find(self, t: str) -> int:
        k = bisect_left(self.suffixes, t)
        return k if k < len(self.suffixes) and self.suffixes[k] == t else -1


class _Access(Generic[V]):
    __slots__ = ("slots", "val")

    def __init__(self) -> None:
        self.slots: dict[str, _Access[V] | _Container[V]] = {}
        self.val: V | None = None


class BurstTrie(Generic[V]):
    """String symbol table; values must not be None."""

    def __init__(self, limit: int = 32) -> None:
        if limit < 1:
            raise ValueError("limit must be positive")
        self.limit = limit
        self.root: _Access[V] = _Access()
        self.n = 0

    def __len__(self) -> int:
        return self.n

    def get(self, s: str) -> V | None:
        """Return the value of key s, or None."""
        x: _Access[V] | _Container[V] = self.root
        d = 0
        while isinstance(x, _Access):  # @line L1
            if d == len(s):  # @line L2
                return x.val
            nxt = x.slots.get(s[d])  # @line L3
            if nxt is None:
                return None
            x, d = nxt, d + 1
        k = x.find(s[d:])  # @line L4
        return x.vals[k] if k >= 0 else None  # @line L5

    def put(self, s: str, v: V) -> None:
        """Set the value of key s to v."""
        if v is None:
            raise ValueError("a value must not be None")
        x = self.root
        d = 0
        while True:  # @line L6
            if d == len(s):
                if x.val is None:
                    self.n += 1
                x.val = v
                return
            nxt = x.slots.get(s[d])
            if nxt is None:  # @line L7
                nxt = x.slots[s[d]] = _Container()
            if isinstance(nxt, _Access):
                x, d = nxt, d + 1
                continue
            t = s[d + 1 :]  # @line L8
            k = bisect_left(nxt.suffixes, t)
            if k < len(nxt.suffixes) and nxt.suffixes[k] == t:
                nxt.vals[k] = v
                return
            nxt.suffixes.insert(k, t)  # @line L9
            nxt.vals.insert(k, v)
            self.n += 1
            if len(nxt.suffixes) > self.limit:  # @line L10
                x.slots[s[d]] = self._burst(nxt)
            return

    def _burst(self, c: _Container[V]) -> _Access[V]:
        """Replace an overfull container by an access node, bursting again where needed."""
        top: _Access[V] = _Access()
        work: list[tuple[_Access[V], _Container[V]]] = [(top, c)]
        while work:
            node, cont = work.pop()
            for t, v in zip(cont.suffixes, cont.vals):  # @line L11
                if t == "":
                    node.val = v
                    continue
                child = node.slots.get(t[0])
                if child is None:
                    child = node.slots[t[0]] = _Container()
                assert isinstance(child, _Container)
                child.suffixes.append(t[1:])  # sorted input gives sorted output
                child.vals.append(v)
            for sym, child in list(node.slots.items()):  # @line L12
                if isinstance(child, _Container) and len(child.suffixes) > self.limit:
                    new: _Access[V] = _Access()
                    node.slots[sym] = new
                    work.append((new, child))
        return top

    def delete(self, s: str) -> None:
        """Remove key s if present; an emptied container is removed from its slot."""
        x = self.root
        d = 0
        while True:
            if d == len(s):
                if x.val is not None:
                    x.val = None
                    self.n -= 1
                return
            nxt = x.slots.get(s[d])
            if nxt is None:
                return
            if isinstance(nxt, _Access):
                x, d = nxt, d + 1
                continue
            k = nxt.find(s[d + 1 :])
            if k >= 0:
                del nxt.suffixes[k]
                del nxt.vals[k]
                self.n -= 1
                if not nxt.suffixes:
                    del x.slots[s[d]]
            return

    def items_with_prefix(self, p: str) -> list[tuple[str, V]]:
        """The (key, value) pairs whose key starts with p, in order."""
        x: _Access[V] | _Container[V] = self.root
        d = 0
        while isinstance(x, _Access) and d < len(p):
            nxt = x.slots.get(p[d])
            if nxt is None:
                return []
            x, d = nxt, d + 1
        out: list[tuple[str, V]] = []
        if isinstance(x, _Container):
            head, rest = p[:d], p[d:]
            k = bisect_left(x.suffixes, rest)
            while k < len(x.suffixes) and x.suffixes[k].startswith(rest):
                out.append((head + x.suffixes[k], x.vals[k]))
                k += 1
            return out
        stack: list[tuple[_Access[V] | _Container[V], str]] = [(x, p)]
        while stack:
            y, path = stack.pop()
            if isinstance(y, _Container):
                out.extend((path + t, v) for t, v in zip(y.suffixes, y.vals))
                continue
            if y.val is not None:
                out.append((path, y.val))
            for sym in sorted(y.slots, reverse=True):
                stack.append((y.slots[sym], path + sym))
        return out

    def keys(self) -> list[str]:
        return [k for k, _ in self.items_with_prefix("")]

    def shape(self) -> tuple[int, int]:
        """The number of access nodes and of containers."""
        acc, cont = 0, 0
        stack: list[_Access[V] | _Container[V]] = [self.root]
        while stack:
            y = stack.pop()
            if isinstance(y, _Container):
                cont += 1
            else:
                acc += 1
                stack.extend(y.slots.values())
        return acc, cont

    def check_invariant(self) -> None:
        count = 0
        stack: list[_Access[V] | _Container[V]] = [self.root]
        while stack:
            y = stack.pop()
            if isinstance(y, _Container):
                assert 1 <= len(y.suffixes) <= self.limit, "container size out of range"
                assert len(y.suffixes) == len(y.vals)
                assert all(a < b for a, b in zip(y.suffixes, y.suffixes[1:])), "container not sorted"
                count += len(y.suffixes)
            else:
                count += y.val is not None
                stack.extend(y.slots.values())
        assert count == self.n
