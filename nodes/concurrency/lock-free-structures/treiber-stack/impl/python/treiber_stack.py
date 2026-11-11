# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/treiber-stack/. The authors are listed in prov/YJWGPQ.jsonl.

"""The Treiber stack on simulated shared memory.

Each method is a generator that yields one shared memory step at a time (see
explorer.py), so a scheduler can interleave several processes step by step.
push and pop are CAS loops on the word "top". With tagged=True, top holds a
pair (pointer, tag) and each successful CAS adds one to the tag, which stops
the ABA problem when the allocator reuses the address of a popped node. With
reclaim=True, pop frees the node that it removes.

Cost: a push or pop that meets no interference takes a constant number of
steps (4 for push, 5 for pop). Under contention a CAS can fail each time, so
the stack is lock-free but not wait-free.
"""

from __future__ import annotations

from typing import Any

from explorer import NULL, Memory, Proc
from lincheck import EMPTY


class TreiberStack:
    def __init__(self, mem: Memory, tagged: bool = False, reclaim: bool = False) -> None:
        self.mem, self.tagged, self.reclaim = mem, tagged, reclaim
        mem.init("top", (NULL, 0) if tagged else NULL)

    def _ptr(self, top: Any) -> int:
        return top[0] if self.tagged else top

    def _with(self, old: Any, ptr: int) -> Any:
        return (ptr, old[1] + 1) if self.tagged else ptr

    def push(self, v: Any) -> Proc:
        n = yield ("alloc", (("val", v), ("next", NULL)))  # @line L1
        while True:  # @line L2
            t = yield ("read", "top")  # @line L3
            yield ("write", (n, "next"), self._ptr(t))  # @line L4
            if (yield ("cas", "top", t, self._with(t, n))):  # @line L5
                return None

    def pop(self) -> Proc:
        while True:  # @line L6
            t = yield ("read", "top")  # @line L7
            if self._ptr(t) == NULL:  # @line L8
                return EMPTY
            nx = yield ("read", (self._ptr(t), "next"))  # @line L9
            if (yield ("cas", "top", t, self._with(t, nx))):  # @line L10
                break
        v = yield ("read", (self._ptr(t), "val"))  # @line L11
        if self.reclaim:
            yield ("free", self._ptr(t))  # @line L12
        return v  # @line L13

    def contents(self) -> list[Any]:
        """The items from top to bottom, read without steps (for tests, in a quiet state)."""
        out, p = [], self._ptr(self.mem.peek("top"))
        while p != NULL:
            out.append(self.mem.peek((p, "val")))
            p = self.mem.peek((p, "next"))
        return out


def push_all(mem: Memory, stack: TreiberStack, items: list[Any]) -> None:
    """Push items in order before a run starts, with no steps (the last one ends on top)."""
    for v in items:
        n = mem.new(val=v, next=stack._ptr(mem.peek("top")))
        mem.init("top", stack._with(mem.peek("top"), n))
