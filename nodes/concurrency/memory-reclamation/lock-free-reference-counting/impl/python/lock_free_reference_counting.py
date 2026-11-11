# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lock-free-reference-counting/. The authors are listed in prov/YM4G39.jsonl.
"""Lock-free reference counting on a Treiber stack and a Michael and Scott queue, on smr_sim.py.

Every node has a count rc of the references to it: links from the roots or
from other nodes, and local references of processes. A process that puts a
new link into a shared word adds one to the target first; a process that
removes a link, or drops a local reference, calls release. Four modes:

  "valois": Valois's scheme with the correction of Michael and Scott. The
     nodes live in a type-stable pool, so a stale increment is harmless.
     safe_read adds one to the count of the node it read, then checks that
     the source still points to it; if not, it releases the node again. The
     count moves in steps of 2, and the low bit is a claim bit: the process
     that brings the count to 0 must also win a CAS from 0 to 1 before it
     frees the node, and allocation adds 1 to clear the bit.
  "naive": the same without the type-stable pool. The increment can come
     after the free, and the simulator reports a use after free.
  "noclaim": the type-stable pool in steps of 1 and without the claim bit,
     as in Valois's paper. Two processes can both see the count go to 0,
     and the simulator reports a double free.
  "dcas": the scheme of Detlefs, Martin, Moir and Steele. safe_read adds
     one to the count with a DCAS that also checks that the source still
     points to the node, so a freed node is never counted.

The removed node is marked with note_retire only so that the simulator can
measure the garbage; the free happens in release.

Precondition: every pointer that a process keeps is counted, and there are
no cycles. Cost: O(1) steps per read without contention; one release can
free a chain of nodes. A process that holds a reference keeps alive every
node that can be reached from it.
"""

from __future__ import annotations

from typing import Any, Optional

from smr_sim import Gen, Memory, conserve, queue_values, stack_values

ONE = {"valois": 2, "naive": 2, "noclaim": 1, "dcas": 1}


class RefCount:
    def __init__(self, mem: Memory, mode: str = "valois") -> None:
        self.mem, self.mode, self.one = mem, mode, ONE[mode]

    def alloc(self, fields: dict) -> Gen:
        """Take a node; in a type-stable pool its count is kept, so add to it."""
        a = yield ("alloc", {**fields, "rc": 1 if self.one == 2 else 0})
        yield ("faa", a, "rc", 1)  # count the own reference (and clear the claim bit)
        return a

    def link(self, q: Optional[int]) -> Gen:
        """Count a new link to q before the CAS that makes it."""
        if q is not None:
            yield ("faa", q, "rc", self.one)

    def safe_read(self, a: Any, f: str) -> Gen:
        """Read the pointer a.f and count a reference to the node it names."""
        while True:
            q = yield ("read", a, f)  # @line L1
            if q is None:
                return None
            if self.mode == "dcas":
                c = yield ("read", q, "rc")
                if (yield ("dcas2", a, f, q, "rc", q, c, q, c + 1)):
                    return q
                continue
            yield ("faa", q, "rc", self.one)  # @line L2
            if (yield ("read", a, f)) == q:  # @line L3
                return q
            yield from self.release(q)  # @line L4

    def release(self, q: Optional[int]) -> Gen:
        """Drop one reference to q, and free q (and release its link) when none is left."""
        while q is not None:
            if (yield ("faa", q, "rc", -self.one)) != self.one:  # @line L5
                return
            if self.mode in ("valois", "naive"):
                if not (yield ("cas", q, "rc", 0, 1)):  # @line L6
                    return
            nxt = yield ("read", q, "next")
            yield ("free", q)  # @line L7
            q = nxt


def push(R: RefCount, v: Any) -> Gen:
    node = yield from R.alloc({"val": v, "next": None})
    while True:
        top = yield from R.safe_read("root", "top")
        yield ("write", node, "next", top)  # the own reference to top becomes the link node.next
        if (yield ("cas", "root", "top", top, node)):  # the own reference to node becomes the root link
            yield from R.release(top)  # the root no longer points to top
            return
        yield ("write", node, "next", None)
        yield from R.release(top)


