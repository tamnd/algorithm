# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fat-pointer/. The authors are listed in prov/QJJ3SE.jsonl.

"""Fat pointers with a base, a bound and a capability, on a simulated heap.

This is the safe pointer of Austin, Breach and Sohi (PLDI 1994) in a small
model. The memory is a Python bytearray, never real memory. Each pointer
carries the base and the bound of its block and the capability number of the
allocation. A load or a store checks the bounds and then asks the capability
store whether the allocation is still live.
"""

from dataclasses import dataclass


class AccessError(Exception):
    """A checked access, free or arithmetic step was refused."""


class SpatialError(AccessError):
    """The access is outside the bounds that the pointer carries."""


class TemporalError(AccessError):
    """The allocation of the pointer was freed."""


@dataclass(frozen=True)
class FatPointer:
    """A pointer value with the bounds [base, bound) and a capability number.

    The capability 0 is never issued, so the null pointer (0, 0, 0, 0) fails
    every check.
    """

    value: int
    base: int
    bound: int
    cap: int


NULL = FatPointer(0, 0, 0, 0)


class FatPointerHeap:
    """A first-fit heap of size bytes whose pointers are fat pointers.

    alloc costs O(h) for h holes in the free list; add, load and store cost
    O(1) plus one lookup in the capability store (a Python set, O(1)
    expected); free costs O(h) for the coalescing.
    """

    def __init__(self, size: int = 256) -> None:
        if size < 1:
            raise ValueError("size must be positive")
        self.mem = bytearray(size)
        self.holes: list[tuple[int, int]] = [(1, size - 1)]  # address 0 stays unused
        self.live: dict[int, tuple[int, int]] = {}  # capability -> (base, bound)
        self.next_cap = 1

    def alloc(self, n: int) -> FatPointer:
        """Allocate n >= 1 bytes, zeroed. Return NULL when no hole is large enough."""
        if n < 1:
            raise ValueError("n must be positive")
        for i, (start, length) in enumerate(self.holes):
            if length >= n:
                break
        else:
            return NULL
        base = start  # @line L1: first fit
        if length == n:
            del self.holes[i]
        else:
            self.holes[i] = (start + n, length - n)
        cap = self.next_cap  # @line L2: a fresh capability, never reused
        self.next_cap += 1
        self.live[cap] = (base, base + n)  # @line L3
        self.mem[base:base + n] = bytes(n)
        return FatPointer(base, base, base + n, cap)  # @line L4

    def add(self, p: FatPointer, k: int) -> FatPointer:
        """Pointer arithmetic p + k. It is not checked; the bounds go along."""
        return FatPointer(p.value + k, p.base, p.bound, p.cap)  # @line L5

    def check(self, p: FatPointer, w: int) -> None:
        """Raise SpatialError or TemporalError unless p may access w bytes."""
        if p.value < p.base or p.value + w > p.bound:  # @line L6
            raise SpatialError(f"access of {w} bytes at {p.value} outside [{p.base}, {p.bound})")  # @line L7
        if p.cap not in self.live:  # @line L8
            raise TemporalError(f"capability {p.cap} is not live")  # @line L9

    def load(self, p: FatPointer, w: int) -> int:
        """Read a little-endian unsigned integer of w bytes at p, after the check."""
        self.check(p, w)  # @line L10
        return int.from_bytes(self.mem[p.value:p.value + w], "little")  # @line L11

    def store(self, p: FatPointer, w: int, v: int) -> None:
        """Write v (taken modulo 2^(8w)) as w little-endian bytes at p, after the check."""
        self.check(p, w)  # @line L10
        self.mem[p.value:p.value + w] = (v % (1 << (8 * w))).to_bytes(w, "little")  # @line L11

    def free(self, p: FatPointer) -> None:
        """Free the block of p. p must point to the start of a live block."""
        if p.value != p.base or p.bound <= p.base:  # @line L12
            raise SpatialError(f"free of {p.value}, which is not the start of a block")
        if p.cap not in self.live:  # @line L13
            raise TemporalError(f"double free of capability {p.cap}")
        del self.live[p.cap]  # @line L14: every copy of p now fails line L8
        self._release(p.base, p.bound - p.base)  # @line L15

    def _release(self, base: int, n: int) -> None:
        """Put [base, base + n) back into the sorted hole list and merge neighbours."""
        holes = self.holes + [(base, n)]
        holes.sort()
        merged: list[tuple[int, int]] = []
        for s, l in holes:
            if merged and merged[-1][0] + merged[-1][1] == s:
                merged[-1] = (merged[-1][0], merged[-1][1] + l)
            else:
                merged.append((s, l))
        self.holes = merged

    def check_invariant(self) -> None:
        """Live blocks and holes are disjoint, inside the memory, and cover it."""
        spans = sorted(list(self.live.values()) + [(s, s + l) for s, l in self.holes])
        pos = 1
        for lo, hi in spans:
            assert lo == pos and hi > lo, (lo, hi, pos)
            pos = hi
        assert pos == len(self.mem)
        assert all(c < self.next_cap and c > 0 for c in self.live)
