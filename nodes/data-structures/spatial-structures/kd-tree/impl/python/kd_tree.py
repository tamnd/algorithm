# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kd-tree/. The authors are listed in prov/39PCSM.jsonl.

import math
import random
from typing import Optional, Sequence

Point = tuple[float, ...]


def superkey(p: Sequence[float], a: int) -> tuple[float, ...]:
    """The key of p for axis a: (p[a], p[a+1], ..., p[a-1]), compared lexicographically."""
    return tuple(p[a:]) + tuple(p[:a])


class Node:
    __slots__ = ("point", "axis", "left", "right")

    def __init__(self, point: Point, axis: int) -> None:
        self.point = point
        self.axis = axis
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None


def _select(items: list[Point], r: int, a: int, rng: random.Random) -> Point:
    """Return the item of rank r (0-based) in the superkey order of axis a.

    Quickselect with a random pivot and a three-way partition: expected O(len(items)).
    """
    xs = items
    while True:
        pivot = superkey(xs[rng.randrange(len(xs))], a)
        lo = [x for x in xs if superkey(x, a) < pivot]
        eq = [x for x in xs if superkey(x, a) == pivot]
        if r < len(lo):
            xs = lo
        elif r < len(lo) + len(eq):
            return eq[0]
        else:
            r -= len(lo) + len(eq)
            xs = [x for x in xs if superkey(x, a) > pivot]


