# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/b-star-tree-floorplan/. The authors are listed in prov/WA1GJ6.jsonl.

"""The B*-tree of Chang, Chang, Wu and Wu (2000) for compacted packings.

The root is at the lower-left corner. The left child of a block b is placed
just to the right of b (x = x_b + w_b), and the right child of b is placed
above b with the same x (x = x_b). Each block is dropped onto the contour of
the blocks placed before it, in preorder. The contour is a linked list of
segments; each block keeps a pointer to its own segment, from which its
children start their walk, so a full packing takes amortized O(n) time.
"""

from typing import Optional

INF = float("inf")


class _Seg:
    """A piece [x0, x1) of the contour at height top."""

    __slots__ = ("x0", "x1", "top", "next")

    def __init__(self, x0: int, x1: float, top: int, nxt: Optional["_Seg"]) -> None:
        self.x0, self.x1, self.top, self.next = x0, x1, top, nxt


class BStarTree:
    """An ordered binary tree on the blocks: left[b] is to the right of b, right[b] is above b."""

    def __init__(self, root: Optional[int], left: dict[int, Optional[int]], right: dict[int, Optional[int]]) -> None:
        self.root = root
        self.left = dict(left)
        self.right = dict(right)

    def blocks(self) -> list[int]:
        """Return the blocks in preorder."""
        out = []
        stack = [self.root] if self.root is not None else []
        while stack:
            b = stack.pop()
            out.append(b)
            if self.right.get(b) is not None:
                stack.append(self.right[b])
            if self.left.get(b) is not None:
                stack.append(self.left[b])
        return out

    def check_invariant(self) -> None:
        """Raise AssertionError unless every block has one parent and the tree is connected."""
        seen = self.blocks()
        assert len(seen) == len(set(seen))
        kids = [c for d in (self.left, self.right) for c in d.values() if c is not None]
        assert len(kids) == len(set(kids)) and self.root not in kids
        assert set(seen) == set(kids) | ({self.root} if self.root is not None else set())

    def pack(self, w: dict[int, int], h: dict[int, int]) -> tuple[int, int, dict[int, tuple[int, int]]]:
        """Return (W, H, pos) of the packing, with the contour. Amortized O(n) time."""
        head = _Seg(0, INF, 0, None)  # @line L1
        seg: dict[int, _Seg] = {}
        pos: dict[int, tuple[int, int]] = {}
        width = height = 0
        if self.root is None:
            return 0, 0, pos
        stack: list[tuple[int, _Seg]] = [(self.root, head)]  # @line L2
        while stack:  # @line L3
            b, start = stack.pop()
            x = start.x0  # @line L4
            end = x + w[b]
            y = 0  # @line L5
            s: Optional[_Seg] = start
            last = start
            while s is not None and s.x0 < end:
                if s.top > y:
                    y = s.top
                last = s
                s = s.next
            rest = _Seg(end, last.x1, last.top, last.next) if last.x1 > end else last.next  # @line L6
            start.x1, start.top, start.next = end, y + h[b], rest
            seg[b] = start
            pos[b] = (x, y)  # @line L7
            width, height = max(width, end), max(height, y + h[b])
            if self.right.get(b) is not None:  # @line L8
                stack.append((self.right[b], start))
            if self.left.get(b) is not None:  # @line L9
                stack.append((self.left[b], start.next))
        return width, height, pos  # @line L10

    def pack_naive(self, w: dict[int, int], h: dict[int, int]) -> tuple[int, int, dict[int, tuple[int, int]]]:
        """The same packing without a contour: each y is the highest top over the x-range. O(n^2)."""
        pos: dict[int, tuple[int, int]] = {}
        if self.root is None:
            return 0, 0, pos
        xs = {self.root: 0}
        for b in self.blocks():
            x = xs[b]
            y = 0
            for a, (xa, ya) in pos.items():
                if xa < x + w[b] and x < xa + w[a]:
                    y = max(y, ya + h[a])
            pos[b] = (x, y)
            if self.left.get(b) is not None:
                xs[self.left[b]] = x + w[b]
            if self.right.get(b) is not None:
                xs[self.right[b]] = x
        return max(x + w[b] for b, (x, _) in pos.items()), max(y + h[b] for b, (_, y) in pos.items()), pos

    def swap(self, a: int, b: int) -> None:
        """Exchange the places of blocks a and b in the tree.

        This version renames the keys of the two maps, in O(n) time. With parent
        pointers in the nodes the same swap takes O(1) time.
        """
        ren = {a: b, b: a}
        f = lambda v: ren.get(v, v) if v is not None else None  # noqa: E731
        self.root = f(self.root)
        self.left = {f(k): f(v) for k, v in self.left.items()}
        self.right = {f(k): f(v) for k, v in self.right.items()}

    def _parent(self, b: int) -> tuple[Optional[int], Optional[str]]:
        for side, d in (("left", self.left), ("right", self.right)):
            for k, v in d.items():
                if v == b:
                    return k, side
        return None, None

    def delete(self, b: int) -> None:
        """Remove block b. A node with two children is first swapped down along left children."""
        while self.left.get(b) is not None and self.right.get(b) is not None:
            self.swap(b, self.left[b])
        child = self.left.get(b) if self.left.get(b) is not None else self.right.get(b)
        p, side = self._parent(b)
        if p is None:
            self.root = child
        else:
            (self.left if side == "left" else self.right)[p] = child
        self.left.pop(b, None)
        self.right.pop(b, None)

    def insert(self, b: int, p: Optional[int], side: str) -> None:
        """Make b the child of p on the given side; the old child moves under b on the same side."""
        self.left[b] = None
        self.right[b] = None
        if p is None:
            old, self.root = self.root, b
            self.left[b] = old
            return
        d = self.left if side == "left" else self.right
        old = d.get(p)
        d[p] = b
        (self.left if side == "left" else self.right)[b] = old
