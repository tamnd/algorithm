# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kogan-petrank-queue/. The authors are listed in prov/MAZDKN.jsonl.

"""The Kogan and Petrank wait-free queue on simulated shared memory.

The queue is the linked list of the Michael and Scott queue (a dummy node,
Head and Tail). Each process i has an entry state[i] that holds an operation
descriptor (phase, pending, enqueue, node). To start an operation, a process
picks a phase one larger than all phases it sees, publishes a pending
descriptor, and then helps every pending operation whose phase is at most its
own, in index order, before it returns. So an operation that is pending is
finished by every operation that starts after it.

A descriptor is an immutable tuple (uid, phase, pending, enqueue, node); a CAS
on state[i] compares the whole tuple, so the uid plays the part of a new
object in the Java code of the paper. Nodes have the fields value, next,
enq_tid and deq_tid. No node is freed (the model of a garbage collector).

Each method is a generator that yields one shared memory step at a time (see
explorer.py).

Cost: every operation completes within O(n^2) of its own steps for n
processes, whatever the other processes do (wait-free); bound(n) below gives
the explicit constant that the page derives.
"""

from __future__ import annotations

from typing import Any

from explorer import NULL, Memory, Proc
from lincheck import EMPTY


def bound(n: int) -> int:
    """The step bound per operation derived on the page."""
    return 2 * n + 1 + n * 20 * (6 * n + 2) + 11


class KPQueue:
    def __init__(self, mem: Memory, n: int) -> None:
        self.mem, self.n = mem, n
        d = mem.new(value=None, next=NULL, enq_tid=-1, deq_tid=-1)
        mem.init("Head", d)
        mem.init("Tail", d)
        for i in range(n):
            mem.init(("state", i), (("init", i), -1, False, True, NULL))

    def handle(self, tid: int) -> "Handle":
        return Handle(self, tid)

    def enq_all(self, items: list[Any]) -> None:
        """Enqueue items before a run starts, with no steps."""
        for v in items:
            node = self.mem.new(value=v, next=NULL, enq_tid=-1, deq_tid=-1)
            self.mem.init((self.mem.peek("Tail"), "next"), node)
            self.mem.init("Tail", node)


class Handle:
    """The operations of process tid."""

    def __init__(self, q: KPQueue, tid: int) -> None:
        self.q, self.tid = q, tid
        self.made = 0

    def desc(self, phase: int, pending: bool, enqueue: bool, node: int) -> tuple:
        """A new descriptor. The uid (creator, count) makes it a new object for CAS."""
        self.made += 1
        return ((self.tid, self.made), phase, pending, enqueue, node)

    def max_phase(self) -> Proc:
        m = -1
        for i in range(self.q.n):
            d = yield ("read", ("state", i))
            m = max(m, d[1])
        return m

    def still_pending(self, tid: int, phase: int) -> Proc:
        d = yield ("read", ("state", tid))
        return d[2] and d[1] <= phase

    def enq(self, v: Any) -> Proc:
        phase = (yield from self.max_phase()) + 1  # @line L1
        node = yield ("alloc", (("value", v), ("next", NULL), ("enq_tid", self.tid), ("deq_tid", -1)))
        yield ("write", ("state", self.tid), self.desc(phase, True, True, node))  # @line L2
        yield from self.help(phase)  # @line L3
        yield from self.help_finish_enq()  # @line L4
        return True

    def deq(self) -> Proc:
        phase = (yield from self.max_phase()) + 1  # @line L5
        yield ("write", ("state", self.tid), self.desc(phase, True, False, NULL))  # @line L6
        yield from self.help(phase)  # @line L7
        yield from self.help_finish_deq()  # @line L8
        d = yield ("read", ("state", self.tid))  # @line L9
        if d[4] == NULL:  # @line L10
            return EMPTY
        nx = yield ("read", (d[4], "next"))  # @line L11
        return (yield ("read", (nx, "value")))

    def help(self, phase: int) -> Proc:
        for i in range(self.q.n):  # @line L12
            d = yield ("read", ("state", i))  # @line L13
            if d[2] and d[1] <= phase:  # @line L14
                if d[3]:
                    yield from self.help_enq(i, phase)  # @line L15
                else:
                    yield from self.help_deq(i, phase)  # @line L16

    def help_enq(self, tid: int, phase: int) -> Proc:
        while (yield from self.still_pending(tid, phase)):  # @line L17
            last = yield ("read", "Tail")  # @line L18
            nxt = yield ("read", (last, "next"))  # @line L19
            if last == (yield ("read", "Tail")):  # @line L20
                if nxt == NULL:  # @line L21
                    if (yield from self.still_pending(tid, phase)):  # @line L22
                        d = yield ("read", ("state", tid))
                        if (yield ("cas", (last, "next"), NULL, d[4])):  # @line L23
                            yield from self.help_finish_enq()  # @line L24
                            return
                else:
                    yield from self.help_finish_enq()  # @line L25

    def help_finish_enq(self) -> Proc:
        last = yield ("read", "Tail")  # @line L26
        nxt = yield ("read", (last, "next"))  # @line L27
        if nxt != NULL:  # @line L28
            tid = yield ("read", (nxt, "enq_tid"))  # @line L29
            cur = yield ("read", ("state", tid))  # @line L30
            if last == (yield ("read", "Tail")) and cur[4] == nxt:  # @line L31
                yield ("cas", ("state", tid), cur, self.desc(cur[1], False, True, nxt))  # @line L32
            yield ("cas", "Tail", last, nxt)  # @line L33

    def help_deq(self, tid: int, phase: int) -> Proc:
        while (yield from self.still_pending(tid, phase)):
            first = yield ("read", "Head")
            last = yield ("read", "Tail")
            nxt = yield ("read", (first, "next"))
            if first != (yield ("read", "Head")):
                continue
            if first == last:
                if nxt == NULL:  # the queue is empty: finish tid with no node
                    cur = yield ("read", ("state", tid))
                    if last == (yield ("read", "Tail")) and cur[2] and cur[1] <= phase:
                        yield ("cas", ("state", tid), cur, self.desc(cur[1], False, False, NULL))
                else:
                    yield from self.help_finish_enq()  # Tail lags: help the enqueue
            else:
                cur = yield ("read", ("state", tid))
                node = cur[4]
                if not (cur[2] and cur[1] <= phase):
                    break
                if first == (yield ("read", "Head")) and node != first:
                    if not (yield ("cas", ("state", tid), cur, self.desc(cur[1], True, False, first))):
                        continue
                yield ("cas", (first, "deq_tid"), -1, tid)  # the linearization point if it succeeds
                yield from self.help_finish_deq()

    def help_finish_deq(self) -> Proc:
        first = yield ("read", "Head")
        nxt = yield ("read", (first, "next"))
        tid = yield ("read", (first, "deq_tid"))
        if tid != -1:
            cur = yield ("read", ("state", tid))
            if first == (yield ("read", "Head")) and nxt != NULL:
                yield ("cas", ("state", tid), cur, self.desc(cur[1], False, False, cur[4]))
                yield ("cas", "Head", first, nxt)
