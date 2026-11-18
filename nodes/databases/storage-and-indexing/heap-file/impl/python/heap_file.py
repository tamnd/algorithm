# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heap-file/. The authors are listed in prov/FWEZG7.jsonl.

"""A heap file in its two classic forms, with a count of page reads and writes.

Data pages have ids 0, 1, 2, ... and hold records of variable length. A record
costs its length plus SLOT bytes of slot entry, and a record id is the pair
(page id, slot). The file finds pages with free space in one of two ways:

* DirectoryHeapFile keeps a chain of directory pages. Each directory page
  holds up to D entries (page id, free bytes), in page id order.
* ListHeapFile keeps a header page with the heads of two doubly linked lists:
  the pages with free space and the full pages. A page is full when it has
  fewer than `min_free` free bytes.

I/O is counted per operation: an operation reads each page it needs once and
writes each page it changes once, as if it had a few private buffer frames.
"""

from typing import Dict, Iterator, List, Optional, Set, Tuple

SLOT = 4
Rid = Tuple[int, int]


class DataPage:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.slots: List[Optional[bytes]] = []
        self.free = capacity
        self.prev: Optional[int] = None  # list form only
        self.next: Optional[int] = None
        self.full = False

    def fits(self, rec: bytes) -> bool:
        return len(rec) + SLOT <= self.free

    def insert(self, rec: bytes) -> int:
        s = next((i for i, r in enumerate(self.slots) if r is None), len(self.slots))
        if s == len(self.slots):
            self.slots.append(rec)
        else:
            self.slots[s] = rec
        self.free -= len(rec) + SLOT
        return s

    def delete(self, s: int) -> None:
        rec = self.slots[s]
        if rec is None:
            raise KeyError(s)
        self.slots[s] = None
        self.free += len(rec) + SLOT


class _Op:
    """The pages one operation reads and writes."""

    def __init__(self) -> None:
        self.read: Set[object] = set()
        self.written: Set[object] = set()


class _Base:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.pages: List[DataPage] = []
        self.reads = 0
        self.writes = 0
        self._op: Optional[_Op] = None

    def _begin(self) -> None:
        self._op = _Op()

    def _end(self) -> Tuple[int, int]:
        r, w = len(self._op.read), len(self._op.written)
        self.reads += r
        self.writes += w
        self._op = None
        return r, w

    def _r(self, key: object) -> None:
        self._op.read.add(key)

    def _w(self, key: object) -> None:
        self._op.written.add(key)

    def _check_size(self, rec: bytes) -> None:
        if len(rec) + SLOT > self.capacity:
            raise ValueError("the record does not fit in an empty page")

    def get(self, rid: Rid) -> bytes:
        self._begin()
        pid, s = rid
        self._r(pid)                                   # @line L21
        page = self.pages[pid] if 0 <= pid < len(self.pages) else None
        rec = page.slots[s] if page is not None and 0 <= s < len(page.slots) else None
        self.last_io = self._end()
        if rec is None:
            raise KeyError(rid)
        return rec

    def n_pages(self) -> int:
        return len(self.pages)

    def records(self) -> Dict[Rid, bytes]:
        return {(pid, s): r for pid, p in enumerate(self.pages)
                for s, r in enumerate(p.slots) if r is not None}


class DirectoryHeapFile(_Base):
    """A heap file whose free space is kept in a chain of directory pages."""

    def __init__(self, capacity: int = 4096, entries_per_dir_page: int = 128) -> None:
        super().__init__(capacity)
        self.D = entries_per_dir_page
        # directory page j holds the entries of data pages j*D .. j*D + D - 1;
        # directory page 0 always exists, so an empty file has one page.
        self.directory: List[List[List[int]]] = [[]]

    def n_dir_pages(self) -> int:
        return len(self.directory)

    def insert(self, rec: bytes) -> Rid:
        self._check_size(rec)
        self._begin()
        need = len(rec) + SLOT
        for j, dpage in enumerate(self.directory):      # @line L1
            self._r(("dir", j))                         # @line L2
            for entry in dpage:                         # @line L3
                pid, free = entry
                if free >= need:                        # @line L4
                    self._r(pid)                        # @line L5
                    s = self.pages[pid].insert(rec)     # @line L5
                    self._w(pid)                        # @line L6
                    entry[1] = self.pages[pid].free     # @line L7
                    self._w(("dir", j))                 # @line L7
                    self.last_io = self._end()
                    return (pid, s)                     # @line L8
        pid = len(self.pages)                           # @line L9
        page = DataPage(self.capacity)
        s = page.insert(rec)
        self.pages.append(page)
        self._w(pid)                                    # @line L10
        if len(self.directory[-1]) == self.D:           # @line L11
            self._w(("dir", len(self.directory) - 1))   # @line L12  the old last page gets a next pointer
            self.directory.append([])                   # @line L12
        self.directory[-1].append([pid, page.free])     # @line L13
        self._w(("dir", len(self.directory) - 1))       # @line L13
        self.last_io = self._end()
        return (pid, s)                                 # @line L14

    def delete(self, rid: Rid) -> None:
        pid, s = rid
        self._begin()
        self._r(pid)
        self.pages[pid].delete(s)
        self._w(pid)
        j = pid // self.D
        self._r(("dir", j))
        self.directory[j][pid % self.D][1] = self.pages[pid].free
        self._w(("dir", j))
        self.last_io = self._end()

    def scan(self) -> Iterator[Tuple[Rid, bytes]]:
        self._begin()
        out = []
        for j, dpage in enumerate(self.directory):      # @line L15
            self._r(("dir", j))                         # @line L16
            for pid, _ in dpage:                        # @line L17
                self._r(pid)                            # @line L18
                for s, r in enumerate(self.pages[pid].slots):  # @line L19
                    if r is not None:
                        out.append(((pid, s), r))       # @line L20
        self.last_io = self._end()
        return iter(out)

    def check(self) -> None:
        flat = [e for d in self.directory for e in d]
        assert [pid for pid, _ in flat] == list(range(len(self.pages)))
        assert all(free == self.pages[pid].free for pid, free in flat)
        assert all(len(d) == self.D for d in self.directory[:-1])


