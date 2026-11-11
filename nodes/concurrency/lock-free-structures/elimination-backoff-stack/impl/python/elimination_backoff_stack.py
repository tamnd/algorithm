# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elimination-backoff-stack/. The authors are listed in prov/BE3KEB.jsonl.

"""The elimination back-off stack on simulated shared memory.

A Treiber stack (the word "top") with an elimination array of exchanger slots.
An operation first tries one CAS on top. If the CAS fails, it picks a random
slot in [0, range) and tries to meet an operation of the other kind there. A
push and a pop that meet cancel: the pop returns the value of the push and
neither touches top. The exchanger is the lock-free exchanger of Herlihy and
Shavit: a slot holds (item, state) with state FREE, WAITING or BUSY. The range
is adapted per process: it grows by one after an elimination and shrinks by one
after a timeout. Timeouts are counted in reads of the slot.

Each method is a generator that yields one shared memory step at a time (see
explorer.py). No node is freed (the model of a garbage collector), so the
stack has no ABA problem.

Cost: alone, a push takes 4 steps and a pop 4 steps (1 on an empty stack).
Under contention an operation can retry without bound, so the stack is
lock-free, not wait-free.
"""

from __future__ import annotations

import random
from typing import Any

from explorer import NULL, Memory, Proc
from lincheck import EMPTY

FREE, WAITING, BUSY = "FREE", "WAITING", "BUSY"
POP = "POP"  # the item that a pop offers in the exchanger
FAIL = "FAIL"


class EliminationBackoffStack:
    """The shared part: the word top and the slots ("slot", i) for i < capacity."""

    def __init__(self, mem: Memory, capacity: int = 2, timeout: int = 2) -> None:
        self.mem, self.capacity, self.timeout = mem, capacity, timeout
        mem.init("top", NULL)
        for i in range(capacity):
            mem.init(("slot", i), (None, FREE))

    def handle(self, pid: int, seed: int = 0) -> "Handle":
        """The view of one process, with its own random source and range policy."""
        return Handle(self, random.Random(seed * 1000 + pid))

    def push_all(self, items: list[Any]) -> None:
        """Push items before a run starts, with no steps (the last one ends on top)."""
        for v in items:
            self.mem.init("top", self.mem.new(val=v, next=self.mem.peek("top")))

    def contents(self) -> list[Any]:
        out, p = [], self.mem.peek("top")
        while p != NULL:
            out.append(self.mem.peek((p, "val")))
            p = self.mem.peek((p, "next"))
        return out


class Handle:
    def __init__(self, stack: EliminationBackoffStack, rng: random.Random) -> None:
        self.s, self.rng = stack, rng
        self.range = 1
        self.eliminated = 0

    def record_success(self) -> None:
        self.eliminated += 1
        self.range = min(self.range + 1, self.s.capacity)

    def record_timeout(self) -> None:
        self.range = max(self.range - 1, 1)

    def try_push(self, n: int) -> Proc:
        t = yield ("read", "top")
        yield ("write", (n, "next"), t)
        return (yield ("cas", "top", t, n))

    def try_pop(self) -> Proc:
        t = yield ("read", "top")
        if t == NULL:
            return EMPTY
        nx = yield ("read", (t, "next"))
        if (yield ("cas", "top", t, nx)):
            return (yield ("read", (t, "val")))
        return FAIL

    def exchange(self, w: Any, mine: Any) -> Proc:
        """Offer mine in slot w. Return (True, the partner's item) or (False, None) on a timeout."""
        for _ in range(self.s.timeout):
            yours, state = yield ("read", w)
            if state == FREE:
                if (yield ("cas", w, (yours, FREE), (mine, WAITING))):
                    for _ in range(self.s.timeout):
                        yours, state = yield ("read", w)
                        if state == BUSY:
                            yield ("write", w, (None, FREE))
                            return True, yours
                    if (yield ("cas", w, (mine, WAITING), (None, FREE))):
                        return False, None
                    yours, _ = yield ("read", w)  # a partner came at the last moment
                    yield ("write", w, (None, FREE))
                    return True, yours
            elif state == WAITING:
                if (yield ("cas", w, (yours, WAITING), (mine, BUSY))):
                    return True, yours
        return False, None

    def push(self, v: Any) -> Proc:
        n = yield ("alloc", (("val", v), ("next", NULL)))  # @line L1
        while True:  # @line L2
            if (yield from self.try_push(n)):  # @line L3
                return None
            i = self.rng.randrange(self.range)  # @line L4
            ok, y = yield from self.exchange(("slot", i), v)  # @line L5
            if ok and y == POP:  # @line L6
                self.record_success()
                return None
            if not ok:  # @line L7
                self.record_timeout()

    def pop(self) -> Proc:
        while True:  # @line L8
            r = yield from self.try_pop()  # @line L9
            if r != FAIL:  # @line L10
                return r
            i = self.rng.randrange(self.range)  # @line L11
            ok, y = yield from self.exchange(("slot", i), POP)  # @line L12
            if ok and y != POP:  # @line L13
                self.record_success()
                return y
            if not ok:  # @line L14
                self.record_timeout()
