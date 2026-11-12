# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shenandoah-collector/. The authors are listed in prov/1QJAF8.jsonl.

"""A model of the Shenandoah collector (Flood et al., PPPJ 2016, and OpenJDK since JDK 12).

This is a model, not a collector. Threads are Python generators, and a
scheduler driven by a random.Random(seed) picks which one takes the next
atomic step. The model keeps the mechanism of Shenandoah:

* Regions, concurrent marking with a snapshot-at-the-beginning (SATB)
  pre-write barrier, and a collection set of the regions with the most garbage.
* Concurrent evacuation. Each object of the collection set has a forwarding
  pointer. The collector, or a mutator that needs the object, copies it and
  installs the forwarding pointer with a compare-and-swap; the loser of the
  race uses the winner's copy.
* Concurrent update of references, then a short pause that fixes the roots
  and frees the collection set.
* Two barrier modes. "brooks" is the design of the 2016 paper: every object
  has a forwarding word (a Brooks pointer); reads go through it, and a write
  to an object of the collection set first evacuates it. A mutator may hold a
  pointer to a from-space object. "lrb" is the load reference barrier of
  JDK 13: a pointer loaded from the heap that points into the collection set
  is evacuated or forwarded at once, and the field is healed. Mutators never
  hold a pointer into the collection set.

Simplifications: each pause is one step taken when every mutator is between
operations; one collector thread; no weak references, no degenerated or full
collections, no humongous regions, and the forwarding pointer is an attribute
of the object in both modes.
"""

from __future__ import annotations

import random
from typing import Iterator


class OutOfMemory(Exception):
    pass


class Obj:
    __slots__ = ("oid", "fields", "fwd")

    def __init__(self, oid: int, fields: list[int | None]) -> None:
        self.oid, self.fields = oid, fields
        self.fwd: int | None = None  # the forwarding pointer; None means "points to itself"


