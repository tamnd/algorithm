# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/b-star-tree/. The authors are listed in prov/FES1ZP.jsonl.

from bisect import bisect_left, bisect_right, insort
from typing import Any, Generic, Optional, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class Node(Generic[K]):
    """A leaf holds keys and a link to the next leaf. An internal node holds
    separators key[0..m-1] and children c[0..m], where c[i] holds the keys k
    with key[i-1] <= k < key[i]."""

    def __init__(self, leaf: bool) -> None:
        self.leaf = leaf
        self.keys: list[K] = []
        self.children: list["Node[K]"] = []
        self.next: Optional["Node[K]"] = None


def entries(x: Node[Any]) -> int:
    """The keys of a leaf, or the children of an internal node."""
    return len(x.keys) if x.leaf else len(x.children)


class BStarTree(Generic[K]):
    """A B*-tree in the B+ form: all keys are in linked leaves.

    Each node other than the root has f to C entries, where C >= 4 is the
    capacity and f = floor((2C + 1) / 3), so every such node is about two
    thirds full. The root may hold up to R = 2f - 1 entries. An overflow
    first shifts entries into a sibling that has room, and only when the
    sibling is full splits the two nodes into three. An underflow borrows
    from a sibling, or merges three nodes into two. `reads` counts node
    reads; the root is kept in memory.
    """

    def __init__(self, capacity: int = 4) -> None:
        if capacity < 4:
            raise ValueError("the capacity must be at least 4")
        self.C = capacity
        self.f = (2 * capacity + 1) // 3
        self.R = 2 * self.f - 1
        self.root: Node[K] = Node(leaf=True)
        self.reads = 0

    def _find_leaf(self, k: K) -> Node[K]:
        x = self.root  # @line L1
        while not x.leaf:  # @line L2
            i = bisect_right(x.keys, k)  # @line L3
            x = x.children[i]  # @line L4
            self.reads += 1
        return x

    def search(self, k: K) -> bool:
        """Return True when k is in the tree."""
        x = self._find_leaf(k)
        j = bisect_left(x.keys, k)
        return j < len(x.keys) and not (k < x.keys[j])  # @line L5

    def range(self, a: K, b: K) -> list[K]:
        """Return the keys k with a <= k <= b, in increasing order."""
        x: Optional[Node[K]] = self._find_leaf(a)
        out: list[K] = []
        while x is not None:
            for k in x.keys:
                if k < a:
                    continue
                if b < k:
                    return out
                out.append(k)
            x = x.next
            if x is not None:
                self.reads += 1
        return out

    def insert(self, k: K) -> bool:
        """Insert k. Return False, and change nothing, if k is present."""
        if self.search(k):
            return False
        self._insert_rec(self.root, k)  # @line L6
        if entries(self.root) > self.R:  # @line L7
            top: Node[K] = Node(leaf=False)  # @line L8
            top.children = [self.root]
            self.root = top
            self._share(top, 0, 1, 2)
        return True

    def _insert_rec(self, x: Node[K], k: K) -> None:
        if x.leaf:  # @line L9
            insort(x.keys, k)
            return
        i = bisect_right(x.keys, k)  # @line L10
        self.reads += 1
        self._insert_rec(x.children[i], k)  # @line L11
        if entries(x.children[i]) <= self.C:  # @line L12
            return
        n = len(x.children)
        for j in (i - 1, i + 1):  # @line L13
            if 0 <= j < n and entries(x.children[j]) < self.C:
                self._share(x, min(i, j), 2, 2)  # @line L14
                return
        j = i - 1 if i > 0 else i + 1  # @line L15
        self._share(x, min(i, j), 2, 3)  # @line L16

    def _share(self, x: Node[K], j: int, g: int, k: int) -> None:
        """Turn the g children x.c[j .. j+g-1] into k children whose entry
        counts differ by at most one, and fix the separators of x."""
        group = x.children[j : j + g]  # @line L17
        self.reads += g - 1
        leaf = group[0].leaf
        if leaf:
            items: list[Any] = [key for y in group for key in y.keys]
            after = group[-1].next
        else:
            items = [c for y in group for c in y.children]
            ks: list[K] = []
            for t, y in enumerate(group):
                ks.extend(y.keys)
                if t < g - 1:
                    ks.append(x.keys[j + t])
        q, r = divmod(len(items), k)  # @line L18
        nodes = group[:k] + [Node[K](leaf) for _ in range(k - g)]
        seps: list[K] = []
        pos = 0
        for t, y in enumerate(nodes):  # @line L19
            size = q + (1 if t < r else 0)
            if leaf:
                y.keys = items[pos : pos + size]
                if t > 0:
                    seps.append(y.keys[0])
            else:
                y.children = items[pos : pos + size]
                y.keys = ks[pos : pos + size - 1]
                if t > 0:
                    seps.append(ks[pos - 1])
            pos += size
        if leaf:  # @line L20
            for y, z in zip(nodes, nodes[1:]):
                y.next = z
            nodes[-1].next = after
        x.children[j : j + g] = nodes
        x.keys[j : j + g - 1] = seps

    def delete(self, k: K) -> bool:
        """Delete k. Return False, and change nothing, if k is absent."""
        if not self.search(k):
            return False
        self._delete_rec(self.root, k)  # @line L21
        if not self.root.leaf and len(self.root.children) == 1:  # @line L22
            self.root = self.root.children[0]
        return True

    def _delete_rec(self, x: Node[K], k: K) -> None:
        if x.leaf:  # @line L23
            x.keys.pop(bisect_left(x.keys, k))
            return
        i = bisect_right(x.keys, k)  # @line L24
        self.reads += 1
        self._delete_rec(x.children[i], k)  # @line L25
        if entries(x.children[i]) >= self.f:  # @line L26
            return
        n = len(x.children)
        for j in (i - 1, i + 1):  # @line L27
            if 0 <= j < n and entries(x.children[j]) > self.f:
                self._share(x, min(i, j), 2, 2)
                return
        if n == 2:  # @line L28
            self._share(x, 0, 2, 1)
            return
        j = min(max(i - 1, 0), n - 3)  # @line L29
        total = sum(entries(y) for y in x.children[j : j + 3])
        self._share(x, j, 3, 2 if total <= 2 * self.C else 3)  # @line L30

    def keys(self) -> list[K]:
        """Return all keys in order by walking the leaf chain."""
        x = self.root
        while not x.leaf:
            x = x.children[0]
        out: list[K] = []
        y: Optional[Node[K]] = x
        while y is not None:
            out.extend(y.keys)
            y = y.next
        return out

    def height(self) -> int:
        """Return the number of edges on a root-to-leaf path."""
        h, x = 0, self.root
        while not x.leaf:
            x, h = x.children[0], h + 1
        return h

    def check_invariant(self) -> None:
        """Raise AssertionError if a B*-tree property fails."""
        leaves: list[Node[K]] = []
        depths: set[int] = set()

        def walk(x: Node[K], lo: Any, hi: Any, depth: int, is_root: bool) -> None:
            e = entries(x)
            assert e <= (self.R if is_root else self.C)
            assert is_root or e >= self.f
            m = len(x.keys)
            assert all(x.keys[j] < x.keys[j + 1] for j in range(m - 1))
            if m:
                assert lo is None or not (x.keys[0] < lo)
                assert hi is None or x.keys[-1] < hi
            if x.leaf:
                assert not x.children
                depths.add(depth)
                leaves.append(x)
                return
            assert len(x.children) == m + 1 >= 2
            bounds = [lo, *x.keys, hi]
            for j, c in enumerate(x.children):
                walk(c, bounds[j], bounds[j + 1], depth + 1, False)

        walk(self.root, None, None, 0, True)
        assert len(depths) == 1
        for a, b in zip(leaves, leaves[1:]):
            assert a.next is b
        assert leaves[-1].next is None
