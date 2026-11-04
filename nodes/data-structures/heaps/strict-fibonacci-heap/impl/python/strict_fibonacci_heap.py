# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/strict-fibonacci-heap/. The authors are listed in prov/V45MQ4.jsonl.

"""Strict Fibonacci heap after Brodal, Lagogiannis and Tarjan (STOC 2012), simplified.

This follows the abstract structure of Sections 2 to 4 of the paper: one
heap-ordered tree, active and passive nodes with a shared flag, rank and loss,
the queue Q, and the five transformations. It does not build the pointer-level
fix-list and rank-list of Section 6. It finds the transformations with sets
and short scans of the children of the root, so an operation takes O(log n)
time in the worst case here, not O(1).
"""

import math
from typing import Any, Dict, Generic, List, Optional, Set, Tuple, TypeVar

K = TypeVar("K")


class Record:
    """The shared active record: a node is active if its record has flag True."""

    __slots__ = ("flag",)

    def __init__(self) -> None:
        self.flag = True


class Item(Generic[K]):
    """A handle: the item with its key, and the node that holds it now."""

    __slots__ = ("key", "uid", "node", "minus_inf")
    _next = 0

    def __init__(self, key: K) -> None:
        self.key = key
        Item._next += 1
        self.uid = Item._next
        self.node: Optional["Node[K]"] = None
        self.minus_inf = False

    def order(self) -> Tuple[Any, ...]:
        """Distinct keys: ties are broken by the item identifier."""
        return (0, self.uid) if self.minus_inf else (1, self.key, self.uid)


class Node(Generic[K]):
    __slots__ = ("item", "parent", "children", "rec", "rank", "loss", "qprev", "qnext")

    def __init__(self, item: Item[K]) -> None:
        self.item = item
        item.node = self
        self.parent: Optional[Node[K]] = None
        self.children: List[Node[K]] = []  # left to right
        self.rec: Optional[Record] = None
        self.rank = 0
        self.loss = 0
        self.qprev: Node[K] = self
        self.qnext: Node[K] = self

    @property
    def active(self) -> bool:
        return self.rec is not None and self.rec.flag

    def key(self) -> Tuple[Any, ...]:
        return self.item.order()


