# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterator-model/. The authors are listed in prov/4TQNVH.jsonl.
"""Query operators in the iterator (Volcano) model.

Each operator has open(), next() and close(). next() returns one tuple, or
None at the end. A parent calls next() on its children, so tuples are pulled
up the plan one at a time. Select, Project, Limit and the probe side of a hash
join are pipelined. Sort, HashAggregate and the build side of a hash join are
blocking: they read all of their input in open().

Tuples are Python tuples. A join outputs left_tuple + right_tuple.
"""

from typing import Any, Callable, Dict, Iterator, List, Optional, Sequence, Tuple

Row = Tuple[Any, ...]


class Operator:
    """Base class. Subclasses override open, next and close."""

    def open(self) -> None:
        raise NotImplementedError

    def next(self) -> Optional[Row]:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError

    def __iter__(self) -> Iterator[Row]:
        self.open()  # @line L8
        try:
            while True:
                t = self.next()  # @line L9
                if t is None:
                    return
                yield t
        finally:
            self.close()  # @line L10


def run(plan: Operator) -> List[Row]:
    """Open the root, call next until the end, close the root."""
    return list(plan)


class Scan(Operator):
    """Read a stored relation. Counts the tuples it returns and its opens."""

    def __init__(self, rows: Sequence[Row]) -> None:
        self.rows = list(rows)
        self.pos = 0
        self.produced = 0
        self.opens = 0

    def open(self) -> None:
        self.pos = 0
        self.opens += 1

    def next(self) -> Optional[Row]:
        if self.pos == len(self.rows):
            return None
        t = self.rows[self.pos]
        self.pos += 1
        self.produced += 1
        return t

    def close(self) -> None:
        pass


class Select(Operator):
    """Return the input tuples that satisfy pred. Pipelined."""

    def __init__(self, child: Operator, pred: Callable[[Row], bool]) -> None:
        self.child, self.pred = child, pred

    def open(self) -> None:
        self.child.open()  # @line L1

    def next(self) -> Optional[Row]:
        while True:  # @line L3
            t = self.child.next()  # @line L4
            if t is None:  # @line L5
                return None
            if self.pred(t):  # @line L6
                return t

    def close(self) -> None:
        self.child.close()  # @line L7


class Project(Operator):
    """Keep the columns at positions cols, with duplicates (bag semantics)."""

    def __init__(self, child: Operator, cols: Sequence[int]) -> None:
        self.child, self.cols = child, list(cols)

    def open(self) -> None:
        self.child.open()

    def next(self) -> Optional[Row]:
        t = self.child.next()
        if t is None:
            return None
        return tuple(t[i] for i in self.cols)

    def close(self) -> None:
        self.child.close()


class NestedLoopJoin(Operator):
    """For each outer tuple, rescan the inner input (close, then open again)."""

    def __init__(self, outer: Operator, inner: Operator, pred: Callable[[Row, Row], bool]) -> None:
        self.outer, self.inner, self.pred = outer, inner, pred
        self.cur: Optional[Row] = None

    def open(self) -> None:
        self.outer.open()
        self.cur = self.outer.next()
        if self.cur is not None:
            self.inner.open()

    def next(self) -> Optional[Row]:
        while self.cur is not None:
            s = self.inner.next()
            if s is None:
                self.inner.close()
                self.cur = self.outer.next()
                if self.cur is not None:
                    self.inner.open()
                continue
            if self.pred(self.cur, s):
                return self.cur + s
        return None

    def close(self) -> None:
        if self.cur is not None:
            self.inner.close()
        self.outer.close()


class HashJoin(Operator):
    """Equijoin. open() reads all of the build input into a hash table
    (blocking); next() pulls the probe input one tuple at a time."""

    def __init__(self, build: Operator, probe: Operator, build_key: Callable[[Row], Any],
                 probe_key: Callable[[Row], Any]) -> None:
        self.build, self.probe = build, probe
        self.build_key, self.probe_key = build_key, probe_key
        self.table: Dict[Any, List[Row]] = {}
        self.matches: List[Row] = []
        self.cur: Optional[Row] = None

    def open(self) -> None:
        self.table = {}
        self.build.open()
        while True:  # @line L2 (INIT-STATE of a hash join reads the build input)
            t = self.build.next()
            if t is None:
                break
            self.table.setdefault(self.build_key(t), []).append(t)
        self.build.close()
        self.probe.open()
        self.matches, self.cur = [], None

    def next(self) -> Optional[Row]:
        while not self.matches:
            self.cur = self.probe.next()
            if self.cur is None:
                return None
            self.matches = list(self.table.get(self.probe_key(self.cur), []))
        return self.matches.pop(0) + self.cur

    def close(self) -> None:
        self.table = {}
        self.probe.close()


class Sort(Operator):
    """Blocking: open() reads and sorts the whole input."""

    def __init__(self, child: Operator, key: Callable[[Row], Any]) -> None:
        self.child, self.key = child, key
        self.buf: List[Row] = []
        self.pos = 0

    def open(self) -> None:
        self.child.open()
        self.buf = []
        while True:
            t = self.child.next()
            if t is None:
                break
            self.buf.append(t)
        self.child.close()
        self.buf.sort(key=self.key)
        self.pos = 0

    def next(self) -> Optional[Row]:
        if self.pos == len(self.buf):
            return None
        self.pos += 1
        return self.buf[self.pos - 1]

    def close(self) -> None:
        self.buf = []


class HashAggregate(Operator):
    """GROUP BY the columns cols with COUNT(*). Blocking. Output: group + (count,)."""

    def __init__(self, child: Operator, cols: Sequence[int]) -> None:
        self.child, self.cols = child, list(cols)
        self.out: List[Row] = []

    def open(self) -> None:
        counts: Dict[Row, int] = {}
        self.child.open()
        while True:
            t = self.child.next()
            if t is None:
                break
            g = tuple(t[i] for i in self.cols)
            counts[g] = counts.get(g, 0) + 1
        self.child.close()
        self.out = [g + (c,) for g, c in counts.items()]

    def next(self) -> Optional[Row]:
        return self.out.pop() if self.out else None

    def close(self) -> None:
        self.out = []


class Limit(Operator):
    """Return at most k tuples, then stop pulling from the child."""

    def __init__(self, child: Operator, k: int) -> None:
        self.child, self.k, self.done = child, k, 0

    def open(self) -> None:
        self.done = 0
        self.child.open()

    def next(self) -> Optional[Row]:
        if self.done >= self.k:
            return None
        t = self.child.next()
        if t is not None:
            self.done += 1
        return t

    def close(self) -> None:
        self.child.close()
