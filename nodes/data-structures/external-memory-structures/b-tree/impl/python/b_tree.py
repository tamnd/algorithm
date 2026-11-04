# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/b-tree/. The authors are listed in prov/KEZ9RE.jsonl.

from bisect import bisect_left
from typing import Any, Generic, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class Node(Generic[K]):
    """One B-tree node: up to 2t - 1 sorted keys and, if internal, one more child."""

    def __init__(self, leaf: bool) -> None:
        self.keys: list[K] = []
        self.children: list["Node[K]"] = []
        self.leaf = leaf


class BTree(Generic[K]):
    """A B-tree of minimum degree t >= 2 over distinct keys (the CLRS version).

    Each node except the root holds t - 1 to 2t - 1 keys, and all leaves have
    the same depth, so the height is at most log_t((n + 1) / 2). Insertion
    splits full nodes on the way down and deletion fills nodes with t - 1 keys
    on the way down, so each operation makes one pass from the root. The
    counters `reads` and `writes` count the DISK-READ and DISK-WRITE calls of
    the pseudocode; the root is kept in memory. search, insert and delete make
    O(log_t n) disk accesses and use O(t log_t n) time.
    """

    def __init__(self, t: int = 2) -> None:
        if t < 2:
            raise ValueError("the minimum degree t must be at least 2")
        self.t = t
        self.root: Node[K] = Node(leaf=True)
        self.reads = 0
        self.writes = 0

    def _read(self, x: Node[K]) -> None:
        self.reads += 1

    def _write(self, x: Node[K]) -> None:
        self.writes += 1

    def search(self, k: K) -> bool:
        """Return True when k is in the tree."""
        x = self.root
        while True:
            i = 0  # @line L1
            while i < len(x.keys) and x.keys[i] < k:  # @line L2
                i += 1
            if i < len(x.keys) and not (k < x.keys[i]):  # @line L3
                return True
            if x.leaf:  # @line L4
                return False
            x = x.children[i]  # @line L6
            self._read(x)  # @line L5

    def insert(self, k: K) -> bool:
        """Insert k. Return False, and change nothing, if k is already present."""
        if self.search(k):
            return False
        r = self.root  # @line L7
        if len(r.keys) == 2 * self.t - 1:  # @line L8
            s: Node[K] = Node(leaf=False)  # @line L9
            s.children.append(r)
            self.root = s  # @line L10
            self._split_child(s, 0)  # @line L11
            r = s  # @line L12
        self._insert_nonfull(r, k)  # @line L13
        return True

    def _split_child(self, x: Node[K], i: int) -> None:
        t = self.t
        y = x.children[i]  # @line L14
        z: Node[K] = Node(leaf=y.leaf)
        z.keys = y.keys[t:]  # @line L15
        if not y.leaf:  # @line L16
            z.children = y.children[t:]
            del y.children[t:]
        median = y.keys[t - 1]
        del y.keys[t - 1 :]  # @line L17
        x.children.insert(i + 1, z)  # @line L18
        x.keys.insert(i, median)  # @line L19
        self._write(y)  # @line L20
        self._write(z)
        self._write(x)

    def _insert_nonfull(self, x: Node[K], k: K) -> None:
        while True:
            i = len(x.keys)  # @line L21
            if x.leaf:  # @line L22
                while i >= 1 and k < x.keys[i - 1]:  # @line L23
                    i -= 1
                x.keys.insert(i, k)  # @line L24
                self._write(x)
                return
            while i >= 1 and k < x.keys[i - 1]:  # @line L25
                i -= 1
            self._read(x.children[i])  # @line L26
            if len(x.children[i].keys) == 2 * self.t - 1:  # @line L27
                self._split_child(x, i)  # @line L28
                if x.keys[i] < k:  # @line L29
                    i += 1
            x = x.children[i]  # @line L30

    def delete(self, k: K) -> bool:
        """Delete k. Return False, and change nothing, if k is not present."""
        found = self._delete(self.root, k)
        if not self.root.leaf and not self.root.keys:
            self.root = self.root.children[0]
        return found

    def _max_key(self, x: Node[K]) -> K:
        while not x.leaf:
            x = x.children[-1]
            self._read(x)
        return x.keys[-1]

    def _min_key(self, x: Node[K]) -> K:
        while not x.leaf:
            x = x.children[0]
            self._read(x)
        return x.keys[0]

    def _delete(self, x: Node[K], k: K) -> bool:
        t = self.t
        while True:
            i = bisect_left(x.keys, k)  # @line L31
            if i < len(x.keys) and not (k < x.keys[i]):  # @line L32
                if x.leaf:  # @line L33
                    x.keys.pop(i)
                    self._write(x)
                    return True
                y, z = x.children[i], x.children[i + 1]  # @line L34
                self._read(y)
                if len(y.keys) >= t:  # @line L35
                    kp = self._max_key(y)
                    x.keys[i] = kp
                    self._write(x)
                    x, k = y, kp
                    continue
                self._read(z)
                if len(z.keys) >= t:  # @line L36
                    ks = self._min_key(z)
                    x.keys[i] = ks
                    self._write(x)
                    x, k = z, ks
                    continue
                y.keys.append(x.keys.pop(i))  # @line L37
                y.keys.extend(z.keys)
                y.children.extend(z.children)
                x.children.pop(i + 1)
                self._write(x)
                self._write(y)
                x = y
                continue
            if x.leaf:  # @line L38
                return False
            c = x.children[i]
            self._read(c)
            if len(c.keys) == t - 1:  # @line L39
                left = x.children[i - 1] if i > 0 else None
                right = x.children[i + 1] if i < len(x.keys) else None
                if left is not None:
                    self._read(left)
                if right is not None:
                    self._read(right)
                if left is not None and len(left.keys) >= t:  # @line L40
                    c.keys.insert(0, x.keys[i - 1])
                    x.keys[i - 1] = left.keys.pop()
                    if not left.leaf:
                        c.children.insert(0, left.children.pop())
                    self._write(left)
                elif right is not None and len(right.keys) >= t:
                    c.keys.append(x.keys[i])
                    x.keys[i] = right.keys.pop(0)
                    if not right.leaf:
                        c.children.append(right.children.pop(0))
                    self._write(right)
                elif right is not None:  # @line L41
                    c.keys.append(x.keys.pop(i))
                    c.keys.extend(right.keys)
                    c.children.extend(right.children)
                    x.children.pop(i + 1)
                else:
                    assert left is not None
                    left.keys.append(x.keys.pop(i - 1))
                    left.keys.extend(c.keys)
                    left.children.extend(c.children)
                    x.children.pop(i)
                    c = left
                self._write(x)
                self._write(c)
            x = c  # @line L42

    def keys(self) -> list[K]:
        """Return all keys in increasing order (an in-order walk)."""
        out: list[K] = []
        stack: list[tuple[Node[K], int]] = [(self.root, 0)]
        while stack:
            x, j = stack.pop()
            if x.leaf:
                out.extend(x.keys)
                continue
            if j == len(x.children):
                continue
            if j > 0:
                out.append(x.keys[j - 1])
            stack.append((x, j + 1))
            stack.append((x.children[j], 0))
        return out

    def height(self) -> int:
        """Return the number of edges on a root-to-leaf path."""
        h, x = 0, self.root
        while not x.leaf:
            x, h = x.children[0], h + 1
        return h

    def check_invariant(self) -> None:
        """Raise AssertionError if a B-tree property fails."""
        t = self.t
        depths: set[int] = set()

        def walk(x: Node[K], lo: Any, hi: Any, d: int, is_root: bool) -> None:
            n = len(x.keys)
            assert n <= 2 * t - 1
            assert is_root or n >= t - 1
            assert all(x.keys[j] < x.keys[j + 1] for j in range(n - 1))
            if n:
                assert lo is None or lo < x.keys[0]
                assert hi is None or x.keys[-1] < hi
            if x.leaf:
                assert not x.children
                depths.add(d)
                return
            assert len(x.children) == n + 1
            assert is_root is False or n >= 1
            bounds = [lo, *x.keys, hi]
            for j, c in enumerate(x.children):
                walk(c, bounds[j], bounds[j + 1], d + 1, False)

        walk(self.root, None, None, 0, True)
        assert len(depths) == 1
