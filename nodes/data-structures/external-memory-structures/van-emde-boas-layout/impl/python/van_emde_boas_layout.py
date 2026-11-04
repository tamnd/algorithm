# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/van-emde-boas-layout/. The authors are listed in prov/VCF4TV.jsonl.

from typing import Any, Generic, Optional, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)


def veb_pos(h: int, d: int, p: int) -> int:
    """Position, in the van Emde Boas layout of a complete binary tree with
    h levels, of the node at depth d (the root has depth 0) whose path from
    the root is given by the d bits of p, most significant first, with 0 for
    left and 1 for right. The top tree has h // 2 levels."""
    if h == 1:  # @line L1
        return 0
    ht = h // 2  # @line L2
    hb = h - ht
    if d < ht:  # @line L3
        return veb_pos(ht, d, p)  # the top tree holds the same path
    j = p >> (d - ht)  # @line L4
    rest = p & ((1 << (d - ht)) - 1)
    return (1 << ht) - 1 + j * ((1 << hb) - 1) + veb_pos(hb, d - ht, rest)  # @line L5


class VEBLayout(Generic[K]):
    """A static search tree on sorted distinct keys, stored as a complete
    binary search tree in the van Emde Boas layout.

    The tree has h levels and 2**h - 1 slots; the slots after the N keys hold
    None, which acts as plus infinity. A search follows one root-to-leaf
    path and touches O(log_B N) blocks of B slots, for every B, without
    knowing B.
    """

    def __init__(self, keys: list[K]) -> None:
        if any(not (a < b) for a, b in zip(keys, keys[1:])):
            raise ValueError("keys must be sorted and distinct")
        n = len(keys)
        h = 1
        while (1 << h) - 1 < n:  # @line L6
            h += 1
        self.h = h
        self.n = n
        size = (1 << h) - 1
        padded: list[Optional[K]] = list(keys) + [None] * (size - n)
        self.slots: list[Optional[K]] = [None] * size
        for d in range(h):  # @line L7
            span = 1 << (h - d)
            for x in range(1 << d):
                rank = x * span + span // 2 - 1  # in-order rank of the node
                self.slots[veb_pos(h, d, x)] = padded[rank]

    def __len__(self) -> int:
        return self.n

    def _less(self, x: Optional[K], k: K) -> bool:
        return x is not None and x < k

    def path(self, k: K) -> list[int]:
        """The slots read by a search for k, from the root down."""
        out: list[int] = []
        d, p = 0, 0
        while d < self.h:
            i = veb_pos(self.h, d, p)
            out.append(i)
            x = self.slots[i]
            if x is not None and not (x < k) and not (k < x):
                break
            p = 2 * p + (1 if self._less(x, k) else 0)
            d += 1
        return out

    def predecessor(self, k: K) -> Optional[K]:
        """The largest key <= k, or None."""
        d, p = 0, 0  # @line L8
        best: Optional[K] = None
        while d < self.h:  # @line L9
            x = self.slots[veb_pos(self.h, d, p)]  # @line L10
            if x is not None and not (x < k) and not (k < x):  # @line L11
                return x
            if self._less(x, k):  # @line L12
                best = x
                p = 2 * p + 1
            else:
                p = 2 * p
            d += 1  # @line L13
        return best  # @line L14

    def __contains__(self, k: K) -> bool:
        x = self.predecessor(k)
        return x is not None and not (x < k)

    def blocks_touched(self, k: K, block_size: int, offset: int = 0) -> int:
        """The number of distinct blocks of block_size slots met by the
        search for k, when slot 0 is at position offset of its block."""
        return len({(offset + i) // block_size for i in self.path(k)})

    def inorder(self) -> list[K]:
        """The keys in in-order, read through the layout."""
        out: list[K] = []

        def walk(d: int, p: int) -> None:
            if d == self.h:
                return
            walk(d + 1, 2 * p)
            x = self.slots[veb_pos(self.h, d, p)]
            if x is not None:
                out.append(x)
            walk(d + 1, 2 * p + 1)

        walk(0, 0)
        return out

    def check_invariant(self) -> None:
        """Raise AssertionError if the layout is not a valid search tree."""
        size = (1 << self.h) - 1
        assert len(self.slots) == size and (self.n == 0 or (size - 1) // 2 < self.n <= size)
        positions = sorted(veb_pos(self.h, d, x) for d in range(self.h) for x in range(1 << d))
        assert positions == list(range(size))
        keys = self.inorder()
        assert len(keys) == self.n
        assert all(a < b for a, b in zip(keys, keys[1:]))
