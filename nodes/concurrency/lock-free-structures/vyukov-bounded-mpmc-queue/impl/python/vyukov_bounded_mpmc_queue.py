# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vyukov-bounded-mpmc-queue/. The authors are listed in prov/8Z65SA.jsonl.

"""Dmitry Vyukov's bounded multi-producer multi-consumer queue.

An array of N cells; each cell has a sequence number seq and a data word.
Cell i starts with seq = i. Two shared counters, enq_pos and deq_pos, hand
out positions. A producer may fill position pos when the cell of pos has
seq = pos; it claims pos with a CAS on enq_pos, writes the data, and sets
seq = pos + 1. A consumer may empty position pos when the cell has
seq = pos + 1; it claims pos with a CAS on deq_pos, reads the data, and sets
seq = pos + N, which makes the cell ready for the producer of the next lap.

The operations are try operations: enq returns FULL and deq returns EMPTY
when the cell they look at is not ready. A producer that stops after its
claim and before it sets seq leaves its cell not ready for ever. Later items
cannot be dequeued, so the queue is not lock-free as a FIFO queue.

The C++ code uses compare_exchange_weak, which on failure loads the current
value; the step ("cmpxchg", w, old, new) does the same.

Each method is a generator that yields one shared memory step at a time (see
explorer.py).
"""

from __future__ import annotations

from typing import Any

from explorer import Memory, Proc
from lincheck import EMPTY, FULL


class VyukovQueue:
    def __init__(self, mem: Memory, capacity: int) -> None:
        self.mem, self.n = mem, capacity
        mem.init("enq_pos", 0)
        mem.init("deq_pos", 0)
        for i in range(capacity):
            mem.init(("seq", i), i)
            mem.init(("data", i), None)

    def enq(self, v: Any) -> Proc:
        pos = yield ("read", "enq_pos")  # @line L1
        while True:  # @line L2
            seq = yield ("read", ("seq", pos % self.n))  # @line L3
            dif = seq - pos  # @line L4
            if dif == 0:  # @line L5
                old = yield ("cmpxchg", "enq_pos", pos, pos + 1)  # @line L6
                if old == pos:  # @line L7
                    break
                pos = old
            elif dif < 0:  # @line L8
                return FULL
            else:
                pos = yield ("read", "enq_pos")  # @line L9
        yield ("write", ("data", pos % self.n), v)  # @line L10
        yield ("write", ("seq", pos % self.n), pos + 1)  # @line L11
        return True

    def deq(self) -> Proc:
        pos = yield ("read", "deq_pos")  # @line L12
        while True:  # @line L13
            seq = yield ("read", ("seq", pos % self.n))  # @line L14
            dif = seq - (pos + 1)  # @line L15
            if dif == 0:  # @line L16
                old = yield ("cmpxchg", "deq_pos", pos, pos + 1)  # @line L17
                if old == pos:  # @line L18
                    break
                pos = old
            elif dif < 0:  # @line L19
                return EMPTY
            else:
                pos = yield ("read", "deq_pos")  # @line L20
        v = yield ("read", ("data", pos % self.n))  # @line L21
        yield ("write", ("seq", pos % self.n), pos + self.n)  # @line L22
        return v

    def deq_wait(self) -> Proc:
        """A blocking dequeue: retry until an item comes."""
        while True:
            v = yield from self.deq()
            if v != EMPTY:
                return v
