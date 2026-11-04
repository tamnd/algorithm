# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/x-tree/. The authors are listed in prov/19MBBA.jsonl.
"""X-tree of Berchtold, Keim and Kriegel (1996), in d dimensions.

A rectangle is a pair (lo, hi) of d-tuples, closed on both sides; a point
is a rectangle with lo == hi. A leaf holds (rect, id) entries and has room
for M of them. A directory node holds child nodes and has room for
blocks * M of them; a node with blocks > 1 is a supernode. Every node keeps
its split history: the set of axes along which it, or a node it came from
by splits, was split.

When a directory node overflows, the tree tries the topological (R*-style)
split; if the two halves overlap by more than MAX_OVERLAP of the volume of
their union, it tries the overlap-minimal split along an axis in the split
history of every child; if that split is unbalanced or still overlaps too
much, the node becomes a supernode with one more block.
"""

from __future__ import annotations

import heapq
import math
from typing import FrozenSet, Hashable, List, Optional, Sequence, Tuple

Vec = Tuple[float, ...]
Rect = Tuple[Vec, Vec]

MAX_OVERLAP = 0.2
MIN_FANOUT = 0.35
TOPO_FILL = 0.4


def volume(r: Rect) -> float:
    v = 1.0
    for a, b in zip(r[0], r[1]):
        v *= b - a
    return v


def margin(r: Rect) -> float:
    return sum(b - a for a, b in zip(r[0], r[1]))


def union(r: Rect, s: Rect) -> Rect:
    return (tuple(map(min, r[0], s[0])), tuple(map(max, r[1], s[1])))


def intersects(r: Rect, s: Rect) -> bool:
    return all(a <= d and c <= b for a, b, c, d in zip(r[0], r[1], s[0], s[1]))


def inter_volume(r: Rect, s: Rect) -> float:
    v = 1.0
    for a, b, c, d in zip(r[0], r[1], s[0], s[1]):
        w = min(b, d) - max(a, c)
        if w <= 0:
            return 0.0
        v *= w
    return v


def overlap_ratio(r: Rect, s: Rect) -> float:
    """Volume of r and s together over the volume of their union, in [0, 1]."""
    i = inter_volume(r, s)
    u = volume(r) + volume(s) - i
    return i / u if u > 0 else 0.0


def mbr(rects: Sequence[Rect]) -> Rect:
    r = rects[0]
    for s in rects[1:]:
        r = union(r, s)
    return r


def mindist(q: Vec, r: Rect) -> float:
    s = 0.0
    for x, a, b in zip(q, r[0], r[1]):
        t = a - x if x < a else (x - b if x > b else 0.0)
        s += t * t
    return math.sqrt(s)


class Node:
    __slots__ = ("leaf", "entries", "parent", "rect", "hist", "blocks")

    def __init__(self, leaf: bool, hist: FrozenSet[int] = frozenset()) -> None:
        self.leaf = leaf
        self.entries: list = []
        self.parent: Optional[Node] = None
        self.rect: Optional[Rect] = None
        self.hist = hist
        self.blocks = 1

    def entry_rect(self, e) -> Rect:
        return e[0] if self.leaf else e.rect

    def refresh(self) -> None:
        self.rect = mbr([self.entry_rect(e) for e in self.entries])


def _groups_rect(node: Node, g: list) -> Rect:
    return mbr([node.entry_rect(e) for e in g])


def topological_split(node: Node, g: int) -> Tuple[int, list, list]:
    """R*-style split: axis by least margin sum, then cut by least overlap, then volume."""
    d = len(node.rect[0])
    n = len(node.entries)
    best = None
    for axis in range(d):  # @line L7
        s = 0.0
        for side in (0, 1):
            es = sorted(node.entries, key=lambda e: (node.entry_rect(e)[side][axis],
                                                     node.entry_rect(e)[1 - side][axis]))
            for k in range(g, n - g + 1):
                s += margin(_groups_rect(node, es[:k])) + margin(_groups_rect(node, es[k:]))
        if best is None or s < best[0]:
            best = (s, axis)
    axis = best[1]
    choice = None
    for side in (0, 1):
        es = sorted(node.entries, key=lambda e: (node.entry_rect(e)[side][axis],
                                                 node.entry_rect(e)[1 - side][axis]))
        for k in range(g, n - g + 1):
            r1, r2 = _groups_rect(node, es[:k]), _groups_rect(node, es[k:])
            key = (inter_volume(r1, r2), volume(r1) + volume(r2))
            if choice is None or key < choice[0]:
                choice = (key, es[:k], es[k:])
    return axis, choice[1], choice[2]


