# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/herlihy-wing-queue/. The authors are listed in prov/FY15RG.jsonl.

"""The Herlihy and Wing array queue on simulated shared memory.

An enqueue takes a fresh slot with fetch-and-add on the word "back" and then
stores its item there. A dequeue reads back and scans the slots 0 .. back-1,
and swaps NONE into each one; the first item it gets out is its result. If the
scan finds nothing, it starts again: a dequeue on an empty queue waits (spins)
until an item is there.

The paper uses an infinite array. Here the array has a fixed capacity, which
must be at least the number of enqueues of a run.

Each method is a generator that yields one shared memory step at a time (see
explorer.py).

Cost: an enqueue takes exactly 2 steps (wait-free). A scan of a dequeue takes
1 + r steps, where r is the value of back that it read. A dequeue on an empty
queue never returns.
"""

from __future__ import annotations

from typing import Any

from explorer import Memory, Proc

NONE = None


class HWQueue:
    def __init__(self, mem: Memory, capacity: int = 8) -> None:
        self.mem, self.capacity = mem, capacity
        mem.init("back", 0)
        for i in range(capacity):
            mem.init(("items", i), NONE)

    def enq(self, x: Any) -> Proc:
        i = yield ("faa", "back", 1)  # @line L1
        if i >= self.capacity:
            raise IndexError("the simulated array is full")
        yield ("write", ("items", i), x)  # @line L2
        return True

    def deq(self) -> Proc:
        while True:  # @line L3
            r = yield ("read", "back")  # @line L4
            for i in range(min(r, self.capacity)):  # @line L5
                x = yield ("swap", ("items", i), NONE)  # @line L6
                if x is not NONE:  # @line L7
                    return x
