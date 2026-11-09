# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trapezoidal-map/. The authors are listed in prov/S5KEK2.jsonl.

"""Trapezoidal map of non-crossing segments with a history DAG for point location.

This follows de Berg, Cheong, van Kreveld and Overmars, Chapter 6, with two changes: there is
no bounding box (an unbounded side is None), and degenerate input is handled by the symbolic
shear (x, y) -> (x + eps * y, y) of their Section 6.3. Under the shear, points are compared in
lexicographic order and no segment is vertical; orient is unchanged by the shear.

Segments have int (or Fraction) end points and may share end points; otherwise they must be
disjoint. A query returns ("vertex", p), ("edge", i) or ("face", top, bottom), where top and
bottom are the indices of the segments that bound the trapezoid containing the query point.

Neighbor slots of a trapezoid T, with left wall through T.leftp:
- if T.bottom starts at T.leftp, the only left neighbor is in T.ul;
- if T.top starts at T.leftp, the only left neighbor is in T.ll;
- if both start there, there is none; if neither does, ul is the upper and ll the lower one.
The right side is the same with ur, lr and the segments that end at T.rightp
(top ends there: the only right neighbor is lr; bottom ends there: it is ur).
"""

import random

Point = tuple[int, int]
Segment = tuple[Point, Point]


