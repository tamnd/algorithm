# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/b-epsilon-tree/. The authors are listed in prov/NA7JW5.jsonl.

from bisect import bisect_left, bisect_right
from typing import Any, Generic, Optional, Protocol, TypeVar, Union


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)
V = TypeVar("V")

PUT, DEL = 0, 1


class Leaf(Generic[K, V]):
    """A leaf: at most L keys in increasing order, with their values."""

    def __init__(self, keys: list[K], vals: list[V]) -> None:
        self.keys = keys
        self.vals = vals


class Inner(Generic[K, V]):
    """An internal node: pivots, children and a buffer of messages.

    The buffer maps a key to its newest pending message, (PUT, value) or
    (DEL, None). All messages in the buffer are newer than all messages
    below this node."""

    def __init__(self) -> None:
        self.pivots: list[K] = []
        self.children: list[Union["Inner[K, V]", Leaf[K, V]]] = []
        self.buf: dict[K, tuple[int, Any]] = {}


Node = Union[Inner[K, V], Leaf[K, V]]


class BEpsilonTree(Generic[K, V]):
    """A B^epsilon-tree: a B+ tree whose internal nodes have fan-out at most
    F and a buffer of at most C pending messages.

    Inserts and deletes are messages put in the root buffer. A full buffer
    is flushed by moving the largest group of messages that go to one child
    down to that child. A search reads the buffers on its path, so its
    answer is immediate. With F = B^eps and C = Theta(B), an update costs
    O(log_B N / (eps B^(1 - eps))) amortized I/Os and a search
    O(log_B N / eps). `ios` counts node reads and writes, one block each.
    """

    def __init__(self, block_size: int = 8, fanout: int = 3) -> None:
        if block_size < 2 or fanout < 3:
            raise ValueError("need block_size >= 2 and fanout >= 3")
        self.C = block_size  # buffer capacity of an internal node
        self.L = block_size  # keys in a leaf
        self.F = fanout
        self.root: Node[K, V] = Leaf([], [])
        self.ios = 0
        self.deletes = 0
        self.base = 0

    # queries -------------------------------------------------------------

    def get(self, k: K, default: Optional[V] = None) -> Optional[V]:
        """Return the value of k, or default if k is absent."""
        x = self.root  # @line L1
        while isinstance(x, Inner):  # @line L2
            self.ios += 1
            if k in x.buf:  # @line L3
                kind, v = x.buf[k]
                return v if kind == PUT else default
            x = x.children[bisect_right(x.pivots, k)]  # @line L4
        self.ios += 1
        i = bisect_left(x.keys, k)  # @line L5
        return x.vals[i] if i < len(x.keys) and not (k < x.keys[i]) else default

    def __contains__(self, k: K) -> bool:
        sentinel = object()
        return self.get(k, sentinel) is not sentinel  # type: ignore[arg-type]

    # updates -------------------------------------------------------------

    def put(self, k: K, v: V) -> None:
        """Insert k with value v, or replace the value of k."""
        self._upsert(k, (PUT, v))

    def delete(self, k: K) -> None:
        """Delete k; deleting an absent key changes nothing."""
        self._upsert(k, (DEL, None))
        self.deletes += 1
        if self.deletes > max(self.L, self.base):
            self._rebuild()

    def _upsert(self, k: K, msg: tuple[int, Any]) -> None:
        if isinstance(self.root, Leaf):  # @line L6
            self._apply(self.root, {k: msg})
        else:
            self.root.buf[k] = msg  # @line L7
            if len(self.root.buf) > self.C:
                self._flush(self.root)
        while self._too_big(self.root):  # @line L8
            new_root: Inner[K, V] = Inner()
            new_root.children = [self.root]
            self.root = new_root
            self._split(new_root, 0)

    def _flush(self, x: Inner[K, V]) -> None:
        self.ios += 1
        while len(x.buf) > self.C:  # @line L9
            groups: dict[int, list[K]] = {}
            for key in x.buf:
                groups.setdefault(bisect_right(x.pivots, key), []).append(key)
            i = max(groups, key=lambda j: len(groups[j]))  # @line L10
            c = x.children[i]
            batch = {key: x.buf.pop(key) for key in groups[i]}
            self.ios += 2  # read and write the child
            if isinstance(c, Leaf):  # @line L11
                self._apply(c, batch)
            else:
                c.buf.update(batch)
                if len(c.buf) > self.C:  # @line L12
                    self._flush(c)
            if self._too_big(c):  # @line L13
                self._split(x, i)

    def _apply(self, leaf: Leaf[K, V], batch: dict[K, tuple[int, Any]]) -> None:
        d = dict(zip(leaf.keys, leaf.vals))
        for k, (kind, v) in batch.items():
            if kind == PUT:
                d[k] = v
            else:
                d.pop(k, None)
        leaf.keys = sorted(d)
        leaf.vals = [d[k] for k in leaf.keys]

    def _too_big(self, x: Node[K, V]) -> bool:
        if isinstance(x, Leaf):
            return len(x.keys) > self.L
        return len(x.children) > self.F

    def _split(self, p: Inner[K, V], i: int) -> None:
        """Split child i of p into two halves, repeating while too big."""
        c = p.children[i]
        if isinstance(c, Leaf):  # @line L14
            h = len(c.keys) // 2
            right: Node[K, V] = Leaf(c.keys[h:], c.vals[h:])
            pivot = c.keys[h]
            c.keys, c.vals = c.keys[:h], c.vals[:h]
        else:
            h = len(c.children) // 2
            r: Inner[K, V] = Inner()
            pivot = c.pivots[h - 1]
            r.children, r.pivots = c.children[h:], c.pivots[h:]
            c.children, c.pivots = c.children[:h], c.pivots[: h - 1]
            r.buf = {k: m for k, m in c.buf.items() if not (k < pivot)}
            c.buf = {k: m for k, m in c.buf.items() if k < pivot}
            right = r
        self.ios += 2
        p.children.insert(i + 1, right)
        p.pivots.insert(i, pivot)
        for j in (i + 1, i):
            if self._too_big(p.children[j]):
                self._split(p, j)

    # whole-tree operations --------------------------------------------------

    def items(self) -> list[tuple[K, V]]:
        """All live pairs in key order, resolving the pending messages."""

        def content(x: Node[K, V]) -> dict[K, V]:
            if isinstance(x, Leaf):
                return dict(zip(x.keys, x.vals))
            d: dict[K, V] = {}
            for c in x.children:
                d.update(content(c))
            for k, (kind, v) in x.buf.items():
                if kind == PUT:
                    d[k] = v
                else:
                    d.pop(k, None)
            return d

        d = content(self.root)
        return [(k, d[k]) for k in sorted(d)]

    def __len__(self) -> int:
        return len(self.items())

    def _rebuild(self) -> None:
        pairs = self.items()
        self.ios += 2 * (len(pairs) // self.L + 1)
        half = max(1, self.L // 2 + 1)
        level: list[Node[K, V]] = [
            Leaf([k for k, _ in pairs[i : i + half]], [v for _, v in pairs[i : i + half]])
            for i in range(0, len(pairs), half)
        ] or [Leaf([], [])]
        lows: list[Any] = [lf.keys[0] if isinstance(lf, Leaf) and lf.keys else None for lf in level]
        while len(level) > 1:
            nxt: list[Node[K, V]] = []
            nlows: list[Any] = []
            step = max(2, (self.F + 1) // 2)
            for i in range(0, len(level), step):
                y: Inner[K, V] = Inner()
                y.children = level[i : i + step]
                y.pivots = lows[i + 1 : i + step]
                nxt.append(y)
                nlows.append(lows[i])
            if len(nxt[-1].children) == 1 and len(nxt) > 1:
                last = nxt.pop()
                prev = nxt[-1]
                assert isinstance(prev, Inner) and isinstance(last, Inner)
                prev.pivots.append(nlows.pop())
                prev.children.extend(last.children)
            level, lows = nxt, nlows
        self.root = level[0]
        self.base = len(pairs)
        self.deletes = 0

    def height(self) -> int:
        h, x = 1, self.root
        while isinstance(x, Inner):
            x, h = x.children[0], h + 1
        return h

    def check_invariant(self) -> None:
        """Raise AssertionError if a property of the tree fails."""
        depths: set[int] = set()

        def walk(x: Node[K, V], lo: Any, hi: Any, depth: int) -> None:
            if isinstance(x, Leaf):
                assert len(x.keys) == len(x.vals) and len(x.keys) <= self.L
                assert all(a < b for a, b in zip(x.keys, x.keys[1:]))
                for k in x.keys:
                    assert (lo is None or not (k < lo)) and (hi is None or k < hi)
                depths.add(depth)
                return
            assert 2 <= len(x.children) <= self.F
            assert len(x.pivots) == len(x.children) - 1
            assert all(a < b for a, b in zip(x.pivots, x.pivots[1:]))
            for p in x.pivots:
                assert (lo is None or lo < p) and (hi is None or p < hi)
            assert len(x.buf) <= self.C
            for k in x.buf:
                assert (lo is None or not (k < lo)) and (hi is None or k < hi)
            bounds = [lo, *x.pivots, hi]
            for j, c in enumerate(x.children):
                walk(c, bounds[j], bounds[j + 1], depth + 1)

        walk(self.root, None, None, 0)
        assert len(depths) == 1