class ShenandoahHeap:
    def __init__(self, regions: int, region_size: int, threads: int, registers: int,
                 mode: str = "lrb", barrier: bool = True, live_limit: float = 0.5) -> None:
        assert mode in ("lrb", "brooks")
        self.S, self.nregions = region_size, regions
        self.mode, self.barrier, self.live_limit = mode, barrier, live_limit
        self.state = ["free"] * regions  # free, alloc, used, cset
        self.top = [0] * regions
        self.seq = [0] * regions  # the cycle in which the region was taken
        self.memory: dict[int, Obj] = {}
        self.regs: list[list[int | None]] = [[None] * registers for _ in range(threads)]
        self.idle = [True] * threads
        self.cycle = 0
        self.phase = "idle"  # idle, mark, evac, update
        self.marked: set[int] = set()
        self.stack: list[int] = []
        self.satb: list[int] = []
        self.cset: set[int] = set()
        self.alloc_region: dict[str, int | None] = {}
        self.result: dict[str, int] = {}
        self.next_oid = 0
        self.cycles = 0
        self.mutator_copies = 0
        self.lost_races = {"mutator": 0, "gc": 0}
        self.from_space_writes = 0  # writes into an object of the collection set while it is moved

    # ---- memory ----

    def region(self, a: int) -> int:
        return a // self.S

    def in_cset(self, a: int | None) -> bool:
        return a is not None and self.region(a) in self.cset

    def take_region(self, owner: str) -> int:
        for r in range(self.nregions):
            if self.state[r] == "free":
                self.state[r], self.top[r], self.seq[r] = "alloc", 0, self.cycle
                self.alloc_region[owner] = r
                return r
        raise OutOfMemory

    def alloc_slot(self, owner: str) -> int:
        r = self.alloc_region.get(owner)
        if r is None or self.top[r] == self.S:
            if r is not None:
                self.state[r] = "used"
            r = self.take_region(owner)
        a = r * self.S + self.top[r]
        self.top[r] += 1
        return a

    def retire_alloc_regions(self) -> None:
        for r in self.alloc_region.values():
            if r is not None:
                self.state[r] = "used"
        self.alloc_region = {}

    def fwd(self, a: int | None) -> int | None:
        if a is None:
            return None
        f = self.memory[a].fwd
        return a if f is None else f

    def live_now(self, a: int) -> bool:
        return a in self.marked or self.seq[self.region(a)] == self.cycle

    def mark(self, a: int | None) -> None:
        if a is not None and not self.live_now(a):
            self.marked.add(a)
            self.stack.append(a)

    def evacuate(self, a: int, owner: str) -> Iterator[None]:
        """Copy a out of the collection set unless someone did; the result is in self.result[owner]."""
        if self.memory[a].fwd is None:  # @line L1
            o = self.memory[a]
            b = self.alloc_slot(owner)  # @line L2
            self.memory[b] = Obj(o.oid, list(o.fields))
            yield
            if self.memory[a].fwd is None:  # @line L3
                self.memory[a].fwd = b
                if owner != "gc":
                    self.mutator_copies += 1
            else:
                self.lost_races["mutator" if owner != "gc" else "gc"] += 1
        self.result[owner] = self.fwd(a)  # @line L4

    def evacuate_now(self, a: int, owner: str) -> int:
        """Evacuate in one step; used only inside a pause."""
        for _ in self.evacuate(a, owner):
            pass
        return self.result[owner]

    # ---- the mutator ----

    def mutator(self, t: int, program: list[tuple], shadow: "Shadow | None" = None) -> Iterator[None]:
        regs, owner = self.regs[t], f"m{t}"
        brooks = self.mode == "brooks" and self.barrier
        for op in program:
            self.idle[t] = False
            kind = op[0]
            if kind == "new":
                _, dst, nf = op
                a = self.alloc_slot(owner)
                self.memory[a] = Obj(self.next_oid, [None] * nf)
                self.next_oid += 1
                regs[dst] = a
            elif kind == "load":
                _, dst, src, f = op
                x = regs[src]
                if x is not None:
                    holder = self.fwd(x) if brooks else x  # the Brooks read barrier
                    if f < len(self.memory[holder].fields):
                        v = self.memory[holder].fields[f]  # @line L5
                        if shadow is not None:
                            shadow.load(t, dst, src, f)
                        if self.mode == "lrb" and self.barrier and self.in_cset(v):  # @line L6
                            yield
                            yield from self.evacuate(v, owner)
                            w = self.result[owner]
                            yield
                            if self.memory[holder].fields[f] == v:  # heal the field by CAS
                                self.memory[holder].fields[f] = w
                            v = w
                        regs[dst] = v  # @line L7
                        if shadow is not None:
                            shadow.check_register(self, t, dst)
            elif kind == "store":
                _, dst, f, src = op
                x = regs[dst]
                if x is not None and f < len(self.memory[self.fwd(x)].fields):
                    if brooks and self.phase in ("evac", "update") and self.in_cset(x):  # @line L9
                        yield
                        yield from self.evacuate(x, owner)  # the Brooks write barrier
                    target = self.fwd(x) if brooks else x
                    o = self.memory[target]
                    if self.phase == "mark" and self.barrier and o.fields[f] is not None:  # @line L8
                        self.satb.append(o.fields[f])
                    y = self.fwd(regs[src]) if brooks else regs[src]  # the store-value barrier
                    if self.in_cset(target) and self.phase in ("evac", "update"):
                        self.from_space_writes += 1
                    o.fields[f] = y  # @line L10
                    if shadow is not None:
                        shadow.store(t, dst, f, src)
            elif kind == "move":
                _, dst, src = op
                regs[dst] = regs[src]
            else:
                regs[op[1]] = None
            if shadow is not None and kind not in ("load", "store"):
                shadow.apply(t, op)
            self.idle[t] = True
            yield

    # ---- the collector ----

    def safepoint(self) -> Iterator[None]:
        while not all(self.idle):
            yield

    def mark_step(self) -> bool:
        if self.satb:
            self.mark(self.satb.pop())
            return True
        if self.stack:
            for y in self.memory[self.stack.pop()].fields:
                self.mark(y)
            return True
        return False

    def collector(self) -> Iterator[None]:
        while True:
            yield from self.safepoint()
            # Init Mark pause.
            self.cycle += 1
            self.retire_alloc_regions()
            self.phase, self.marked, self.stack, self.satb = "mark", set(), [], []
            for regs in self.regs:  # @line L11
                for v in regs:
                    self.mark(v)
            yield
            while self.mark_step():  # @line L12
                yield
            yield from self.safepoint()
            # Final Mark pause: finish marking, choose the collection set, evacuate the roots.
            while self.mark_step():  # @line L13
                pass
            self.choose_collection_set()
            self.phase = "evac"
            self.retire_alloc_regions()
            for regs in self.regs:
                for i, v in enumerate(regs):
                    if self.in_cset(v):
                        regs[i] = self.evacuate_now(v, "gc")
            yield
            for r in sorted(self.cset):  # @line L14
                for a in range(r * self.S, r * self.S + self.top[r]):
                    if a in self.marked and self.memory[a].fwd is None:
                        yield from self.evacuate(a, "gc")
                        yield
            yield from self.safepoint()
            self.phase = "update"  # Init Update Refs pause
            yield
            todo = [r for r in range(self.nregions) if self.state[r] in ("alloc", "used")]
            for r in todo:  # @line L15
                for a in range(r * self.S, r * self.S + self.top[r]):
                    if a in self.memory and self.live_now(a):
                        o = self.memory[a]
                        for f, v in enumerate(o.fields):
                            if self.in_cset(v):
                                o.fields[f] = self.fwd(v)  # a CAS: no other step runs in between
                        yield
            yield from self.safepoint()
            # Final Update Refs pause: fix the roots, free the collection set.
            for regs in self.regs:  # @line L16
                for i, v in enumerate(regs):
                    if self.in_cset(v):
                        regs[i] = self.fwd(v)
            for r in self.cset:
                self.free_region(r)
            self.cset, self.phase = set(), "idle"
            self.cycles += 1
            yield

    def choose_collection_set(self) -> None:
        live = [0] * self.nregions
        for a in self.marked:
            live[self.region(a)] += 1
        for r in range(self.nregions):
            if self.state[r] != "used" or self.seq[r] == self.cycle:
                continue
            if live[r] == 0:
                self.free_region(r)  # immediate garbage
            elif live[r] <= self.live_limit * self.top[r]:
                self.state[r] = "cset"
                self.cset.add(r)

    def free_region(self, r: int) -> None:
        for a in range(r * self.S, (r + 1) * self.S):
            self.memory.pop(a, None)
        self.state[r], self.top[r] = "free", 0

    # ---- checks ----

    def to_space_ok(self, t: int) -> bool:
        """With the LRB, no register points into the collection set while it is moved.
        In both modes, every register names an object that exists."""
        for v in self.regs[t]:
            if v is None:
                continue
            if v not in self.memory:
                return False
            if self.mode == "lrb" and self.phase in ("evac", "update") and self.in_cset(v):
                return False
        return True

    def logical_graph(self) -> tuple:
        def oid(v: int | None) -> int | None:
            return None if v is None else self.memory[self.fwd(v)].oid
        seen: dict[int, tuple] = {}
        stack = [v for regs in self.regs for v in regs if v is not None]
        while stack:
            o = self.memory[self.fwd(stack.pop())]
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

    def check_register(self, h: ShenandoahHeap, t: int, dst: int) -> None:
        v = h.regs[t][dst]
        got = None if v is None else h.memory[h.fwd(v)].oid
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


def run(seed: int, mode: str = "lrb", threads: int = 3, registers: int = 4, length: int = 300,
        regions: int = 40, region_size: int = 8, gc_share: float = 0.3, barrier: bool = True,
        check=None) -> ShenandoahHeap:
    """Run random programs on all mutators and the collector under a seeded interleaving."""
    rng = random.Random(seed)
    h = ShenandoahHeap(regions, region_size, threads, registers, mode=mode, barrier=barrier)
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
