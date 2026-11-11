# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/read-copy-update/. The authors are listed in prov/0AQA6S.jsonl.
"""A small read-copy-update (RCU) on the simulator in smr_sim.py.

The shared word "cfg" points to a node. A reader brackets its reads with
read_lock and read_unlock and never waits. An updater copies the node,
changes the copy, publishes it with one write, waits for a grace period
with synchronize, and then frees the old node.

The grace period uses a counter G and one word per reader: read_lock
writes the value of G it saw, read_unlock writes 0. synchronize adds 1 to
G, which gives a new value g, and then waits until every other reader shows
0 or a value of at least g. This is the scheme of user-space RCU with a
global counter; the Linux kernel instead waits for every CPU to pass a
quiescent state.

The class RCU makes the same calls into an SMR scheme for the Treiber stack
and the Michael and Scott queue of smr_sim.py: an operation is a read-side
section, and after the section the process waits for a grace period and
frees the node it removed. This is synchronous RCU: a reader that stops
inside its section blocks every later grace period.

Cost: read_lock and read_unlock are one read and one write each, with no
wait. synchronize is one fetch-and-add and one read per reader, and it
waits for every reader that started before it.
"""

from __future__ import annotations

from typing import Any

from smr_sim import Corrupt, Gen, Memory, NoReclaim


class AtLeast:
    """The set {0} together with all values >= g, for the wait step."""

    def __init__(self, g: int) -> None:
        self.g = g

    def __contains__(self, v: Any) -> bool:
        return v == 0 or (isinstance(v, int) and v >= self.g)


def read_lock(t: Any) -> Gen:
    g = yield ("read", "rcu", "G")  # @line L1
    yield ("write", "rcu", t, g)  # @line L2


def read_unlock(t: Any) -> Gen:
    yield ("write", "rcu", t, 0)  # @line L3


def synchronize(others: list) -> Gen:
    """Wait for a grace period: every reader that may hold an old pointer has left."""
    g = (yield ("faa", "rcu", "G", 1)) + 1  # @line L6
    for q in others:
        yield ("wait", "rcu", q, AtLeast(g))  # @line L7


def reader(t: Any) -> Gen:
    """Read the current value. Never waits."""
    yield from read_lock(t)
    p = yield ("read", "cfg", "ptr")  # @line L4
    v = yield ("read", p, "val")  # @line L5
    yield from read_unlock(t)
    return v


def updater(v: Any, readers: list, sync: bool = True) -> Gen:
    """Copy, change, publish, wait, free. One updater at a time."""
    old = yield ("read", "cfg", "ptr")
    new = yield ("alloc", {"val": v})  # @line L8
    yield ("write", "cfg", "ptr", new)  # @line L9
    if sync:
        yield from synchronize(readers)
    yield ("free", old)  # @line L10


def setup(nreaders: int, values: list, sync: bool = True, reads: int = 2):
    """A make() for the explorer: nreaders readers with `reads` reads each, and one updater."""

    def make() -> tuple:
        m = Memory()
        m.cells["rcu"] = {"G": 1, **{q: 0 for q in range(nreaders)}}
        m.static("cfg", ptr=m.new(val="v0"))
        allowed = {"v0", *values}

        def rd(t: int) -> Gen:
            out = []
            for _ in range(reads):
                out.append((yield from reader(t)))
            return out

        def up() -> Gen:
            for v in values:
                yield from updater(v, list(range(nreaders)), sync)
            return []

        def check(mm: Memory, rets: list) -> None:
            for r in rets:
                for v in r:
                    if v not in allowed:
                        raise Corrupt(f"a reader saw {v!r}")

        return m, [rd(t) for t in range(nreaders)] + [up()], None, check

    return make


class RCU(NoReclaim):
    """Synchronous RCU as an SMR scheme: an operation is a read-side section,
    and after it the process waits for a grace period and frees what it removed.

    With defer=True the process does not wait. It is the pattern of call_rcu:
    the removed nodes wait in a list, and every R removals the process starts
    a grace period with a fetch-and-add and checks the readers once without
    waiting. If all of them passed, it frees the nodes that were in the list
    before the fetch-and-add. A stopped reader then blocks nobody, but the
    lists grow without bound.
    """

    name = "rcu"

    def __init__(self, mem: Memory, n: int, sync: bool = True, defer: bool = False, R: int = 4) -> None:
        super().__init__(mem, n)
        self.sync, self.defer, self.R = sync, defer, R
        self.pending: list = [[] for _ in range(n)]
        mem.cells["rcu"] = {"G": 1, **{q: 0 for q in range(n)}}

    def begin(self, t: int) -> Gen:
        yield from read_lock(t)

    def retire(self, t: int, a: int) -> Gen:
        self.mem.note_retire(a)
        self.pending[t].append(a)
        return
        yield

    def end(self, t: int) -> Gen:
        yield from read_unlock(t)
        if self.defer:
            if len(self.pending[t]) >= self.R:
                batch = list(self.pending[t])
                g = (yield ("faa", "rcu", "G", 1)) + 1
                for q in range(self.n):
                    if q != t and (yield ("read", "rcu", q)) not in AtLeast(g):
                        return
                for a in batch:
                    self.pending[t].remove(a)
                    yield ("free", a)
            return
        if self.pending[t]:
            if self.sync:
                yield from synchronize([q for q in range(self.n) if q != t])
            while self.pending[t]:
                yield ("free", self.pending[t].pop())
