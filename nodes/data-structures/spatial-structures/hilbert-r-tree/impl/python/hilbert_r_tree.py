# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hilbert-r-tree/. The authors are listed in prov/P4XVG6.jsonl.

from bisect import bisect_left
from typing import Optional

Rect = tuple[int, int, int, int]  # closed [x1, x2] x [y1, y2], written (x1, y1, x2, y2)
Key = tuple[int, Rect]  # (Hilbert value of the center, the rectangle), a total order


def hilbert_index(order: int, x: int, y: int) -> int:
    """The index of the cell (x, y) on the Hilbert curve of the 2^order by 2^order grid."""
    n = 1 << order
    d = 0
    s = n >> 1
    while s > 0:
        rx = 1 if x & s else 0
        ry = 1 if y & s else 0
        d += s * s * ((3 * rx) ^ ry)
        if ry == 0:
            if rx == 1:
                x, y = n - 1 - x, n - 1 - y
            x, y = y, x
        s >>= 1
    return d


def union(a: Optional[Rect], b: Rect) -> Rect:
    if a is None:
        return b
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


def meets(a: Rect, b: Rect) -> bool:
    return a[0] <= b[2] and b[0] <= a[2] and a[1] <= b[3] and b[1] <= a[3]


class Node:
    """A node of the tree. A leaf holds keys (h, rect) sorted by key; an internal
    node holds children sorted by their largest Hilbert value (lhv). mbr is the
    bounding rectangle of everything below, and lhv the largest key below."""

    __slots__ = ("leaf", "entries", "mbr", "lhv")

    def __init__(self, leaf: bool, entries: Optional[list] = None) -> None:
        self.leaf = leaf
        self.entries: list = entries if entries is not None else []
        self.mbr: Optional[Rect] = None
        self.lhv: Optional[Key] = None
        self.refresh()

    def refresh(self) -> None:
        m: Optional[Rect] = None
        if self.leaf:
            for _, r in self.entries:
                m = union(m, r)
            self.lhv = self.entries[-1] if self.entries else None
        else:
            for c in self.entries:
                m = union(m, c.mbr)
            self.lhv = self.entries[-1].lhv if self.entries else None
        self.mbr = m


def _deal(items: list, nodes: list[Node]) -> None:
    """Give the items, in order, to the nodes as evenly as possible."""
    q, r = divmod(len(items), len(nodes))
    k = 0
    for i, u in enumerate(nodes):
        take = q + (1 if i < r else 0)
        u.entries = items[k : k + take]
        k += take
        u.refresh()


