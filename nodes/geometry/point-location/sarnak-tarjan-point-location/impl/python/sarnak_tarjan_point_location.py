# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sarnak-tarjan-point-location/. The authors are listed in prov/SN1BV9.jsonl.

"""Planar point location by a persistent search tree (Sarnak and Tarjan 1986).

The slabs of the slab method are the versions of one search tree, built by a sweep from left
to right. This file makes the tree persistent by path copying on an AVL tree: each update
copies the O(log n) nodes on one search path, so the total space is O(n log n). Sarnak and
Tarjan's node copying on a red-black tree brings the space down to O(n); see the page.

Input: segments with int (or Fraction) end points that meet only at shared end points.
Vertical segments are allowed. Degeneracies are removed by the symbolic shear
(x, y) -> (x + eps * y, y): points are compared in lexicographic order, and above or below is
decided by orient, which the shear does not change.

A query returns ("vertex", p), ("edge", i) or ("face", above, below), where above and below are
segment indices (or None) hit by the vertical rays from the query point in the sheared plane.
"""

from bisect import bisect_left

Point = tuple[int, int]
Segment = tuple[Point, Point]


def orient(p: Point, q: Point, r: Point) -> int:
    """Twice the signed area of pqr: positive for a counterclockwise turn. Exact for int and Fraction."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def normalize(seg: Segment) -> Segment:
    a, b = seg
    return (a, b) if a < b else (b, a)


def seg_cmp(s: Segment, t: Segment) -> int:
    """Vertical order of two non-crossing normalized segments that span one slab: -1 if s is below t."""
    if s == t:
        return 0
    a, b = s
    c, d = t
    if c >= a:
        o = orient(a, b, c)
        if o == 0:
            o = orient(a, b, d)
        return -1 if o > 0 else 1
    o = orient(c, d, a)
    if o == 0:
        o = orient(c, d, b)
    return 1 if o > 0 else -1


class Node:
    """An immutable AVL node. A version of the tree is a root; old versions are never changed."""

    __slots__ = ("seg", "left", "right", "height")

    def __init__(self, seg: int, left: "Node | None", right: "Node | None") -> None:
        self.seg = seg
        self.left = left
        self.right = right
        self.height = 1 + max(_h(left), _h(right))


def _h(t: "Node | None") -> int:
    return t.height if t is not None else 0


class PersistentAVL:
    """A functional AVL tree of segment indices ordered by a comparator. Counts created nodes."""

    def __init__(self, cmp) -> None:
        self.cmp = cmp
        self.created = 0

    def _node(self, seg, left, right) -> Node:
        self.created += 1
        return Node(seg, left, right)

    def _balance(self, seg, left, right) -> Node:
        hl, hr = _h(left), _h(right)
        if hl > hr + 1:
            if _h(left.left) >= _h(left.right):
                return self._node(left.seg, left.left, self._node(seg, left.right, right))
            lr = left.right
            return self._node(lr.seg, self._node(left.seg, left.left, lr.left), self._node(seg, lr.right, right))
        if hr > hl + 1:
            if _h(right.right) >= _h(right.left):
                return self._node(right.seg, self._node(seg, left, right.left), right.right)
            rl = right.left
            return self._node(rl.seg, self._node(seg, left, rl.left), self._node(right.seg, rl.right, right.right))
        return self._node(seg, left, right)

    def insert(self, t: "Node | None", seg: int) -> Node:
        if t is None:
            return self._node(seg, None, None)
        c = self.cmp(seg, t.seg)
        if c < 0:
            return self._balance(t.seg, self.insert(t.left, seg), t.right)
        if c > 0:
            return self._balance(t.seg, t.left, self.insert(t.right, seg))
        raise ValueError("duplicate segment")

    def _pop_min(self, t: Node) -> tuple[int, "Node | None"]:
        if t.left is None:
            return t.seg, t.right
        m, rest = self._pop_min(t.left)
        return m, self._balance(t.seg, rest, t.right)

    def delete(self, t: "Node | None", seg: int) -> "Node | None":
        if t is None:
            raise KeyError(seg)
        c = self.cmp(seg, t.seg)
        if c < 0:
            return self._balance(t.seg, self.delete(t.left, seg), t.right)
        if c > 0:
            return self._balance(t.seg, t.left, self.delete(t.right, seg))
        if t.left is None:
            return t.right
        if t.right is None:
            return t.left
        m, rest = self._pop_min(t.right)
        return self._balance(m, t.left, rest)


def inorder(t: "Node | None") -> list[int]:
    out: list[int] = []
    stack: list[Node] = []
    while stack or t is not None:
        while t is not None:
            stack.append(t)
            t = t.left
        t = stack.pop()
        out.append(t.seg)
        t = t.right
    return out


class SarnakTarjanLocator:
    """Build: O(n log n) time. Space: O(n log n) with path copying. Query: O(log n). All worst case."""

    def __init__(self, segments: list[Segment]) -> None:
        segs = [normalize(s) for s in segments]
        for a, b in segs:
            if a == b:
                raise ValueError("a segment must have two distinct end points")
        self.segs = segs
        self.X: list[Point] = sorted({p for s in segs for p in s})  # @line L1
        starts: dict[Point, list[int]] = {}
        ends: dict[Point, list[int]] = {}
        for i, (a, b) in enumerate(segs):
            starts.setdefault(a, []).append(i)
            ends.setdefault(b, []).append(i)
        self.tree = PersistentAVL(lambda i, j: seg_cmp(segs[i], segs[j]))
        root: "Node | None" = None  # @line L2
        self.roots: list["Node | None"] = []
        for x in self.X[:-1]:  # @line L3
            for i in ends.get(x, ()):  # the comparator is valid just left of x
                root = self.tree.delete(root, i)  # @line L4
            for i in starts.get(x, ()):  # and just right of x
                root = self.tree.insert(root, i)  # @line L5
            self.roots.append(root)  # @line L6

    def locate(self, q: Point):
        X = self.X
        j = bisect_left(X, q)
        if j < len(X) and X[j] == q:  # @line L7
            return ("vertex", q)
        i = j - 1
        if i < 0 or i >= len(self.roots):  # @line L8
            return ("face", None, None)
        t = self.roots[i]
        above = below = None
        while t is not None:  # @line L9
            a, b = self.segs[t.seg]
            o = orient(a, b, q)
            if o == 0:
                return ("edge", t.seg)
            if o > 0:
                below, t = t.seg, t.right
            else:
                above, t = t.seg, t.left
        return ("face", above, below)  # @line L10
