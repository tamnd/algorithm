# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/softbound/. The authors are listed in prov/4RX746.jsonl.

"""SoftBound: per-pointer bounds in a disjoint metadata table, on a simulated memory.

A pointer in a register is a triple (value, base, bound). In memory a pointer
is a plain 4-byte word, so the memory layout does not change. Its base and
bound go to a separate table keyed by the address where the pointer is
stored. A pointer store writes the table entry; a pointer load reads it. An
address with no entry gives the empty bounds (0, 0), so the pointer cannot be
used.

The memory is a Python bytearray, never real memory. As in SoftBound itself,
this checks spatial safety only; objects are never freed here.
"""

from dataclasses import dataclass

WORD = 4  # bytes in a stored pointer


class BoundsError(Exception):
    """An access left the bounds of its pointer."""


@dataclass(frozen=True)
class Ptr:
    """A pointer in a register: its value and the bounds [base, bound)."""

    value: int
    base: int
    bound: int


NULL = Ptr(0, 0, 0)


class SoftBoundMemory:
    """A bump-allocated memory with a disjoint metadata table.

    Every operation costs O(1) time (one dictionary access for the table,
    expected O(1)). The table holds one entry for each address where a pointer
    was stored. Precondition: the program makes pointers only with alloc,
    add, field, load_ptr and int_to_ptr.
    """

    def __init__(self, size: int = 256) -> None:
        if size < 2 * WORD:
            raise ValueError("size is too small")
        self.mem = bytearray(size)
        self.top = WORD  # addresses below WORD stay unused, so 0 is null
        self.meta: dict[int, tuple[int, int]] = {}  # address of a stored pointer -> (base, bound)

    def alloc(self, n: int) -> Ptr:
        """A new zeroed object of n >= 1 bytes, or NULL when the memory is full."""
        if n < 1:
            raise ValueError("n must be positive")
        if self.top + n > len(self.mem):
            return NULL
        b = self.top  # @line L1
        self.top += n
        return Ptr(b, b, b + n)  # @line L2

    def add(self, p: Ptr, k: int) -> Ptr:
        """Pointer arithmetic: the bounds go along unchanged."""
        return Ptr(p.value + k, p.base, p.bound)  # @line L3

    def field(self, p: Ptr, off: int, size: int) -> Ptr:
        """A pointer to the sub-object [p + off, p + off + size), with bounds narrowed to it."""
        v = p.value + off  # @line L4: never wider than the bounds of p
        lo = max(v, p.base)
        hi = max(lo, min(v + size, p.bound))
        return Ptr(v, lo, hi)

    def int_to_ptr(self, v: int) -> Ptr:
        """A pointer made from an integer has empty bounds."""
        return Ptr(v, 0, 0)  # @line L16

    def check(self, p: Ptr, w: int) -> None:
        """Raise BoundsError unless the w bytes at p lie in [p.base, p.bound)."""
        if p.value < p.base or p.value + w > p.bound:  # @line L5
            raise BoundsError(f"access of {w} bytes at {p.value} outside [{p.base}, {p.bound})")  # @line L6

    def load(self, p: Ptr, w: int) -> int:
        """Read a little-endian integer of w bytes."""
        self.check(p, w)  # @line L7
        return int.from_bytes(self.mem[p.value:p.value + w], "little")  # @line L8

    def store(self, p: Ptr, w: int, v: int) -> None:
        """Write an integer of w bytes. The metadata table does not change."""
        self.check(p, w)  # @line L7
        self.mem[p.value:p.value + w] = (v % (1 << (8 * w))).to_bytes(w, "little")  # @line L8

    def store_ptr(self, loc: Ptr, q: Ptr) -> None:
        """Store the pointer q at loc: its value in memory, its bounds in the table."""
        self.check(loc, WORD)  # @line L9
        self.mem[loc.value:loc.value + WORD] = (q.value % (1 << (8 * WORD))).to_bytes(WORD, "little")  # @line L10
        self.meta[loc.value] = (q.base, q.bound)  # @line L11

    def load_ptr(self, loc: Ptr) -> Ptr:
        """Load a pointer from loc together with the bounds stored for that address."""
        self.check(loc, WORD)  # @line L12
        v = int.from_bytes(self.mem[loc.value:loc.value + WORD], "little")  # @line L13
        b, e = self.meta.get(loc.value, (0, 0))  # @line L14: no entry gives empty bounds
        return Ptr(v, b, e)  # @line L15
