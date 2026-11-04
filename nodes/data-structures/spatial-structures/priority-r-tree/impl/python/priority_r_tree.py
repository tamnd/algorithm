# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/priority-r-tree/. The authors are listed in prov/8PZPPQ.jsonl.
"""The priority R-tree (PR-tree) of Arge, de Berg, Haverkort and Yi, in the plane.

A rectangle (xmin, ymin, xmax, ymax) is seen as a point of four
dimensions. A pseudo-PR-tree on a set of rectangles takes out four
priority leaves of B rectangles each: the B with the smallest xmin, then
of the rest the B with the smallest ymin, the B with the largest xmax and
the B with the largest ymax. The rest is split at the median of one of
the four coordinates, in turn, as in a four-dimensional k-d tree. The
PR-tree is built bottom up: its leaves are the leaves of a pseudo-PR-tree
on the data; the nodes of each next level are the leaves of a
pseudo-PR-tree on the bounding boxes of the level below; this goes on
until one node is left. The result is a static R-tree whose nodes hold at
most B entries and whose leaves are all at one depth.
"""

from __future__ import annotations

from typing import Hashable, List, Sequence, Tuple

Rect = Tuple[float, float, float, float]
# sort keys for the four priority leaves: smallest xmin, smallest ymin,
# largest xmax, largest ymax
KEYS = (lambda r: r[0], lambda r: r[1], lambda r: -r[2], lambda r: -r[3])


def intersects(a: Rect, b: Rect) -> bool:
    return a[0] <= b[2] and b[0] <= a[2] and a[1] <= b[3] and b[1] <= a[3]


def mbr(rects: Sequence[Rect]) -> Rect:
    return (min(r[0] for r in rects), min(r[1] for r in rects),
            max(r[2] for r in rects), max(r[3] for r in rects))


def pseudo_pr_leaves(items: List[Tuple[Rect, object]], B: int, depth: int = 0) -> List[List[Tuple[Rect, object]]]:
    """The leaves of a pseudo-PR-tree on items (rect, payload), each a list of
    at most B items, in the order of the tree."""
    if len(items) <= B:  # @line L1
        return [items] if items else []
    rest = items
    out = []
    for key in KEYS:  # @line L2
        if not rest:
            break
        rest = sorted(rest, key=lambda it: (key(it[0]), it[0]))
        out.append(rest[:B])  # @line L3
        rest = rest[B:]
    if rest:
        axis = depth % 4  # @line L4
        rest = sorted(rest, key=lambda it: (it[0][axis], it[0]))
        h = len(rest) // 2
        out += pseudo_pr_leaves(rest[:h], B, depth + 1)  # @line L5
        out += pseudo_pr_leaves(rest[h:], B, depth + 1)
    return out


class Node:
    __slots__ = ("leaf", "entries")

    def __init__(self, leaf: bool, entries: list) -> None:
        self.leaf = leaf
        self.entries = entries  # list of (rect, id) or (rect, Node)

    def rect(self) -> Rect:
        return mbr([r for r, _ in self.entries])


class PRTree:
    def __init__(self, data: Sequence[Tuple[Hashable, Rect]], B: int = 4) -> None:
        if B < 2:
            raise ValueError("B must be at least 2")
        for _, r in data:
            if r[0] > r[2] or r[1] > r[3]:
                raise ValueError("empty rectangle")
        self.B = B
        self.n = len(data)
        level = [Node(True, grp) for grp in
                 pseudo_pr_leaves([(tuple(r), oid) for oid, r in data], B)]  # @line L6
        self.levels = 1
        while len(level) > 1:  # @line L7
            items = [(u.rect(), u) for u in level]
            level = [Node(False, grp) for grp in pseudo_pr_leaves(items, B)]  # @line L8
            self.levels += 1
        self.root = level[0] if level else None

    def search(self, q: Rect) -> List[Hashable]:
        out: List[Hashable] = []
        if self.root is None:
            return out
        stack = [self.root]
        self.visited = 0
        while stack:
            u = stack.pop()
            self.visited += 1
            for r, x in u.entries:  # @line L9
                if intersects(r, q):  # @line L10
                    if u.leaf:
                        out.append(x)
                    else:
                        stack.append(x)  # @line L11
        return out

    def height(self) -> int:
        return self.levels - 1 if self.root is not None else -1

    def check_invariant(self) -> None:
        if self.root is None:
            assert self.n == 0
            return
        seen = []
        depths = set()
        stack = [(self.root, 0)]
        while stack:
            u, d = stack.pop()
            assert 1 <= len(u.entries) <= self.B
            if u.leaf:
                depths.add(d)
                seen += [x for _, x in u.entries]
            else:
                for r, ch in u.entries:
                    assert r == ch.rect()
                    stack.append((ch, d + 1))
        assert depths == {self.levels - 1}
        assert len(seen) == self.n
