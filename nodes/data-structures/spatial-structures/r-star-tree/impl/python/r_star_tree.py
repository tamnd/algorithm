# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/r-star-tree/. The authors are listed in prov/DENQWV.jsonl.
"""R*-tree of Beckmann, Kriegel, Schneider and Seeger (1990), in the plane.

Rectangles are closed, (xmin, ymin, xmax, ymax). A leaf entry is
(rect, id); an internal entry is (rect, child). The rules that differ from
Guttman's R-tree: ChooseSubtree by least overlap enlargement above the
leaves, forced reinsertion of the p entries farthest from the node center
once per level and insertion, and the split by margin, then overlap.
"""

from __future__ import annotations

from typing import Hashable, List, Optional, Set, Tuple

Rect = Tuple[float, float, float, float]


def area(r: Rect) -> float:
    return (r[2] - r[0]) * (r[3] - r[1])


def margin(r: Rect) -> float:
    return (r[2] - r[0]) + (r[3] - r[1])


def union(a: Rect, b: Rect) -> Rect:
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


def overlap(a: Rect, b: Rect) -> float:
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    return w * h if w > 0 and h > 0 else 0.0


def intersects(a: Rect, b: Rect) -> bool:
    return a[0] <= b[2] and b[0] <= a[2] and a[1] <= b[3] and b[1] <= a[3]


def mbr(rects: List[Rect]) -> Rect:
    r = rects[0]
    for s in rects[1:]:
        r = union(r, s)
    return r


class Node:
    __slots__ = ("leaf", "entries", "parent")

    def __init__(self, leaf: bool) -> None:
        self.leaf = leaf
        self.entries: list = []
        self.parent: Optional[Node] = None

    def rect(self) -> Rect:
        return mbr([e[0] for e in self.entries])


def _sorted_by(entries: list, side: int) -> list:
    """Sort by one side of the rectangles (0, 1: lower x, y; 2, 3: upper),
    with the opposite side on the same axis as the second key."""
    other = side + 2 if side < 2 else side - 2
    return sorted(entries, key=lambda e: (e[0][side], e[0][other]))


def rstar_split(entries: list, m: int) -> Tuple[list, list]:
    """Split by the axis of least margin sum, then the distribution of least
    overlap (ties: least area sum). Entries are (rect, payload)."""
    n = len(entries)
    best_axis, best_s = 0, None
    for axis in (0, 1):  # @line L10
        s = 0.0
        for side in (axis, axis + 2):
            srt = _sorted_by(entries, side)
            for k in range(m, n - m + 1):
                s += margin(mbr([e[0] for e in srt[:k]])) + margin(mbr([e[0] for e in srt[k:]]))
        if best_s is None or s < best_s:  # @line L11
            best_axis, best_s = axis, s
    best = None
    for side in (best_axis, best_axis + 2):  # @line L12
        srt = _sorted_by(entries, side)
        for k in range(m, n - m + 1):
            r1 = mbr([e[0] for e in srt[:k]])
            r2 = mbr([e[0] for e in srt[k:]])
            key = (overlap(r1, r2), area(r1) + area(r2))
            if best is None or key < best[0]:
                best = (key, srt[:k], srt[k:])
    assert best is not None
    return best[1], best[2]  # @line L13


