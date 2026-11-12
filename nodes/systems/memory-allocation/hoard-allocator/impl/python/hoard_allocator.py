# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hoard-allocator/. The authors are listed in prov/HAC5RQ.jsonl.

"""A small model of the Hoard allocator (Berger, McKinley, Blumofe and Wilson, ASPLOS 2000).

This is a model, not the real allocator. It runs in one Python thread, so it
has no locks; a "thread" is only a number that selects a heap. It keeps the
bookkeeping of Figure 2 of the paper: heap 0 is the global heap, heaps 1..P
belong to processors, memory comes from the system in superblocks of S
bytes, each superblock holds blocks of one size class in a LIFO free list,
and each heap i keeps u[i] (bytes in use) and a[i] (bytes of superblocks it
holds). After a free, while heap i crosses the emptiness threshold, its
emptiest superblock moves to the global heap. Objects larger than S/2 get
their own mapping. Superblocks start at multiples of S, so the superblock of
an address is address // S.
"""


class Superblock:
    def __init__(self, sid: int, size: int, nblocks: int, owner: int) -> None:
        self.sid = sid
        self.size = size
        self.owner = owner
        self.used = 0  # s.u in the paper, in bytes
        self.free = list(range(nblocks - 1, -1, -1))  # LIFO stack of block indices


class Hoard:
    def __init__(self, processors: int, sb_size: int = 4096, f: float = 0.25, k: int = 0) -> None:
        self.P = processors
        self.S = sb_size
        self.f = f
        self.K = k
        self.u = [0] * (processors + 1)
        self.a = [0] * (processors + 1)
        self.heaps: list[list[Superblock]] = [[] for _ in range(processors + 1)]
        self.sbs: dict[int, Superblock] = {}
        self.large: dict[int, int] = {}
        self.next_sid = 0
        self.next_large = 1 << 40
        self.os_bytes = 0  # memory taken from the system for superblocks
        self.transfers = 0  # superblocks moved to the global heap
        self.max_moves_per_free = 0

    def size_class(self, sz: int) -> int:
        """Size classes are powers of b = 2, from 8 bytes up to S/2."""
        c = 8
        while c < sz:
            c <<= 1
        return c

    def heap_of(self, thread: int) -> int:
        return 1 + thread % self.P

    def crosses_threshold(self, i: int) -> bool:
        return self.u[i] < self.a[i] - self.K * self.S and self.u[i] < (1 - self.f) * self.a[i]

    def _move(self, s: Superblock, dst: int) -> None:
        src = s.owner
        self.heaps[src].remove(s)
        self.u[src] -= s.used
        self.a[src] -= self.S
        self.heaps[dst].append(s)
        self.u[dst] += s.used
        self.a[dst] += self.S
        s.owner = dst

    def malloc(self, thread: int, sz: int) -> int:
        if sz > self.S // 2:  # @line L1
            a = self.next_large
            self.next_large += sz + self.S
            self.large[a] = sz
            return a
        i = self.heap_of(thread)  # @line L2
        c = self.size_class(sz)
        cands = [s for s in self.heaps[i] if s.size == c and s.free]  # @line L3
        s = max(cands, key=lambda b: b.used) if cands else None
        if s is None:  # @line L4
            spare = [b for b in self.heaps[0] if b.size == c and b.free]
            spare = spare or [b for b in self.heaps[0] if b.used == 0]
            if spare:  # @line L5
                s = max(spare, key=lambda b: b.used)
                if s.size != c:  # an empty superblock is reused for any size class
                    s.size, s.free = c, list(range(self.S // c - 1, -1, -1))
                self._move(s, i)
            else:  # @line L6
                s = Superblock(self.next_sid, c, self.S // c, i)
                self.next_sid += 1
                self.sbs[s.sid] = s
                self.heaps[i].append(s)
                self.a[i] += self.S
                self.os_bytes += self.S
        idx = s.free.pop()  # @line L7
        s.used += c
        self.u[i] += c
        return s.sid * self.S + idx * c  # @line L8

    def free(self, ptr: int) -> None:
        if ptr in self.large:  # @line L9
            del self.large[ptr]
            return
        s = self.sbs[ptr // self.S]  # @line L10
        i = s.owner
        idx = (ptr % self.S) // s.size  # @line L11
        if idx in s.free:
            raise ValueError("double free")
        s.free.append(idx)
        s.used -= s.size
        self.u[i] -= s.size
        if i == 0:  # @line L12
            return
        moves = 0
        while self.crosses_threshold(i):  # @line L13
            victim = min(self.heaps[i], key=lambda b: b.used)  # @line L14
            self._move(victim, 0)
            self.transfers += 1
            moves += 1
        self.max_moves_per_free = max(self.max_moves_per_free, moves)

    def invariant_holds(self, i: int) -> bool:
        """(u_i >= a_i - K*S) or (u_i >= (1 - f) * a_i), the invariant of Section 3.1."""
        return self.u[i] >= self.a[i] - self.K * self.S or self.u[i] >= (1 - self.f) * self.a[i]
