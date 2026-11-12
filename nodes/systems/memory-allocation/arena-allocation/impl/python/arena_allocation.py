# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arena-allocation/. The authors are listed in prov/WB0SXP.jsonl.

"""Arena allocation in the style of Hanson (1990).

An arena is a list of chunks. The last chunk has a bump range [avail, limit).
alloc(n) rounds n up to the alignment and bumps avail. When the request does
not fit, the arena takes a chunk from a shared list of free chunks, or a new
chunk of n + K bytes from the system, and goes on there. free_all() puts every
chunk of the arena on the shared free list at once, so later arenas reuse the
memory without asking the system again. There is no free of single blocks.
"""

ALIGN = 8


class System:
    """Hands out fresh address ranges, like malloc of whole chunks."""

    def __init__(self) -> None:
        self.next = 0
        self.chunks = 0

    def get(self, size: int) -> tuple[int, int]:
        start = self.next
        self.next += size
        self.chunks += 1
        return start, start + size


class ChunkPool:
    """The shared list of free chunks (Hanson's freeblocks), with the system behind it."""

    def __init__(self, k: int = 1024, system: System | None = None) -> None:
        self.k = k  # the extra room in each new chunk
        self.system = system or System()
        self.free: list[tuple[int, int]] = []  # a stack of (start, end)


class Arena:
    def __init__(self, pool: ChunkPool) -> None:
        self.pool = pool
        self.chunks: list[tuple[int, int]] = []
        self.avail = self.limit = 0  # an empty range until the first chunk

    def alloc(self, n: int) -> int:
        """Return the address of n bytes that live until free_all()."""
        if n < 0:
            raise ValueError("n must be at least 0")
        n = (n + ALIGN - 1) // ALIGN * ALIGN
        while self.limit - self.avail < n:  # @line L1
            if self.pool.free:  # @line L2
                c = self.pool.free.pop()
            else:
                c = self.pool.system.get(n + self.pool.k)  # @line L3
            self.chunks.append(c)  # @line L4
            self.avail, self.limit = c
        p = self.avail  # @line L5
        self.avail += n
        return p

    def free_all(self) -> None:
        """Free every block of the arena; its chunks go to the shared free list."""
        self.pool.free.extend(reversed(self.chunks))  # @line L6
        self.chunks.clear()
        self.avail = self.limit = 0
