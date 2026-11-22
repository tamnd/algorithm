# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baggy-bounds-checking/. The authors are listed in prov/81GP9H.jsonl.

"""Baggy bounds checking on a simulated memory of 2^bits bytes.

Each allocation is padded to a power of two 2^e (at least one slot of 16
bytes) and aligned to it by a binary buddy allocator. A bounds table has one
byte per slot that holds e, so the base and the size of the allocation that
holds an address come from one table read. Pointer arithmetic checks the
result with one xor and one shift. A result less than half a slot out of
bounds gets a mark bit, so it can come back; a result further out is an error.

The memory is a Python bytearray, never real memory. There is no temporal
checking, as in the original.
"""

LOG_SLOT = 4  # slots of 16 bytes
SLOT = 1 << LOG_SLOT
HALF = SLOT // 2


class BoundsError(Exception):
    """An arithmetic result or an access left its padded allocation."""


class BaggyHeap:
    """A buddy heap with a baggy bounds table.

    alloc and free cost O(bits) for the buddy allocator plus O(2^e / 16) to
    write the table entries of the block; add and the access check cost O(1).
    Precondition: pointers come from alloc or add.
    """

    def __init__(self, bits: int = 10) -> None:
        if bits < LOG_SLOT + 1:
            raise ValueError("the memory must hold at least two slots")
        self.bits = bits
        self.mark = 1 << (bits + 1)  # above every address, so a marked pointer is never valid
        self.mem = bytearray(1 << bits)
        self.table = bytearray([bits]) * ((1 << bits) >> LOG_SLOT)  # default: the whole memory
        self.free_blocks: dict[int, set[int]] = {e: set() for e in range(LOG_SLOT, bits + 1)}
        self.free_blocks[bits].add(0)
        self.live: dict[int, tuple[int, int]] = {}  # base -> (e, requested size)
        self.reserved = self._take(LOG_SLOT)  # slot 0 stays unused, so 0 is a null pointer

    def _take(self, e: int) -> int:
        """Remove a free block of 2^e bytes from the buddy lists, splitting a larger one."""
        j = e
        while j <= self.bits and not self.free_blocks[j]:
            j += 1
        if j > self.bits:
            return -1
        b = min(self.free_blocks[j])
        self.free_blocks[j].remove(b)
        while j > e:
            j -= 1
            self.free_blocks[j].add(b + (1 << j))
        return b

    def alloc(self, n: int) -> int:
        """Allocate n >= 1 bytes, padded to a power of two. Return 0 if nothing fits."""
        if n < 1:
            raise ValueError("n must be positive")
        e = max(LOG_SLOT, (n - 1).bit_length())  # @line L1: the padded size is 2^e
        if e > self.bits:
            return 0
        b = self._take(e)  # @line L2: aligned to 2^e
        if b < 0:
            return 0
        for s in range(b >> LOG_SLOT, (b + (1 << e)) >> LOG_SLOT):  # @line L3
            self.table[s] = e
        self.mem[b:b + (1 << e)] = bytes(1 << e)  # @line L4: the padding is cleared too
        self.live[b] = (e, n)
        return b  # @line L5

    def is_marked(self, p: int) -> bool:
        return bool(p & self.mark)

    def add(self, p: int, k: int) -> int:
        """Checked pointer arithmetic p + k."""
        if p & self.mark:  # @line L6: find the referent from the half of the slot
            r = p & ~self.mark
            ref = r - HALF if r % SLOT < HALF else r + HALF
        else:
            r = ref = p  # @line L7
        e = self.table[ref >> LOG_SLOT]  # @line L8
        q = r + k  # @line L9
        if q >= 0 and (ref ^ q) >> e == 0:  # @line L10: inside the padded allocation
            return q
        base = ref & ~((1 << e) - 1)  # @line L11
        if q >= 0 and base - HALF <= q < base + (1 << e) + HALF:  # @line L12
            return q | self.mark
        raise BoundsError(f"{r} + {k} is far outside the allocation [{base}, {base + (1 << e)})")  # @line L13

    def check_access(self, p: int, w: int) -> None:
        """The check for an access of w bytes at p: unmarked, and the last byte in the block."""
        if p & self.mark:  # @line L14: a marked pointer faults
            raise BoundsError(f"access through an out-of-bounds pointer {p & ~self.mark}")
        e = self.table[p >> LOG_SLOT]
        if (p ^ (p + w - 1)) >> e != 0:  # @line L15
            raise BoundsError(f"access of {w} bytes at {p} crosses the end of its allocation")

    def load(self, p: int, w: int) -> int:
        self.check_access(p, w)
        return int.from_bytes(self.mem[p:p + w], "little")

    def store(self, p: int, w: int, v: int) -> None:
        self.check_access(p, w)
        self.mem[p:p + w] = (v % (1 << (8 * w))).to_bytes(w, "little")

    def free(self, p: int) -> None:
        """Free the allocation with base p and give its slots the default entry."""
        if p not in self.live:  # @line L16
            raise BoundsError(f"free of {p}, which is not the base of an allocation")
        e, _ = self.live.pop(p)
        for s in range(p >> LOG_SLOT, (p + (1 << e)) >> LOG_SLOT):  # @line L17
            self.table[s] = self.bits
        while e < self.bits and (p ^ (1 << e)) in self.free_blocks[e]:  # buddy merge
            self.free_blocks[e].remove(p ^ (1 << e))
            p = min(p, p ^ (1 << e))
            e += 1
        self.free_blocks[e].add(p)

    def check_invariant(self) -> None:
        """Blocks tile the memory, are aligned, and the table matches the live blocks."""
        spans = [(self.reserved, LOG_SLOT)] + [(b, e) for b, (e, _) in self.live.items()]
        spans += [(b, e) for e, s in self.free_blocks.items() for b in s]
        spans.sort()
        pos = 0
        for b, e in spans:
            assert b == pos and b % (1 << e) == 0
            pos = b + (1 << e)
        assert pos == len(self.mem)
        want = bytearray([self.bits]) * len(self.table)
        for b, (e, _) in self.live.items():
            for s in range(b >> LOG_SLOT, (b + (1 << e)) >> LOG_SLOT):
                want[s] = e
        assert self.table == want
