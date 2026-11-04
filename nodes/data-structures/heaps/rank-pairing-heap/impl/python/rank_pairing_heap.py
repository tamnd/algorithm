# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rank-pairing-heap/. The authors are listed in prov/Q9AZES.jsonl.

from typing import Any, Generic, Optional, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class Node(Generic[K]):
    """A node of a half-ordered half tree.

    left and right are the binary children; parent is the binary parent, or
    None for a root. next links the roots in the root list.
    """

    __slots__ = ("key", "rank", "left", "right", "parent", "next")

    def __init__(self, key: K) -> None:
        self.key = key
        self.rank = 0
        self.left: Optional[Node[K]] = None
        self.right: Optional[Node[K]] = None
        self.parent: Optional[Node[K]] = None
        self.next: Optional[Node[K]] = None


def _rank(x: "Optional[Node[Any]]") -> int:
    return -1 if x is None else x.rank


def type2_rank(v: "Optional[Node[Any]]", w: "Optional[Node[Any]]") -> int:
    """The rank that the type-2 rank rule gives a non-root with children v and w."""
    a, b = _rank(v), _rank(w)
    return max(a, b) if abs(a - b) > 1 else max(a, b) + 1


class RankPairingHeap(Generic[K]):
    """Type-2 rank-pairing heap of Haeupler, Sen and Tarjan, with multipass linking."""

    def __init__(self) -> None:
        self.head: Optional[Node[K]] = None
        self.tail: Optional[Node[K]] = None
        self.min: Optional[Node[K]] = None
        self.n = 0
        self.links = 0
        self.rank_steps = 0

    def __len__(self) -> int:
        return self.n

    def _add_root(self, x: Node[K]) -> None:
        x.parent, x.next = None, None
        if self.tail is None:
            self.head = self.tail = x
        else:
            self.tail.next = x
            self.tail = x
        if self.min is None or x.key < self.min.key:
            self.min = x

    def _link(self, x: Node[K], y: Node[K]) -> Node[K]:
        """Link two half trees of equal rank; the root with the smaller key wins."""
        self.links += 1
        if y.key < x.key:  # @line L1
            x, y = y, x
        y.right = x.left  # @line L2
        if y.right is not None:
            y.right.parent = y
        x.left, y.parent = y, x
        x.rank += 1
        return x

    def insert(self, key: K) -> Node[K]:
        """Add key and return its node, for decrease_key."""
        x = Node(key)
        self._add_root(x)  # @line L3
        self.n += 1
        return x

    def meld(self, other: "RankPairingHeap[K]") -> None:
        """Move all items of other into this heap in O(1) time."""
        if other.head is None:
            return
        if self.tail is None:
            self.head, self.tail, self.min = other.head, other.tail, other.min
        else:
            self.tail.next = other.head
            self.tail = other.tail
            assert self.min is not None and other.min is not None
            if other.min.key < self.min.key:
                self.min = other.min
        self.n += other.n
        other.head = other.tail = other.min = None
        other.n = 0

    def find_min(self) -> K:
        if self.min is None:
            raise IndexError("find_min on an empty heap")
        return self.min.key

    def delete_min(self) -> K:
        """Remove and return a smallest key."""
        z = self.min
        if z is None:
            raise IndexError("delete_min on an empty heap")
        trees: list[Node[K]] = []
        s = z.left  # @line L4
        while s is not None:  # disassemble the right spine of z.left
            nxt = s.right
            s.right = None
            s.rank = _rank(s.left) + 1
            trees.append(s)
            s = nxt
        r = self.head
        while r is not None:
            nxt = r.next
            if r is not z:
                trees.append(r)
            r = nxt
        buckets: dict[int, Node[K]] = {}
        for x in trees:
            x.parent = x.next = None
            while x.rank in buckets:  # @line L5
                x = self._link(x, buckets.pop(x.rank))
            buckets[x.rank] = x  # @line L6
        self.head = self.tail = self.min = None
        for k in sorted(buckets):  # @line L7
            self._add_root(buckets[k])
        self.n -= 1
        return z.key

    def decrease_key(self, x: Node[K], key: K) -> None:
        """Lower the key of node x to key, which must not be larger."""
        if x.key < key:
            raise ValueError("new key is larger")
        x.key = key  # @line L8
        if x.parent is None:
            assert self.min is not None
            if key < self.min.key:
                self.min = x
            return
        u, y = x.parent, x.right  # @line L9
        if u.left is x:
            u.left = y
        else:
            u.right = y
        if y is not None:
            y.parent = u
        x.right = None
        x.rank = _rank(x.left) + 1
        self._add_root(x)
        while u is not None:  # @line L10
            self.rank_steps += 1
            if u.parent is None:  # @line L11
                u.rank = _rank(u.left) + 1
                return
            k = type2_rank(u.left, u.right)  # @line L12
            if k >= u.rank:  # @line L13
                return
            u.rank = k  # @line L14
            u = u.parent

    def roots(self) -> list[Node[K]]:
        out = []
        r = self.head
        while r is not None:
            out.append(r)
            r = r.next
        return out

    def check_invariant(self) -> None:
        """Check half order, the type-2 rank rule, the pointers and the size bound."""
        fib = [0, 1]
        while len(fib) < 100:
            fib.append(fib[-1] + fib[-2])
        count = 0
        best: Optional[Node[K]] = None
        for root in self.roots():
            assert root.parent is None and root.right is None
            assert root.rank == _rank(root.left) + 1, "a root must be a 1-node"
            if best is None or root.key < best.key:
                best = root
            order: list[Node[K]] = []
            stack: list[Node[K]] = [root]
            while stack:
                v = stack.pop()
                order.append(v)
                for c in (v.left, v.right):
                    if c is not None:
                        assert c.parent is v
                        stack.append(c)
            size: dict[int, int] = {}
            for v in reversed(order):
                s = 1 + sum(size[id(c)] for c in (v.left, v.right) if c is not None)
                size[id(v)] = s
                if v is not root:
                    d = sorted((v.rank - _rank(v.left), v.rank - _rank(v.right)))
                    assert d in ([1, 1], [1, 2]) or (d[0] == 0 and d[1] > 1), f"rank rule {d}"
                    assert s >= fib[v.rank + 3] - 1, "size bound"
            count += len(order)
            # half order: a key is at most every key in its left subtree
            stack = [root]
            while stack:
                v = stack.pop()
                if v.left is not None:
                    sub = [v.left]
                    while sub:
                        w = sub.pop()
                        assert not (w.key < v.key), "half order"
                        sub.extend(c for c in (w.left, w.right) if c is not None)
                stack.extend(c for c in (v.left, v.right) if c is not None)
        assert count == self.n
        if best is None:
            assert self.min is None
        else:
            assert self.min is not None and not (best.key < self.min.key)
