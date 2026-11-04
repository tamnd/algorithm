# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/str-packing/. The authors are listed in prov/4SAGYZ.jsonl.
"""Sort-Tile-Recursive (STR) bulk loading of an R-tree in the plane.

Rectangles are (xmin, ymin, xmax, ymax), closed. Leaf entries are
(rect, id); internal entries are (rect, Node). Every level is built by the
same tiling step, applied to the entries of the level below.
"""

from __future__ import annotations

import math
from typing import Hashable, List, Tuple

Rect = Tuple[float, float, float, float]


def union(a: Rect, b: Rect) -> Rect:
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


def intersects(a: Rect, b: Rect) -> bool:
    return a[0] <= b[2] and b[0] <= a[2] and a[1] <= b[3] and b[1] <= a[3]


class Node:
    __slots__ = ("leaf", "entries", "rect")

    def __init__(self, leaf: bool, entries: list) -> None:
        self.leaf = leaf
        self.entries = entries
        r = entries[0][0]
        for e in entries[1:]:
            r = union(r, e[0])
        self.rect: Rect = r


def _cx(e) -> float:
    return (e[0][0] + e[0][2]) / 2


def _cy(e) -> float:
    return (e[0][1] + e[0][3]) / 2


def tile(entries: list, M: int, leaf: bool) -> List[Node]:
    """One STR pass: group the entries into ceil(len / M) nodes."""
    P = math.ceil(len(entries) / M)  # @line L2
    S = math.ceil(math.sqrt(P))
    by_x = sorted(entries, key=_cx)  # @line L3
    nodes: List[Node] = []
    for s in range(0, len(by_x), S * M):  # @line L4
        slab = sorted(by_x[s:s + S * M], key=_cy)  # @line L5
        for t in range(0, len(slab), M):
            nodes.append(Node(leaf, slab[t:t + M]))
    return nodes


class STRTree:
    def __init__(self, items: List[Tuple[Hashable, Rect]], M: int = 4) -> None:
        if M < 2:
            raise ValueError("M must be at least 2")
        self.M = M
        self.n = len(items)
        self.levels: List[List[Node]] = []
        if not items:
            self.root = None
            return
        entries: list = [(r, oid) for oid, r in items]
        leaf = True
        while True:  # @line L1
            nodes = tile(entries, M, leaf)
            self.levels.append(nodes)
            if len(nodes) == 1:
                break
            entries = [(nd.rect, nd) for nd in nodes]  # @line L6
            leaf = False
        self.root = self.levels[-1][0]

    def height(self) -> int:
        return len(self.levels) - 1

    def search(self, q: Rect) -> List[Hashable]:
        out: List[Hashable] = []
        if self.root is None or not intersects(self.root.rect, q):
            return out
        stack = [self.root]
        while stack:
            nd = stack.pop()
            for r, x in nd.entries:  # @line L7
                if intersects(r, q):
                    if nd.leaf:
                        out.append(x)  # @line L8
                    else:
                        stack.append(x)  # @line L9
        return out

    def check_invariant(self) -> None:
        seen = []
        for lvl, nodes in enumerate(self.levels):
            for nd in nodes:
                assert 1 <= len(nd.entries) <= self.M
                assert nd.leaf == (lvl == 0)
                r = nd.entries[0][0]
                for e in nd.entries[1:]:
                    r = union(r, e[0])
                assert r == nd.rect
                if not nd.leaf:
                    for rr, c in nd.entries:
                        assert rr == c.rect
                else:
                    seen.extend(x for _, x in nd.entries)
        assert len(seen) == self.n
