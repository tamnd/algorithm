# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/r-plus-tree/. The authors are listed in prov/SFMMBA.jsonl.
"""An R+-tree in the plane, in the form of a k-d-B tree with clipping.

Every node has a half-open region [x0, x1) x [y0, y1); the root region is
the whole plane. The regions of the children of a node partition the
region of the node, so sibling regions never overlap. Objects are closed
rectangles (xmin, ymin, xmax, ymax). A leaf stores every object that
meets its region, so an object that crosses a cut is stored in several
leaves. A query reports an object once, in the leaf whose region holds
the lower left corner of the intersection of the query and the object.

Capacity M is soft: a node is split only by a cut that makes both sides
smaller than the node. If no such cut exists (more than M objects meet at
one point), the node stays over full, as Sellis et al. note.
"""

from __future__ import annotations

from typing import Hashable, List, Optional, Tuple

INF = float("inf")
Rect = Tuple[float, float, float, float]


def meets(b: Rect, reg: Rect) -> bool:
    """Closed rectangle b meets half-open region reg."""
    return b[0] < reg[2] and b[2] >= reg[0] and b[1] < reg[3] and b[3] >= reg[1]


def contains_point(reg: Rect, x: float, y: float) -> bool:
    return reg[0] <= x < reg[2] and reg[1] <= y < reg[3]


def intersects(a: Rect, b: Rect) -> bool:
    return a[0] <= b[2] and b[0] <= a[2] and a[1] <= b[3] and b[1] <= a[3]


class Node:
    __slots__ = ("leaf", "region", "items", "children")

    def __init__(self, leaf: bool, region: Rect) -> None:
        self.leaf = leaf
        self.region = region
        self.items: List[Tuple[Hashable, Rect]] = []  # leaves
        self.children: List[Node] = []  # internal nodes

    def size(self) -> int:
        return len(self.items) if self.leaf else len(self.children)


def halves(reg: Rect, axis: int, c: float) -> Tuple[Rect, Rect]:
    if axis == 0:
        return (reg[0], reg[1], c, reg[3]), (c, reg[1], reg[2], reg[3])
    return (reg[0], reg[1], reg[2], c), (reg[0], c, reg[2], reg[3])


def cut_node(u: Node, axis: int, c: float) -> Tuple[Node, Node]:
    """Split u by the line axis = c into two nodes; children that cross the
    line are cut too, down to the leaves."""
    lr, rr = halves(u.region, axis, c)
    left, right = Node(u.leaf, lr), Node(u.leaf, rr)
    if u.leaf:
        left.items = [it for it in u.items if meets(it[1], lr)]  # @line L12
        right.items = [it for it in u.items if meets(it[1], rr)]
        return left, right
    for ch in u.children:
        lo, hi = ch.region[axis], ch.region[axis + 2]
        if hi <= c:
            left.children.append(ch)
        elif lo >= c:
            right.children.append(ch)
        else:
            a, b = cut_node(ch, axis, c)  # @line L13
            left.children.append(a)
            right.children.append(b)
    return left, right


def choose_cut(u: Node, clean: bool = False) -> Optional[Tuple[int, float]]:
    """The cut that makes the larger side smallest (ties: fewer copies), among
    the sides of the entries; None if no cut makes both sides smaller.
    With clean=True, only cuts that cross no entry are allowed."""
    best = None
    n = u.size()
    for axis in (0, 1):  # @line L10
        lo_r, hi_r = u.region[axis], u.region[axis + 2]
        if u.leaf:
            cands = {b[axis] for _, b in u.items} | {b[axis + 2] for _, b in u.items}
        else:
            cands = {ch.region[axis] for ch in u.children} | {ch.region[axis + 2] for ch in u.children}
        for c in sorted(cands):
            if not lo_r < c < hi_r:
                continue
            if u.leaf:
                nl = sum(1 for _, b in u.items if b[axis] < c)
                nr = sum(1 for _, b in u.items if b[axis + 2] >= c)
            else:
                nl = sum(1 for ch in u.children if ch.region[axis] < c)
                nr = sum(1 for ch in u.children if ch.region[axis + 2] > c)
            if max(nl, nr) >= n or min(nl, nr) == 0:
                continue
            if clean and nl + nr > n:
                continue
            key = (max(nl, nr), nl + nr, axis, c)
            if best is None or key < best:
                best = key
    return None if best is None else (best[2], best[3])  # @line L11


