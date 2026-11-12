# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lock-free-memory-allocator/. The authors are listed in prov/9J5R6H.jsonl.

"""A sequential model of Michael's lock-free allocator (PLDI 2004).

This is a model, not a real allocator, and it uses no threads. Each malloc
and free is a Python generator that yields once before each access to shared
memory, so one resumption is one atomic step: a read, a write or a CAS. A
scheduler picks which thread takes the next step, which makes every
interleaving reproducible. Memory is sequentially consistent, so the fences
of the paper are not needed.

The model follows Figures 4 and 6 of the paper for one size class: the
Active field with credits, the Anchor (avail, count, state, tag) changed only
by CAS, the four superblock states, the Partial slot of each processor heap
and the FIFO partial list of the size class. Left out: large blocks, several
size classes, descriptor reuse (DescAlloc and DescRetire, which need hazard
pointers), and hyperblocks. A list operation on the size-class partial list
is one atomic step, as if done by a lock-free queue. With use_tag=False the
tag is never changed, which shows the ABA problem of the paper.
"""

import random
from collections import deque
from collections.abc import Generator
from typing import NamedTuple

ACTIVE, FULL, PARTIAL, EMPTY = 0, 1, 2, 3
END = -1  # next index of the last block of a new superblock

Block = tuple[int, int]  # (superblock id, block index)
Step = Generator[None, None, object]


class Anchor(NamedTuple):
    avail: int  # index of the first available block
    count: int  # unreserved available blocks
    state: int
    tag: int


class Desc:
    def __init__(self, sb: int, maxcount: int, heap: "Heap") -> None:
        self.sb = sb
        self.maxcount = maxcount
        self.heap = heap
        self.anchor = Anchor(0, 0, ACTIVE, 0)


class Heap:
    def __init__(self) -> None:
        self.active: tuple[Desc, int] | None = None  # (descriptor, credits)
        self.partial: Desc | None = None


class LockFreeAllocator:
    def __init__(self, nheaps: int = 2, maxcount: int = 6, maxcredits: int = 3, use_tag: bool = True) -> None:
        assert maxcount >= 2 and maxcredits >= 1
        self.heaps = [Heap() for _ in range(nheaps)]
        self.sc_partial: deque[Desc] = deque()
        self.maxcount = maxcount
        self.maxcredits = maxcredits
        self.tag_step = 1 if use_tag else 0
        self.mem: dict[Block, object] = {}  # first word of each block
        self.descs: dict[int, Desc] = {}
        self.freed: set[int] = set()  # superblocks given back to the system
        self.next_sb = 0
        self.errors: list[str] = []
        self.cas_ok = 0
        self.cas_fail = 0

    # ----- shared memory --------------------------------------------------------
    def _read(self, b: Block) -> object:
        if b[0] in self.freed:
            self.errors.append(f"read of freed superblock {b[0]}")
        return self.mem.get(b)

    def _cas_anchor(self, d: Desc, old: Anchor, new: Anchor) -> bool:
        if d.anchor == old:
            d.anchor = new
            self.cas_ok += 1
            return True
        self.cas_fail += 1
        return False

    def _cas_active(self, h: Heap, old: tuple[Desc, int] | None, new: tuple[Desc, int] | None) -> bool:
        cur = h.active
        same = cur is old or (cur is not None and old is not None and cur[0] is old[0] and cur[1] == old[1])
        if same:
            h.active = new
            self.cas_ok += 1
            return True
        self.cas_fail += 1
        return False

    # ----- malloc ---------------------------------------------------------------
    def malloc(self, t: int) -> Step:
        heap = self.heaps[t % len(self.heaps)]  # @line L1
        while True:
            for part in (self._from_active, self._from_partial, self._from_new_sb):
                b = yield from part(heap)
                if b is not None:
                    return b

    def _from_active(self, heap: Heap) -> Step:
        while True:  # first step: reserve a block
            yield
            old = heap.active  # @line L2
            if old is None:
                return None
            new = None if old[1] == 0 else (old[0], old[1] - 1)
            yield
            if self._cas_active(heap, old, new):
                break
        desc, credits = old
        while True:  # second step: pop the reserved block
            yield
            a = desc.anchor  # @line L3
            b = (desc.sb, a.avail)
            yield
            nxt = self._read(b)
            n = a._replace(avail=nxt, tag=a.tag + self.tag_step)  # @line L4
            more = 0
            if credits == 0:
                if a.count == 0:
                    n = n._replace(state=FULL)
                else:
                    more = min(a.count, self.maxcredits)
                    n = n._replace(count=a.count - more)
            yield
            if self._cas_anchor(desc, a, n):  # @line L5
                break
        if credits == 0 and a.count > 0:  # @line L6
            yield from self._update_active(heap, desc, more)
        return b

    def _update_active(self, heap: Heap, desc: Desc, more: int) -> Step:
        yield
        if self._cas_active(heap, None, (desc, more - 1)):  # @line L7
            return None
        while True:  # someone installed another active superblock: give the credits back
            yield
            a = desc.anchor  # @line L8
            n = a._replace(count=a.count + more, state=PARTIAL)
            yield
            if self._cas_anchor(desc, a, n):
                break
        yield from self._heap_put_partial(desc)
        return None

    def _heap_get_partial(self, heap: Heap) -> Step:
        while True:
            yield
            desc = heap.partial
            if desc is None:
                yield
                return self.sc_partial.popleft() if self.sc_partial else None
            yield
            if heap.partial is desc:
                heap.partial = None
                return desc

    def _heap_put_partial(self, desc: Desc) -> Step:
        while True:
            yield
            heap = desc.heap
            yield
            prev = heap.partial
            yield
            if heap.partial is prev:
                heap.partial = desc
                break
        if prev is not None:
            yield
            self.sc_partial.append(prev)
        return None

    def _from_partial(self, heap: Heap) -> Step:
        while True:
            desc = yield from self._heap_get_partial(heap)  # @line L9
            if desc is None:
                return None
            yield
            desc.heap = heap
            retired = False
            while True:  # reserve blocks
                yield
                a = desc.anchor  # @line L10
                if a.state == EMPTY:
                    retired = True  # DescRetire; the model does not reuse descriptors
                    break
                more = min(a.count - 1, self.maxcredits)
                n = a._replace(count=a.count - (more + 1), state=ACTIVE if more > 0 else FULL)
                yield
                if self._cas_anchor(desc, a, n):
                    break
            if not retired:
                break
        while True:  # pop the reserved block
            yield
            a = desc.anchor  # @line L11
            b = (desc.sb, a.avail)
            yield
            nxt = self._read(b)
            yield
            if self._cas_anchor(desc, a, a._replace(avail=nxt, tag=a.tag + self.tag_step)):
                break
        if more > 0:
            yield from self._update_active(heap, desc, more)
        return b

    def _from_new_sb(self, heap: Heap) -> Step:
        sb = self.next_sb  # @line L12
        self.next_sb += 1
        desc = Desc(sb, self.maxcount, heap)
        self.descs[sb] = desc
        for i in range(self.maxcount):
            self.mem[(sb, i)] = i + 1 if i + 1 < self.maxcount else END
        credits = min(self.maxcount - 1, self.maxcredits) - 1
        desc.anchor = Anchor(1, (self.maxcount - 1) - (credits + 1), ACTIVE, 0)
        yield
        if self._cas_active(heap, None, (desc, credits)):  # @line L13
            return (sb, 0)
        self.freed.add(sb)
        return None

    # ----- free -----------------------------------------------------------------
    def free(self, b: Block) -> Step:
        desc = self.descs[b[0]]  # @line L14
        while True:
            yield
            a = desc.anchor
            yield
            self.mem[b] = a.avail
            n = a._replace(avail=b[1])
            if a.state == FULL:
                n = n._replace(state=PARTIAL)
            if a.count == desc.maxcount - 1:  # @line L15
                yield
                heap = desc.heap
                n = n._replace(state=EMPTY)
            else:
                n = n._replace(count=a.count + 1)
            yield
            if self._cas_anchor(desc, a, n):
                break
        if n.state == EMPTY:  # @line L16
            self.freed.add(desc.sb)
            yield from self._remove_empty_desc(heap, desc)
        elif a.state == FULL:
            yield from self._heap_put_partial(desc)
        return None

    def _remove_empty_desc(self, heap: Heap, desc: Desc) -> Step:
        yield
        if heap.partial is desc:
            heap.partial = None
            return None
        yield  # ListRemoveEmptyDesc on the FIFO list, as one step
        for _ in range(len(self.sc_partial)):
            d = self.sc_partial.popleft()
            if d.anchor.state != EMPTY:
                self.sc_partial.append(d)
                break
        return None


