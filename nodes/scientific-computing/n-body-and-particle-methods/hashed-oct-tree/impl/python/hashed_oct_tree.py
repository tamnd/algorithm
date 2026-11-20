# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hashed-oct-tree/. The authors are listed in prov/4795RQ.jsonl.
"""Hashed oct-tree: an octree whose cells live in a hash table keyed by Morton keys.

A cell at level l (the root is level 0) with integer coordinates (i, j, k),
0 <= i, j, k < 2^l, has the key 1 followed by the l octal digits of the
interleaved bits of (i, j, k). So the root key is 1, the children of key k are
8k + c for c = 0..7, the parent is k >> 3, and the level is
(bit_length(k) - 1) / 3. Bodies get keys at the deepest level L, the bodies
are sorted by key, and each cell owns a contiguous range of the sorted bodies.
The table maps a key to its cell (a Python dict is the hash table).
"""

from typing import Sequence

Vec = Sequence[float]


def interleave(i: int, j: int, k: int, level: int) -> int:
    """Key of the cell (i, j, k) at the given level, with the leading 1 bit."""
    key = 1  # @line L2
    for b in range(level - 1, -1, -1):  # @line L3
        key = (key << 3) | (((k >> b) & 1) << 2) | (((j >> b) & 1) << 1) | ((i >> b) & 1)
    return key  # @line L4


def deinterleave(key: int) -> tuple[int, int, int, int]:
    """Inverse of interleave: return (level, i, j, k)."""
    level = (key.bit_length() - 1) // 3
    i = j = k = 0
    for b in range(level):
        digit = (key >> (3 * b)) & 7
        i |= (digit & 1) << b
        j |= ((digit >> 1) & 1) << b
        k |= ((digit >> 2) & 1) << b
    return level, i, j, k


def parent(key: int) -> int:
    return key >> 3  # @line L10


def child(key: int, c: int) -> int:
    return (key << 3) | c


def level_of(key: int) -> int:
    return (key.bit_length() - 1) // 3


class HashedOctTree:
    def __init__(self, x: Sequence[Vec], leaf_size: int = 1, depth: int = 21) -> None:
        if not x:
            raise ValueError("no bodies")
        self.depth = depth
        self.leaf_size = leaf_size
        self.lo = [min(p[d] for p in x) for d in range(3)]
        side = max(max(p[d] for p in x) - self.lo[d] for d in range(3)) or 1.0
        self.side = side * (1 + 1e-9)
        keys = [self.body_key(p) for p in x]
        self.order = sorted(range(len(x)), key=lambda n: keys[n])  # @line L5
        self.keys = [keys[n] for n in self.order]
        self.table: dict[int, tuple[int, int]] = {}  # key -> (start, end) in self.order
        stack = [(1, 0, len(x))]  # @line L6
        while stack:
            key, start, end = stack.pop()
            self.table[key] = (start, end)  # @line L7
            lev = level_of(key)
            if end - start > leaf_size and lev < depth:  # @line L8
                shift = 3 * (depth - lev - 1)
                s = start
                while s < end:
                    c = (self.keys[s] >> shift) & 7
                    e = s
                    while e < end and (self.keys[e] >> shift) & 7 == c:
                        e += 1
                    stack.append((child(key, c), s, e))
                    s = e

    def body_key(self, p: Vec) -> int:
        n = 1 << self.depth
        q = [min(n - 1, int((p[d] - self.lo[d]) / self.side * n)) for d in range(3)]  # @line L1
        return interleave(q[0], q[1], q[2], self.depth)

    def lookup(self, key: int) -> list[int]:
        """Indices of the bodies in the cell with this key; KeyError if the cell does not exist."""
        start, end = self.table[key]  # @line L9
        return self.order[start:end]

    def children(self, key: int) -> list[int]:
        return [child(key, c) for c in range(8) if child(key, c) in self.table]

    def is_leaf(self, key: int) -> bool:
        return not self.children(key)

    def bounds(self, key: int) -> tuple[list[float], float]:
        """Lower corner and side of the cube of a key."""
        lev, i, j, k = deinterleave(key)
        s = self.side / (1 << lev)
        return [self.lo[0] + i * s, self.lo[1] + j * s, self.lo[2] + k * s], s

    def leaf_of(self, p: Vec) -> int:
        """Key of the deepest cell of the tree whose cube holds the point p."""
        bk = self.body_key(p)
        key = 1
        for lev in range(1, self.depth + 1):
            nxt = bk >> (3 * (self.depth - lev))
            if nxt not in self.table:
                break
            key = nxt
        return key
