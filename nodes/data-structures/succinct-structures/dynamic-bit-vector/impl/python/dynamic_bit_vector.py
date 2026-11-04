# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-bit-vector/. The authors are listed in prov/ZZJ07J.jsonl.
"""Dynamic bit vector: rank, select, insert and delete in O(log n) expected time.

The bits are cut into chunks of at most 2B bits. The chunks, in order,
are the nodes of an implicit treap; each node also stores the number of
bits and of 1s in its subtree. A query walks down from the root and
finishes inside one chunk; an update changes one chunk, fixes the counts
on the path, and splits a chunk that grows past 2B bits.
"""

from __future__ import annotations

import random
from typing import Optional


class _Node:
    __slots__ = ("chunk", "pri", "left", "right", "size", "ones")

    def __init__(self, chunk: list[int], pri: float) -> None:
        self.chunk = chunk
        self.pri = pri
        self.left: Optional[_Node] = None
        self.right: Optional[_Node] = None
        self.size = len(chunk)
        self.ones = sum(chunk)


def _size(t: Optional[_Node]) -> int:
    return t.size if t else 0


def _ones(t: Optional[_Node]) -> int:
    return t.ones if t else 0


def _chunk_ones(t: _Node) -> int:
    """Number of 1s in the node's own chunk."""
    return t.ones - _ones(t.left) - _ones(t.right)


def _pull(t: _Node) -> None:
    t.size = _size(t.left) + len(t.chunk) + _size(t.right)
    t.ones = _ones(t.left) + sum(t.chunk) + _ones(t.right)


def _split(t: Optional[_Node], k: int) -> tuple[Optional[_Node], Optional[_Node]]:
    """Split at bit k, which must be a chunk boundary: left has bits [0, k)."""
    if t is None:
        return None, None
    ls = _size(t.left)
    if k <= ls:
        a, b = _split(t.left, k)
        t.left = b
        _pull(t)
        return a, t
    a, b = _split(t.right, k - ls - len(t.chunk))
    t.right = a
    _pull(t)
    return t, b


def _merge(a: Optional[_Node], b: Optional[_Node]) -> Optional[_Node]:
    if a is None:
        return b
    if b is None:
        return a
    if a.pri > b.pri:
        a.right = _merge(a.right, b)
        _pull(a)
        return a
    b.left = _merge(a, b.left)
    _pull(b)
    return b


def _pop_leftmost(t: _Node) -> Optional[_Node]:
    if t.left is None:
        return t.right
    t.left = _pop_leftmost(t.left)
    _pull(t)
    return t


class DynamicBitVector:
    """A bit vector with access, rank, select, insert, delete and set."""

    def __init__(self, bits: Optional[list[int]] = None, block: int = 64, seed: int = 0) -> None:
        """Build from ``bits``; chunks hold between 1 and 2 * ``block`` bits."""
        self.B = block
        self.rng = random.Random(seed)
        self.root: Optional[_Node] = None
        bits = list(bits or [])
        for s in range(0, len(bits), block):
            self.root = _merge(self.root, _Node(bits[s:s + block], self.rng.random()))

    def __len__(self) -> int:
        return _size(self.root)

    def to_list(self) -> list[int]:
        """All bits, in order."""
        out: list[int] = []

        def walk(t: Optional[_Node]) -> None:
            if t:
                walk(t.left)
                out.extend(t.chunk)
                walk(t.right)

        walk(self.root)
        return out

    def _find(self, i: int) -> tuple[list[_Node], int, int]:
        """Path to the node holding bit i (or the last node if i = n), offset, start."""
        path: list[_Node] = []
        x, start = self.root, 0
        while x is not None:
            path.append(x)
            ls = _size(x.left)
            if i < ls:
                x = x.left
            elif i < ls + len(x.chunk) or (x.right is None and i == ls + len(x.chunk)):
                return path, i - ls, start + ls
            else:
                i -= ls + len(x.chunk)
                start += ls + len(x.chunk)
                x = x.right
        raise IndexError("position out of range")

    def access(self, i: int) -> int:
        """The bit at position i."""
        if not 0 <= i < len(self):
            raise IndexError("position out of range")
        path, off, _ = self._find(i)
        return path[-1].chunk[off]

    def rank1(self, i: int) -> int:
        """Number of 1s in positions 0..i-1, for 0 <= i <= n."""
        x, r = self.root, 0  # @line L1
        while x is not None:  # @line L2
            ls = _size(x.left)
            if i < ls:  # @line L3
                x = x.left
            elif i <= ls + len(x.chunk):  # @line L4
                return r + _ones(x.left) + sum(x.chunk[: i - ls])
            else:  # @line L5
                r += _ones(x.left) + _chunk_ones(x)
                i -= ls + len(x.chunk)
                x = x.right
        return r  # @line L6

    def rank0(self, i: int) -> int:
        """Number of 0s in positions 0..i-1."""
        return i - self.rank1(i)

    def select1(self, j: int) -> int:
        """Position of the j-th 1, for 1 <= j <= rank1(n)."""
        if not 1 <= j <= _ones(self.root):
            raise IndexError("no such 1")
        x, base = self.root, 0  # @line L7
        while x is not None:  # @line L8
            lo, ls = _ones(x.left), _size(x.left)
            co = _chunk_ones(x)
            if j <= lo:  # @line L9
                x = x.left
            elif j <= lo + co:  # @line L10
                j -= lo
                for k, b in enumerate(x.chunk):
                    j -= b
                    if j == 0:
                        return base + ls + k
            else:  # @line L11
                j -= lo + co
                base += ls + len(x.chunk)
                x = x.right
        raise AssertionError("unreachable")

    def select0(self, j: int) -> int:
        """Position of the j-th 0, by binary search over rank0."""
        if not 1 <= j <= len(self) - _ones(self.root):
            raise IndexError("no such 0")
        lo, hi = 0, len(self) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if self.rank0(mid + 1) >= j:
                hi = mid
            else:
                lo = mid + 1
        return lo

    def insert(self, i: int, b: int) -> None:
        """Insert bit b before position i, for 0 <= i <= n."""
        if not 0 <= i <= len(self):
            raise IndexError("position out of range")
        if self.root is None:
            self.root = _Node([b], self.rng.random())
            return
        path, off, start = self._find(i)  # @line L12
        x = path[-1]
        x.chunk.insert(off, b)  # @line L13
        for y in reversed(path):  # @line L14
            _pull(y)
        if len(x.chunk) > 2 * self.B:  # @line L15
            half = len(x.chunk) // 2
            new = _Node(x.chunk[half:], self.rng.random())
            x.chunk = x.chunk[:half]
            for y in reversed(path):
                _pull(y)
            left, right = _split(self.root, start + half)
            self.root = _merge(_merge(left, new), right)

    def delete(self, i: int) -> int:
        """Remove and return the bit at position i."""
        if not 0 <= i < len(self):
            raise IndexError("position out of range")
        path, off, start = self._find(i)  # @line L16
        x = path[-1]
        b = x.chunk.pop(off)  # @line L17
        for y in reversed(path):  # @line L18
            _pull(y)
        if not x.chunk:  # @line L19
            left, right = _split(self.root, start)
            assert right is not None
            self.root = _merge(left, _pop_leftmost(right))
        return b

    def set(self, i: int, b: int) -> None:
        """Overwrite the bit at position i with b."""
        if not 0 <= i < len(self):
            raise IndexError("position out of range")
        path, off, _ = self._find(i)
        path[-1].chunk[off] = b
        for y in reversed(path):
            _pull(y)
