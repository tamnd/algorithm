# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lamport-spsc-queue/. The authors are listed in prov/63WNND.jsonl.

"""Lamport's single-producer single-consumer ring buffer, and FastForward.

LamportQueue keeps two shared counters: tail, written only by the producer,
and head, written only by the consumer. Slot t mod N holds the item with
index t. Each operation does at most four reads and writes and no
read-modify-write step, so both operations are wait-free.

The flag store_reorder=True models a machine that may make the write of
tail visible before the write of the slot (no release order). It is there to
show the bug that the release order prevents.

FastForwardQueue (Giacomoni, Moseley and Vachharajani, 2008) keeps the
indices in local variables and marks an empty slot with NONE, so the two
processes share only the slots.

Each method is a generator that yields one shared memory step at a time (see
explorer.py).
"""

from __future__ import annotations

from typing import Any

from explorer import Memory, Proc
from lincheck import EMPTY, FULL

NONE = None


class LamportQueue:
    def __init__(self, mem: Memory, capacity: int, store_reorder: bool = False) -> None:
        self.mem, self.n = mem, capacity
        self.store_reorder = store_reorder
        mem.init("head", 0)
        mem.init("tail", 0)
        for i in range(capacity):
            mem.init(("buf", i), NONE)

    def enq(self, v: Any) -> Proc:
        t = yield ("read", "tail")  # @line L1
        h = yield ("read", "head")
        if t - h == self.n:  # @line L2
            return FULL
        if self.store_reorder:  # the bug: tail is visible before the item
            yield ("write", "tail", t + 1)
            yield ("write", ("buf", t % self.n), v)
            return True
        yield ("write", ("buf", t % self.n), v)  # @line L3
        yield ("write", "tail", t + 1)  # @line L4
        return True  # @line L5

    def deq(self) -> Proc:
        h = yield ("read", "head")  # @line L6
        t = yield ("read", "tail")
        if t == h:  # @line L7
            return EMPTY
        v = yield ("read", ("buf", h % self.n))  # @line L8
        yield ("write", "head", h + 1)  # @line L9
        return v  # @line L10


class FastForwardQueue:
    """The producer and the consumer each keep their own index locally."""

    def __init__(self, mem: Memory, capacity: int) -> None:
        self.mem, self.n = mem, capacity
        self.t = 0  # local to the producer
        self.h = 0  # local to the consumer
        for i in range(capacity):
            mem.init(("slot", i), NONE)

    def enq(self, v: Any) -> Proc:
        cell = ("slot", self.t % self.n)
        if (yield ("read", cell)) is not NONE:
            return FULL
        yield ("write", cell, v)
        self.t += 1
        return True

    def deq(self) -> Proc:
        cell = ("slot", self.h % self.n)
        v = yield ("read", cell)
        if v is NONE:
            return EMPTY
        yield ("write", cell, NONE)
        self.h += 1
        return v