class RPlusTree:
    def __init__(self, max_entries: int = 4) -> None:
        if max_entries < 2:
            raise ValueError("M must be at least 2")
        self.M = max_entries
        self.root = Node(True, (-INF, -INF, INF, INF))
        self.n = 0

    def search(self, q: Rect) -> List[Hashable]:
        out: List[Hashable] = []
        stack = [self.root]
        while stack:
            u = stack.pop()
            if u.leaf:
                for oid, b in u.items:  # @line L3
                    if intersects(q, b) and contains_point(
                            u.region, max(q[0], b[0]), max(q[1], b[1])):  # @line L4
                        out.append(oid)
            else:
                for ch in u.children:  # @line L1
                    if meets(q, ch.region):  # @line L2
                        stack.append(ch)
        return out

    def insert(self, oid: Hashable, b: Rect) -> None:
        if b[0] > b[2] or b[1] > b[3]:
            raise ValueError("empty rectangle")
        b = tuple(b)
        pieces = self._insert_at(self.root, oid, b)
        while len(pieces) > 1:  # @line L8
            root = Node(False, self.root.region)
            root.children = pieces
            self.root = root
            pieces = self._split_all(root, clean=True)
        self.root = pieces[0]
        self.n += 1

    def _insert_at(self, u: Node, oid: Hashable, b: Rect) -> List[Node]:
        """Add b to every leaf below u that it meets; return the nodes that replace u."""
        if u.leaf:
            u.items.append((oid, b))  # @line L6
        else:
            new: List[Node] = []
            for ch in u.children:
                if meets(b, ch.region):  # @line L5
                    new.extend(self._insert_at(ch, oid, b))
                else:
                    new.append(ch)
            u.children = new
        return self._split_all(u)  # @line L7

    def _split_all(self, u: Node, clean: bool = False) -> List[Node]:
        """Cut u while it has more than M entries and a good cut exists."""
        if u.size() <= self.M:
            return [u]
        cut = choose_cut(u, clean)  # @line L9
        if cut is None:
            return [u]
        a, c = cut_node(u, *cut)
        return self._split_all(a, clean) + self._split_all(c, clean)

    def delete(self, oid: Hashable, b: Rect) -> bool:
        b = tuple(b)
        found = False
        stack = [self.root]
        while stack:  # @line L14
            u = stack.pop()
            if u.leaf:
                k = len(u.items)
                u.items = [it for it in u.items if it != (oid, b)]
                found |= len(u.items) != k
            else:
                stack.extend(ch for ch in u.children if meets(b, ch.region))
        if found:
            self.n -= 1
        return found

    # ---- helpers ----
    def leaves(self) -> List[Node]:
        out, stack = [], [self.root]
        while stack:
            u = stack.pop()
            if u.leaf:
                out.append(u)
            else:
                stack.extend(u.children)
        return out

    def copies(self) -> int:
        return sum(len(u.items) for u in self.leaves())

    def height(self) -> int:
        h, u = 0, self.root
        while not u.leaf:
            u = u.children[0]
            h += 1
        return h

    def check_invariant(self, objects: dict) -> None:
        """objects: id -> rect of the stored set."""
        depths = set()
        stack = [(self.root, 0)]
        while stack:
            u, d = stack.pop()
            if u.leaf:
                depths.add(d)
                want = sorted((k, r) for k, r in objects.items() if meets(r, u.region))
                assert sorted(u.items) == want, "leaf must hold the objects that meet it"
                continue
            assert u.children
            area = 0.0
            for ch in u.children:
                assert u.region[0] <= ch.region[0] < ch.region[2] <= u.region[2]
                assert u.region[1] <= ch.region[1] < ch.region[3] <= u.region[3]
                stack.append((ch, d + 1))
            for i, a in enumerate(u.children):  # disjoint siblings
                for b in u.children[i + 1:]:
                    ra, rb = a.region, b.region
                    assert not (ra[0] < rb[2] and rb[0] < ra[2] and ra[1] < rb[3] and rb[1] < ra[3])
        assert len(depths) == 1
