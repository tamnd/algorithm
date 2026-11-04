# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hollow-heap/. The authors are listed in prov/AQJK5W.jsonl.

from typing import Any, Generic, Optional, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)
V = TypeVar("V")


class Item(Generic[K, V]):
    """A handle to a value in a hollow heap; node is the full node holding it."""

    __slots__ = ("value", "node")

    def __init__(self, value: V) -> None:
        self.value = value
        self.node: Optional["Node[K, V]"] = None


class Node(Generic[K, V]):
    """A node of the DAG. A node is full if item is set, and hollow else.

    child is the first child; next is the next sibling. A node with two
    parents has ep, its extra (second) parent, and it is the last child of ep.
    """

    __slots__ = ("item", "key", "rank", "child", "next", "ep")

    def __init__(self, item: Item[K, V], key: K) -> None:
        self.item: Optional[Item[K, V]] = item
        self.key = key
        self.rank = 0
        self.child: Optional[Node[K, V]] = None
        self.next: Optional[Node[K, V]] = None
        self.ep: Optional[Node[K, V]] = None
        item.node = self


def _add_child(w: Node[K, V], v: Node[K, V]) -> None:
    w.next = v.child
    v.child = w


def _link(v: Node[K, V], w: Node[K, V]) -> Node[K, V]:
    if not v.key < w.key:  # @line L1
        _add_child(v, w)  # @line L2
        return w
    _add_child(w, v)  # @line L3
    return v


def _children(x: Node[K, V]) -> list[Node[K, V]]:
    out = []
    w = x.child
    while w is not None:
        out.append(w)
        if w.ep is x:
            break
        w = w.next
    return out


class HollowHeap(Generic[K, V]):
    """The one-root hollow heap of Hansen, Kaplan, Tarjan and Zwick.

    insert, meld, find_min and decrease_key take O(1) time in the worst case;
    delete and delete_min take O(log N) amortized time, where N is the
    number of nodes ever made. Keys need only "<".
    """

    def __init__(self) -> None:
        self.root: Optional[Node[K, V]] = None
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def insert(self, value: V, key: K) -> Item[K, V]:
        e: Item[K, V] = Item(value)
        u = Node(e, key)  # @line L4
        self.root = u if self.root is None else _link(u, self.root)  # @line L5
        self.size += 1
        return e

    def meld(self, other: "HollowHeap[K, V]") -> None:
        if other.root is not None:
            self.root = other.root if self.root is None else _link(self.root, other.root)  # @line L6
        self.size += other.size
        other.root, other.size = None, 0

    def find_min(self) -> tuple[V, K]:
        if self.root is None or self.root.item is None:
            raise IndexError("find_min from an empty heap")
        return self.root.item.value, self.root.key

    def decrease_key(self, e: Item[K, V], k: K) -> None:
        u = e.node
        if u is None:
            raise KeyError("item not in the heap")
        if u.key < k:
            raise ValueError("new key is larger than the current key")
        assert self.root is not None
        if u is self.root:  # @line L7
            u.key = k
            return
        v = Node(e, k)  # @line L8
        u.item = None  # @line L9
        v.rank = max(0, u.rank - 2)  # @line L10
        v.child = u  # @line L11
        u.ep = v
        self.root = _link(v, self.root)  # @line L12

    def delete_min(self) -> tuple[V, K]:
        if self.root is None:
            raise IndexError("delete_min from an empty heap")
        assert self.root.item is not None
        e = self.root.item
        key = self.root.key
        self.delete(e)
        return e.value, key

    def delete(self, e: Item[K, V]) -> None:
        u = e.node
        if u is None:
            raise KeyError("item not in the heap")
        u.item = None  # @line L13
        e.node = None
        self.size -= 1
        assert self.root is not None
        if self.root.item is not None:  # @line L14
            return
        ranks: dict[int, Node[K, V]] = {}
        h: Optional[Node[K, V]] = self.root  # @line L15
        h.next = None
        while h is not None:  # @line L16
            w = h.child
            x = h
            h = h.next
            while w is not None:  # @line L17
                u = w
                w = w.next
                if u.item is None:  # @line L18
                    if u.ep is None:  # @line L19
                        u.next = h
                        h = u
                    else:  # @line L20
                        if u.ep is x:
                            w = None
                        else:
                            u.next = None
                        u.ep = None
                else:
                    while u.rank in ranks:  # @line L21
                        u = _link(u, ranks.pop(u.rank))  # @line L22
                        u.rank += 1
                    ranks[u.rank] = u  # @line L23
            x.child = None  # @line L24
            x.next = None
        root: Optional[Node[K, V]] = None
        for r in sorted(ranks):  # @line L25
            t = ranks[r]
            t.next = None
            root = t if root is None else _link(t, root)  # @line L26
        self.root = root

    def check_invariant(self) -> None:
        full = 0
        if self.root is None:
            assert self.size == 0
            return
        assert self.root.item is not None
        seen: set[int] = set()
        stack = [self.root]
        parents: dict[int, int] = {}
        while stack:
            x = stack.pop()
            if id(x) in seen:
                continue
            seen.add(id(x))
            if x.item is not None:
                full += 1
                assert x.item.node is x
            assert x.rank >= 0
            for c in _children(x):
                assert not c.key < x.key
                parents[id(c)] = parents.get(id(c), 0) + 1
                stack.append(c)
        assert full == self.size
        for c, p in parents.items():
            assert p <= 2
