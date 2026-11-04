# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/external-memory-priority-queue/. The authors are listed in prov/Z1W9D1.jsonl.

from bisect import bisect_right, insort
from math import ceil
from typing import Any, Generic, Optional, Protocol, TypeVar, Union


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)

Item = tuple[Any, int]  # (key, insertion number): makes equal keys distinct


class Leaf:
    """A leaf block: at most B items in increasing order."""

    def __init__(self, items: list[Item]) -> None:
        self.items = items


class Node:
    """An internal node of the buffer tree, with routing items, children and
    a buffer of pending inserts. A bottom node has leaves as children."""

    def __init__(self, bottom: bool, parent: Optional["Node"] = None) -> None:
        self.bottom = bottom
        self.parent = parent
        self.routing: list[Item] = []
        self.children: list[Union["Node", Leaf]] = []
        self.buf: list[Item] = []


class ExternalMemoryPriorityQueue(Generic[K]):
    """Arge's priority queue on a buffer tree.

    The smallest items are kept in memory in `mem`; every item in `mem` is
    smaller than every item in the tree. The tree is a buffer tree with
    fan-out at most m, leaves of B items and buffers of M = m * B inserts.
    When `mem` runs empty, the buffers on the leftmost path are emptied and
    the leaves of the leftmost bottom node, up to M items, move to memory.
    N operations cost O((N/B) log_m (N/B)) I/Os; `ios` counts transfers.
    """

    def __init__(self, block_size: int = 4, fanout: int = 4) -> None:
        if block_size < 1 or fanout < 4:
            raise ValueError("need block_size >= 1 and fanout >= 4")
        self.B = block_size
        self.m = fanout
        self.M = fanout * block_size
        self.root = self._new_root()
        self.mem: list[Item] = []
        self.count = 0
        self.size = 0
        self.ios = 0

    @staticmethod
    def _new_root() -> Node:
        r = Node(bottom=True)
        r.children = [Leaf([])]
        return r

    def __len__(self) -> int:
        return self.size

    # operations ---------------------------------------------------------

    def insert(self, k: K) -> None:
        """Insert key k; equal keys come out in insertion order."""
        item: Item = (k, self.count)
        self.count += 1
        self.size += 1
        if self.mem and item < self.mem[-1]:  # @line L1
            item, self.mem[-1] = self.mem[-1], item  # @line L2
            self.mem.sort()
        self._tree_insert(item)  # @line L3

    def delete_min(self) -> K:
        """Remove and return a smallest key."""
        if not self.mem:  # @line L4
            self._refill()
        if not self.mem:  # @line L5
            raise IndexError("delete_min from an empty priority queue")
        self.size -= 1
        return self.mem.pop(0)[0]  # @line L6

    def find_min(self) -> K:
        """Return a smallest key without removing it."""
        if not self.mem:
            self._refill()
        if not self.mem:
            raise IndexError("find_min of an empty priority queue")
        return self.mem[0][0]

    def _refill(self) -> None:
        while True:  # @line L7
            x = self.root
            while not x.buf and not x.bottom:
                c = x.children[0]
                assert isinstance(c, Node)
                x = c
            if not x.buf:
                break
            self._empty(x)
        x = self.root  # @line L8
        while not x.bottom:
            c = x.children[0]
            assert isinstance(c, Node)
            x = c
        for leaf in x.children:  # @line L9
            assert isinstance(leaf, Leaf)
            self.mem.extend(leaf.items)
        self.ios += len(x.children)
        self._remove(x)  # @line L10
        while not self.root.bottom and len(self.root.children) == 1:  # @line L11
            c = self.root.children[0]
            assert isinstance(c, Node)
            c.parent = None
            self.root = c

    def _remove(self, x: Node) -> None:
        p = x.parent
        if p is None:
            self.root = self._new_root()
            return
        j = p.children.index(x)
        del p.children[j]
        if p.routing:
            del p.routing[max(j - 1, 0)]
        if not p.children:
            self._remove(p)

    # the buffer tree, inserts only ---------------------------------------

    def _tree_insert(self, item: Item) -> None:
        self.root.buf.append(item)
        if len(self.root.buf) % self.B == 0:
            self.ios += 1
        if len(self.root.buf) > self.M:
            self._empty(self.root)

    def _empty(self, x: Node) -> None:
        items, x.buf = x.buf, []
        self.ios += ceil(len(items) / self.B)
        if x.bottom:
            self._empty_bottom(x, items)
            return
        counts = [0] * len(x.children)
        for it in items:
            i = bisect_right(x.routing, it)
            child = x.children[i]
            assert isinstance(child, Node)
            child.buf.append(it)
            counts[i] += 1
        self.ios += sum(ceil(c / self.B) for c in counts)
        full = [c for c in x.children if isinstance(c, Node) and len(c.buf) > self.M]
        for c in full:
            self._empty(c)

    def _empty_bottom(self, x: Node, items: list[Item]) -> None:
        old: list[Item] = []
        for leaf in x.children:
            assert isinstance(leaf, Leaf)
            old.extend(leaf.items)
        self.ios += len(x.children)
        allitems = sorted(old + items)
        leaves: list[Union[Node, Leaf]] = [
            Leaf(allitems[i : i + self.B]) for i in range(0, len(allitems), self.B)
        ] or [Leaf([])]
        self.ios += len(leaves)
        x.children = leaves
        x.routing = [lf.items[0] for lf in leaves[1:] if isinstance(lf, Leaf)]
        if len(x.children) > self.m:
            self._split(x)

    def _split(self, x: Node) -> None:
        assert not x.buf
        c = len(x.children)
        g = ceil(c / self.m)
        q, r = divmod(c, g)
        sizes = [q + (1 if t < r else 0) for t in range(g)]
        kids, routes = x.children, x.routing
        nodes = [x] + [Node(x.bottom, x.parent) for _ in range(g - 1)]
        seps: list[Item] = []
        pos = 0
        for t, y in enumerate(nodes):
            y.children = kids[pos : pos + sizes[t]]
            y.routing = routes[pos : pos + sizes[t] - 1]
            if t > 0:
                seps.append(routes[pos - 1])
            for ch in y.children:
                if isinstance(ch, Node):
                    ch.parent = y
            pos += sizes[t]
        self.ios += g
        p = x.parent
        if p is None:
            p = Node(bottom=False)
            p.children = [x]
            self.root = p
            for y in nodes:
                y.parent = p
        j = p.children.index(x)
        p.children[j + 1 : j + 1] = nodes[1:]
        p.routing[j:j] = seps
        if len(p.children) > self.m:
            self._split(p)

    # checking -----------------------------------------------------------

    def tree_items(self) -> list[Item]:
        """All items in the tree, in leaves or buffers, in no fixed order."""
        out: list[Item] = []

        def walk(x: Union[Node, Leaf]) -> None:
            if isinstance(x, Leaf):
                out.extend(x.items)
            else:
                out.extend(x.buf)
                for c in x.children:
                    walk(c)

        walk(self.root)
        return out

    def check_invariant(self) -> None:
        """Raise AssertionError if a property of the queue fails."""
        assert self.mem == sorted(self.mem)
        rest = self.tree_items()
        assert len(rest) + len(self.mem) == self.size
        if self.mem and rest:
            assert self.mem[-1] < min(rest)
        depths: set[int] = set()

        def walk(x: Node, lo: Any, hi: Any, depth: int) -> None:
            assert len(x.children) == len(x.routing) + 1 <= self.m
            assert all(a < b for a, b in zip(x.routing, x.routing[1:]))
            assert len(x.buf) <= self.M
            for it in x.buf:
                assert (lo is None or not (it < lo)) and (hi is None or it < hi)
            bounds = [lo, *x.routing, hi]
            for j, c in enumerate(x.children):
                if x.bottom:
                    assert isinstance(c, Leaf) and len(c.items) <= self.B
                    assert c.items == sorted(c.items)
                    for it in c.items:
                        assert bounds[j] is None or not (it < bounds[j])
                        assert bounds[j + 1] is None or it < bounds[j + 1]
                    depths.add(depth)
                else:
                    assert isinstance(c, Node) and c.parent is x
                    walk(c, bounds[j], bounds[j + 1], depth + 1)

        assert self.root.parent is None
        walk(self.root, None, None, 0)
        assert len(depths) == 1
