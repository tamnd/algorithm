# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chase-lev-deque/. The authors are listed in prov/HJCFRC.jsonl.

"""The Chase-Lev work-stealing deque, with a growable circular array.

The owner pushes and pops at the bottom; thieves steal at the top. top only
grows. bottom is written only by the owner. Items live in a circular array
at index i mod size; when it is full, the owner copies the live items into an
array twice as large and publishes it. Old arrays are not freed (a thief may
still read one).

Flags that model known bugs, for the tests:

- last_cas=False: the owner takes the last item without the CAS on top, so
  the owner and a thief can both get it;
- reorder_pop=True: the owner reads top before its write of bottom is
  visible (a store-load reordering that x86 allows without a fence).

Each method is a generator that yields one shared memory step at a time (see
explorer.py).
"""

from __future__ import annotations

from typing import Any

from explorer import Memory, Proc
from lincheck import ABORT, EMPTY


class ChaseLevDeque:
    def __init__(self, mem: Memory, size: int = 2, last_cas: bool = True, reorder_pop: bool = False) -> None:
        self.mem = mem
        self.last_cas, self.reorder_pop = last_cas, reorder_pop
        mem.init("top", 0)
        mem.init("bottom", 0)
        a = mem.new(size=size, **{f"s{i}": None for i in range(size)})
        mem.init("array", a)

    def _grow(self, a: int, size: int, b: int, t: int) -> Proc:
        """Copy items t..b-1 into a new array of twice the size."""
        fields = (("size", 2 * size),) + tuple((f"s{i}", None) for i in range(2 * size))
        na = yield ("alloc", fields)
        for i in range(t, b):
            x = yield ("read", (a, f"s{i % size}"))
            yield ("write", (na, f"s{i % (2 * size)}"), x)
        yield ("write", "array", na)
        return na, 2 * size

    def push(self, x: Any) -> Proc:
        b = yield ("read", "bottom")  # @line L1
        t = yield ("read", "top")
        a = yield ("read", "array")
        size = yield ("read", (a, "size"))
        if b - t >= size - 1:  # @line L2
            a, size = yield from self._grow(a, size, b, t)
        yield ("write", (a, f"s{b % size}"), x)  # @line L3
        yield ("write", "bottom", b + 1)  # @line L4
        return None

    def pop(self) -> Proc:
        b = (yield ("read", "bottom")) - 1  # @line L5
        a = yield ("read", "array")
        if self.reorder_pop:  # the bug: top is read before bottom is written
            t = yield ("read", "top")
            yield ("write", "bottom", b)
        else:
            yield ("write", "bottom", b)  # @line L6
            t = yield ("read", "top")  # @line L7
        if t > b:  # @line L8
            yield ("write", "bottom", b + 1)
            return EMPTY
        size = yield ("read", (a, "size"))
        x = yield ("read", (a, f"s{b % size}"))  # @line L9
        if t < b or not self.last_cas:  # @line L10
            return x
        ok = yield ("cas", "top", t, t + 1)  # @line L11
        yield ("write", "bottom", b + 1)  # @line L12
        return x if ok else EMPTY  # @line L13

    def steal(self) -> Proc:
        t = yield ("read", "top")  # @line L14
        b = yield ("read", "bottom")  # @line L15
        if t >= b:  # @line L16
            return EMPTY
        a = yield ("read", "array")  # @line L17
        size = yield ("read", (a, "size"))
        x = yield ("read", (a, f"s{t % size}"))
        if not (yield ("cas", "top", t, t + 1)):  # @line L18
            return ABORT
        return x  # @line L19