class RStarTree:
    def __init__(self, max_entries: int = 4, min_entries: Optional[int] = None,
                 reinsert: Optional[int] = None) -> None:
        M = max_entries
        m = max(1, (2 * M) // 5) if min_entries is None else min_entries
        p = max(1, (3 * M) // 10) if reinsert is None else reinsert
        if M < 2 or not 1 <= m <= M // 2 or not 0 <= p <= M - m:
            raise ValueError("need M >= 2, 1 <= m <= M // 2 and 0 <= p <= M - m")
        self.M, self.m, self.p = M, m, p
        self.root = Node(True)
        self.size = 0
        self._done: Set[int] = set()

    def height(self) -> int:
        h, u = 0, self.root
        while not u.leaf:
            u = u.entries[0][1]
            h += 1
        return h

    def search(self, q: Rect) -> List[Hashable]:
        out: List[Hashable] = []
        stack = [self.root]
        while stack:
            u = stack.pop()
            for r, x in u.entries:
                if intersects(r, q):  # @line L17
                    if u.leaf:
                        out.append(x)
                    else:
                        stack.append(x)
        return out

    # ---- insertion ----
    def _choose(self, rect: Rect, level: int) -> Node:
        u, h = self.root, self.height()
        while h > level:
            es = u.entries
            best = None
            for k, (r, _) in enumerate(es):
                big = union(r, rect)
                d_area = area(big) - area(r)
                if h == 1:  # children are leaves: least overlap enlargement
                    d_ov = sum(overlap(big, es[j][0]) - overlap(r, es[j][0])
                               for j in range(len(es)) if j != k)
                    key = (d_ov, d_area, area(r))
                else:
                    key = (d_area, area(r), 0.0)
                if best is None or key < best[0]:
                    best = (key, k)
            assert best is not None
            u = es[best[1]][1]  # @line L2
            h -= 1
        return u

    def _fix_up(self, u: Node) -> None:
        while u.parent is not None:
            p = u.parent
            for k, (_, c) in enumerate(p.entries):
                if c is u:
                    p.entries[k] = (u.rect(), u)
                    break
            u = p

    def _insert_at(self, entry, level: int) -> None:
        u = self._choose(entry[0], level)
        if not u.leaf:
            entry[1].parent = u
        u.entries.append(entry)  # @line L3
        h = level
        while u is not None:  # @line L4
            if len(u.entries) > self.M:
                if u.parent is not None and h not in self._done and self.p > 0:  # @line L5
                    self._done.add(h)
                    c = u.rect()
                    cx, cy = (c[0] + c[2]) / 2, (c[1] + c[3]) / 2

                    def dist(e):
                        r = e[0]
                        return ((r[0] + r[2]) / 2 - cx) ** 2 + ((r[1] + r[3]) / 2 - cy) ** 2
                    order = sorted(range(len(u.entries)), key=lambda k: -dist(u.entries[k]))
                    out = set(order[: self.p])
                    removed = [u.entries[k] for k in order[: self.p]]
                    u.entries = [e for k, e in enumerate(u.entries) if k not in out]
                    self._fix_up(u)
                    for e in reversed(removed):  # close reinsert: nearest first
                        self._insert_at(e, h)
                    return
                g1, g2 = rstar_split(u.entries, self.m)  # @line L6
                v = Node(u.leaf)
                u.entries, v.entries = g1, g2
                if not u.leaf:
                    for _, ch in v.entries:
                        ch.parent = v
                    for _, ch in u.entries:
                        ch.parent = u
                if u.parent is None:  # @line L7
                    root = Node(False)
                    root.entries = [(u.rect(), u), (v.rect(), v)]
                    u.parent = v.parent = root
                    self.root = root
                    return
                v.parent = u.parent
                u.parent.entries.append((v.rect(), v))  # @line L8
            p = u.parent
            if p is not None:  # @line L9
                for k, (_, ch) in enumerate(p.entries):
                    if ch is u:
                        p.entries[k] = (u.rect(), u)
                        break
            u, h = p, h + 1

    def insert(self, oid: Hashable, rect: Rect) -> None:
        if rect[0] > rect[2] or rect[1] > rect[3]:
            raise ValueError("empty rectangle")
        self._done = set()  # @line L1
        self._insert_at((tuple(rect), oid), 0)
        self.size += 1

    # ---- deletion ----
    def delete(self, oid: Hashable, rect: Rect) -> bool:
        rect = tuple(rect)
        leaf = None
        stack = [self.root]
        while stack and leaf is None:  # @line L14
            u = stack.pop()
            for r, x in u.entries:
                if u.leaf:
                    if x == oid and r == rect:
                        leaf = u
                        break
                elif r[0] <= rect[0] and r[1] <= rect[1] and rect[2] <= r[2] and rect[3] <= r[3]:
                    stack.append(x)
        if leaf is None:
            return False
        leaf.entries = [e for e in leaf.entries if not (e[1] == oid and e[0] == rect)]
        self.size -= 1
        orphans = []
        u, h = leaf, 0
        while u.parent is not None:  # @line L15
            p = u.parent
            if len(u.entries) < self.m:
                p.entries = [e for e in p.entries if e[1] is not u]
                orphans.append((u, h))
            else:
                for k, (_, c) in enumerate(p.entries):
                    if c is u:
                        p.entries[k] = (u.rect(), u)
            u, h = p, h + 1
        for node, nh in orphans:
            for e in node.entries:
                self._done = set()
                self._insert_at(e, nh)
        while not self.root.leaf and len(self.root.entries) == 1:  # @line L16
            self.root = self.root.entries[0][1]
            self.root.parent = None
        return True

    # ---- helpers ----
    def items(self) -> List[Tuple[Hashable, Rect]]:
        out = []
        stack = [self.root]
        while stack:
            u = stack.pop()
            for r, x in u.entries:
                if u.leaf:
                    out.append((x, r))
                else:
                    stack.append(x)
        return out

    def check_invariant(self) -> None:
        depths = set()
        count = 0
        stack = [(self.root, 0)]
        while stack:
            u, d = stack.pop()
            assert len(u.entries) <= self.M
            if u is not self.root:
                assert len(u.entries) >= self.m
            elif not u.leaf:
                assert len(u.entries) >= 2
            if u.leaf:
                depths.add(d)
                count += len(u.entries)
            else:
                for r, c in u.entries:
                    assert c.parent is u and c.entries and r == c.rect()
                    stack.append((c, d + 1))
        assert len(depths) <= 1
        assert count == self.size
