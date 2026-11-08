# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-convex-hull/. The authors are listed in prov/WCEQ10.jsonl.

from __future__ import annotations

import random
from fractions import Fraction
from typing import Optional

Point = tuple[int, int]


def orient(p: Point, q: Point, r: Point) -> int:
    """Twice the signed area of the triangle pqr: positive for a left turn, zero when collinear."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


class Chain:
    """A node of a persistent treap that stores one hull chain in lexicographic order.

    Nodes are never changed after they are made, so many chains can share them.
    lo and hi are the first and the last point of the subtree.
    """

    __slots__ = ("p", "prio", "left", "right", "lo", "hi")

    def __init__(self, p: Point, prio: int, left: Optional[Chain], right: Optional[Chain]) -> None:
        self.p, self.prio, self.left, self.right = p, prio, left, right
        self.lo = left.lo if left else p
        self.hi = right.hi if right else p


def chain_upto(t: Optional[Chain], key: Point) -> Optional[Chain]:
    """The points of t that are <= key, by path copying."""
    if t is None:
        return None
    if t.p <= key:
        return Chain(t.p, t.prio, t.left, chain_upto(t.right, key))
    return chain_upto(t.left, key)


def chain_from(t: Optional[Chain], key: Point) -> Optional[Chain]:
    """The points of t that are >= key, by path copying."""
    if t is None:
        return None
    if t.p >= key:
        return Chain(t.p, t.prio, chain_from(t.left, key), t.right)
    return chain_from(t.right, key)


def chain_concat(a: Optional[Chain], b: Optional[Chain]) -> Optional[Chain]:
    """Concatenate two chains; every point of a comes before every point of b."""
    if a is None:
        return b
    if b is None:
        return a
    if a.prio > b.prio:
        return Chain(a.p, a.prio, a.left, chain_concat(a.right, b))
    return Chain(b.p, b.prio, chain_concat(a, b.left), b.right)


def chain_points(t: Optional[Chain]) -> list[Point]:
    """The points of a chain in order, without recursion."""
    out: list[Point] = []
    stack: list[Chain] = []
    while stack or t is not None:
        while t is not None:
            stack.append(t)
            t = t.left
        t = stack.pop()
        out.append(t.p)
        t = t.right
    return out


def bridge(a_root: Chain, b_root: Chain, s: int) -> tuple[Point, Point]:
    """The bridge of two chains A and B, every point of A before every point of B.

    For s = +1 the chains are upper hulls, for s = -1 lower hulls. Cost: O(depth A + depth B).
    """
    alpha, a_pred, a_succ = a_root, None, None  # subtree of A, and its outside neighbors
    beta, b_pred, b_succ = b_root, None, None
    r0 = b_root.lo  # @line L18
    while True:  # @line L19
        assert alpha is not None and beta is not None
        a, b = alpha.p, beta.p  # @line L20
        am = alpha.left.hi if alpha.left else a_pred
        ap = alpha.right.lo if alpha.right else a_succ
        bm = beta.left.hi if beta.left else b_pred
        bp = beta.right.lo if beta.right else b_succ
        a_left = am is not None and s * orient(a, b, am) >= 0
        b_right = bp is not None and s * orient(a, b, bp) >= 0
        if a_left or b_right:  # @line L21
            if a_left:  # @line L22
                alpha, a_succ = alpha.left, a
            if b_right:  # @line L23
                beta, b_pred = beta.right, b
            continue
        a_up = ap is not None and s * orient(a, b, ap) > 0
        b_up = bm is not None and s * orient(a, b, bm) > 0
        if not a_up and not b_up:  # @line L24
            return a, b
        if not b_up:  # @line L25
            alpha, a_pred = alpha.right, a
        elif not a_up:  # @line L26
            beta, b_succ = beta.left, b
        else:
            assert ap is not None and bm is not None
            d1 = (ap[0] - a[0], ap[1] - a[1])  # @line L27
            d2 = (b[0] - bm[0], b[1] - bm[1])
            den = d1[0] * d2[1] - d1[1] * d2[0]
            t = Fraction((bm[0] - a[0]) * d2[1] - (bm[1] - a[1]) * d2[0], den)
            z = (a[0] + t * d1[0], a[1] + t * d1[1])
            if z < r0:
                alpha, a_pred = alpha.right, a
            else:
                beta, b_succ = beta.left, b


def merge(a: Optional[Chain], b: Optional[Chain], s: int) -> Optional[Chain]:
    """The hull chain of A and B together; every point of A comes before every point of B."""
    if a is None or b is None:  # @line L15
        return a if b is None else b
    l, r = bridge(a, b, s)  # @line L16
    return chain_concat(chain_upto(a, l), chain_from(b, r))  # @line L17


class Node:
    """A node of the base treap over the points, with the two hull chains of its subtree."""

    __slots__ = ("p", "prio", "left", "right", "up", "low", "size")

    def __init__(self, p: Point, prio: int, left: Optional[Node], right: Optional[Node]) -> None:
        self.p, self.prio, self.left, self.right = p, prio, left, right
        single = Chain(p, prio, None, None)
        self.up = merge(merge(left.up if left else None, single, 1), right.up if right else None, 1)  # @line L13
        self.low = merge(merge(left.low if left else None, single, -1), right.low if right else None, -1)
        self.size = 1 + (left.size if left else 0) + (right.size if right else 0)  # @line L14


def split(t: Optional[Node], p: Point) -> tuple[Optional[Node], Optional[Node]]:
    """The points of t before p and after p, as two treaps; p itself is dropped."""
    if t is None:  # @line L6
        return None, None
    if t.p < p:  # @line L7
        x, y = split(t.right, p)
        return Node(t.p, t.prio, t.left, x), y
    if t.p > p:  # @line L8
        x, y = split(t.left, p)
        return x, Node(t.p, t.prio, y, t.right)
    return t.left, t.right  # @line L9


def join(x: Optional[Node], y: Optional[Node]) -> Optional[Node]:
    """Join two treaps; every point of x comes before every point of y."""
    if x is None or y is None:  # @line L10
        return x if y is None else y
    if x.prio > y.prio:  # @line L11
        return Node(x.p, x.prio, x.left, join(x.right, y))
    return Node(y.p, y.prio, join(x, y.left), y.right)  # @line L12


class DynamicConvexHull:
    """The convex hull of a set of points under insertions and deletions.

    The points are kept in a treap ordered lexicographically. Every treap node stores the upper and
    the lower hull chain of its subtree as persistent treaps, and a node's chains are built from
    those of its children by two bridge searches. Coordinates must be int so that every test is
    exact. Cost: O(log^2 n) expected time per insert or delete, O(log n) expected for contains,
    O(h) for hull; O(n log n) expected space. The recursion depth is O(log n) expected.
    """

    def __init__(self, seed: int = 0) -> None:
        self.root: Optional[Node] = None
        self.rng = random.Random(seed)

    def __len__(self) -> int:
        return self.root.size if self.root else 0

    def __contains__(self, p: Point) -> bool:
        t = self.root
        while t is not None:
            if p == t.p:
                return True
            t = t.left if p < t.p else t.right
        return False

    def insert(self, p: Point) -> bool:
        """Add p. Returns False, and changes nothing, if p is already in the set."""
        if p in self:  # @line L1
            return False
        x, y = split(self.root, p)  # @line L2
        self.root = join(join(x, Node(p, self.rng.getrandbits(62), None, None)), y)  # @line L3
        return True

    def delete(self, p: Point) -> bool:
        """Remove p. Returns False, and changes nothing, if p is not in the set."""
        if p not in self:
            return False
        x, y = split(self.root, p)  # @line L4
        self.root = join(x, y)  # @line L5
        return True

    def hull(self) -> list[Point]:
        """The hull vertices, counterclockwise from the lexicographically smallest point.

        Only strictly convex vertices are returned. With all points on one line the result is the
        two end points, one point for a single point, and nothing for the empty set.
        """
        if self.root is None:
            return []
        low = chain_points(self.root.low)  # @line L28
        up = chain_points(self.root.up)
        return low + up[-2:0:-1]

    def check_invariant(self) -> None:
        """Check the treap order, the heap order and every stored chain against a direct computation.

        Cost: O(n^2) time; meant for tests.
        """
        if self.root is None:
            return
        order: list[tuple[Node, int]] = [(self.root, 0)]
        done: dict[int, list[Point]] = {}
        while order:
            t, state = order.pop()
            if state == 0:
                order.append((t, 1))
                for c in (t.left, t.right):
                    if c is not None:
                        assert c.prio <= t.prio
                        order.append((c, 0))
                continue
            left = done.pop(id(t.left), []) if t.left else []
            right = done.pop(id(t.right), []) if t.right else []
            assert all(q < t.p for q in left) and all(q > t.p for q in right)
            pts = left + [t.p] + right
            assert t.size == len(pts)
            lower, upper = monotone_chains(pts)
            for c, want in ((t.low, lower), (t.up, upper)):
                assert chain_points(c) == want
                check_chain(c)
            done[id(t)] = pts


def monotone_chains(pts: list[Point]) -> tuple[list[Point], list[Point]]:
    """Lower and upper hull chains of distinct sorted points, by Andrew's monotone chain."""
    lower: list[Point] = []
    upper: list[Point] = []
    for p in pts:
        while len(lower) >= 2 and orient(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
        while len(upper) >= 2 and orient(upper[-2], upper[-1], p) >= 0:
            upper.pop()
        upper.append(p)
    return lower, upper


def check_chain(t: Optional[Chain]) -> None:
    """Check the order, the heap order and the stored first and last points of a chain treap."""
    stack = [t] if t else []
    while stack:
        c = stack.pop()
        pts = chain_points(c)
        assert c.lo == pts[0] and c.hi == pts[-1]
        assert pts == sorted(pts) and len(set(pts)) == len(pts)
        for k in (c.left, c.right):
            if k is not None:
                assert k.prio <= c.prio
                stack.append(k)