class ListHeapFile(_Base):
    """A heap file with a header page and two doubly linked lists of data pages."""

    def __init__(self, capacity: int = 4096, min_free: int = 64) -> None:
        super().__init__(capacity)
        self.min_free = min_free
        self.head = {"free": None, "full": None}

    # The list moves below read and write the neighbours they change.

    def _unlink(self, pid: int) -> None:
        page = self.pages[pid]
        lst = "full" if page.full else "free"
        if page.prev is None:
            self.head[lst] = page.next
            self._w("hdr")
        else:
            self._r(page.prev)
            self.pages[page.prev].next = page.next
            self._w(page.prev)
        if page.next is not None:
            self._r(page.next)
            self.pages[page.next].prev = page.prev
            self._w(page.next)
        page.prev = page.next = None

    def _push(self, pid: int, full: bool) -> None:
        page = self.pages[pid]
        lst = "full" if full else "free"
        page.full = full
        old = self.head[lst]
        page.prev, page.next = None, old
        if old is not None:
            self._r(old)
            self.pages[old].prev = pid
            self._w(old)
        self.head[lst] = pid
        self._w("hdr")
        self._w(pid)

    def _is_full(self, page: DataPage) -> bool:
        return page.free < self.min_free

    def free_list(self) -> List[int]:
        out, p = [], self.head["free"]
        while p is not None:
            out.append(p)
            p = self.pages[p].next
        return out

    def full_list(self) -> List[int]:
        out, p = [], self.head["full"]
        while p is not None:
            out.append(p)
            p = self.pages[p].next
        return out

    def insert(self, rec: bytes) -> Rid:
        self._check_size(rec)
        self._begin()
        self._r("hdr")                                  # @line L22
        p = self.head["free"]
        while p is not None:                            # @line L23
            self._r(p)                                  # @line L24
            page = self.pages[p]
            if page.fits(rec):                          # @line L25
                s = page.insert(rec)                    # @line L26
                self._w(p)                              # @line L26
                if self._is_full(page):                 # @line L27
                    self._unlink(p)                     # @line L28
                    self._push(p, True)                 # @line L28
                self.last_io = self._end()
                return (p, s)                           # @line L29
            p = page.next                               # @line L30
        pid = len(self.pages)                           # @line L31
        page = DataPage(self.capacity)
        s = page.insert(rec)
        self.pages.append(page)
        self._push(pid, self._is_full(page))            # @line L32
        self.last_io = self._end()
        return (pid, s)                                 # @line L33

    def delete(self, rid: Rid) -> None:
        pid, s = rid
        self._begin()
        self._r(pid)
        page = self.pages[pid]
        page.delete(s)
        self._w(pid)
        if page.full and not self._is_full(page):
            self._r("hdr")
            self._unlink(pid)
            self._push(pid, False)
        self.last_io = self._end()

    def scan(self) -> Iterator[Tuple[Rid, bytes]]:
        self._begin()
        self._r("hdr")
        out = []
        for lst in ("full", "free"):
            p = self.head[lst]
            while p is not None:
                self._r(p)
                for s, r in enumerate(self.pages[p].slots):
                    if r is not None:
                        out.append(((p, s), r))
                p = self.pages[p].next
        self.last_io = self._end()
        return iter(out)

    def check(self) -> None:
        free, full = self.free_list(), self.full_list()
        assert sorted(free + full) == list(range(len(self.pages)))
        for lst in (free, full):
            for a, b in zip(lst, lst[1:]):
                assert self.pages[b].prev == a
            if lst:
                assert self.pages[lst[0]].prev is None
        assert all(not self.pages[p].full and not self._is_full(self.pages[p]) for p in free)
        assert all(self.pages[p].full and self._is_full(self.pages[p]) for p in full)