class StrictFibonacciHeap(Generic[K]):
    def __init__(self) -> None:
        self.root: Optional[Node[K]] = None
        self.n = 0
        self.rec = Record()
        self.qhead: Optional[Node[K]] = None
        self.aroots: Set[Node[K]] = set()  # active roots
        self.lossy: Set[Node[K]] = set()  # active nodes with positive loss
        self.counts: Dict[str, int] = {}

    def __len__(self) -> int:
        return self.n

    # -- helpers -------------------------------------------------------------

    def _count(self, name: str) -> None:
        self.counts[name] = self.counts.get(name, 0) + 1

    def _is_aroot(self, x: Node[K]) -> bool:
        return x.active and x.parent is not None and not x.parent.active

    def _cut(self, x: Node[K]) -> Node[K]:
        """Remove x from the child list of its parent and return the parent."""
        p = x.parent
        assert p is not None
        p.children.remove(x)
        x.parent = None
        return p

    def _link(self, x: Node[K], y: Node[K]) -> None:
        """Make x a child of y: leftmost if x is active, rightmost if passive."""
        if x.parent is not None:
            self._cut(x)
        x.parent = y
        if x.active:
            y.children.insert(0, x)
        else:
            y.children.append(x)

    def _set_loss(self, x: Node[K], loss: int) -> None:
        x.loss = loss
        if loss > 0 and x.active:
            self.lossy.add(x)
        else:
            self.lossy.discard(x)

    def _refresh_aroot(self, x: Node[K]) -> None:
        if self._is_aroot(x):
            self.aroots.add(x)
        else:
            self.aroots.discard(x)

    @staticmethod
    def _linkable(x: Node[K]) -> bool:
        return not x.active and (not x.children or not x.children[0].active)

    # -- the queue Q ---------------------------------------------------------

    @staticmethod
    def _concat(a: Optional[Node[K]], b: Optional[Node[K]]) -> Optional[Node[K]]:
        if a is None:
            return b
        if b is None:
            return a
        at, bt = a.qprev, b.qprev
        at.qnext, b.qprev = b, at
        bt.qnext, a.qprev = a, bt
        return a

    def _q_remove(self, x: Node[K]) -> None:
        if x.qnext is x:
            self.qhead = None
        else:
            x.qprev.qnext, x.qnext.qprev = x.qnext, x.qprev
            if self.qhead is x:
                self.qhead = x.qnext
        x.qprev = x.qnext = x

    # -- transformations -----------------------------------------------------

    def _active_root_reduction(self) -> bool:
        """Link two active roots of equal rank."""
        by_rank: Dict[int, Node[K]] = {}
        for a in self.aroots:
            b = by_rank.get(a.rank)
            if b is None:
                by_rank[a.rank] = a
                continue
            self._count("active-root")
            x, y = (a, b) if a.key() < b.key() else (b, a)
            self._link(y, x)
            x.rank += 1
            self.aroots.discard(y)
            z = x.children[-1]
            if not z.active:
                assert self.root is not None
                self._link(z, self.root)
            return True
        return False

    def _root_degree_reduction(self) -> bool:
        """Make three passive linkable children of the root into two active nodes."""
        root = self.root
        assert root is not None
        cand = [c for c in reversed(root.children) if self._linkable(c)][:3]
        if len(cand) < 3:
            return False
        self._count("root-degree")
        x, y, z = sorted(cand, key=lambda v: v.key())
        x.rec = y.rec = self.rec
        x.rank, y.rank = 0, 0
        self._link(z, y)
        self._link(y, x)
        x.rank = 1
        self._link(x, root)  # x is active, so it becomes the leftmost child
        self._set_loss(x, 0)
        self._set_loss(y, 0)
        self.aroots.add(x)
        return True

    def _loss_reduction(self) -> bool:
        """One-node or two-node loss reduction, if possible."""
        by_rank: Dict[int, Node[K]] = {}
        for x in list(self.lossy):
            if x.loss >= 2:
                self._count("one-node-loss")
                y = self._cut(x)
                assert self.root is not None
                self._link(x, self.root)
                self._set_loss(x, 0)
                self.aroots.add(x)
                y.rank -= 1
                if not self._is_aroot(y):
                    self._set_loss(y, y.loss + 1)
                return True
        for x in list(self.lossy):
            other = by_rank.get(x.rank)
            if other is None:
                by_rank[x.rank] = x
                continue
            self._count("two-node-loss")
            a, b = (x, other) if x.key() < other.key() else (other, x)
            z = self._cut(b)
            self._link(b, a)
            a.rank += 1
            self._set_loss(a, 0)
            self._set_loss(b, 0)
            # The old parent z is updated last: z may be a itself.
            z.rank -= 1
            if not self._is_aroot(z):
                self._set_loss(z, z.loss + 1)
            return True
        return False

    def _reductions(self, arr: int, rdr: int) -> None:
        """Do up to arr active root reductions and rdr root degree reductions."""
        while arr > 0 or rdr > 0:
            done = False
            if arr > 0 and self._active_root_reduction():
                arr -= 1
                done = True
            if rdr > 0 and self._root_degree_reduction():
                rdr -= 1
                done = True
            if not done:
                return

    # -- operations ----------------------------------------------------------

    def insert(self, key: K) -> Item[K]:
        """Insert key and return its handle."""
        it: Item[K] = Item(key)
        other: StrictFibonacciHeap[K] = StrictFibonacciHeap()
        other.root = Node(it)  # @line L1
        other.n = 1
        self.meld(other)
        return it

    def meld(self, other: "StrictFibonacciHeap[K]") -> None:
        """Move all items of other into this heap. other becomes empty."""
        if other.root is None:
            return
        if self.root is None:
            self.root, self.n, self.rec, self.qhead = other.root, other.n, other.rec, other.qhead
            self.aroots, self.lossy = other.aroots, other.lossy
        else:
            big, small = (self, other) if other.n <= self.n else (other, self)
            small.rec.flag = False  # @line L2
            rx, ry = small.root, big.root
            assert rx is not None and ry is not None
            u, v = (rx, ry) if rx.key() < ry.key() else (ry, rx)
            v.parent = None
            self._link_root(v, u)  # @line L3
            vq: Node[K] = v
            v.qprev = v.qnext = v
            q = self._concat(self._concat(small.qhead, vq), big.qhead)
            self.root, self.n, self.rec, self.qhead = u, self.n + other.n, big.rec, q
            self.aroots, self.lossy = big.aroots, big.lossy
            for a in [a for a in self.aroots if a.parent is v or a.parent is u]:
                self._refresh_aroot(a)
            self._reductions(1, 1)  # @line L4
        other.root, other.n, other.qhead = None, 0, None
        other.rec, other.aroots, other.lossy = Record(), set(), set()

    def _link_root(self, v: Node[K], u: Node[K]) -> None:
        v.parent = u
        if v.active:
            u.children.insert(0, v)
        else:
            u.children.append(v)

    def find_min(self) -> K:
        """Return the smallest key, stored at the root."""
        if self.root is None:
            raise IndexError("the heap is empty")
        return self.root.item.key  # @line L5

    def decrease_key(self, it: Item[K], key: K) -> None:
        """Lower the key of the item it to key."""
        if key > it.key:  # type: ignore[operator]
            raise ValueError("new key is larger than the current key")
        it.key = key  # @line L6
        self._after_decrease(it)

    def _after_decrease(self, it: Item[K]) -> None:
        x, z = it.node, self.root
        assert x is not None and z is not None
        if x is z:
            return
        if x.key() < z.key():
            x.item, z.item = z.item, x.item
            x.item.node, z.item.node = x, z
        y = x.parent
        assert y is not None
        was_inner_active = x.active and y.active
        if y is not z:
            self._link(x, z)  # @line L7
        if was_inner_active:  # @line L8
            self._set_loss(x, 0)
            self.aroots.add(x)
            y.rank -= 1
            if not self._is_aroot(y):
                self._set_loss(y, y.loss + 1)
        self._loss_reduction()  # @line L9
        self._reductions(6, 4)

    def delete(self, it: Item[K]) -> None:
        """Delete the item it: decrease its key to minus infinity, then delete-min."""
        it.minus_inf = True
        self._after_decrease(it)
        self.delete_min()

    def delete_min(self) -> K:
        """Remove and return the smallest key."""
        z = self.root
        if z is None:
            raise IndexError("the heap is empty")
        key = z.item.key
        z.item.node = None
        self.n -= 1
        if not z.children:
            self.root = None
            self.qhead = None
            self.aroots, self.lossy = set(), set()
            return key
        x = min(z.children, key=lambda c: c.key())  # @line L10
        if x.active:
            self.aroots.discard(x)
            self.lossy.discard(x)
            x.rec = None
        z.children.remove(x)
        x.parent = None
        for c in x.children:
            if c.active:
                self._set_loss(c, 0)
                self.aroots.add(c)
        for c in list(z.children):
            c.parent = None
            self._link_root(c, x)  # @line L11
            self._refresh_aroot(c)
        z.children = []
        self._q_remove(x)
        self.root = x
        for _ in range(2):  # @line L12
            if self.qhead is None:
                break
            y = self.qhead
            self.qhead = y.qnext
            for c in [c for c in y.children[-2:] if not c.active]:
                self._link(c, x)
                self._refresh_aroot(c)
        self._loss_reduction()  # @line L13
        while self._active_root_reduction() or self._root_degree_reduction():  # @line L14
            pass
        return key

    # -- checking ------------------------------------------------------------

    def nodes(self) -> List[Node[K]]:
        out: List[Node[K]] = []
        stack = [self.root] if self.root is not None else []
        while stack:
            v = stack.pop()
            out.append(v)
            stack.extend(v.children)
        return out

    def check_invariant(self) -> None:
        """Check heap order, the queue, the sets, and the invariants I1 to I4 of the paper."""
        if self.root is None:
            assert self.n == 0 and self.qhead is None
            return
        root = self.root
        nodes = self.nodes()
        assert len(nodes) == self.n and root.parent is None and not root.active
        pos: Dict[Node[K], int] = {}
        if self.qhead is not None:
            v, p = self.qhead, 1
            while True:
                pos[v] = p
                assert v.qnext.qprev is v
                v, p = v.qnext, p + 1
                if v is self.qhead:
                    break
        assert set(pos) == set(nodes) - {root}
        total_loss = 0
        R = 2 * math.log2(self.n) + 6
        for v in nodes:
            assert v.item.node is v
            seen_passive = False
            act = 0
            for c in v.children:
                assert c.parent is v and v.key() < c.key()
                if c.active:
                    assert not seen_passive, "I1: active children must be left of passive ones"
                    act += 1
                else:
                    seen_passive = True
            if v.active:
                assert v.rank == act
                total_loss += v.loss
                assert (v in self.lossy) == (v.loss > 0)
                actives = [c for c in v.children if c.active]
                for i, c in enumerate(reversed(actives), start=1):
                    assert c.rank + c.loss >= i - 1, "I1: rank + loss of the i-th active child"
                if self._is_aroot(v):
                    assert v.loss == 0 and v in self.aroots
            else:
                assert v not in self.aroots and v not in self.lossy
            if v is not root:
                bound = 2 * math.log2(2 * self.n - pos[v]) + 9
                if v.active and v.loss == 0:
                    bound += 1
                assert len(v.children) <= bound, "I4: degree"
        assert all(a.active for a in self.aroots) and all(a.active for a in self.lossy)
        assert len(self.aroots) <= R + 1, "I2"
        assert total_loss <= R + 1, "I3"
        assert len(root.children) <= R + 3, "I4: root degree"
