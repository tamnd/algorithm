# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/c4-collector/. The authors are listed in prov/G25N97.jsonl.

"""A model of one generation of the C4 collector (Tene, Iyengar and Wolf, ISMM 2011).

This is a model, not a collector. Threads are Python generators, and a
scheduler driven by a random.Random(seed) picks which one takes the next
atomic step. The model keeps the mechanism of C4:

* The loaded value barrier (LVB). Every pointer loaded from the heap is tested
  for two conditions: its not-marked-through (NMT) bit differs from the value
  expected in this cycle, or it points into a protected page (a page that is
  being relocated, or whose memory has already been released). Either one traps.
  The trap marks the object, or finds or makes its new copy, and writes the
  fixed pointer back into the field it came from (self-healing).
* Mark, Relocate, Remap. Marking flips the expected NMT value, so every old
  pointer is "not marked through" again. Relocation protects the pages chosen,
  copies their live objects to new pages (a mutator that traps does the copy
  itself if it gets there first), and releases each page's memory at once
  (quick release). The forwarding data stay off the page. The remap of stale
  pointers is folded into the next marking, after which the protected virtual
  pages are freed.

Simplifications: C4 has no global pause; each mutator passes a checkpoint on
its own. The model takes each checkpoint for all mutators in one step, when
every mutator is between operations. The model has one generation (C4 runs a
young and an old collector, both with this algorithm), one collector thread,
no weak references, and page protection is a set of page numbers.
"""

from __future__ import annotations

import random
from typing import Iterator

ADDRESS_BITS = 20
ADDRESS_MASK = (1 << ADDRESS_BITS) - 1
NMT = 1 << ADDRESS_BITS


class OutOfMemory(Exception):
    pass


class Obj:
    __slots__ = ("oid", "fields")

    def __init__(self, oid: int, fields: list[int | None]) -> None:
        self.oid, self.fields = oid, fields


def address(p: int) -> int:
    return p & ADDRESS_MASK


def nmt(p: int) -> int:
    return 1 if p & NMT else 0


