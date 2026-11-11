# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/michael-scott-queue/. The authors are listed in prov/N8QFHV.jsonl.

"""The Michael and Scott lock-free queue, and their two-lock queue, on simulated memory.

The lock-free queue is a singly linked list with a dummy node. Head points to
the dummy; the items are in the nodes after it. Tail points to the last node
or to the node just before it (Tail can lag by one). An enqueue links its node
with a CAS on the next field of the last node, then swings Tail with a CAS. An
operation that finds Tail lagging swings it first: this is the helping step.

Two flags switch parts of the algorithm off, to show why they are there:
help=False removes the two helping CASes on Tail, and head_tail_check=False
removes the test "Head = Tail" in dequeue, so Head can pass Tail.

Each method is a generator that yields one shared memory step at a time (see
explorer.py). Nodes are not freed (the model of a garbage collector).

Cost: alone, an enqueue takes 6 steps and a dequeue 6 steps (4 on an empty
queue). Under contention an operation can retry without bound: the queue is
lock-free, not wait-free. The two-lock queue takes O(1) steps plus the wait
for its lock, and it is blocking.
"""

from __future__ import annotations

from typing import Any

from explorer import NULL, Memory, Proc
from lincheck import EMPTY


class MSQueue:
    def __init__(self, mem: Memory, help: bool = True, head_tail_check: bool = True) -> None:
        self.mem, self.help, self.head_tail_check = mem, help, head_tail_check
        d = mem.new(val=None, next=NULL)
        mem.init("Head", d)
        mem.init("Tail", d)

    def enq(self, v: Any) -> Proc:
        n = yield ("alloc", (("val", v), ("next", NULL)))  # @line L1
        while True:  # @line L2
            t = yield ("read", "Tail")  # @line L3
            nx = yield ("read", (t, "next"))  # @line L4
            if t == (yield ("read", "Tail")):  # @line L5
                if nx == NULL:  # @line L6
                    if (yield ("cas", (t, "next"), NULL, n)):  # @line L7
                        break
                elif self.help:
                    yield ("cas", "Tail", t, nx)  # @line L8
        yield ("cas", "Tail", t, n)  # @line L9
        return True

    def deq(self) -> Proc:
        while True:  # @line L10
            h = yield ("read", "Head")  # @line L11
            t = yield ("read", "Tail")  # @line L12
            nx = yield ("read", (h, "next"))  # @line L13
            if h == (yield ("read", "Head")):  # @line L14
                if self.head_tail_check and h == t:  # @line L15
                    if nx == NULL:  # @line L16
                        return EMPTY
                    if self.help:
                        yield ("cas", "Tail", t, nx)  # @line L17
                else:
                    if nx == NULL:  # only reached when the check is removed
                        return EMPTY
                    v = yield ("read", (nx, "val"))  # @line L18
                    if (yield ("cas", "Head", h, nx)):  # @line L19
                        return v  # @line L20

    def contents(self) -> list[Any]:
        out, p = [], self.mem.peek((self.mem.peek("Head"), "next"))
        while p != NULL:
            out.append(self.mem.peek((p, "val")))
            p = self.mem.peek((p, "next"))
        return out

    def enq_all(self, items: list[Any]) -> None:
        """Enqueue items before a run starts, with no steps."""
        for v in items:
            n = self.mem.new(val=v, next=NULL)
            self.mem.init((self.mem.peek("Tail"), "next"), n)
            self.mem.init("Tail", n)

    def tail_reachable_from_head(self) -> bool:
        """The invariant that the check Head = Tail protects: Tail is at or after Head."""
        p, tail = self.mem.peek("Head"), self.mem.peek("Tail")
        while p != NULL:
            if p == tail:
                return True
            p = self.mem.peek((p, "next"))
        return False


class TwoLockQueue:
    """The blocking queue of the same paper: one lock for Head, one for Tail.

    The locks are test-and-set spin locks built from CAS. A process that stops
    while it holds a lock blocks every other process of the same side.
    """

    def __init__(self, mem: Memory) -> None:
        self.mem = mem
        d = mem.new(val=None, next=NULL)
        mem.init("Head", d)
        mem.init("Tail", d)
        mem.init("HLock", False)
        mem.init("TLock", False)

    def _lock(self, w: str) -> Proc:
        while not (yield ("cas", w, False, True)):
            pass

    def enq(self, v: Any) -> Proc:
        n = yield ("alloc", (("val", v), ("next", NULL)))
        yield from self._lock("TLock")
        t = yield ("read", "Tail")
        yield ("write", (t, "next"), n)
        yield ("write", "Tail", n)
        yield ("write", "TLock", False)
        return True

    def deq(self) -> Proc:
        yield from self._lock("HLock")
        h = yield ("read", "Head")
        nx = yield ("read", (h, "next"))
        if nx == NULL:
            yield ("write", "HLock", False)
            return EMPTY
        v = yield ("read", (nx, "val"))
        yield ("write", "Head", nx)
        yield ("write", "HLock", False)
        return v
