# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/addresssanitizer/. The authors are listed in prov/B574DH.jsonl.

"""AddressSanitizer on a simulated memory.

One shadow byte describes each granule of 8 bytes of application memory:
0 means all 8 bytes are addressable, k in 1..7 means only the first k are,
and a negative value (as a signed byte) means none are. The allocator puts a
poisoned redzone on each side of every object and keeps freed chunks in a
FIFO quarantine before it reuses them. Each load and store checks the shadow
byte of its address first.

The memory is a Python bytearray, never real memory. The shadow region sits
after the application bytes in the same array, at a symbolic offset.
"""

from collections import deque

GRANULE = 8
LOG_GRANULE = 3
REDZONE = 16  # bytes on each side of an object, a multiple of GRANULE
HEAP_REDZONE = 0xFA  # negative as a signed byte: a redzone or memory never allocated
FREED = 0xFD  # negative as a signed byte: a freed object


class ASanError(Exception):
    """A report: kind is heap-buffer-overflow, heap-use-after-free, double-free or bad-free."""

    def __init__(self, kind: str, addr: int) -> None:
        super().__init__(f"{kind} at {addr}")
        self.kind = kind
        self.addr = addr


def _signed(b: int) -> int:
    return b - 256 if b >= 128 else b


def round_up(n: int) -> int:
    """n rounded up to a multiple of GRANULE."""
    return (n + GRANULE - 1) & ~(GRANULE - 1)


class ASanHeap:
    """A first-fit heap with redzones, a quarantine and shadow checks.

    A check costs O(1). Malloc and free cost O(n / 8) shadow writes for an
    object of n bytes, plus the first-fit search over the holes. The shadow
    takes size / 8 bytes. Precondition: accesses have a width of 1, 2, 4 or 8
    bytes, are aligned to their width and lie inside the application memory.
    """

    def __init__(self, size: int = 512, quarantine_limit: int = 64) -> None:
        if size <= 0 or size % GRANULE:
            raise ValueError("size must be a positive multiple of 8")
        self.size = size
        self.offset = size  # the shadow follows the application bytes
        self.mem = bytearray(size + size // GRANULE)
        self.mem[self.offset:] = bytes([HEAP_REDZONE]) * (size // GRANULE)
        self.holes: list[tuple[int, int]] = [(0, size)]
        self.live: dict[int, tuple[int, int, int]] = {}  # base -> (chunk, chunk length, n)
        self.quarantine: deque[tuple[int, int]] = deque()  # (chunk, chunk length), oldest first
        self.quarantine_bytes = 0
        self.quarantine_limit = quarantine_limit

    def shadow_addr(self, a: int) -> int:
        """The address of the shadow byte of the granule that holds a."""
        return (a >> LOG_GRANULE) + self.offset  # @line L1

    def check(self, a: int, w: int) -> None:
        """Raise ASanError if any of the w bytes at a is not addressable."""
        if w not in (1, 2, 4, 8) or a % w or a < 0 or a + w > self.size:
            raise ValueError("an access must be aligned, of width 1, 2, 4 or 8, and in memory")
        k = _signed(self.mem[self.shadow_addr(a)])  # @line L2
        if k != 0 and (a & (GRANULE - 1)) + w - 1 >= k:  # @line L3
            kind = "heap-use-after-free" if k == _signed(FREED) else "heap-buffer-overflow"
            raise ASanError(kind, a)

    def _poison(self, lo: int, hi: int, value: int) -> None:
        for g in range(lo >> LOG_GRANULE, hi >> LOG_GRANULE):
            self.mem[self.offset + g] = value

    def malloc(self, n: int) -> int:
        """Allocate n >= 1 bytes between two redzones. Return 0 if no hole fits."""
        if n < 1:
            raise ValueError("n must be positive")
        length = REDZONE + round_up(n) + REDZONE
        for i, (start, hole) in enumerate(self.holes):
            if hole >= length:
                break
        else:
            return 0
        if hole == length:
            del self.holes[i]
        else:
            self.holes[i] = (start + length, hole - length)
        c = start
        b = c + REDZONE  # @line L4
        self._poison(c, b, HEAP_REDZONE)  # @line L5
        self._poison(b + round_up(n), c + length, HEAP_REDZONE)
        full = n >> LOG_GRANULE  # @line L6
        self._poison(b, b + full * GRANULE, 0)
        if n & (GRANULE - 1):
            self.mem[self.shadow_addr(b) + full] = n & (GRANULE - 1)
        self.live[b] = (c, length, n)
        return b  # @line L7

    def free(self, p: int) -> None:
        """Free the object at p, poison it and put its chunk in the quarantine."""
        if p not in self.live:  # @line L8
            if any(c + REDZONE == p for c, _ in self.quarantine):
                raise ASanError("double-free", p)
            raise ASanError("bad-free", p)
        c, length, n = self.live.pop(p)
        self._poison(p, p + round_up(n), FREED)  # @line L9
        self.quarantine.append((c, length))  # @line L10
        self.quarantine_bytes += length
        while self.quarantine_bytes > self.quarantine_limit:  # @line L11
            c0, l0 = self.quarantine.popleft()  # @line L12
            self.quarantine_bytes -= l0
            self._release(c0, l0)

    def load(self, a: int, w: int) -> int:
        self.check(a, w)
        return int.from_bytes(self.mem[a:a + w], "little")

    def store(self, a: int, w: int, v: int) -> None:
        self.check(a, w)
        self.mem[a:a + w] = (v % (1 << (8 * w))).to_bytes(w, "little")

    def _release(self, start: int, length: int) -> None:
        holes = sorted(self.holes + [(start, length)])
        merged: list[tuple[int, int]] = []
        for s, l in holes:
            if merged and merged[-1][0] + merged[-1][1] == s:
                merged[-1] = (merged[-1][0], merged[-1][1] + l)
            else:
                merged.append((s, l))
        self.holes = merged

    def check_invariant(self) -> None:
        """Chunks and holes tile the memory, and every shadow byte has its expected value."""
        pieces = sorted(
            [(c, l) for c, l, _ in self.live.values()] + list(self.quarantine) + self.holes
        )
        pos = 0
        for s, l in pieces:
            assert s == pos and l > 0 and s % GRANULE == 0 and l % GRANULE == 0
            pos += l
        assert pos == self.size
        assert self.quarantine_bytes == sum(l for _, l in self.quarantine)
        assert self.quarantine_bytes <= self.quarantine_limit
        expect = [None] * (self.size // GRANULE)
        for b, (c, l, n) in self.live.items():
            assert b == c + REDZONE and l == 2 * REDZONE + round_up(n)
            for g in range(c // GRANULE, (c + l) // GRANULE):
                expect[g] = HEAP_REDZONE
            for i in range(round_up(n) // GRANULE):
                left = n - i * GRANULE
                expect[b // GRANULE + i] = 0 if left >= GRANULE else left
        for c, l in self.quarantine:
            for g in range(c // GRANULE, (c + l) // GRANULE):
                inside = c + REDZONE <= g * GRANULE < c + l - REDZONE
                expect[g] = FREED if inside else HEAP_REDZONE
        for g, e in enumerate(expect):
            v = self.mem[self.offset + g]
            if e is None:
                assert _signed(v) < 0  # quarantined and free memory is poisoned
            else:
                assert v == e
