# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/computation-dag/. The authors are listed in prov/54BC6D.jsonl.

"""A computation DAG of unit-time strands, with its work and span.

The module has three parts.

* ``ComputationDag``: the data structure. Strands are the integers
  0, 1, ..., n - 1. Each edge has one of the four kinds of CLRS, third
  edition, Section 27.1: continuation, spawn, call and return.
  ``work_and_span`` finds the work W (the number of strands) and the span S
  (the number of strands on a longest path) in one pass over a topological
  order, in Theta(n + m) time.
* ``ForkJoinTracer``: runs a fork-join program written with ``spawn``,
  ``call`` and ``sync`` and records its computation DAG with the CLRS edge
  kinds.
* ``Part``, ``strand``, ``chain``, ``series`` and ``parallel``: series-parallel
  composition, for programs that are described by their structure only.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable

EDGE_KINDS = ("continuation", "spawn", "call", "return")


class ComputationDag:
    """A directed acyclic graph of unit-time strands."""

    def __init__(self) -> None:
        self.labels: list[str] = []
        self.succ: list[list[int]] = []
        self.pred: list[list[int]] = []
        self.kind: dict[tuple[int, int], str] = {}

    def add_strand(self, label: str = "") -> int:
        """Add a strand with no edges and return its number. Cost O(1)."""
        self.labels.append(label)
        self.succ.append([])
        self.pred.append([])
        return len(self.labels) - 1

    def add_edge(self, u: int, v: int, kind: str = "continuation") -> None:
        """Add the dependency u -> v: u must finish before v starts. Cost O(1).

        A repeated edge is ignored. The edge must not close a cycle; the
        check is made by ``topological_order``, not here.
        """
        if kind not in EDGE_KINDS:
            raise ValueError(f"unknown edge kind {kind!r}")
        if not (0 <= u < len(self.labels) and 0 <= v < len(self.labels)) or u == v:
            raise ValueError("an edge joins two different existing strands")
        if (u, v) in self.kind:
            return
        self.kind[(u, v)] = kind
        self.succ[u].append(v)
        self.pred[v].append(u)

    def num_strands(self) -> int:
        return len(self.labels)

    def num_edges(self) -> int:
        return len(self.kind)

    def topological_order(self) -> list[int]:
        """Kahn's algorithm. Raise ValueError if the graph has a cycle. Theta(n + m)."""
        indeg = [len(p) for p in self.pred]
        queue = deque(v for v in range(len(indeg)) if indeg[v] == 0)
        order: list[int] = []
        while queue:
            u = queue.popleft()
            order.append(u)
            for v in self.succ[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    queue.append(v)
        if len(order) < len(indeg):
            raise ValueError("the graph has a cycle")
        return order

    def work_and_span(self) -> tuple[int, int]:
        """Return (W, S): the number of strands and the strands on a longest path.

        Every strand takes unit time, so W = T_1 and S = T_infinity. The cost
        is Theta(n + m). Raise ValueError if the graph has a cycle.
        """
        n = len(self.labels)
        indeg = [0] * n  # @line L1
        d = [0] * n
        for v in range(n):
            indeg[v] = len(self.pred[v])
        queue = deque(v for v in range(n) if indeg[v] == 0)  # @line L2
        work, span = 0, 0  # @line L3
        while queue:  # @line L4
            u = queue.popleft()  # @line L5
            work += 1  # @line L6
            d[u] += 1  # @line L7
            span = max(span, d[u])  # @line L8
            for v in self.succ[u]:  # @line L9
                d[v] = max(d[v], d[u])  # @line L10
                indeg[v] -= 1  # @line L11
                if indeg[v] == 0:  # @line L12
                    queue.append(v)
        if work < n:  # @line L13
            raise ValueError("the graph has a cycle")
        return work, span  # @line L14

    def work(self) -> int:
        return self.work_and_span()[0]

    def span(self) -> int:
        return self.work_and_span()[1]

    def critical_path(self) -> list[int]:
        """Return one longest path, as a list of strands from a source to a sink."""
        n = len(self.labels)
        if n == 0:
            return []
        d = [0] * n
        back = [-1] * n
        for u in self.topological_order():
            d[u] += 1
            for v in self.succ[u]:
                if d[u] > d[v]:
                    d[v] = d[u]
                    back[v] = u
        end = max(range(n), key=lambda v: d[v])
        path = [end]
        while back[path[-1]] >= 0:
            path.append(back[path[-1]])
        path.reverse()
        return path

    def check_invariant(self) -> None:
        """The edge lists agree with each other, the kinds are valid, and there is no cycle."""
        assert len(self.succ) == len(self.pred) == len(self.labels)
        count = 0
        for u, vs in enumerate(self.succ):
            for v in vs:
                assert u in self.pred[v]
                assert self.kind[(u, v)] in EDGE_KINDS
                count += 1
        assert count == len(self.kind) == sum(len(p) for p in self.pred)
        self.topological_order()


# ---------------------------------------------------------------- fork-join tracer


@dataclass
class _Frame:
    cur: int
    pending: list[tuple[int, str]] = field(default_factory=list)
    need_new: bool = False
    outstanding: list[int] = field(default_factory=list)


class ForkJoinTracer:
    """Run a fork-join program and record its computation DAG.

    A procedure is a Python function whose first argument is the tracer. It
    uses ``t.spawn(f, ...)``, ``t.call(f, ...)``, ``t.sync()`` and
    ``t.step()``. Each procedure instance starts with a new strand. A spawn
    adds a spawn edge to the child and a continuation edge to the next strand
    of the parent. A call adds a call edge and no continuation edge. A sync
    adds a return edge from the last strand of each spawned child to the
    strand after the sync. The strand after a call gets a return edge from the
    last strand of the callee. Each procedure ends with an implicit sync.
    ``step`` ends the current strand and starts the next one, so that a
    procedure can charge serial work: k calls of ``step`` add k strands.
    """

    def __init__(self) -> None:
        self.dag = ComputationDag()
        self._frames: list[_Frame] = []

    def _strand(self) -> int:
        f = self._frames[-1]
        if f.need_new:
            v = self.dag.add_strand()
            for u, kind in f.pending:
                self.dag.add_edge(u, v, kind)
            f.pending, f.need_new, f.cur = [], False, v
        return f.cur

    def _enter(self, proc: Callable[..., Any], args: tuple, kind: str) -> tuple[Any, int]:
        parent = self._strand() if self._frames else None
        first = self.dag.add_strand(getattr(proc, "__name__", "proc"))
        if parent is not None:
            self.dag.add_edge(parent, first, kind)
        self._frames.append(_Frame(cur=first))
        result = proc(self, *args)
        self.sync()
        last = self._strand()
        self._frames.pop()
        return result, last

    def run(self, proc: Callable[..., Any], *args: Any) -> Any:
        """Run the top-level procedure. Return its result."""
        return self._enter(proc, args, "call")[0]

    def spawn(self, proc: Callable[..., Any], *args: Any) -> Any:
        u = self._strand()
        result, last = self._enter(proc, args, "spawn")
        f = self._frames[-1]
        f.outstanding.append(last)
        f.pending, f.need_new = [(u, "continuation")], True
        return result

    def call(self, proc: Callable[..., Any], *args: Any) -> Any:
        self._strand()
        result, last = self._enter(proc, args, "call")
        f = self._frames[-1]
        f.pending, f.need_new = [(last, "return")], True
        return result

    def sync(self) -> None:
        f = self._frames[-1]
        if not f.outstanding:
            return
        if not f.need_new:
            f.pending, f.need_new = [(f.cur, "continuation")], True
        f.pending += [(x, "return") for x in f.outstanding]
        f.outstanding = []

    def step(self) -> None:
        u = self._strand()
        f = self._frames[-1]
        f.pending, f.need_new = [(u, "continuation")], True
        self._strand()


def p_fib(t: ForkJoinTracer, n: int) -> int:
    """P-FIB of CLRS, third edition, Section 27.1."""
    if n <= 1:
        return n
    x = t.spawn(p_fib, n - 1)
    y = t.call(p_fib, n - 2)
    t.sync()
    return x + y


def p_sum(t: ForkJoinTracer, a: list[int], lo: int, hi: int) -> int:
    """Sum a[lo:hi], hi - lo >= 1: spawn the left half, call the right half."""
    if hi - lo == 1:
        return a[lo]
    mid = (lo + hi) // 2
    x = t.spawn(p_sum, a, lo, mid)
    y = t.call(p_sum, a, mid, hi)
    t.sync()
    return x + y


# ---------------------------------------------------------------- series-parallel parts


@dataclass
class Part:
    """A sub-DAG given by its sources and sinks, with its work and span by the rules."""

    sources: list[int]
    sinks: list[int]
    work: int
    span: int


def strand(dag: ComputationDag, label: str = "") -> Part:
    v = dag.add_strand(label)
    return Part([v], [v], 1, 1)


def series(dag: ComputationDag, *parts: Part) -> Part:
    """A then B: an edge from each sink of A to each source of B. W adds and S adds."""
    parts = tuple(p for p in parts if p.work > 0)
    if not parts:
        return Part([], [], 0, 0)
    acc = parts[0]
    for b in parts[1:]:
        for u in acc.sinks:
            for v in b.sources:
                dag.add_edge(u, v, "continuation")
        acc = Part(acc.sources, b.sinks, acc.work + b.work, acc.span + b.span)
    return acc


def parallel(dag: ComputationDag, *parts: Part) -> Part:
    """A and B side by side, with no edge between them. W adds and S is the max."""
    parts = tuple(p for p in parts if p.work > 0)
    return Part(
        [v for p in parts for v in p.sources],
        [v for p in parts for v in p.sinks],
        sum(p.work for p in parts),
        max((p.span for p in parts), default=0),
    )


def chain(dag: ComputationDag, k: int, label: str = "") -> Part:
    """k strands in series (k >= 0): serial work of k units."""
    return series(dag, *[strand(dag, label) for _ in range(k)])


def sp_sum(dag: ComputationDag, n: int) -> Part:
    """Parallel sum of n >= 1 numbers: split ; (left || right) ; add."""
    if n == 1:
        return strand(dag, "leaf")
    left = sp_sum(dag, (n + 1) // 2)
    right = sp_sum(dag, n // 2)
    return series(dag, strand(dag, "split"), parallel(dag, left, right), strand(dag, "add"))


def sp_fib(dag: ComputationDag, n: int) -> Part:
    """Fibonacci, n >= 0: test ; (fib(n - 1) || fib(n - 2)) ; add."""
    if n <= 1:
        return strand(dag, "base")
    return series(dag, strand(dag, "test"), parallel(dag, sp_fib(dag, n - 1), sp_fib(dag, n - 2)), strand(dag, "add"))


def sp_merge_sort_serial_merge(dag: ComputationDag, n: int) -> Part:
    """Merge sort with parallel calls and a serial merge of n unit steps."""
    if n == 1:
        return strand(dag, "leaf")
    left = sp_merge_sort_serial_merge(dag, (n + 1) // 2)
    right = sp_merge_sort_serial_merge(dag, n // 2)
    return series(dag, strand(dag, "split"), parallel(dag, left, right), chain(dag, n, "merge"))


def _lower_bound(t: list, lo: int, hi: int, x: Any) -> tuple[int, int]:
    """First index in t[lo:hi] with t[i] >= x, and the number of probes made."""
    probes = 0
    while lo < hi:
        probes += 1
        mid = (lo + hi) // 2
        if t[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo, probes


def sp_p_merge(dag: ComputationDag, t: list, lo1: int, hi1: int, lo2: int, hi2: int, out: list, lo3: int) -> Part:
    """P-MERGE of CLRS 3rd ed. Section 27.3, on half-open ranges, writing into out.

    Cost charged: one strand for the setup, one strand for each probe of the
    binary search, one strand to place the median, then the two recursive
    merges in parallel, then one strand after the sync.
    """
    if hi1 - lo1 < hi2 - lo2:
        lo1, hi1, lo2, hi2 = lo2, hi2, lo1, hi1
    if hi1 == lo1:
        return strand(dag, "empty")
    q1 = (lo1 + hi1) // 2
    q2, probes = _lower_bound(t, lo2, hi2, t[q1])
    q3 = lo3 + (q1 - lo1) + (q2 - lo2)
    out[q3] = t[q1]
    head = chain(dag, probes + 2, "merge-head")
    left = sp_p_merge(dag, t, lo1, q1, lo2, q2, out, lo3)
    right = sp_p_merge(dag, t, q1 + 1, hi1, q2, hi2, out, q3 + 1)
    return series(dag, head, parallel(dag, left, right), strand(dag, "merge-sync"))


def sp_p_merge_sort(dag: ComputationDag, a: list, lo: int, hi: int, out: list, lo_out: int) -> Part:
    """P-MERGE-SORT of CLRS 3rd ed. Section 27.3: sort a[lo:hi] into out[lo_out:]."""
    n = hi - lo
    if n == 1:
        out[lo_out] = a[lo]
        return strand(dag, "leaf")
    tmp = [None] * n
    mid = (lo + hi) // 2
    left = sp_p_merge_sort(dag, a, lo, mid, tmp, 0)
    right = sp_p_merge_sort(dag, a, mid, hi, tmp, mid - lo)
    merge = sp_p_merge(dag, tmp, 0, mid - lo, mid - lo, n, out, lo_out)
    return series(dag, strand(dag, "split"), parallel(dag, left, right), merge)
