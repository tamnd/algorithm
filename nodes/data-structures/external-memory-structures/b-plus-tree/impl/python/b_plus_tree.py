# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/b-plus-tree/. The authors are listed in prov/M7WT2F.jsonl.

from bisect import bisect_left, bisect_right, insort
from typing import Any, Generic, Optional, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class Node(Generic[K]):
    """A B+ tree node. A leaf holds keys and a link to the next leaf. An
    internal node holds separators key[0..m-1] and children c[0..m], where
    c[i] holds the keys k with key[i-1] <= k < key[i]."""

    def __init__(self, leaf: bool) -> None:
        self.leaf = leaf
        self.keys: list[K] = []
        self.children: list["Node[K]"] = []
        self.next: Optional["Node[K]"] = None


class BPlusTree(Generic[K]):
    """A B+ tree of order d >= 1 over distinct keys.

    Every node except the root holds d to 2d keys. All keys are in the
    leaves, which are linked from left to right; internal nodes hold only
    separators. Insertion and deletion work bottom-up along the search path.
    search, insert and delete make O(log_d n) node reads; range(a, b) makes
    O(log_d n + z / d) reads when it reports z keys. `reads` counts the node
    reads; the root is kept in memory.
    """

    def __init__(self, d: int = 2) -> None:
        if d < 1:
            raise ValueError("the order d must be at least 1")
        self.d = d
        self.root: Node[K] = Node(leaf=True)
        self.reads = 0

    def _find_leaf(self, k: K) -> Node[K]:
        x = self.root  # @line L1
        while not x.leaf:  # @line L2
            i = bisect_right(x.keys, k)  # @line L3
            x = x.children[i]  # @line L4
            self.reads += 1
        return x  # @line L5

    def search(self, k: K) -> bool:
        """Return True when k is in the tree."""
        x = self._find_leaf(k)
        j = bisect_left(x.keys, k)
        return j < len(x.keys) and not (k < x.keys[j])

    def range(self, a: K, b: K) -> list[K]:
        """Return the keys k with a <= k <= b, in increasing order."""
        x: Optional[Node[K]] = self._find_leaf(a)  # @line L6
        out: list[K] = []
        while x is not None:  # @line L7
            for k in x.keys:  # @line L8
                if k < a:
                    continue
                if b < k:
                    return out
                out.append(k)
            if x.next is None:  # @line L9
                return out
            x = x.next  # @line L10
            self.reads += 1
        return out

    def insert(self, k: K) -> bool:
        """Insert k. Return False, and change nothing, if k is present."""
        if self.search(k):
            return False
        r = self._insert_rec(self.root, k)  # @line L11
        if r is not None:  # @line L12
            s, z = r
            new_root: Node[K] = Node(leaf=False)  # @line L13
            new_root.keys = [s]
            new_root.children = [self.root, z]
            self.root = new_root
        return True

    def _insert_rec(self, x: Node[K], k: K) -> Optional[tuple[K, Node[K]]]:
        d = self.d
        if x.leaf:  # @line L14
            insort(x.keys, k)  # @line L15
            if len(x.keys) <= 2 * d:  # @line L16
                return None
            z: Node[K] = Node(leaf=True)  # @line L17
            z.keys = x.keys[d:]
            del x.keys[d:]
            z.next, x.next = x.next, z  # @line L18
            return (z.keys[0], z)  # @line L19
        i = bisect_right(x.keys, k)  # @line L20
        self.reads += 1
        r = self._insert_rec(x.children[i], k)  # @line L21
        if r is None:  # @line L22
            return None
        s, z = r  # @line L23
        x.keys.insert(i, s)
        x.children.insert(i + 1, z)
        if len(x.keys) <= 2 * d:  # @line L24
            return None
        z2: Node[K] = Node(leaf=False)  # @line L25
        z2.keys = x.keys[d + 1 :]
        z2.children = x.children[d + 1 :]
        s2 = x.keys[d]  # @line L26
        del x.keys[d:]
        del x.children[d + 1 :]
        return (s2, z2)  # @line L27

    def delete(self, k: K) -> bool:
        """Delete k. Return False, and change nothing, if k is absent."""
        if not self.search(k):
            return False
        self._delete_rec(self.root, k)  # @line L28
        if not self.root.leaf and not self.root.keys:  # @line L29
            self.root = self.root.children[0]
        return True

    def _delete_rec(self, x: Node[K], k: K) -> bool:
        if x.leaf:  # @line L30
            j = bisect_left(x.keys, k)
            if j < len(x.keys) and not (k < x.keys[j]):
                x.keys.pop(j)
            return len(x.keys) < self.d
        i = bisect_right(x.keys, k)  # @line L31
        self.reads += 1
        if not self._delete_rec(x.children[i], k):  # @line L32
            return False
        self._fix_child(x, i)  # @line L33
        return len(x.keys) < self.d  # @line L34

    def _fix_child(self, x: Node[K], i: int) -> None:
        d = self.d
        c = x.children[i]
        left = x.children[i - 1] if i > 0 else None  # @line L35
        right = x.children[i + 1] if i + 1 < len(x.children) else None
        if left is not None and len(left.keys) > d:  # @line L36
            if c.leaf:
                c.keys.insert(0, left.keys.pop())
                x.keys[i - 1] = c.keys[0]
            else:
                c.keys.insert(0, x.keys[i - 1])
                x.keys[i - 1] = left.keys.pop()
                c.children.insert(0, left.children.pop())
            return
        if right is not None and len(right.keys) > d:
            if c.leaf:
                c.keys.append(right.keys.pop(0))
                x.keys[i] = right.keys[0]
            else:
                c.keys.append(x.keys[i])
                x.keys[i] = right.keys.pop(0)
                c.children.append(right.children.pop(0))
            return
        if right is not None:  # @line L37
            j, a, b = i, c, right
        else:
            assert left is not None
            j, a, b = i - 1, left, c
        sep = x.keys.pop(j)
        x.children.pop(j + 1)
        if a.leaf:
            a.keys.extend(b.keys)
            a.next = b.next
        else:
            a.keys.append(sep)
            a.keys.extend(b.keys)
            a.children.extend(b.children)

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
        """Raise AssertionError if a B+ tree property fails."""
        d = self.d
        leaves: list[Node[K]] = []
        depths: set[int] = set()

        def walk(x: Node[K], lo: Any, hi: Any, depth: int, is_root: bool) -> None:
            m = len(x.keys)
            assert m <= 2 * d
            assert is_root or m >= d
            assert all(x.keys[j] < x.keys[j + 1] for j in range(m - 1))
            if m:
                assert lo is None or not (x.keys[0] < lo)
                assert hi is None or x.keys[-1] < hi
            if x.leaf:
                assert not x.children
                depths.add(depth)
                leaves.append(x)
                return
            assert m >= 1 and len(x.children) == m + 1
            bounds = [lo, *x.keys, hi]
            for j, c in enumerate(x.children):
                walk(c, bounds[j], bounds[j + 1], depth + 1, False)

        walk(self.root, None, None, 0, True)
        assert len(depths) == 1
        for a, b in zip(leaves, leaves[1:]):
            assert a.next is b
        assert leaves[-1].next is None
