# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/o-tree-floorplan/. The authors are listed in prov/GM5XEG.jsonl.

"""The horizontal O-tree of Guo, Cheng and Yoshimura (1999).

An O-tree on n blocks is an ordered tree with n + 1 nodes. The root is a
virtual block of width 0 at x = 0, the left wall. A child c of a node p has
x_c = x_p + w_p. The tree is stored as a 2n-bit string T, written in a
depth-first walk (0: go down to a new child, 1: go back up), and a list perm
of the blocks in the order the walk meets them. The blocks are placed in that
order, and each block drops onto the contour of the blocks before it, so the
packing takes O(n) time.
"""

from typing import Optional

INF = float("inf")


class _Seg:
    """A piece [x0, x1) of the contour at height top."""

    __slots__ = ("x0", "x1", "top", "next")

    def __init__(self, x0: int, x1: float, top: int, nxt: Optional["_Seg"]) -> None:
        self.x0, self.x1, self.top, self.next = x0, x1, top, nxt


def is_tree_string(bits: str) -> bool:
    """True if bits is a walk of an ordered tree: every prefix has at least as many 0 as 1, and the counts are equal."""
    depth = 0
    for c in bits:
        if c == "0":
            depth += 1
        elif c == "1":
            depth -= 1
            if depth < 0:
                return False
        else:
            return False
    return depth == 0


class OTree:
    """An O-tree given by its bit string and its permutation."""

    def __init__(self, bits: str, perm: list[int]) -> None:
        """Raise ValueError unless bits is a tree string with one 0 for each block of perm."""
        if not is_tree_string(bits) or bits.count("0") != len(perm) or len(set(perm)) != len(perm):
            raise ValueError("not an O-tree")
        self.bits = bits
        self.perm = list(perm)

    def parents(self) -> dict[int, Optional[int]]:
        """Return the parent of each block; None is the virtual root. O(n)."""
        par: dict[int, Optional[int]] = {}
        stack: list[Optional[int]] = [None]
        k = 0
        for c in self.bits:
            if c == "0":
                b = self.perm[k]
                k += 1
                par[b] = stack[-1]
                stack.append(b)
            else:
                stack.pop()
        return par

    def pack(self, w: dict[int, int], h: dict[int, int]) -> tuple[int, int, dict[int, tuple[int, int]]]:
        """Return (W, H, pos) of the packing, with the contour. O(n) time."""
        head = _Seg(0, INF, 0, None)  # @line L1
        pos: dict[int, tuple[int, int]] = {}
        width = height = 0
        # each stack entry is [block, the contour segment where its next child starts]
        stack: list[list] = [[None, head]]  # @line L2
        k = 0
        for c in self.bits:  # @line L3
            if c == "1":
                stack.pop()  # @line L4
                continue
            b = self.perm[k]  # @line L5
            k += 1
            entry = stack[-1]
            start = entry[1]
            x = start.x0  # @line L6
            end = x + w[b]
            y = 0
            s: Optional[_Seg] = start
            last = start
            while s is not None and s.x0 < end:  # @line L7
                if s.top > y:
                    y = s.top
                last = s
                s = s.next
            rest = _Seg(end, last.x1, last.top, last.next) if last.x1 > end else last.next  # @line L8
            start.x1, start.top, start.next = end, y + h[b], rest
            pos[b] = (x, y)
            width, height = max(width, end), max(height, y + h[b])
            entry[1] = start  # the next sibling of b starts where b starts  # @line L9
            stack.append([b, start.next])
        return width, height, pos  # @line L10

    def pack_naive(self, w: dict[int, int], h: dict[int, int]) -> tuple[int, int, dict[int, tuple[int, int]]]:
        """The same packing without a contour: each y is the highest top over the x-range. O(n^2)."""
        par = self.parents()
        pos: dict[int, tuple[int, int]] = {}
        for b in self.perm:
            p = par[b]
            x = 0 if p is None else pos[p][0] + w[p]
            y = 0
            for a, (xa, ya) in pos.items():
                if xa < x + w[b] and x < xa + w[a]:
                    y = max(y, ya + h[a])
            pos[b] = (x, y)
        if not pos:
            return 0, 0, pos
        return max(x + w[b] for b, (x, _) in pos.items()), max(y + h[b] for b, (_, y) in pos.items()), pos

    def to_b_star(self) -> tuple[Optional[int], dict[int, Optional[int]], dict[int, Optional[int]]]:
        """Return (root, left, right) of the left-child right-sibling form: a B*-tree. O(n)."""
        left: dict[int, Optional[int]] = {b: None for b in self.perm}
        right: dict[int, Optional[int]] = {b: None for b in self.perm}
        first_child: Optional[int] = None
        # last[i] is the last child seen so far of the node at depth i of the stack
        stack: list[Optional[int]] = [None]
        last: list[Optional[int]] = [None]
        k = 0
        for c in self.bits:
            if c == "1":
                stack.pop()
                last.pop()
                continue
            b = self.perm[k]
            k += 1
            p, prev = stack[-1], last[-1]
            if prev is not None:
                right[prev] = b
            elif p is not None:
                left[p] = b
            else:
                first_child = b
            last[-1] = b
            stack.append(b)
            last.append(None)
        return first_child, left, right

    @staticmethod
    def from_b_star(root: Optional[int], left: dict, right: dict) -> "OTree":
        """The inverse of to_b_star: the O-tree whose left-child right-sibling form is the given tree. O(n)."""
        bits: list[str] = []
        perm: list[int] = []

        # the children of a node are its left child and then the chain of right children
        def walk(first: Optional[int]) -> None:
            stack = [(first, 0)]
            while stack:
                b, state = stack.pop()
                if b is None:
                    continue
                if state == 0:
                    bits.append("0")
                    perm.append(b)
                    stack.append((b, 1))
                    stack.append((left.get(b), 0))
                else:
                    bits.append("1")
                    stack.append((right.get(b), 0))

        walk(root)
        return OTree("".join(bits), perm)