class C4Heap:
    def __init__(self, pages: int, page_size: int, threads: int, registers: int,
                 barrier: bool = True, live_limit: float = 0.5) -> None:
        self.S, self.npages = page_size, pages
        self.barrier, self.live_limit = barrier, live_limit
        self.state = ["free"] * pages  # free, alloc, used, chosen, released
        self.top = [0] * pages
        self.seq = [0] * pages  # the cycle in which the page was taken
        self.protected: set[int] = set()  # pages the mutators may not touch
        self.memory: dict[int, Obj] = {}
        self.regs: list[list[int | None]] = [[None] * registers for _ in range(threads)]
        self.idle = [True] * threads
        self.cycle = 0
        self.expected = 0  # the NMT value of a marked-through pointer in this cycle
        self.marking = False
        self.phase = "idle"
        self.marked: set[int] = set()
        self.stack: list[int] = []
        self.forwarding: dict[int, int] = {}  # kept off the pages, until the next marking ends
        self.reloc: set[int] = set()
        self.alloc_page: dict[str, int | None] = {}
        self.result: dict[str, int] = {}
        self.next_oid = 0
        self.cycles = 0
        self.traps = {"nmt": 0, "protected": 0}
        self.mutator_copies = 0
        self.lost_races = {"mutator": 0, "gc": 0}

    # ---- memory ----

    def page(self, a: int) -> int:
        return a // self.S

    def take_page(self, owner: str) -> int:
        for p in range(self.npages):
            if self.state[p] == "free":
                self.state[p], self.top[p], self.seq[p] = "alloc", 0, self.cycle
                self.alloc_page[owner] = p
                return p
        raise OutOfMemory

    def alloc_slot(self, owner: str) -> int:
        p = self.alloc_page.get(owner)
        if p is None or self.top[p] == self.S:
            if p is not None:
                self.state[p] = "used"
            p = self.take_page(owner)
        a = p * self.S + self.top[p]
        self.top[p] += 1
        return a

    def retire_alloc_pages(self) -> None:
        for p in self.alloc_page.values():
            if p is not None:
                self.state[p] = "used"
        self.alloc_page = {}

    def remap(self, a: int) -> int:
        return self.forwarding.get(a, a)

    def pointer(self, a: int) -> int:
        return a | (NMT if self.expected else 0)

    def needs_trap(self, v: int) -> bool:
        return nmt(v) != self.expected or self.page(address(v)) in self.protected

    def live_now(self, a: int) -> bool:
        return a in self.marked or self.seq[self.page(a)] == self.cycle

    def mark(self, a: int) -> None:
        if not self.live_now(a):
            self.marked.add(a)
            self.stack.append(a)

    def copy(self, a: int, owner: str) -> int:
        b = self.alloc_slot(owner)
        o = self.memory[a]
        self.memory[b] = Obj(o.oid, list(o.fields))
        return b

    def relocate_now(self, a: int, owner: str) -> int:
        """Copy and install in one step; used only inside the relocation checkpoint."""
        a = self.remap(a)
        if self.page(a) in self.protected and a not in self.forwarding:
            self.forwarding[a] = self.copy(a, owner)
        return self.forwarding.get(a, a)

    # ---- the loaded value barrier ----

    def trap(self, holder: int, f: int, v: int, owner: str) -> Iterator[None]:
        """The LVB trap for a pointer v loaded from field f of the object at holder.
        Yields between atomic steps; the fixed pointer is left in self.result[owner]."""
        a = address(v)  # @line L4
        if self.page(a) in self.protected:  # @line L5
            self.traps["protected"] += 1
            if a not in self.forwarding:  # @line L6
                b = self.copy(a, owner)
                yield
                if a in self.forwarding:  # the compare-and-swap on the forwarding entry
                    self.lost_races["mutator"] += 1
                else:
                    self.forwarding[a] = b
                    self.mutator_copies += 1
            a = self.forwarding[a]  # @line L7
        if nmt(v) != self.expected:
            self.traps["nmt"] += 1
            if self.marking:  # @line L8
                self.mark(a)
        good = self.pointer(a)
        yield
        o = self.memory[holder]
        if o.fields[f] == v:  # @line L9
            o.fields[f] = good
        self.result[owner] = good

    # ---- the mutator ----

    def mutator(self, t: int, program: list[tuple], shadow: "Shadow | None" = None) -> Iterator[None]:
        regs, owner = self.regs[t], f"m{t}"
        for op in program:
            self.idle[t] = False
            kind = op[0]
            if kind == "new":
                _, dst, nf = op
                a = self.alloc_slot(owner)
                self.memory[a] = Obj(self.next_oid, [None] * nf)
                self.next_oid += 1
                regs[dst] = self.pointer(a)
            elif kind == "load":
                _, dst, src, f = op
                x = regs[src]
                if x is not None and f < len(self.memory[address(x)].fields):
                    holder = address(x)
                    v = self.memory[holder].fields[f]  # @line L1
                    if shadow is not None:
                        shadow.load(t, dst, src, f)
                    if v is not None and self.barrier and self.needs_trap(v):  # @line L2
                        yield
                        yield from self.trap(holder, f, v, owner)
                        v = self.result[owner]
                    regs[dst] = v  # @line L3
                    if shadow is not None:
                        shadow.check_register(self, t, dst)
            elif kind == "store":
                _, dst, f, src = op
                x = regs[dst]
                if x is not None and f < len(self.memory[address(x)].fields):
                    self.memory[address(x)].fields[f] = regs[src]
                    if shadow is not None:
                        shadow.store(t, dst, f, src)
            elif kind == "move":
                _, dst, src = op
                regs[dst] = regs[src]
            else:
                regs[op[1]] = None
            if shadow is not None and kind != "load":
                shadow.apply(t, op)
            self.idle[t] = True
            yield

    # ---- the collector ----

    def checkpoint(self) -> Iterator[None]:
        """Wait until every mutator is between operations (all threads pass at once in the model)."""
        while not all(self.idle):
            yield

    def collector(self) -> Iterator[None]:
        while True:
            yield from self.checkpoint()
            # Mark: flip the expected NMT value, then mark and fix the roots.
            self.cycle += 1
            self.expected = 1 - self.expected  # @line L10
            self.marking, self.phase, self.marked, self.stack = True, "mark", set(), []
            self.retire_alloc_pages()
            for regs in self.regs:
                for i, v in enumerate(regs):
                    if v is not None:
                        a = self.remap(address(v))
                        self.mark(a)
                        regs[i] = self.pointer(a)
            yield
            while True:
                while self.stack:  # @line L11
                    o = self.memory[self.stack.pop()]
                    for f in range(len(o.fields)):  # @line L12
                        v = o.fields[f]
                        if v is not None and self.needs_trap(v):
                            a = self.remap(address(v))
                            self.mark(a)
                            o.fields[f] = self.pointer(a)
                        yield
                yield from self.checkpoint()
                if not self.stack:
                    break
            # Every live pointer is remapped: free the released virtual pages and their forwarding data.
            self.marking = False
            for p in range(self.npages):  # @line L13
                if self.state[p] == "released":
                    self.protected.discard(p)
                    self.free_page(p)
            self.forwarding = {}
            self.select_relocation_set()
            yield
            yield from self.checkpoint()
            # Relocate: protect the chosen pages, then fix the roots that point into them.
            self.phase = "relocate"
            self.protected |= self.reloc  # @line L15
            self.retire_alloc_pages()
            for regs in self.regs:
                for i, v in enumerate(regs):
                    if v is not None:
                        regs[i] = self.pointer(self.relocate_now(address(v), "gc"))
            yield
            for p in sorted(self.reloc):  # @line L16
                for a in range(p * self.S, p * self.S + self.top[p]):
                    if a in self.marked and a not in self.forwarding:
                        b = self.copy(a, "gc")
                        yield
                        if a in self.forwarding:
                            self.lost_races["gc"] += 1
                        else:
                            self.forwarding[a] = b
                        yield
                self.release(p)  # @line L17
                yield
            self.reloc, self.phase = set(), "idle"
            self.cycles += 1
            yield

    def select_relocation_set(self) -> None:
        live = [0] * self.npages
        for a in self.marked:
            live[self.page(a)] += 1
        for p in range(self.npages):  # @line L14
            if self.state[p] != "used" or self.seq[p] == self.cycle:
                continue
            if live[p] == 0:
                self.free_page(p)
            elif live[p] <= self.live_limit * self.top[p]:
                self.state[p] = "chosen"
                self.reloc.add(p)

    def release(self, p: int) -> None:
        """Quick release: the memory goes back now; the page stays protected until the next marking ends."""
        for a in range(p * self.S, (p + 1) * self.S):
            self.memory.pop(a, None)
        self.state[p] = "released"

    def free_page(self, p: int) -> None:
        for a in range(p * self.S, (p + 1) * self.S):
            self.memory.pop(a, None)
        self.state[p], self.top[p] = "free", 0

    # ---- checks ----

    def to_space_ok(self, t: int) -> bool:
        """Every register of thread t is marked through and points to an unprotected page that holds the object."""
        for v in self.regs[t]:
            if v is None:
                continue
            a = address(v)
            if self.needs_trap(v) or a not in self.memory:
                return False
        return True

    def resolve(self, v: int) -> int:
        return self.remap(address(v))

    def logical_graph(self) -> tuple:
        def oid(v: int | None) -> int | None:
            return None if v is None else self.memory[self.resolve(v)].oid
        seen: dict[int, tuple] = {}
        stack = [v for regs in self.regs for v in regs if v is not None]
        while stack:
            o = self.memory[self.resolve(stack.pop())]
            if o.oid in seen:
                continue
            seen[o.oid] = tuple(oid(y) for y in o.fields)
            stack.extend(y for y in o.fields if y is not None)
        return tuple(tuple(oid(v) for v in regs) for regs in self.regs), tuple(sorted(seen.items()))


