# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blink-tree/. The authors are listed in prov/DQ5FW8.jsonl.

import bisect
import threading
import time
from collections.abc import Generator
from typing import Any, NamedTuple, TypeVar

R = TypeVar("R")

SPIN = "spin"  # what a step generator yields while it waits

Steps = Generator[str | None, None, R]


def run(steps: "Steps[R]") -> R:
    """Run a step generator to its end in the calling thread and return its result."""
    while True:
        try:
            if next(steps) == SPIN:
                time.sleep(0)
        except StopIteration as stop:
            return stop.value


class Page(NamedTuple):
    """The contents of a node, read and written as one unit, like a disk page.

    A leaf holds keys and their values. An internal node holds separators and
    children: child i covers the keys up to keys[i], above keys[i - 1]. The
    last separator equals high. high is None for the rightmost node of a
    level (no upper bound), and link is the right sibling or None.
    """

    leaf: bool
    level: int
    keys: tuple
    vals: tuple
    high: Any
    link: int | None


def above(k: Any, high: Any) -> bool:
    """True if key k is larger than the high key (None means no bound)."""
    return high is not None and k > high


class Node:
    __slots__ = ("page", "lock")

    def __init__(self, page: Page) -> None:
        self.page = page
        self.lock = threading.Lock()


class BLinkTree:
    """The Lehman-Yao B-link tree: a concurrent B+-tree map.

    Searches take no locks. An update locks at most three nodes at a time,
    always below or to the right of the nodes it already holds. A split
    writes the new right node first and then the old node, whose new high
    key and right link make the moved keys reachable before the parent knows
    about them. Every shared access (a page read, a page write, a lock try)
    is one step of a generator.
    """

    def __init__(self, capacity: int = 3) -> None:
        if capacity < 3:
            raise ValueError("capacity must be at least 3")
        self.capacity = capacity
        self.nodes: list[Node] = []
        self._alloc = threading.Lock()
        self._anchor = threading.Lock()  # guards root and height
        self.root = self._new(Page(True, 0, (), (), None, None))
        self.height = 0  # the level of the root

    # ---- shared memory ----

    def _new(self, page: Page) -> int:
        with self._alloc:
            self.nodes.append(Node(page))
            return len(self.nodes) - 1

    def _read(self, n: int) -> Page:
        return self.nodes[n].page

    def _write(self, n: int, page: Page) -> None:
        self.nodes[n].page = page

    def _lock_steps(self, n: int) -> "Steps[None]":
        while not self.nodes[n].lock.acquire(blocking=False):
            yield SPIN
        yield None

    def _unlock(self, n: int) -> None:
        self.nodes[n].lock.release()

    # ---- helpers ----

    @staticmethod
    def _child(a: Page, k: Any) -> int:
        for sep, c in zip(a.keys, a.vals):
            if not above(k, sep):
                return c
        raise AssertionError("key above the high key")

    def _descend_steps(self, k: Any, level: int, stack: list[int] | None) -> "Steps[int]":
        """Walk without locks to the node of the given level that covers k.

        If stack is given, push the last node visited at each higher level.
        """
        n = self.root
        yield None
        a = self._read(n)
        yield None
        while a.level > level or above(k, a.high):
            if above(k, a.high):
                n = a.link  # type: ignore[assignment]
            else:
                if stack is not None:
                    stack.append(n)
                n = self._child(a, k)
            a = self._read(n)
            yield None
        return n

    def _move_right_steps(self, n: int, a: Page, k: Any) -> "Steps[tuple[int, Page]]":
        """With n locked, move right until n covers k, lock coupling to the right."""
        while above(k, a.high):  # @line L18
            nxt = a.link
            assert nxt is not None
            yield from self._lock_steps(nxt)
            self._unlock(n)
            n = nxt
            a = self._read(n)
            yield None
        return n, a

    def _locate_steps(self, k: Any, stack: list[int]) -> "Steps[tuple[int, Page]]":
        """Find and lock the leaf that covers k."""
        n = yield from self._descend_steps(k, 0, stack)
        yield from self._lock_steps(n)
        a = self._read(n)
        yield None
        return (yield from self._move_right_steps(n, a, k))

    # ---- operations ----

    def search_steps(self, k: Any) -> "Steps[Any]":
        n = self.root  # @line L1
        yield None
        a = self._read(n)  # @line L2
        yield None
        while not a.leaf or above(k, a.high):  # @line L3
            n = a.link if above(k, a.high) else self._child(a, k)  # type: ignore[assignment] # @line L4
            a = self._read(n)  # @line L5
            yield None
        i = bisect.bisect_left(a.keys, k)
        return a.vals[i] if i < len(a.keys) and a.keys[i] == k else None  # @line L6

    def insert_steps(self, k: Any, v: Any) -> "Steps[Any]":
        """Map k to v. Return the old value of k, or None if k was absent."""
        stack: list[int] = []
        n = yield from self._descend_steps(k, 0, stack)  # @line L7
        yield from self._lock_steps(n)  # @line L8
        a = self._read(n)
        yield None
        n, a = yield from self._move_right_steps(n, a, k)
        i = bisect.bisect_left(a.keys, k)
        if i < len(a.keys) and a.keys[i] == k:  # @line L9
            old = a.vals[i]
            self._write(n, a._replace(vals=a.vals[:i] + (v,) + a.vals[i + 1 :]))
            yield None
            self._unlock(n)
            return old
        y, w = k, v  # @line L10
        while True:  # @line L11
            a = self._insert_entry(a, y, w)  # @line L12
            if len(a.keys) <= self.capacity:  # @line L13
                self._write(n, a)
                yield None
                self._unlock(n)
                return None
            h = (len(a.keys) + 1) // 2  # @line L14
            b = Page(a.leaf, a.level, a.keys[h:], a.vals[h:], a.high, a.link)
            u = self._new(b)
            yield None
            left = Page(a.leaf, a.level, a.keys[:h], a.vals[:h], a.keys[h - 1], u)
            self._write(n, left)
            yield None
            y, w, old, level = left.high, u, n, a.level  # @line L15
            if stack:  # @line L16
                n = stack.pop()
            else:
                while True:
                    with self._anchor:
                        if self.height > level:
                            break
                        if self.root == old:
                            r = self._new(Page(False, level + 1, (y, None), (old, u), None, None))
                            self.root, self.height = r, level + 1
                            self._unlock(old)
                            return None
                    yield SPIN  # another node of the top level split first; wait for its new root
                yield None
                n = yield from self._descend_steps(y, level + 1, None)
            yield from self._lock_steps(n)  # @line L17
            a = self._read(n)
            yield None
            n, a = yield from self._move_right_steps(n, a, y)
            self._unlock(old)

    @staticmethod
    def _insert_entry(a: Page, y: Any, w: Any) -> Page:
        if a.leaf:
            i = bisect.bisect_left(a.keys, y)
            return a._replace(keys=a.keys[:i] + (y,) + a.keys[i:], vals=a.vals[:i] + (w,) + a.vals[i:])
        # child c with separator m (the first with y <= m) splits at y into c and w
        i = next(j for j, m in enumerate(a.keys) if not above(y, m))
        keys = a.keys[:i] + (y,) + a.keys[i:]
        vals = a.vals[: i + 1] + (w,) + a.vals[i + 1 :]
        return a._replace(keys=keys, vals=vals)

    def delete_steps(self, k: Any) -> "Steps[Any]":
        """Remove k. Return its value, or None if k was absent. Nodes never merge."""
        n, a = yield from self._locate_steps(k, [])  # @line L19
        i = bisect.bisect_left(a.keys, k)
        old = None
        if i < len(a.keys) and a.keys[i] == k:  # @line L20
            old = a.vals[i]
            self._write(n, a._replace(keys=a.keys[:i] + a.keys[i + 1 :], vals=a.vals[:i] + a.vals[i + 1 :]))
            yield None
        self._unlock(n)
        return old

    def search(self, k: Any) -> Any:
        return run(self.search_steps(k))

    def insert(self, k: Any, v: Any) -> Any:
        return run(self.insert_steps(k, v))

    def delete(self, k: Any) -> Any:
        return run(self.delete_steps(k))

    # ---- checks, for a quiescent tree ----

    def items(self) -> list[tuple[Any, Any]]:
        """All pairs in key order, by the leaf level's right links."""
        n: int | None = self.root
        a = self._read(self.root)
        while not a.leaf:
            n = a.vals[0]
            a = self._read(n)  # type: ignore[arg-type]
        out = []
        while n is not None:
            a = self._read(n)
            out.extend(zip(a.keys, a.vals))
            n = a.link
        return out

    def _level(self, first: int) -> list[int]:
        out = []
        n: int | None = first
        while n is not None:
            out.append(n)
            n = self._read(n).link
        return out

    def check_invariant(self) -> None:
        """Check a quiescent tree: every level is a chain of nodes with growing
        high keys, each key lies in its node's range, and the children of each
        level, in order, are exactly the next level with separators equal to
        their high keys. Raise AssertionError if not."""
        assert not any(node.lock.locked() for node in self.nodes), "a lock is held"
        top = self._read(self.root)
        assert top.level == self.height and top.link is None
        level_nodes = [self.root]
        for level in range(self.height, -1, -1):
            low = None
            for n in level_nodes:
                a = self._read(n)
                assert a.level == level and a.leaf == (level == 0)
                assert len(a.keys) == len(a.vals) and len(a.keys) <= self.capacity
                for key in a.keys if a.leaf else a.keys[:-1]:
                    assert (low is None or key > low) and not above(key, a.high)
                if not a.leaf:
                    assert a.keys and a.keys[-1] == a.high
                    assert list(a.keys[:-1]) == sorted(a.keys[:-1])
                low = a.high
            assert self._read(level_nodes[-1]).high is None
            if level:
                children = [c for n in level_nodes for c in self._read(n).vals]
                seps = [m for n in level_nodes for m in self._read(n).keys]
                assert children == self._level(children[0]), "parents miss a child"
                assert seps == [self._read(c).high for c in children]
                level_nodes = children
