# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/buffer-tree/. The authors are listed in prov/5H2XC9.jsonl.

from bisect import bisect_right
from math import ceil
from typing import Any, Generic, NamedTuple, Optional, Protocol, TypeVar, Union


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)

INSERT, DELETE, QUERY = 0, 1, 2


class Op(NamedTuple):
    time: int
    kind: int
    key: Any
    qid: int


class Leaf(Generic[K]):
    """A leaf block: at most B keys in increasing order."""

    def __init__(self, keys: list[K]) -> None:
        self.keys = keys


class Node(Generic[K]):
    """An internal node with routing keys, children and a buffer of pending
    operations. A bottom node has leaves as its children."""

    def __init__(self, bottom: bool, parent: Optional["Node[K]"] = None) -> None:
        self.bottom = bottom
        self.parent = parent
        self.routing: list[K] = []
        self.children: list[Union["Node[K]", Leaf[K]]] = []
        self.buf: list[Op] = []


class BufferTree(Generic[K]):
    """Arge's buffer tree for a batched dictionary of distinct keys.

    The tree has fan-out at most m, leaves of at most B keys, and a buffer of
    up to M = m * B operations in each internal node. Inserts, deletes and
    membership queries go into the root buffer; a buffer that overflows is
    emptied one level down, and a bottom node applies its operations to its
    leaves in time order. A query is answered when it reaches the leaves, so
    the answers come late: `flush` empties all buffers and returns them.
    N operations cost O((N/B) log_m (N/B)) I/Os in total; `ios` counts the
    block transfers. Deletions are rebalanced by global rebuilding.
    """

    def __init__(self, block_size: int = 4, fanout: int = 4) -> None:
        if block_size < 1 or fanout < 4:
            raise ValueError("need block_size >= 1 and fanout >= 4")
        self.B = block_size
        self.m = fanout
        self.M = fanout * block_size
        self.root: Node[K] = Node(bottom=True)
        self.root.children = [Leaf([])]
        self.time = 0
        self.next_qid = 0
        self.answers: dict[int, bool] = {}
        self.ios = 0
        self.base = 0
        self.deletes = 0

    # operations ---------------------------------------------------------

    def insert(self, k: K) -> None:
        """Insert k; inserting a present key changes nothing."""
        self._operation(INSERT, k, -1)

    def delete(self, k: K) -> None:
        """Delete k; deleting an absent key changes nothing."""
        self._operation(DELETE, k, -1)
        self.deletes += 1
        if self.deletes > max(self.M, self.base // 2):
            self._rebuild()

    def query(self, k: K) -> int:
        """Ask whether k is present now. Return a query id; the answer is in
        `answers` once the query has reached the leaves."""
        q = self.next_qid
        self.next_qid += 1
        self._operation(QUERY, k, q)
        return q

    def _operation(self, kind: int, k: K, qid: int) -> None:
        self.time += 1
        self.root.buf.append(Op(self.time, kind, k, qid))  # @line L1
        if len(self.root.buf) % self.B == 0:
            self.ios += 1  # a full block of the root buffer goes to disk
        if len(self.root.buf) > self.M:  # @line L2
            self._empty(self.root)

    # buffer emptying ----------------------------------------------------

    def _empty(self, x: Node[K]) -> None:
        ops, x.buf = x.buf, []  # @line L3
        self.ios += ceil(len(ops) / self.B)
        if x.bottom:  # @line L4
            self._empty_bottom(x, ops)
            return
        counts = [0] * len(x.children)
        for op in ops:  # @line L5
            i = bisect_right(x.routing, op.key)
            child = x.children[i]
            assert isinstance(child, Node)
            child.buf.append(op)
            counts[i] += 1
        self.ios += sum(ceil(c / self.B) for c in counts)
        full = [c for c in x.children if isinstance(c, Node) and len(c.buf) > self.M]
        for c in full:  # @line L6
            self._empty(c)

    def _empty_bottom(self, x: Node[K], ops: list[Op]) -> None:
        present: set[Any] = set()  # @line L7
        for leaf in x.children:
            assert isinstance(leaf, Leaf)
            present.update(leaf.keys)
        self.ios += len(x.children)
        for op in ops:  # @line L8
            if op.kind == INSERT:  # @line L9
                present.add(op.key)
            elif op.kind == DELETE:
                present.discard(op.key)
            else:
                self.answers[op.qid] = op.key in present
        keys = sorted(present)  # @line L10
        leaves: list[Union[Node[K], Leaf[K]]] = [
            Leaf(keys[i : i + self.B]) for i in range(0, len(keys), self.B)
        ] or [Leaf([])]
        self.ios += len(leaves)
        x.children = leaves
        x.routing = [leaf.keys[0] for leaf in leaves[1:] if isinstance(leaf, Leaf)]
        if len(x.children) > self.m:  # @line L11
            self._split(x)

    def _split(self, x: Node[K]) -> None:
        assert not x.buf
        c = len(x.children)
        g = ceil(c / self.m)  # @line L12
        q, r = divmod(c, g)
        sizes = [q + (1 if t < r else 0) for t in range(g)]
        kids, routes = x.children, x.routing
        nodes: list[Node[K]] = [x] + [Node(x.bottom, x.parent) for _ in range(g - 1)]
        seps: list[K] = []
        pos = 0
        for t, y in enumerate(nodes):  # @line L13
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
        if p is None:  # @line L14
            p = Node(bottom=False)
            p.children = [x]
            self.root = p
            for y in nodes:
                y.parent = p
        j = p.children.index(x)
        p.children[j + 1 : j + 1] = nodes[1:]
        p.routing[j:j] = seps
        if len(p.children) > self.m:  # @line L15
            self._split(p)

    # flushing and rebuilding --------------------------------------------

    def flush(self) -> dict[int, bool]:
        """Empty every buffer, top-down, and return all answers so far."""

        def force(x: Node[K]) -> None:
            if x.buf or not x.bottom:
                self._empty(x)
            if not x.bottom:
                for c in list(x.children):
                    assert isinstance(c, Node)
                    force(c)

        # A split during the pass can move unvisited children to a new node,
        # so repeat the pass until no buffer holds an operation.
        while self._pending(self.root):
            force(self.root)
        return self.answers

    def _pending(self, x: Node[K]) -> bool:
        if x.buf:
            return True
        return not x.bottom and any(self._pending(c) for c in x.children if isinstance(c, Node))

    def keys(self) -> list[K]:
        """Flush, then return all keys in increasing order."""
        self.flush()
        out: list[K] = []

        def walk(x: Union[Node[K], Leaf[K]]) -> None:
            if isinstance(x, Leaf):
                out.extend(x.keys)
            else:
                for c in x.children:
                    walk(c)

        walk(self.root)
        return out

    def _rebuild(self) -> None:
        keys = self.keys()
        level: list[Union[Node[K], Leaf[K]]] = [
            Leaf(keys[i : i + self.B]) for i in range(0, len(keys), self.B)
        ] or [Leaf([])]
        lows: list[Any] = [lf.keys[0] if isinstance(lf, Leaf) and lf.keys else None for lf in level]
        bottom = True
        while True:
            g = ceil(len(level) / self.m)
            q, r = divmod(len(level), g)
            nxt: list[Union[Node[K], Leaf[K]]] = []
            nlows: list[Any] = []
            pos = 0
            for t in range(g):
                size = q + (1 if t < r else 0)
                y: Node[K] = Node(bottom)
                y.children = level[pos : pos + size]
                y.routing = lows[pos + 1 : pos + size]
                for ch in y.children:
                    if isinstance(ch, Node):
                        ch.parent = y
                nxt.append(y)
                nlows.append(lows[pos])
                pos += size
            self.ios += len(nxt) + (len(level) if bottom else 0)
            level, lows, bottom = nxt, nlows, False
            if len(level) == 1:
                break
        root = level[0]
        assert isinstance(root, Node)
        self.root = root
        self.base = len(keys)
        self.deletes = 0

    # checking -----------------------------------------------------------

    def height(self) -> int:
        """The number of internal levels."""
        h, x = 1, self.root
        while not x.bottom:
            c = x.children[0]
            assert isinstance(c, Node)
            x, h = c, h + 1
        return h

    def check_invariant(self) -> None:
        """Raise AssertionError if a buffer tree property fails."""
        depths: set[int] = set()

        def walk(x: Node[K], lo: Any, hi: Any, depth: int, younger: float) -> None:
            assert len(x.children) == len(x.routing) + 1 <= self.m
            assert all(a < b for a, b in zip(x.routing, x.routing[1:]))
            assert all(lo is None or not (r < lo) for r in x.routing)
            assert all(hi is None or r < hi for r in x.routing)
            assert len(x.buf) <= self.M
            times = [op.time for op in x.buf]
            assert times == sorted(times)
            assert not times or times[-1] < younger
            for op in x.buf:
                assert lo is None or not (op.key < lo)
                assert hi is None or op.key < hi
            oldest = times[0] if times else younger
            bounds = [lo, *x.routing, hi]
            for j, c in enumerate(x.children):
                if x.bottom:
                    assert isinstance(c, Leaf) and len(c.keys) <= self.B
                    assert all(a < b for a, b in zip(c.keys, c.keys[1:]))
                    for k in c.keys:
                        assert bounds[j] is None or not (k < bounds[j])
                        assert bounds[j + 1] is None or k < bounds[j + 1]
                    depths.add(depth)
                else:
                    assert isinstance(c, Node) and c.parent is x
                    walk(c, bounds[j], bounds[j + 1], depth + 1, oldest)

        assert self.root.parent is None
        walk(self.root, None, None, 0, float("inf"))
        assert len(depths) == 1