class KdTree:
    """A k-d tree with one point in each node (Bentley's form).

    Invariant: at a node t with axis a, each point of t.left is less than
    t.point in the superkey order of axis a, and each point of t.right is
    greater than or equal to it. The axis of a node is its depth mod k.
    Duplicate points are allowed; they go to the right.
    """

    def __init__(self, k: int, points: Sequence[Sequence[float]] = ()) -> None:
        """Build a tree on the points by median splits. Expected O(n log n) time."""
        if k < 1:
            raise ValueError("k must be at least 1")
        self.k = k
        self.root: Optional[Node] = None
        self.size = 0
        pts = [tuple(float(c) for c in p) for p in points]
        for p in pts:
            if len(p) != k:
                raise ValueError("a point has the wrong dimension")
        self.size = len(pts)
        self.root = self._build(pts)

    def _build(self, pts: list[Point]) -> Optional[Node]:
        rng = random.Random(len(pts))
        root: Optional[Node] = None
        # each entry: (points, depth, parent, is_left); an explicit stack keeps
        # the recursion of BUILD off the Python call stack
        stack: list[tuple[list[Point], int, Optional[Node], bool]] = [(pts, 0, None, False)]
        while stack:
            p_set, depth, parent, is_left = stack.pop()
            if not p_set:  # @line L1
                continue
            a = depth % self.k  # @line L2
            m = _select(p_set, len(p_set) // 2, a, rng)  # @line L3
            t = Node(m, a)  # @line L4
            if parent is None:
                root = t
            elif is_left:
                parent.left = t
            else:
                parent.right = t
            km = superkey(m, a)
            left = [p for p in p_set if superkey(p, a) < km]  # @line L5
            right = [p for p in p_set if superkey(p, a) >= km]  # @line L6
            right.remove(m)  # one copy of m is the node itself
            stack.append((left, depth + 1, t, True))
            stack.append((right, depth + 1, t, False))
        return root  # @line L7

    def insert(self, p: Sequence[float]) -> None:
        """Add the point p at a new leaf. O(h) time, h the height."""
        q = tuple(float(c) for c in p)
        if len(q) != self.k:
            raise ValueError("the point has the wrong dimension")
        self.size += 1
        if self.root is None:  # @line L13
            self.root = Node(q, 0)
            return
        t = self.root
        while True:  # @line L14
            a = t.axis
            if superkey(q, a) < superkey(t.point, a):  # @line L15
                if t.left is None:
                    t.left = Node(q, (a + 1) % self.k)
                    return
                t = t.left
            else:
                if t.right is None:  # @line L16
                    t.right = Node(q, (a + 1) % self.k)
                    return
                t = t.right

    def contains(self, p: Sequence[float]) -> bool:
        """Return True when p is in the tree. O(h) time."""
        q = tuple(float(c) for c in p)
        t = self.root
        while t is not None:
            if t.point == q:
                return True
            t = t.left if superkey(q, t.axis) < superkey(t.point, t.axis) else t.right
        return False

    def range_search(self, lo: Sequence[float], hi: Sequence[float]) -> list[Point]:
        """Return the points p with lo[i] <= p[i] <= hi[i] for each axis i.

        O(n^(1-1/k) + r) nodes for a tree built by the constructor on points
        with distinct coordinates, r the output size; O(n) in any case.
        """
        out: list[Point] = []
        stack = [self.root]
        while stack:
            t = stack.pop()
            if t is None:  # @line L8
                continue
            if all(lo[i] <= t.point[i] <= hi[i] for i in range(self.k)):  # @line L9
                out.append(t.point)
            a = t.axis  # @line L10
            if lo[a] <= t.point[a]:  # @line L11
                stack.append(t.left)
            if hi[a] >= t.point[a]:  # @line L12
                stack.append(t.right)
        return out

    def nearest(self, q: Sequence[float]) -> Optional[Point]:
        """Return a point of the tree at the least Euclidean distance from q, or None.

        Branch and bound; each subtree carries a lower bound on the squared
        distance from q to its points.
        """
        best: Optional[Point] = None
        best_d = math.inf
        stack: list[tuple[Optional[Node], float]] = [(self.root, 0.0)]
        while stack:
            t, bound = stack.pop()
            if t is None or bound >= best_d:  # @line L17
                continue
            d = sum((q[i] - t.point[i]) ** 2 for i in range(self.k))
            if d < best_d:  # @line L18
                best, best_d = t.point, d
            a = t.axis  # @line L19
            delta = q[a] - t.point[a]
            near, far = (t.left, t.right) if delta < 0 else (t.right, t.left)  # @line L20
            stack.append((far, max(bound, delta * delta)))  # @line L22: searched only if delta^2 < best
            stack.append((near, bound))  # @line L21
        return best

    def _find_min(self, t: Node, a: int) -> tuple[Node, Optional[Node]]:
        """Return (node, parent) of a node of least superkey for axis a in the subtree t."""
        best, best_parent = t, None
        stack: list[tuple[Node, Optional[Node]]] = [(t, None)]
        while stack:
            u, par = stack.pop()
            if superkey(u.point, a) < superkey(best.point, a):
                best, best_parent = u, par
            if u.left is not None:
                stack.append((u.left, u))
            if u.right is not None and u.axis != a:  # @line L27: on axis a, the right side is not smaller
                stack.append((u.right, u))
        if best_parent is None and best is not t:
            raise AssertionError("unreachable")
        return best, best_parent

    def delete(self, p: Sequence[float]) -> bool:
        """Remove one copy of p. Return False when p is not in the tree. O(h) to find p,
        plus the cost of the replacement searches."""
        q = tuple(float(c) for c in p)
        parent: Optional[Node] = None
        t = self.root
        while t is not None and t.point != q:  # @line L23
            parent = t
            t = t.left if superkey(q, t.axis) < superkey(t.point, t.axis) else t.right
        if t is None:
            return False
        self.size -= 1
        while True:
            a = t.axis
            if t.right is not None:  # @line L24
                m, mp = self._find_min(t.right, a)
                t.point = m.point
                parent, t = (mp if mp is not None else t), m
            elif t.left is not None:  # @line L25
                m, mp = self._find_min(t.left, a)
                t.point = m.point
                t.right, t.left = t.left, None
                parent, t = (mp if mp is not None else t), m
            else:  # @line L26: a leaf is cut off
                if parent is None:
                    self.root = None
                elif parent.left is t:
                    parent.left = None
                else:
                    parent.right = None
                return True

    def height(self) -> int:
        """The number of nodes on a longest root-to-leaf path (0 for an empty tree)."""
        h = 0
        stack = [(self.root, 1)]
        while stack:
            t, d = stack.pop()
            if t is not None:
                h = max(h, d)
                stack.append((t.left, d + 1))
                stack.append((t.right, d + 1))
        return h

    def points(self) -> list[Point]:
        out: list[Point] = []
        stack = [self.root]
        while stack:
            t = stack.pop()
            if t is not None:
                out.append(t.point)
                stack.append(t.left)
                stack.append(t.right)
        return out

    def check_invariant(self) -> None:
        """Raise AssertionError if the axes or the order of some node are wrong."""
        count = 0
        # each entry: node, depth, list of (axis, key, side) constraints from ancestors
        stack: list[tuple[Optional[Node], int, list[tuple[int, tuple[float, ...], bool]]]] = [(self.root, 0, [])]
        while stack:
            t, depth, cons = stack.pop()
            if t is None:
                continue
            count += 1
            assert t.axis == depth % self.k
            for a, key, is_left in cons:
                if is_left:
                    assert superkey(t.point, a) < key
                else:
                    assert superkey(t.point, a) >= key
            key = superkey(t.point, t.axis)
            stack.append((t.left, depth + 1, cons + [(t.axis, key, True)]))
            stack.append((t.right, depth + 1, cons + [(t.axis, key, False)]))
        assert count == self.size
