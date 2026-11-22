# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shadow-memory/. The authors are listed in prov/ZD4SXZ.jsonl.

"""Shadow memory on a simulated address space.

Two representations of the same abstract type: a map from each granule of
2^k bytes of application memory to one metadata byte.

- DirectShadow: the shadow lives in the same simulated memory, at
  (a >> k) + offset, as in AddressSanitizer.
- TwoLevelShadow: a primary table of chunk references; every chunk starts as a
  shared, read-only distinguished chunk and is copied on the first write that
  changes it, as in Valgrind's Memcheck.

Nothing here touches real memory: the address space is a Python bytearray.
"""


class DirectShadow:
    """Application bytes [0, size) and their shadow at [offset, offset + size >> k).

    Every operation costs O(1) per granule; the space is size / 2^k bytes.
    """

    def __init__(self, size: int, k: int, default: int = 0) -> None:
        if k < 0 or size < 1 or size % (1 << k):
            raise ValueError("size must be a positive multiple of 2^k")
        self.size = size
        self.k = k
        self.offset = size  # the shadow region starts right after the application region
        self.mem = bytearray(size + (size >> k))  # one simulated address space
        for g in range(size >> k):
            self.mem[self.offset + g] = default

    def shadow_addr(self, a: int) -> int:
        """The address of the metadata byte of application address a."""
        if not 0 <= a < self.size:
            raise IndexError(f"address {a} is not an application address")
        return (a >> self.k) + self.offset  # @line L1: one shift and one add

    def get(self, a: int) -> int:
        """The metadata of the granule that holds a."""
        return self.mem[self.shadow_addr(a)]  # @line L2

    def set(self, a: int, v: int) -> None:
        """Set the metadata of the granule that holds a to v (0 to 255)."""
        self.mem[self.shadow_addr(a)] = v  # @line L3

    def set_range(self, lo: int, hi: int, v: int) -> None:
        """Set the metadata of every granule of [lo, hi); lo and hi are multiples of 2^k."""
        g = 1 << self.k
        if lo % g or hi % g or lo > hi:
            raise ValueError("the range must be granule aligned")
        for a in range(lo, hi, g):  # @line L4
            self.set(a, v)  # @line L5


class TwoLevelShadow:
    """A sparse shadow for an address space of 2^bits bytes.

    The primary table has 2^(bits - c) entries, one for each chunk of 2^c
    application bytes. A chunk holds 2^(c - k) metadata bytes. get costs O(1);
    set costs O(1), or O(2^(c - k)) when it copies a distinguished chunk.
    Space: the primary table plus one chunk for each chunk that was changed.
    """

    def __init__(self, bits: int, c: int, k: int, default: int = 0) -> None:
        if not 0 <= k <= c <= bits:
            raise ValueError("need 0 <= k <= c <= bits")
        self.bits, self.c, self.k = bits, c, k
        self.per_chunk = 1 << (c - k)
        self.dsm: dict[int, bytes] = {}  # distinguished chunks, shared and read-only
        self.primary: list[bytes | bytearray] = [self._distinguished(default)] * (1 << (bits - c))

    def _distinguished(self, v: int) -> bytes:
        if v not in self.dsm:
            self.dsm[v] = bytes([v]) * self.per_chunk
        return self.dsm[v]

    def get(self, a: int) -> int:
        """The metadata of the granule that holds a, 0 <= a < 2^bits."""
        chunk = self.primary[a >> self.c]  # @line L6: the high bits pick the chunk
        return chunk[(a & ((1 << self.c) - 1)) >> self.k]  # @line L7: the low bits pick the byte

    def set(self, a: int, v: int) -> None:
        """Set the metadata of the granule that holds a."""
        i = a >> self.c  # @line L6
        chunk = self.primary[i]
        j = (a & ((1 << self.c) - 1)) >> self.k  # @line L7
        if isinstance(chunk, bytes):  # @line L8: a distinguished chunk is never written
            if chunk[j] == v:
                return
            chunk = bytearray(chunk)  # @line L9: copy on write
            self.primary[i] = chunk
        chunk[j] = v  # @line L10

    def set_range(self, lo: int, hi: int, v: int) -> None:
        """Set every granule of [lo, hi); lo and hi are multiples of 2^k.

        A whole chunk inside the range goes back to the distinguished chunk of
        v, which frees its private copy.
        """
        g, cs = 1 << self.k, 1 << self.c
        if lo % g or hi % g or lo > hi:
            raise ValueError("the range must be granule aligned")
        a = lo
        while a < hi:
            if a % cs == 0 and a + cs <= hi:  # @line L11
                self.primary[a >> self.c] = self._distinguished(v)  # @line L12
                a += cs
            else:
                self.set(a, v)  # @line L13
                a += g

    def private_chunks(self) -> int:
        """The number of chunks that hold a private copy."""
        return sum(1 for ch in self.primary if isinstance(ch, bytearray))

    def check_invariant(self) -> None:
        """Distinguished chunks still hold only their own value."""
        for v, ch in self.dsm.items():
            assert isinstance(ch, bytes) and ch == bytes([v]) * self.per_chunk
        for ch in self.primary:
            assert len(ch) == self.per_chunk
