# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/buffer-pool/. The authors are listed in prov/GQQFSE.jsonl.

"""A buffer pool: B frames, a page table, pin counts, dirty bits and a policy.

The disk is a dict from page id to bytes that counts reads and writes. A caller
fetches a page (which pins it), reads or changes the frame's bytes, and unpins
it, saying whether it changed the page. A pinned frame is never chosen as a
victim. Two replacement policies are given, LRU and CLOCK.
"""

from typing import Dict, List, Optional


class AllFramesPinned(Exception):
    """Every frame is pinned, so no page can be brought in."""


class Disk:
    def __init__(self, pages: Optional[Dict[int, bytes]] = None) -> None:
        self.pages: Dict[int, bytes] = dict(pages or {})
        self.reads = 0
        self.writes = 0

    def read(self, pid: int) -> bytes:
        self.reads += 1
        return self.pages[pid]

    def write(self, pid: int, data: bytes) -> None:
        self.writes += 1
        self.pages[pid] = bytes(data)

    def allocate(self, size: int) -> int:
        pid = max(self.pages, default=-1) + 1
        self.pages[pid] = bytes(size)
        return pid


class Frame:
    __slots__ = ("pid", "data", "pin", "dirty", "ref", "stamp")

    def __init__(self) -> None:
        self.pid: Optional[int] = None
        self.data = bytearray()
        self.pin = 0
        self.dirty = False
        self.ref = False   # CLOCK reference bit
        self.stamp = 0     # LRU time of last access


class BufferPool:
    def __init__(self, disk: Disk, n_frames: int, policy: str = "lru") -> None:
        if n_frames < 1:
            raise ValueError("a pool needs at least one frame")
        if policy not in ("lru", "clock"):
            raise ValueError("policy must be lru or clock")
        self.disk = disk
        self.frames: List[Frame] = [Frame() for _ in range(n_frames)]
        self.table: Dict[int, int] = {}   # page id -> frame number
        self.policy = policy
        self.hand = 0
        self.clock = 0
        self.hits = 0
        self.misses = 0

    # ------------------------------------------------------------ policy

    def _touch(self, f: Frame) -> None:
        self.clock += 1
        f.stamp = self.clock
        f.ref = True

    def _victim(self) -> Optional[int]:
        if all(f.pin > 0 for f in self.frames):
            return None
        if self.policy == "lru":
            cands = [i for i, f in enumerate(self.frames) if f.pin == 0]
            return min(cands, key=lambda i: self.frames[i].stamp)
        while True:                                       # @line L15
            i = self.hand                                 # @line L16
            self.hand = (self.hand + 1) % len(self.frames)  # @line L16
            f = self.frames[i]
            if f.pin == 0:                                # @line L17
                if f.ref:                                 # @line L18
                    f.ref = False                         # @line L18
                else:
                    return i                              # @line L19

    # ------------------------------------------------------------ interface

    def fetch(self, pid: int) -> bytearray:
        """Pin page pid and return its frame's bytes."""
        if pid in self.table:                             # @line L1
            f = self.frames[self.table[pid]]              # @line L2
            f.pin += 1                                    # @line L2
            self._touch(f)                                # @line L2
            self.hits += 1
            return f.data                                 # @line L3
        self.misses += 1
        free = next((i for i, f in enumerate(self.frames) if f.pid is None), None)
        if free is not None:                              # @line L4
            i = free                                      # @line L4
        else:                                             # @line L5
            i = self._victim()                            # @line L6
            if i is None:                                 # @line L7
                self.misses -= 1
                raise AllFramesPinned(pid)                # @line L7
            v = self.frames[i]
            if v.dirty:                                   # @line L8
                self.disk.write(v.pid, v.data)            # @line L8
            del self.table[v.pid]                         # @line L9
        f = self.frames[i]
        f.data = bytearray(self.disk.read(pid))           # @line L10
        f.pid, f.pin, f.dirty = pid, 1, False             # @line L11
        self.table[pid] = i                               # @line L11
        self._touch(f)                                    # @line L12
        return f.data                                     # @line L12

    def unpin(self, pid: int, dirty: bool = False) -> None:
        f = self.frames[self.table[pid]]                  # @line L13
        if f.pin == 0:
            raise ValueError(f"page {pid} is not pinned")
        f.pin -= 1                                        # @line L13
        f.dirty = f.dirty or dirty                        # @line L14

    def new_page(self, size: int) -> int:
        """Allocate a page on disk and fetch it pinned. Its frame starts dirty."""
        pid = self.disk.allocate(size)
        reads = self.disk.reads
        self.fetch(pid)
        self.disk.reads = reads   # the new page has nothing to read
        self.frames[self.table[pid]].dirty = True
        return pid

    def flush(self, pid: int) -> None:
        f = self.frames[self.table[pid]]
        if f.dirty:
            self.disk.write(pid, f.data)
            f.dirty = False

    def flush_all(self) -> None:
        for pid in list(self.table):
            self.flush(pid)

    def pin_count(self, pid: int) -> int:
        return self.frames[self.table[pid]].pin if pid in self.table else 0

    def resident(self) -> List[int]:
        return sorted(self.table)

    def check(self) -> None:
        for pid, i in self.table.items():
            assert self.frames[i].pid == pid
        assert sum(f.pid is not None for f in self.frames) == len(self.table)
        assert all(f.pin >= 0 for f in self.frames)