def pop(R: RefCount) -> Gen:
    while True:
        top = yield from R.safe_read("root", "top")
        if top is None:
            return None
        nxt = yield from R.safe_read(top, "next")
        if (yield ("cas", "root", "top", top, nxt)):  # the own reference to nxt becomes the root link
            R.mem.note_retire(top)
            v = yield ("read", top, "val")
            yield from R.release(top)  # the link of the root
            yield from R.release(top)  # the own reference
            return v
        yield from R.release(nxt)
        yield from R.release(top)


def enq(R: RefCount, v: Any) -> Gen:
    node = yield from R.alloc({"val": v, "next": None})
    while True:
        tl = yield from R.safe_read("q", "tail")
        nx = yield from R.safe_read(tl, "next")
        if (yield ("read", "q", "tail")) == tl:
            if nx is None:
                yield from R.link(node)
                if (yield ("cas", tl, "next", None, node)):
                    yield from R.link(node)
                    if (yield ("cas", "q", "tail", tl, node)):
                        yield from R.release(tl)  # the tail no longer points to tl
                    else:
                        yield from R.release(node)
                    yield from R.release(tl)
                    yield from R.release(node)  # the own reference
                    return
                yield from R.release(node)
            else:
                yield from R.link(nx)
                if (yield ("cas", "q", "tail", tl, nx)):
                    yield from R.release(tl)
                else:
                    yield from R.release(nx)
        yield from R.release(nx)
        yield from R.release(tl)


def deq(R: RefCount) -> Gen:
    while True:
        hd = yield from R.safe_read("q", "head")
        tl = yield from R.safe_read("q", "tail")
        nx = yield from R.safe_read(hd, "next")
        v = None
        done = False
        if (yield ("read", "q", "head")) == hd:
            if nx is None:
                done = True
            elif hd == tl:
                yield from R.link(nx)
                if (yield ("cas", "q", "tail", tl, nx)):
                    yield from R.release(tl)
                else:
                    yield from R.release(nx)
            else:
                v = yield ("read", nx, "val")
                yield from R.link(nx)
                if (yield ("cas", "q", "head", hd, nx)):
                    R.mem.note_retire(hd)
                    yield from R.release(hd)  # the head no longer points to hd
                    done = True
                else:
                    yield from R.release(nx)
        yield from R.release(nx)
        yield from R.release(tl)
        yield from R.release(hd)
        if done:
            return v


def setup(programs: list, mode: str = "valois", kind: str = "stack", initial: int = 2):
    """A make() for the explorer: a counted stack or queue with `initial` values."""

    def make() -> tuple:
        ts = mode in ("valois", "noclaim", "dcas")
        m = Memory(type_stable=ts, stable=("rc",))
        one = ONE[mode]
        if kind == "stack":
            m.static("root", top=None)
            for j in range(initial):
                top = m.cells["root"]["top"]
                m.cells["root"]["top"] = m.new(val=("init", j), next=top, rc=one)
        else:
            d = m.new(val=None, next=None, rc=2 * one)
            m.static("q", head=d, tail=d)
            for j in range(initial):
                tl = m.cells["q"]["tail"]
                a = m.new(val=("init", j), next=None, rc=2 * one)
                m.cells[tl]["next"] = a
                m.cells[tl]["rc"] -= one
                m.cells["q"]["tail"] = a
        R = RefCount(m, mode)
        pushed = [("init", j) for j in range(initial)] + [op[1] for p in programs for op in p if op[0] in ("push", "enq")]

        def prog(ops: list) -> Gen:
            out = []
            for op in ops:
                if op[0] == "push":
                    yield from push(R, op[1])
                elif op[0] == "enq":
                    yield from enq(R, op[1])
                elif op[0] == "pop":
                    out.append((yield from pop(R)))
                else:
                    out.append((yield from deq(R)))
            return out

        def check(mm: Memory, rets: list) -> None:
            left = stack_values(mm) if kind == "stack" else queue_values(mm)
            conserve(pushed, [v for r in rets for v in r], left)

        return m, [prog(p) for p in programs], None, check

    return make