class Shadow:
    """The same operations on a graph of identities, with no collector."""

    def __init__(self, threads: int, registers: int) -> None:
        self.regs: list[list[int | None]] = [[None] * registers for _ in range(threads)]
        self.cells: dict[int, list[int | None]] = {}
        self.next = 0
        self.pending: dict[int, int | None] = {}

    def load(self, t: int, dst: int, src: int, f: int) -> None:
        self.pending[t] = self.cells[self.regs[t][src]][f]
        self.regs[t][dst] = self.pending[t]

    def check_register(self, h: C4Heap, t: int, dst: int) -> None:
        v = h.regs[t][dst]
        got = None if v is None else h.memory[h.resolve(v)].oid
        assert got == self.pending[t], "a load returned another object"

    def store(self, t: int, dst: int, f: int, src: int) -> None:
        self.cells[self.regs[t][dst]][f] = self.regs[t][src]

    def apply(self, t: int, op: tuple) -> None:
        if op[0] == "new":
            self.cells[self.next] = [None] * op[2]
            self.regs[t][op[1]] = self.next
            self.next += 1
        elif op[0] == "move":
            self.regs[t][op[1]] = self.regs[t][op[2]]
        elif op[0] == "clear":
            self.regs[t][op[1]] = None

    def logical_graph(self) -> tuple:
        seen: dict[int, tuple] = {}
        stack = [x for regs in self.regs for x in regs if x is not None]
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen[x] = tuple(self.cells[x])
            stack.extend(y for y in self.cells[x] if y is not None)
        return tuple(tuple(regs) for regs in self.regs), tuple(sorted(seen.items()))


def random_program(rng: random.Random, length: int, registers: int) -> list[tuple]:
    prog = []
    for _ in range(length):
        u, d, s, f = rng.random(), rng.randrange(registers), rng.randrange(registers), rng.randrange(2)
        if u < 0.2:
            prog.append(("new", d, rng.randint(1, 2)))
        elif u < 0.6:
            prog.append(("load", d, s, f))
        elif u < 0.9:
            prog.append(("store", d, f, s))
        elif u < 0.96:
            prog.append(("move", d, s))
        else:
            prog.append(("clear", d))
    return prog


def run(seed: int, threads: int = 3, registers: int = 4, length: int = 300, pages: int = 40,
        page_size: int = 8, gc_share: float = 0.3, barrier: bool = True, check=None) -> C4Heap:
    """Run random programs on all mutators and the collector under a seeded interleaving."""
    rng = random.Random(seed)
    h = C4Heap(pages, page_size, threads, registers, barrier=barrier)
    shadow = Shadow(threads, registers)
    muts = {t: h.mutator(t, random_program(rng, length, registers), shadow) for t in range(threads)}
    gc = h.collector()
    while muts:
        if rng.random() < gc_share:
            next(gc)
        else:
            t = rng.choice(sorted(muts))
            try:
                next(muts[t])
            except StopIteration:
                del muts[t]
        if check is not None:
            check(h, shadow)
    return h
