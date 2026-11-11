# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arora-blumofe-plaxton-deque/. The authors are listed in prov/YWVGPT.jsonl.

"""The Arora-Blumofe-Plaxton (ABP) non-blocking work-stealing deque.

The owner calls push_bottom and pop_bottom; thieves call pop_top. The items
live in a fixed array deq[0..capacity-1]. The word age holds the pair
(tag, top) and is changed by CAS as one word. When the owner empties the
deque it resets top and bot to 0 and adds one to the tag, so that a thief
with an old copy of age cannot succeed (the ABA problem).

The paper returns NULL from popTop both when the deque is empty and when the
CAS fails. This module returns EMPTY in the first case and ABORT in the
second, so that the tests can tell them apart.

Flag that models a known bug, for the tests:

- tag=False: the owner does not change the tag on a reset, so the CAS of a
  slow thief can succeed on a deque that was emptied and refilled.

Each method is a generator that yields one shared memory step at a time (see
explorer.py).
"""

from __future__ import annotations

from typing import Any

from explorer import Memory, Proc
from lincheck import ABORT, EMPTY


class ABPDeque:
    def __init__(self, mem: Memory, capacity: int = 4, tag: bool = True) -> None:
        self.mem, self.capacity, self.tag = mem, capacity, tag
        mem.init("age", (0, 0))  # (tag, top)
        mem.init("bot", 0)
        for i in range(capacity):
            mem.init(("deq", i), None)

    # The paper calls these pushBottom, popBottom and popTop. The short names
    # push, pop and steal let the tests use the shared specification.

    def push(self, x: Any) -> Proc:
        local_bot = yield ("read", "bot")  # @line L1
        if local_bot >= self.capacity:
            raise OverflowError("the ABP deque has a fixed size")
        yield ("write", ("deq", local_bot), x)  # @line L2
        yield ("write", "bot", local_bot + 1)  # @line L3
        return None

    def steal(self) -> Proc:
        old_age = yield ("read", "age")  # @line L4
        local_bot = yield ("read", "bot")  # @line L5
        if local_bot <= old_age[1]:  # @line L6
            return EMPTY
        x = yield ("read", ("deq", old_age[1]))  # @line L7
        new_age = (old_age[0], old_age[1] + 1)  # @line L8
        if (yield ("cas", "age", old_age, new_age)):  # @line L9
            return x
        return ABORT  # @line L10

    def pop(self) -> Proc:
        local_bot = yield ("read", "bot")  # @line L11
        if local_bot == 0:  # @line L12
            return EMPTY
        local_bot -= 1
        yield ("write", "bot", local_bot)  # @line L13
        x = yield ("read", ("deq", local_bot))  # @line L14
        old_age = yield ("read", "age")  # @line L15
        if local_bot > old_age[1]:  # @line L16
            return x
        yield ("write", "bot", 0)  # @line L17
        new_age = (old_age[0] + 1 if self.tag else old_age[0], 0)  # @line L18
        if local_bot == old_age[1]:  # @line L19
            if (yield ("cas", "age", old_age, new_age)):
                return x
        yield ("write", "age", new_age)  # @line L20
        return EMPTY
