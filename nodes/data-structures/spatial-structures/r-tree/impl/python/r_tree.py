# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/r-tree/. The authors are listed in prov/SKDGZ3.jsonl.

from typing import Hashable, Optional, Union

Rect = tuple[float, float, float, float]  # (xmin, ymin, xmax, ymax), closed


def area(r: Rect) -> float:
    return (r[2] - r[0]) * (r[3] - r[1])


def union(a: Rect, b: Rect) -> Rect:
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


def intersects(a: Rect, b: Rect) -> bool:
    return a[0] <= b[2] and b[0] <= a[2] and a[1] <= b[3] and b[1] <= a[3]


def mbr(rects: list[Rect]) -> Rect:
    r = rects[0]
    for s in rects[1:]:
        r = union(r, s)
    return r


class Node:
    """A node of the R-tree. A leaf entry is (rect, object id); an internal
    entry is (rect, child node), where rect is the MBR of the child."""

    __slots__ = ("leaf", "entries", "parent")

    def __init__(self, leaf: bool) -> None:
        self.leaf = leaf
        self.entries: list[tuple[Rect, Union[Hashable, "Node"]]] = []
        self.parent: Optional[Node] = None

    def rect(self) -> Rect:
        return mbr([e[0] for e in self.entries])


Entry = tuple[Rect, object]


def quadratic_split(entries: list[Entry], m: int) -> tuple[list[Entry], list[Entry]]:
    """Guttman's quadratic split of M + 1 entries into two groups of at least m. O(M^2)."""
    n = len(entries)
    best = None
    for i in range(n):  # pick the seeds: the pair that wastes the most area
        for j in range(i + 1, n):
            d = area(union(entries[i][0], entries[j][0])) - area(entries[i][0]) - area(entries[j][0])
            if best is None or d > best[0]:
                best = (d, i, j)
    assert best is not None
    _, i, j = best
    g1, g2 = [entries[i]], [entries[j]]
    r1, r2 = entries[i][0], entries[j][0]
    rest = [e for k, e in enumerate(entries) if k != i and k != j]
    while rest:
        if len(g1) + len(rest) == m:
            g1.extend(rest)
            break
        if len(g2) + len(rest) == m:
            g2.extend(rest)
            break
        pick, diff = 0, -1.0
        for k, e in enumerate(rest):  # pick the entry with the strongest preference
            d1 = area(union(r1, e[0])) - area(r1)
            d2 = area(union(r2, e[0])) - area(r2)
            if abs(d1 - d2) > diff:
                pick, diff = k, abs(d1 - d2)
        e = rest.pop(pick)
        d1 = area(union(r1, e[0])) - area(r1)
        d2 = area(union(r2, e[0])) - area(r2)
        key1 = (d1, area(r1), len(g1))
        key2 = (d2, area(r2), len(g2))
        if key1 <= key2:
            g1.append(e)
            r1 = union(r1, e[0])
        else:
            g2.append(e)
            r2 = union(r2, e[0])
    return g1, g2