def overlap_minimal_split(node: Node, g: int) -> Optional[Tuple[int, list, list]]:
    """Split along an axis in the history of every child, at the cut of least overlap."""
    common = frozenset.intersection(*[c.hist for c in node.entries])  # @line L9
    n = len(node.entries)
    choice = None
    for axis in sorted(common):
        es = sorted(node.entries, key=lambda c: (c.rect[0][axis], c.rect[1][axis]))
        for k in range(g, n - g + 1):  # @line L10
            r1, r2 = _groups_rect(node, es[:k]), _groups_rect(node, es[k:])
            key = (overlap_ratio(r1, r2), abs(n - 2 * k))
            if choice is None or key < choice[0]:
                choice = (key, axis, es[:k], es[k:])
    if choice is None or choice[0][0] > MAX_OVERLAP:
        return None
    return choice[1], choice[2], choice[3]


class XTree:
    def __init__(self, max_entries: int = 4, min_entries: Optional[int] = None) -> None:
        if max_entries < 2:
            raise ValueError("max_entries must be at least 2")
        self.M = max_entries
        self.m = min_entries if min_entries is not None else max(1, int(MIN_FANOUT * max_entries))
        if not 1 <= self.m <= self.M // 2:
            raise ValueError("min_entries must be in [1, M/2]")
        self.root = Node(True)
        self.n = 0

    # ---- shape ----
    def height(self) -> int:
        h, u = 0, self.root
        while not u.leaf:
            h += 1
            u = u.entries[0]
        return h

    def capacity(self, u: Node) -> int:
        return self.M * u.blocks

    def supernodes(self) -> List[Node]:
        out, stack = [], [self.root]
        while stack:
            u = stack.pop()
            if not u.leaf:
                if u.blocks > 1:
                    out.append(u)
                stack.extend(u.entries)
        return out

    def _node_height(self, u: Node) -> int:
        h = 0
        while not u.leaf:
            h += 1
            u = u.entries[0]
        return h

    # ---- insertion ----
    def _choose(self, rect: Rect, level: int) -> Node:
        u, h = self.root, self.height()
        while h > level:  # @line L1
            kids = u.entries
            if h == 1:
                def key(c):
                    grown = union(c.rect, rect)
                    before = sum(inter_volume(c.rect, o.rect) for o in kids if o is not c)
                    after = sum(inter_volume(grown, o.rect) for o in kids if o is not c)
                    return (after - before, volume(grown) - volume(c.rect), volume(c.rect))
            else:
                def key(c):
                    grown = union(c.rect, rect)
                    return (volume(grown) - volume(c.rect), volume(c.rect))
            u = min(kids, key=key)  # @line L2
            h -= 1
        return u

    def _split(self, u: Node) -> Optional[Node]:
        """Split an overfull node u in place; return the new sibling, or None for a supernode."""
        n = len(u.entries)
        if u.leaf:
            axis, g1, g2 = topological_split(u, max(self.m, int(TOPO_FILL * n)))  # @line L6
        else:
            axis, g1, g2 = topological_split(u, max(self.m, int(TOPO_FILL * n)))
            r1, r2 = _groups_rect(u, g1), _groups_rect(u, g2)
            if overlap_ratio(r1, r2) > MAX_OVERLAP:  # @line L8
                alt = overlap_minimal_split(u, max(self.m, math.ceil(MIN_FANOUT * n)))
                if alt is None:
                    u.blocks += 1  # @line L11
                    return None
                axis, g1, g2 = alt
        v = Node(u.leaf, u.hist | {axis})  # @line L12
        u.hist = v.hist
        u.entries, v.entries = list(g1), list(g2)
        for w in (u, v):
            w.blocks = 1 if w.leaf else max(1, math.ceil(len(w.entries) / self.M))
            if not w.leaf:
                for c in w.entries:
                    c.parent = w
            w.refresh()
        return v

    def _insert_at(self, entry, level: int) -> None:
        rect = entry[0] if level == 0 else entry.rect
        u = self._choose(rect, level)
        u.entries.append(entry)  # @line L3
        if level > 0:
            entry.parent = u
        while u is not None:  # @line L4
            u.refresh()
            nxt = u.parent
            if len(u.entries) > self.capacity(u):  # @line L5
                v = self._split(u)
                if v is not None:
                    if u.parent is None:  # @line L13
                        root = Node(False)
                        root.entries = [u, v]
                        u.parent = v.parent = root
                        root.refresh()
                        self.root = root
                    else:
                        v.parent = u.parent
                        u.parent.entries.append(v)
            u = nxt

    def insert(self, oid: Hashable, rect) -> None:
        r = _as_rect(rect)
        if self.n and len(r[0]) != len(self.root.rect[0]):
            raise ValueError("dimension mismatch")
        self._insert_at((r, oid), 0)
        self.n += 1

    # ---- deletion ----
    def delete(self, oid: Hashable, rect) -> bool:
        r = _as_rect(rect)
        if self.n == 0:
            return False
        leaf, stack = None, [self.root]
        while stack and leaf is None:  # @line L14
            u = stack.pop()
            if not intersects(u.rect, r):
                continue
            if u.leaf:
                if (r, oid) in u.entries:
                    leaf = u
            else:
                stack.extend(u.entries)
        if leaf is None:
            return False
        leaf.entries.remove((r, oid))
        self.n -= 1
        orphans: list = []
        u = leaf
        while u.parent is not None:  # @line L15
            p = u.parent
            if len(u.entries) < self.m:
                p.entries.remove(u)
                h = self._node_height(u) if u.entries else 0
                orphans.extend((e, h) for e in u.entries)
            else:
                if not u.leaf:
                    u.blocks = max(1, math.ceil(len(u.entries) / self.M))
                u.refresh()
            u = p
        if self.root.entries:
            if not self.root.leaf:
                self.root.blocks = max(1, math.ceil(len(self.root.entries) / self.M))
            self.root.refresh()
        else:
            self.root = Node(True)
        for e, h in orphans:
            self._reinsert(e, h)
        while not self.root.leaf and len(self.root.entries) == 1:  # @line L16
            self.root = self.root.entries[0]
            self.root.parent = None
        return True

    def _reinsert(self, e, h: int) -> None:
        if h == 0:
            if not self.root.entries:
                self.root = Node(True)
            self._insert_at(e, 0)
        else:
            if not self.root.entries:
                self.root = e
                e.parent = None
                return
            self._insert_at(e, h)

    # ---- queries ----
    def search(self, q) -> List[Hashable]:
        q = _as_rect(q)
        out: List[Hashable] = []
        if self.n == 0:
            return out
        stack = [self.root]
        while stack:
            u = stack.pop()
            if not intersects(u.rect, q):  # @line L17
                continue
            if u.leaf:
                out.extend(oid for r, oid in u.entries if intersects(r, q))
            else:
                stack.extend(u.entries)
        return out

    def knn(self, q: Sequence[float], k: int) -> List[Tuple[float, Hashable]]:
        q = tuple(float(x) for x in q)
        out: List[Tuple[float, Hashable]] = []
        if self.n == 0 or k <= 0:
            return out
        heap: list = [(mindist(q, self.root.rect), 0, 1, self.root)]
        cnt = 1
        while heap and len(out) < k:  # @line L18
            dd, _, kind, x = heapq.heappop(heap)
            if kind == 0:
                out.append((dd, x))
                continue
            for e in x.entries:
                cnt += 1
                if x.leaf:
                    heapq.heappush(heap, (mindist(q, e[0]), cnt, 0, e[1]))
                else:
                    heapq.heappush(heap, (mindist(q, e.rect), cnt, 1, e))
        return out

    # ---- checks ----
    def items(self) -> List[Tuple[Hashable, Rect]]:
        out, stack = [], [self.root]
        while stack:
            u = stack.pop()
            if u.leaf:
                out.extend((oid, r) for r, oid in u.entries)
            else:
                stack.extend(u.entries)
        return out

    def check_invariant(self) -> None:
        depths = set()

        def walk(u: Node, depth: int) -> None:
            if u is not self.root:
                assert self.m <= len(u.entries), "underfull node"
                assert u.parent is not None
            assert len(u.entries) <= self.capacity(u), "overfull node"
            assert u.leaf or u.blocks >= 1
            assert not u.leaf or u.blocks == 1, "leaves are never supernodes"
            if u.entries:
                assert u.rect == mbr([u.entry_rect(e) for e in u.entries]), "stale rectangle"
            if u.leaf:
                depths.add(depth)
            else:
                assert u is not self.root or len(u.entries) >= 2
                for c in u.entries:
                    assert c.parent is u
                    walk(c, depth + 1)

        walk(self.root, 0)
        assert len(depths) == 1, "leaves at different depths"
        assert len(self.items()) == self.n


def _as_rect(r) -> Rect:
    lo, hi = r
    lo = tuple(float(x) for x in lo)
    hi = tuple(float(x) for x in hi)
    if len(lo) != len(hi) or any(a > b for a, b in zip(lo, hi)):
        raise ValueError("bad rectangle")
    return (lo, hi)
