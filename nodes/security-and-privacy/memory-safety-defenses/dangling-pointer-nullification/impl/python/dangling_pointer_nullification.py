# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dangling-pointer-nullification/. The authors are listed in prov/2R0MXX.jsonl.

"""Dangling pointer nullification on a simulated memory.

Every heap object has a shadow object that records two sets: the heap
locations that hold a pointer into the object (in), and the locations inside
the object that hold a pointer to another object (out). Each pointer store
into the heap updates the sets. Free walks the in set and overwrites every
location that still points into the object with a null value, so a later use
of those pointers hits the null page and faults.

The memory is a Python bytearray, never real memory. It has a null page at
the bottom, a region for globals that is not tracked, and a heap. The shadow
objects are kept in a sorted list of bases; the original uses a red-black tree.
"""

from bisect import bisect_right, insort
from dataclasses import dataclass, field

WORD = 4  # bytes in a stored pointer
NULL_PAGE = 16  # any access below this address faults


class NullFault(Exception):
    """An access to the null page: a nullified pointer was used."""


class FreeError(Exception):
    """A free of an address that is not the base of a live heap object."""


@dataclass
class Shadow:
    """The shadow object of the heap object [base, end)."""

    base: int
    end: int
    inb: set[int] = field(default_factory=set)  # heap locations that point into this object
    outb: dict[int, int] = field(default_factory=dict)  # location in this object -> base of the target


class DangNullHeap:
    """A first-fit heap with pointer tracking and nullification on free.

    With t live objects: a pointer store costs O(log t) to find the two shadow
    objects; free costs O(log t) plus O(1) per tracked pointer into or out of
    the object. Precondition: pointers are stored with store_ptr, so that
    trace runs on each pointer store, at addresses that are multiples of
    WORD, so that two stored pointers never overlap.
    """

    def __init__(self, size: int = 256, globals_size: int = 32, nullify_value: int = 0) -> None:
        if not 0 <= nullify_value < NULL_PAGE:
            raise ValueError("the null value must lie in the null page")
        self.heap_start = NULL_PAGE + globals_size
        if size <= self.heap_start:
            raise ValueError("no room for a heap")
        self.mem = bytearray(size)
        self.nullify_value = nullify_value
        self.holes: list[tuple[int, int]] = [(self.heap_start, size - self.heap_start)]
        self.bases: list[int] = []
        self.shadow: dict[int, Shadow] = {}

    def find(self, a: int) -> Shadow | None:
        """The shadow object of the live heap object that holds address a, or None."""
        i = bisect_right(self.bases, a) - 1
        if i >= 0:
            s = self.shadow[self.bases[i]]
            if a < s.end:
                return s
        return None

    def trace(self, lhs: int, rhs: int) -> None:
        """Record the store of the pointer value rhs at the location lhs."""
        src = self.find(lhs)
        if src is None:  # @line L1: not in a heap object, so not tracked
            return
        old = src.outb.pop(lhs, None)  # @line L2: drop the old relation of lhs
        if old is not None and old in self.shadow:
            self.shadow[old].inb.discard(lhs)
        dst = self.find(rhs)  # @line L3
        if dst is None:  # @line L4
            return
        src.outb[lhs] = dst.base  # @line L5
        dst.inb.add(lhs)

    def alloc(self, n: int) -> int:
        """Allocate n >= 1 zeroed bytes. Return 0 if no hole is large enough."""
        if n < 1:
            raise ValueError("n must be positive")
        for i, (start, length) in enumerate(self.holes):
            if length >= n:
                break
        else:
            return 0
        if length == n:
            del self.holes[i]
        else:
            self.holes[i] = (start + n, length - n)
        self.mem[start:start + n] = bytes(n)
        insort(self.bases, start)  # @line L6
        self.shadow[start] = Shadow(start, start + n)
        return start  # @line L7

    def free(self, p: int) -> None:
        """Free the object with base p and nullify the pointers into it."""
        if p < NULL_PAGE:
            return  # free of a null pointer does nothing, as in C
        o = self.shadow.get(p)  # @line L8
        if o is None:
            raise FreeError(f"free of {p}, which is not the base of a live object")
        for lhs in list(o.inb):  # @line L9
            src = self.find(lhs)
            if src is not None:
                src.outb.pop(lhs, None)  # @line L10
            if o.base <= self._word(lhs) < o.end:  # @line L11: still points into o
                self.mem[lhs:lhs + WORD] = self.nullify_value.to_bytes(WORD, "little")
        for lhs, target in o.outb.items():  # @line L12
            if target in self.shadow:
                self.shadow[target].inb.discard(lhs)
        del self.shadow[p]  # @line L13
        self.bases.remove(p)
        self._release(p, o.end - p)

    def _word(self, a: int) -> int:
        return int.from_bytes(self.mem[a:a + WORD], "little")

    def _touch(self, a: int, w: int) -> None:
        if a < NULL_PAGE or a + w > len(self.mem):
            raise NullFault(f"access of {w} bytes at {a}")

    def store_ptr(self, lhs: int, rhs: int) -> None:
        """The instrumented pointer store *lhs = rhs."""
        self._touch(lhs, WORD)
        self.trace(lhs, rhs)
        self.mem[lhs:lhs + WORD] = (rhs % (1 << (8 * WORD))).to_bytes(WORD, "little")

    def load_ptr(self, lhs: int) -> int:
        self._touch(lhs, WORD)
        return self._word(lhs)

    def store(self, a: int, w: int, v: int) -> None:
        """A store of an integer: not traced."""
        self._touch(a, w)
        self.mem[a:a + w] = (v % (1 << (8 * w))).to_bytes(w, "little")

    def load(self, a: int, w: int) -> int:
        self._touch(a, w)
        return int.from_bytes(self.mem[a:a + w], "little")

    def _release(self, base: int, n: int) -> None:
        holes = sorted(self.holes + [(base, n)])
        merged: list[tuple[int, int]] = []
        for s, l in holes:
            if merged and merged[-1][0] + merged[-1][1] == s:
                merged[-1] = (merged[-1][0], merged[-1][1] + l)
            else:
                merged.append((s, l))
        self.holes = merged

    def check_invariant(self) -> None:
        """The in and out sets mirror each other, and every location lies in its object."""
        assert self.bases == sorted(self.shadow)
        for s in self.shadow.values():
            for lhs, target in s.outb.items():
                assert s.base <= lhs < s.end and target in self.shadow
                assert lhs in self.shadow[target].inb
            for lhs in s.inb:
                src = self.find(lhs)
                assert src is not None and src.outb.get(lhs) == s.base