class RTree:
    """Guttman's R-tree of rectangles with node capacity M and minimum fill m.

    Invariant: every leaf is at the same depth; each node other than the
    root has between m and M entries; the root has at least two entries
    unless it is a leaf; the rectangle of each internal entry is the MBR of
    its child. Needs 1 <= m <= M // 2 (Guttman uses m >= 2).
    """

    def __init__(self, max_entries: int = 4, min_entries: Optional[int] = None) -> None:
        m = max_entries // 2 if min_entries is None else min_entries
        if max_entries < 2 or m < 1 or m > max_entries // 2:
            raise ValueError("need M >= 2 and 1 <= m <= M // 2")
        self.M, self.m = max_entries, m
        self.root = Node(True)
        self.size = 0

    def __len__(self) -> int:
        return self.size

    # ---- search ----
    def search(self, q: Rect) -> list[Hashable]:
        """The ids of the stored rectangles that meet q (closed rectangles)."""
        out: list[Hashable] = []
        stack = [self.root]
        while stack:
            u = stack.pop()
            for r, x in u.entries:
                if intersects(r, q):  # @line L1
                    if u.leaf:
                        out.append(x)  # @line L2
                    else:
                        stack.append(x)  # @line L3
        return out

    # ---- insert ----
    def _choose(self, rect: Rect, level: int) -> Node:
        """Descend to a node at height `level` (0 = leaf) by least enlargement."""
        u = self.root
        h = self.height()
        while h > level:
            best = None
            for k, (r, _) in enumerate(u.entries):  # @line L5
                key = (area(union(r, rect)) - area(r), area(r))
                if best is None or key < best[0]:
                    best = (key, k)
            assert best is not None
            u = u.entries[best[1]][1]
            h -= 1
        return u

    def _insert_entry(self, entry: Entry, level: int) -> None:
        u = self._choose(entry[0], level)  # @line L4
        if not u.leaf:
            entry[1].parent = u
        u.entries.append(entry)  # @line L6
        while u is not None:  # @line L7
            if len(u.entries) > self.M:  # @line L8
                g1, g2 = quadratic_split(u.entries, self.m)
                v = Node(u.leaf)
                u.entries, v.entries = g1, g2
                if not u.leaf:
                    for _, c in v.entries:
                        c.parent = v
                if u.parent is None:  # @line L10
                    root = Node(False)
                    root.entries = [(u.rect(), u), (v.rect(), v)]
                    u.parent = v.parent = root
                    self.root = root
                    return
                v.parent = u.parent
                u.parent.entries.append((v.rect(), v))  # @line L9
            p = u.parent
            if p is not None:  # @line L11: fix the rectangle of u in its parent
                for k, (_, c) in enumerate(p.entries):
                    if c is u:
                        p.entries[k] = (u.rect(), u)
                        break
            u = p

    def insert(self, oid: Hashable, rect: Rect) -> None:
        """Add the object oid with rectangle rect. O(M^2 log_m n) worst."""
        if rect[0] > rect[2] or rect[1] > rect[3]:
            raise ValueError("need xmin <= xmax and ymin <= ymax")
        self._insert_entry((tuple(rect), oid), 0)
        self.size += 1

    # ---- delete ----
    def delete(self, oid: Hashable, rect: Rect) -> bool:
        """Remove the object oid stored with rectangle rect; False if absent."""
        leaf = None
        stack = [self.root]
        while stack and leaf is None:  # @line L12: find the leaf
            u = stack.pop()
            for r, x in u.entries:
                if u.leaf:
                    if x == oid and r == tuple(rect):
                        leaf = u
                        break
                elif intersects(r, rect) and r[0] <= rect[0] and r[1] <= rect[1] and rect[2] <= r[2] and rect[3] <= r[3]:
                    stack.append(x)
        if leaf is None:
            return False
        leaf.entries = [e for e in leaf.entries if not (e[1] == oid and e[0] == tuple(rect))]  # @line L13
        self.size -= 1
        orphans: list[tuple[Node, int]] = []  # removed nodes and their heights
        u, h = leaf, 0
        while u.parent is not None:  # @line L14: condense the tree
            p = u.parent
            if len(u.entries) < self.m:
                p.entries = [e for e in p.entries if e[1] is not u]
                orphans.append((u, h))
            else:
                for k, (_, c) in enumerate(p.entries):
                    if c is u:
                        p.entries[k] = (u.rect(), u)
            u, h = p, h + 1
        for node, nh in orphans:  # @line L15: reinsert the entries of removed nodes
            for e in node.entries:
                self._insert_entry(e, nh)
        while not self.root.leaf and len(self.root.entries) == 1:  # @line L16
            self.root = self.root.entries[0][1]
            self.root.parent = None
        return True

    # ---- helpers ----
    def height(self) -> int:
        """Number of levels below the root (0 when the root is a leaf)."""
        h, u = 0, self.root
        while not u.leaf:
            u = u.entries[0][1]
            h += 1
        return h

    def items(self) -> list[tuple[Hashable, Rect]]:
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
        """Raise AssertionError if the R-tree properties fail."""
        depths: set[int] = set()
        count = 0
        stack: list[tuple[Node, int]] = [(self.root, 0)]
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
                    assert c.parent is u
                    assert c.entries and r == c.rect()
                    stack.append((c, d + 1))
        assert len(depths) <= 1
        assert count == self.size
