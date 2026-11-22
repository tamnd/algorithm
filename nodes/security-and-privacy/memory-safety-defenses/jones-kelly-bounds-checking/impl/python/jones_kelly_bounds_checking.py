# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jones-kelly-bounds-checking/. The authors are listed in prov/F1X4NS.jsonl.

"""Jones-Kelly bounds checking with an object table, on a simulated heap.

Pointers stay plain integers. The heap keeps a table of live objects. Pointer
arithmetic looks up the object of the operand and turns a result outside
[base, base + size] into ILLEGAL; a dereference looks up the object again and
checks that the access fits. Each object gets one pad byte, so the pointer one
past the end still belongs to its object.

The memory is a Python bytearray, never real memory. The object table is a
sorted list searched with bisect; the original uses a splay tree.
"""

from bisect import bisect_right, insort

ILLEGAL = -2  # the value that marks an out-of-bounds pointer, as in the original


class BoundsError(Exception):
    """An arithmetic step, an access or a free was refused."""


class JonesKellyHeap:
    """A first-fit heap whose objects are recorded in an object table.

    With t live objects and h holes: alloc costs O(h + t) here (O(h + log t)
    with a balanced tree), add and the access check cost O(log t), and free
    costs O(h + t). Precondition: every pointer the program uses was returned
    by alloc or add, or is ILLEGAL.
    """

    def __init__(self, size: int = 256) -> None:
        if size < 2:
            raise ValueError("size must be at least 2")
        self.mem = bytearray(size)
        self.holes: list[tuple[int, int]] = [(1, size - 1)]  # address 0 stays unused
        self.bases: list[int] = []  # sorted bases of the live objects
        self.size_of: dict[int, int] = {}  # base -> size n (without the pad byte)

    def alloc(self, n: int) -> int:
        """Allocate n >= 1 zeroed bytes plus one pad byte. Return 0 if nothing fits."""
        if n < 1:
            raise ValueError("n must be positive")
        need = n + 1
        for i, (start, length) in enumerate(self.holes):
            if length >= need:
                break
        else:
            return 0
        b = start  # @line L1: first fit, n + 1 bytes
        if length == need:
            del self.holes[i]
        else:
            self.holes[i] = (start + need, length - need)
        insort(self.bases, b)  # @line L2
        self.size_of[b] = n
        self.mem[b:b + need] = bytes(need)
        return b  # @line L3

    def lookup(self, p: int) -> int | None:
        """The base of the live object [b, b + n] with b <= p <= b + n, or None."""
        i = bisect_right(self.bases, p) - 1  # @line L4
        if i >= 0 and p <= self.bases[i] + self.size_of[self.bases[i]]:
            return self.bases[i]
        return None

    def add(self, p: int, k: int) -> int:
        """Pointer arithmetic p + k, checked against the object of p."""
        if p == ILLEGAL:  # @line L5
            raise BoundsError("arithmetic on an ILLEGAL pointer")
        b = self.lookup(p)  # @line L6
        if b is None:  # @line L7: not in a checked object, so not checked
            return p + k
        if b <= p + k <= b + self.size_of[b]:  # @line L8: one past the end is allowed
            return p + k
        return ILLEGAL  # @line L9

    def check(self, p: int, w: int) -> None:
        """Raise BoundsError unless the w bytes at p lie in one live object."""
        if p == ILLEGAL:  # @line L10
            raise BoundsError("dereference of an ILLEGAL pointer")
        b = self.lookup(p)  # @line L11
        if b is None:  # @line L12: all simulated memory is checked
            raise BoundsError(f"address {p} is in no live object")
        if p + w > b + self.size_of[b]:  # @line L13
            raise BoundsError(f"access of {w} bytes at {p} past the end {b + self.size_of[b]}")

    def load(self, p: int, w: int) -> int:
        """Read a little-endian unsigned integer of w bytes at p, after the check."""
        self.check(p, w)
        return int.from_bytes(self.mem[p:p + w], "little")

    def store(self, p: int, w: int, v: int) -> None:
        """Write v modulo 2^(8w) as w little-endian bytes at p, after the check."""
        self.check(p, w)
        self.mem[p:p + w] = (v % (1 << (8 * w))).to_bytes(w, "little")

    def free(self, p: int) -> None:
        """Free the object whose base is p."""
        if p not in self.size_of:  # @line L14
            raise BoundsError(f"free of {p}, which is not the base of a live object")
        n = self.size_of.pop(p)  # @line L15
        self.bases.remove(p)
        self._release(p, n + 1)

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
        """Objects with their pad bytes and the holes tile the memory from address 1."""
        assert self.bases == sorted(self.size_of)
        spans = sorted([(b, b + self.size_of[b] + 1) for b in self.bases] + [(s, s + l) for s, l in self.holes])
        pos = 1
        for lo, hi in spans:
            assert lo == pos and hi > lo
            pos = hi
        assert pos == len(self.mem)