class HilbertRTree:
    """A Hilbert R-tree of rectangles with integer corners in [0, 2^depth)^2.

    Node capacity C >= 4, minimum fill m = C // 2 >= 2 for nodes other than the
    root, so each node other than a leaf root has a sibling to share with, and
    the 2-to-3 split policy: an overflowing node first shares its entries with
    one sibling, and only when both are full do the two become three. The leaf
    entries, read from left to right, are sorted by the Hilbert value of the
    center of each rectangle, so the tree is a B+ tree on that key, and each
    node also keeps the bounding rectangle used by searches.
    """

    def __init__(self, depth: int, capacity: int = 4) -> None:
        if depth < 0 or capacity < 4:
            raise ValueError("need depth >= 0 and capacity >= 4")
        self.depth = depth
        self.C = capacity
        self.m = capacity // 2
        self.root = Node(True)
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def key(self, r: Rect) -> Key:
        """The Hilbert value of the center of r, on the grid of doubled coordinates."""
        x1, y1, x2, y2 = (int(v) for v in r)
        side = 1 << self.depth
        if not (0 <= x1 <= x2 < side and 0 <= y1 <= y2 < side):
            raise ValueError("need 0 <= x1 <= x2 < 2^depth and 0 <= y1 <= y2 < 2^depth")
        return hilbert_index(self.depth + 1, x1 + x2, y1 + y2), (x1, y1, x2, y2)

    def _descend(self, k: Key) -> tuple[Node, list[tuple[Node, int]]]:
        u, path = self.root, []
        while not u.leaf:  # @line L2
            i = 0
            while i < len(u.entries) - 1 and u.entries[i].lhv < k:  # @line L3
                i += 1
            path.append((u, i))
            u = u.entries[i]
        return u, path

    def insert(self, r: Rect) -> bool:
        """Add r. Returns False if it was stored."""
        k = self.key(r)  # @line L1
        leaf, path = self._descend(k)
        i = bisect_left(leaf.entries, k)
        if i < len(leaf.entries) and leaf.entries[i] == k:
            return False
        leaf.entries.insert(i, k)  # @line L4
        self.size += 1
        ancestors = [u for u, _ in path]
        u = leaf
        while len(u.entries) > self.C:  # @line L5
            if not path:  # @line L6
                a, b = Node(u.leaf), Node(u.leaf)
                _deal(u.entries, [a, b])
                self.root = Node(False, [a, b])
                break
            parent, i = path.pop()
            j = i + 1 if i + 1 < len(parent.entries) else i - 1
            lo = min(i, j)
            group = parent.entries[lo : lo + 2]  # @line L7
            items = group[0].entries + group[1].entries
            if len(items) <= 2 * self.C:  # @line L8
                _deal(items, group)
                break
            fresh = Node(u.leaf)  # @line L9
            _deal(items, [group[0], group[1], fresh])
            parent.entries[lo : lo + 2] = [group[0], group[1], fresh]
            u = parent  # @line L10
        leaf.refresh()
        for a in reversed(ancestors):  # @line L11
            a.refresh()
        self.root.refresh()
        return True

    def delete(self, r: Rect) -> bool:
        """Remove r. Returns False if it was not stored."""
        k = self.key(r)
        leaf, path = self._descend(k)  # @line L12
        i = bisect_left(leaf.entries, k)
        if i == len(leaf.entries) or leaf.entries[i] != k:
            return False
        del leaf.entries[i]  # @line L13
        self.size -= 1
        ancestors = [u for u, _ in path]
        u = leaf
        while path and len(u.entries) < self.m:  # @line L14
            parent, i = path.pop()
            j = i + 1 if i + 1 < len(parent.entries) else i - 1
            lo = min(i, j)
            group = parent.entries[lo : lo + 2]
            items = group[0].entries + group[1].entries
            if len(items) >= 2 * self.m:  # @line L15
                _deal(items, group)
                break
            group[0].entries = items  # @line L16
            group[0].refresh()
            parent.entries[lo : lo + 2] = [group[0]]
            u = parent
        leaf.refresh()
        for a in reversed(ancestors):
            a.refresh()
        while not self.root.leaf and len(self.root.entries) == 1:  # @line L17
            self.root = self.root.entries[0]
        return True

    def window(self, q: Rect) -> list[Rect]:
        """All stored rectangles that meet the closed rectangle q."""
        out: list[Rect] = []
        stack = [self.root]
        while stack:  # @line L18
            u = stack.pop()
            if u.mbr is None or not meets(u.mbr, q):  # @line L19
                continue
            if u.leaf:
                out.extend(r for _, r in u.entries if meets(r, q))  # @line L20
            else:
                stack.extend(u.entries)  # @line L21
        return out

    def rects(self) -> list[Rect]:
        """All rectangles, in Hilbert order."""
        out: list[Rect] = []
        stack = [self.root]
        while stack:
            u = stack.pop()
            if u.leaf:
                out.extend(r for _, r in u.entries)
            else:
                stack.extend(reversed(u.entries))
        return out

    def height(self) -> int:
        h, u = 0, self.root
        while not u.leaf:
            u, h = u.entries[0], h + 1
        return h

    def check_invariant(self) -> None:
        depths: set[int] = set()
        keys: list[Key] = []
        stack: list[tuple[Node, int]] = [(self.root, 0)]
        order: list[Node] = []
        while stack:
            u, d = stack.pop()
            order.append(u)
            n = len(u.entries)
            assert n <= self.C, "node overflow"
            if u is self.root:
                assert u.leaf or n >= 2, "internal root with one child"
            else:
                assert n >= self.m, "node underflow"
            m: Optional[Rect] = None
            if u.leaf:
                depths.add(d)
                for h, r in u.entries:
                    assert (h, r) == self.key(r), "wrong key"
                    m = union(m, r)
                keys.extend(u.entries)
                assert u.lhv == (u.entries[-1] if u.entries else None), "wrong lhv"
            else:
                for c in u.entries:
                    m = union(m, c.mbr)
                assert u.lhv == u.entries[-1].lhv, "wrong lhv"
                assert all(c.lhv is not None for c in u.entries), "empty child"
                stack.extend((c, d + 1) for c in reversed(u.entries))
            assert u.mbr == m, "wrong bounding rectangle"
        assert len(depths) <= 1, "leaves at different depths"
        assert keys == sorted(set(keys)), "leaf entries not in strict Hilbert order"
        assert len(keys) == self.size, "size is wrong"