def orient(p: Point, q: Point, r: Point) -> int:
    """Twice the signed area of pqr: positive for a counterclockwise turn. Exact for int and Fraction."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


class Trap:
    __slots__ = ("top", "bottom", "leftp", "rightp", "ul", "ll", "ur", "lr", "node")

    def __init__(self, top, bottom, leftp, rightp) -> None:
        self.top, self.bottom = top, bottom  # segment indices, None for unbounded
        self.leftp, self.rightp = leftp, rightp  # points, None for unbounded
        self.ul = self.ll = self.ur = self.lr = None
        self.node = None


class Node:
    """A DAG node: kind 'x' (point), 'y' (segment) or 'leaf' (trapezoid)."""

    __slots__ = ("kind", "key", "left", "right", "trap")

    def __init__(self, trap: Trap) -> None:
        self.kind, self.key, self.left, self.right, self.trap = "leaf", None, None, None, trap
        trap.node = self


def _fix_right_ptrs(t: "Trap | None", old: Trap, new: Trap) -> None:
    # t is a left neighbor of old: its right pointer to old now points to new
    if t is not None:
        if t.ur is old:
            t.ur = new
        if t.lr is old:
            t.lr = new


def _fix_left_ptrs(t: "Trap | None", old: Trap, new: Trap) -> None:
    # t is a right neighbor of old: its left pointer to old now points to new
    if t is not None:
        if t.ul is old:
            t.ul = new
        if t.ll is old:
            t.ll = new


class TrapezoidalMap:
    """Expected O(n log n) build and O(log n) query for a random insertion order; O(n) trapezoids."""

    def __init__(self) -> None:
        self.segs: list[Segment] = []
        self.points: set[Point] = set()
        first = Trap(None, None, None, None)
        self.root = Node(first)
        self.created = 1  # number of trapezoids ever created

    # predicates in the sheared plane
    def _above(self, s: int, q: Point) -> int:
        a, b = self.segs[s]
        return orient(a, b, q)

    def _find_start(self, p: Point, r: Point) -> Trap:
        """The trapezoid that contains the points of segment pr just right of p."""
        v = self.root
        while v.kind != "leaf":
            if v.kind == "x":
                v = v.left if p < v.key else v.right  # equal: go right
            else:
                o = self._above(v.key, p)
                if o == 0:  # p is the left end point of the node segment
                    o = self._above(v.key, r)
                v = v.left if o > 0 else v.right
        return v.trap

    def insert(self, seg: Segment) -> None:
        p, r = seg if seg[0] < seg[1] else (seg[1], seg[0])
        if p == r:
            raise ValueError("a segment must have two distinct end points")
        s = len(self.segs)
        self.segs.append((p, r))
        crossed = [self._find_start(p, r)]  # @line L1
        while crossed[-1].rightp is not None and crossed[-1].rightp < r:  # @line L2
            t = crossed[-1]
            crossed.append(t.lr if orient(p, r, t.rightp) > 0 else t.ur)  # @line L3
        pnew, rnew = p not in self.points, r not in self.points
        self.points.update((p, r))
        k = len(crossed) - 1
        d0, dk = crossed[0], crossed[-1]
        # upper and lower chains, cut at the right points above and below s
        upper: list[Trap] = [Trap(d0.top, s, p, None)]  # @line L4
        lower: list[Trap] = [Trap(s, d0.bottom, p, None)]
        up_of, low_of = [], []
        for j, t in enumerate(crossed):
            up_of.append(upper[-1])
            low_of.append(lower[-1])
            if j == k:
                break
            v = t.rightp
            nxt = crossed[j + 1]
            if orient(p, r, v) > 0:  # v above s: cut the upper chain
                u, w = upper[-1], Trap(nxt.top, s, v, None)
                u.rightp = v
                u.lr, w.ll = w, u
                u.ur = t.ur
                _fix_left_ptrs(t.ur, t, u)
                w.ul = nxt.ul
                _fix_right_ptrs(nxt.ul, nxt, w)
                upper.append(w)
            else:  # v below s: cut the lower chain
                u, w = lower[-1], Trap(s, nxt.bottom, v, None)
                u.rightp = v
                u.ur, w.ul = w, u
                u.lr = t.lr
                _fix_left_ptrs(t.lr, t, u)
                w.ll = nxt.ll
                _fix_right_ptrs(nxt.ll, nxt, w)
                lower.append(w)
        upper[-1].rightp = lower[-1].rightp = r
        u0, l0, ue, le = upper[0], lower[0], upper[-1], lower[-1]
        A = B = None
        if pnew:  # @line L5
            A = Trap(d0.top, d0.bottom, d0.leftp, p)
            A.ul, A.ll = d0.ul, d0.ll
            _fix_right_ptrs(d0.ul, d0, A)
            _fix_right_ptrs(d0.ll, d0, A)
            A.ur, A.lr = u0, l0
            u0.ul, l0.ll = A, A
        else:
            u0.ul, l0.ll = d0.ul, d0.ll
            _fix_right_ptrs(d0.ul, d0, u0)
            _fix_right_ptrs(d0.ll, d0, l0)
        if rnew:
            B = Trap(dk.top, dk.bottom, r, dk.rightp)
            B.ur, B.lr = dk.ur, dk.lr
            _fix_left_ptrs(dk.ur, dk, B)
            _fix_left_ptrs(dk.lr, dk, B)
            B.ul, B.ll = ue, le
            ue.ur, le.lr = B, B
        else:
            ue.ur, le.lr = dk.ur, dk.lr
            _fix_left_ptrs(dk.ur, dk, ue)
            _fix_left_ptrs(dk.lr, dk, le)
        self.created += len(upper) + len(lower) + pnew + rnew
        # replace the leaves of the crossed trapezoids in the DAG
        leaf = {}

        def leaf_of(t: Trap) -> Node:
            if id(t) not in leaf:
                leaf[id(t)] = Node(t)
            return leaf[id(t)]

        for j, t in enumerate(crossed):  # @line L6
            node = t.node
            y = Node.__new__(Node)
            y.kind, y.key, y.trap = "y", s, None
            y.left, y.right = leaf_of(up_of[j]), leaf_of(low_of[j])
            top = y
            if j == k and rnew:
                x = Node.__new__(Node)
                x.kind, x.key, x.trap, x.left, x.right = "x", r, None, top, leaf_of(B)
                top = x
            if j == 0 and pnew:
                x = Node.__new__(Node)
                x.kind, x.key, x.trap, x.left, x.right = "x", p, None, leaf_of(A), top
                top = x
            node.kind, node.key, node.left, node.right, node.trap = top.kind, top.key, top.left, top.right, None
            t.node = None

    def find(self, q: Point):
        """Descend the DAG. Returns (answer, depth) with the canonical answer."""
        v = self.root
        depth = 0
        while v.kind != "leaf":  # @line L7
            depth += 1
            if v.kind == "x":
                if q == v.key:
                    return ("vertex", q), depth
                v = v.left if q < v.key else v.right  # @line L8
            else:
                o = self._above(v.key, q)
                if o == 0:
                    return ("edge", v.key), depth
                v = v.left if o > 0 else v.right  # @line L9
        t = v.trap
        return ("face", t.top, t.bottom), depth  # @line L10

    def locate(self, q: Point):
        return self.find(q)[0]

    # inspection helpers used by the tests
    def trapezoids(self) -> list[Trap]:
        out, seen, stack = [], set(), [self.root]
        while stack:
            v = stack.pop()
            if id(v) in seen:
                continue
            seen.add(id(v))
            if v.kind == "leaf":
                out.append(v.trap)
            else:
                stack.extend((v.left, v.right))
        return out

    def depth(self) -> int:
        best, stack = 0, [(self.root, 0)]
        memo: dict[int, int] = {}
        while stack:
            v, d = stack.pop()
            if memo.get(id(v), -1) >= d:
                continue
            memo[id(v)] = d
            best = max(best, d)
            if v.kind != "leaf":
                stack.append((v.left, d + 1))
                stack.append((v.right, d + 1))
        return best


def build(segments: list[Segment], seed: "int | None" = None) -> TrapezoidalMap:
    """Insert the segments in a random order (fixed by seed), or in the given order if seed is None."""
    order = list(range(len(segments)))
    if seed is not None:
        random.Random(seed).shuffle(order)
    tm = TrapezoidalMap()
    # keep the input indices: insert in the chosen order but store segments by input index
    perm_segs = [segments[i] for i in order]
    for sg in perm_segs:
        tm.insert(sg)
    remap = {new: old for new, old in enumerate(order)}
    tm.index = remap  # the input index of each stored segment
    return tm


def locate(tm: TrapezoidalMap, q: Point):
    """The canonical answer with input segment indices."""
    ans = tm.locate(q)
    m = tm.index
    if ans[0] == "edge":
        return ("edge", m[ans[1]])
    if ans[0] == "face":
        return ("face", None if ans[1] is None else m[ans[1]], None if ans[2] is None else m[ans[2]])
    return ans
