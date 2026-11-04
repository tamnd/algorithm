# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/persistent-vector/. The authors are listed in prov/E5Q5G6.jsonl.

"""A persistent vector: a wide trie of fixed-size leaves plus a tail buffer.

This is the layout of the Clojure vector. Each node has up to M = 2^B
children (B = 5 gives M = 32). Nodes are tuples, so they cannot change.
Index i is found by its digits in base M. An update copies one node per
level, and push and pop at the end mostly copy only the tail.
Recursion depth is the height of the trie, which is about log n / B.
"""

from typing import Generic, Iterator, Optional, Tuple, TypeVar

T = TypeVar("T")

Node = Tuple[object, ...]


class PersistentVector(Generic[T]):
    """An immutable sequence with index, set, push and pop at the end."""

    __slots__ = ("_b", "_m", "_size", "_shift", "_root", "_tail")

    def __init__(self, bits: int = 5) -> None:
        """The empty vector with branching factor 2^bits. Cost: O(1)."""
        if bits < 1:
            raise ValueError("bits must be at least 1")
        self._b = bits
        self._m = 1 << bits
        self._size = 0
        self._shift = bits
        self._root: Node = ()
        self._tail: Node = ()

    def _make(self, size: int, shift: int, root: Node, tail: Node) -> "PersistentVector[T]":
        v: PersistentVector[T] = PersistentVector.__new__(PersistentVector)
        v._b, v._m = self._b, self._m
        v._size, v._shift, v._root, v._tail = size, shift, root, tail
        return v

    @classmethod
    def from_iterable(cls, items: "Iterator[T] | list[T]", bits: int = 5) -> "PersistentVector[T]":
        """Build by repeated push. Cost: O(n) amortized over the pushes."""
        v: PersistentVector[T] = cls(bits)
        for x in items:
            v = v.push(x)
        return v

    def _tailoff(self) -> int:
        if self._size < self._m:
            return 0
        return ((self._size - 1) >> self._b) << self._b

    def __len__(self) -> int:
        """Number of items. Cost: O(1)."""
        return self._size

    def _leaf_for(self, i: int) -> Node:
        if i >= self._tailoff():
            return self._tail
        node = self._root
        level = self._shift
        while level > 0:  # @line L2
            node = node[(i >> level) & (self._m - 1)]  # type: ignore[assignment]
            level -= self._b
        return node

    def get(self, i: int) -> T:
        """Item at index i. Cost: Θ(1 + log n / B)."""
        if not 0 <= i < self._size:
            raise IndexError("index out of range")
        if i >= self._tailoff():  # @line L1
            return self._tail[i - self._tailoff()]  # type: ignore[return-value]
        return self._leaf_for(i)[i & (self._m - 1)]  # type: ignore[return-value]  # @line L3

    def __getitem__(self, i: int) -> T:
        return self.get(i)

    def _set_path(self, node: Node, level: int, i: int, x: T) -> Node:
        c = list(node)  # @line L6
        if level == 0:  # @line L7
            c[i & (self._m - 1)] = x
        else:
            j = (i >> level) & (self._m - 1)
            c[j] = self._set_path(node[j], level - self._b, i, x)  # type: ignore[arg-type]
        return tuple(c)  # @line L8

    def set(self, i: int, x: T) -> "PersistentVector[T]":
        """A vector equal to this one with item i replaced by x.

        Cost: Θ(1 + log n / B) time; one copied node of at most M slots per
        level.
        """
        if not 0 <= i < self._size:
            raise IndexError("index out of range")
        off = self._tailoff()
        if i >= off:  # @line L4
            tail = list(self._tail)
            tail[i - off] = x
            return self._make(self._size, self._shift, self._root, tuple(tail))
        root = self._set_path(self._root, self._shift, i, x)  # @line L5
        return self._make(self._size, self._shift, root, self._tail)

    def _new_path(self, level: int, leaf: Node) -> Node:
        node = leaf
        while level > 0:
            node = (node,)
            level -= self._b
        return node

    def _push_tail(self, node: Node, level: int, i: int, leaf: Node) -> Node:
        j = (i >> level) & (self._m - 1)  # @line L13
        c = list(node)
        if level == self._b:  # @line L14
            child: Node = leaf
        elif j < len(node):  # @line L15
            child = self._push_tail(node[j], level - self._b, i, leaf)  # type: ignore[arg-type]
        else:  # @line L16
            child = self._new_path(level - self._b, leaf)
        if j < len(c):
            c[j] = child
        else:
            c.append(child)
        return tuple(c)

    def push(self, x: T) -> "PersistentVector[T]":
        """A vector with x added at the end.

        Cost: Θ(1) when the tail has room (one copy of the tail), else
        Θ(1 + log n / B); O(1) amortized over a run of pushes.
        """
        if self._size - self._tailoff() < self._m:  # @line L9
            return self._make(self._size + 1, self._shift, self._root, self._tail + (x,))
        shift = self._shift
        if (self._size >> self._b) > (1 << self._shift):  # @line L10
            root: Node = (self._root, self._new_path(self._shift, self._tail))
            shift += self._b
        else:  # @line L11
            root = self._push_tail(self._root, self._shift, self._size - 1, self._tail)
        return self._make(self._size + 1, shift, root, (x,))  # @line L12

    def _pop_tail(self, node: Node, level: int, i: int) -> Optional[Node]:
        j = (i >> level) & (self._m - 1)
        if level > self._b:  # @line L23
            c = self._pop_tail(node[j], level - self._b, i)  # type: ignore[arg-type]
            if c is None and j == 0:
                return None
            rest = list(node[:j])
            if c is not None:
                rest.append(c)
            return tuple(rest)
        if j == 0:  # @line L24
            return None
        return node[:j]  # @line L25

    def pop(self) -> "PersistentVector[T]":
        """A vector without its last item. Cost: Θ(1 + log n / B)."""
        if self._size == 0:
            raise IndexError("pop from empty vector")
        if self._size == 1:  # @line L17
            return self._make(0, self._b, (), ())
        if self._size - self._tailoff() > 1:  # @line L18
            return self._make(self._size - 1, self._shift, self._root, self._tail[:-1])
        new_tail = self._leaf_for(self._size - 2)  # @line L19
        root = self._pop_tail(self._root, self._shift, self._size - 2)  # @line L20
        if root is None:
            root = ()
        shift = self._shift
        if shift > self._b and len(root) == 1:  # @line L21
            root = root[0]  # type: ignore[assignment]
            shift -= self._b
        return self._make(self._size - 1, shift, root, new_tail)  # @line L22

    def __iter__(self) -> Iterator[T]:
        off = self._tailoff()
        i = 0
        while i < off:
            leaf = self._leaf_for(i)
            for x in leaf:
                yield x  # type: ignore[misc]
            i += self._m
        for x in self._tail:
            yield x  # type: ignore[misc]

    def to_list(self) -> "list[T]":
        """All items in order. Cost: Θ(n)."""
        return list(iter(self))

    def height(self) -> int:
        """Levels of the trie below the root (shift / B). Cost: O(1)."""
        return self._shift // self._b

    def check_invariant(self) -> None:
        """Check the layout: full leaves, left-packed inner nodes, tail size.

        The trie holds the first tailoff items in full leaves of M items,
        packed from the left, and the tail holds the rest (1 to M items
        when the vector is not empty). The root has room for the trie.
        Cost: Θ(n / M) nodes visited.
        """
        off = self._tailoff()
        assert len(self._tail) == self._size - off
        assert self._size == 0 or 1 <= len(self._tail) <= self._m
        assert off % self._m == 0
        leaves = off // self._m
        assert self._shift >= self._b and self._shift % self._b == 0
        assert leaves <= 1 << self._shift
        if self._shift > self._b:
            assert leaves > 1 << (self._shift - self._b)
        count = 0
        stack = [(self._root, self._shift)]
        while stack:
            node, level = stack.pop()
            assert len(node) <= self._m
            if level == 0:
                assert len(node) == self._m
                count += 1
                continue
            if node is not self._root:
                assert len(node) >= 1
            for child in node:
                stack.append((child, level - self._b))  # type: ignore[arg-type]
        assert count == leaves