# ----- the scheduler ------------------------------------------------------------
class Run:
    """Threads that each do a list of operations; the scheduler interleaves their steps."""

    def __init__(self, alloc: LockFreeAllocator, nthreads: int, seed: int = 0) -> None:
        self.alloc = alloc
        self.held: dict[int, list[Block]] = {t: [] for t in range(nthreads)}
        self.owner: dict[Block, int] = {}  # block -> thread that holds it
        self.current: dict[int, tuple[str, Step, Block | None]] = {}
        self.rng = random.Random(seed)
        self.double: list[Block] = []
        self.done = {t: 0 for t in range(nthreads)}

    def start(self, t: int, op: str, b: Block | None = None) -> None:
        if op == "free":
            if b is None:
                b = self.held[t][self.rng.randrange(len(self.held[t]))]
            self.held[t].remove(b)
            del self.owner[b]  # the program gives the block up when it calls free
            self.current[t] = ("free", self.alloc.free(b), b)
        else:
            self.current[t] = ("malloc", self.alloc.malloc(t), None)

    def step(self, t: int) -> None:
        """Run one atomic step of thread t, which must have an operation in progress."""
        op, gen, _ = self.current[t]
        try:
            next(gen)
        except StopIteration as stop:
            del self.current[t]
            self.done[t] += 1
            if op == "malloc":
                b = stop.value
                if b in self.owner:
                    self.double.append(b)
                self.owner[b] = t
                self.held[t].append(b)

    def finish(self, t: int) -> None:
        while t in self.current:
            self.step(t)


def random_run(alloc: LockFreeAllocator, nthreads: int, ops: int, seed: int, crash: int | None = None) -> Run:
    """Each thread does ops operations; steps are interleaved at random.

    If crash is a thread number, that thread stops for good after a random
    number of steps in the middle of an operation.
    """
    r = Run(alloc, nthreads, seed)
    rng = r.rng
    left = {t: ops for t in range(nthreads)}
    crash_after = rng.randint(1, 40) if crash is not None else -1
    crash_steps = 0
    while True:
        ready = [t for t in range(nthreads) if left[t] > 0 or t in r.current]
        if crash is not None and crash_steps >= crash_after and crash in r.current:
            ready = [t for t in ready if t != crash]
        if not ready:
            return r
        t = rng.choice(ready)
        if t not in r.current:
            left[t] -= 1
            r.start(t, "free" if r.held[t] and rng.random() < 0.5 else "malloc")
        r.step(t)
        if t == crash:
            crash_steps += 1
