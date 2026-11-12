# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/concurrent-garbage-collection/. The authors are listed in prov/0GJMF8.jsonl.

"""Mostly concurrent mark-sweep with a card table (Boehm, Demers and Shenker
1991; Printezis and Detlefs 2000).

This is a model, not a runtime. The heap has H cells with `fields` pointer
fields each, grouped into cards of C consecutive cells. The mutator holds r
registers (the roots). A scheduler picks, at each tick, either one mutator
operation or one collector step, from a random.Random(seed) that the caller
passes in. Each mutator operation, with its write barrier, is atomic, and each
collector step (scan one cell, clean one card, sweep one cell) is atomic. Two
steps are pauses: the initial mark and the remark. In them the mutator does not
run.

Phases: idle, mark, preclean, sweep. The write barrier dirties the card of the
cell that is written. The remark rescans the roots and the marked cells on
dirty cards, and then drains the gray stack. Precleaning cleans dirty cards
concurrently, before the remark, so that the remark has less to do. When an
allocation finds no free cell, the cycle is finished in one pause: this is a
concurrent mode failure.
"""

from __future__ import annotations

import random

IDLE, MARK, PRECLEAN, SWEEP = "idle", "mark", "preclean", "sweep"


class OutOfMemory(Exception):
    pass


class Heap:
    def __init__(self, size: int, registers: int, card: int = 4, fields: int = 2,
                 trigger: int = 0, barrier: bool = True, preclean: bool = True) -> None:
        self.H, self.C, self.F = size, card, trigger
        self.fields: list[list[int | None]] = [[None] * fields for _ in range(size)]
        self.marked = [False] * size
        self.is_free = [True] * size
        self.free = list(range(size - 1, -1, -1))
        self.dirty = [False] * (-(-size // card))
        self.regs: list[int | None] = [None] * registers
        self.barrier, self.preclean = barrier, preclean
        self.phase = IDLE
        self.work: list[int] = []
        self.s = 0
        self.cycles = 0
        self.preclean_budget = 0
        self.remark_pauses: list[int] = []  # units of work in each remark
        self.failures = 0  # concurrent mode failures

    def shade(self, y: int | None) -> None:
        if y is not None and not self.marked[y]:
            self.marked[y] = True
            self.work.append(y)

    def scan(self, x: int) -> None:
        for y in self.fields[x]:
            self.shade(y)

    def cells_of(self, c: int) -> range:
        return range(c * self.C, min((c + 1) * self.C, self.H))

    # The collector: two pauses and three concurrent steps.

    def initial_mark(self) -> None:
        self.dirty = [False] * len(self.dirty)  # @line L1
        for r in self.regs:
            self.shade(r)
        self.phase = MARK
        self.cycles += 1
        self.preclean_budget = 2 * len(self.dirty) if self.preclean else 0

    def mark_step(self) -> None:
        x = self.work.pop()  # @line L2
        self.scan(x)  # @line L3

    def preclean_step(self, c: int) -> None:
        self.dirty[c] = False  # @line L4
        for x in self.cells_of(c):  # @line L5
            if self.marked[x] and not self.is_free[x]:
                self.scan(x)

    def remark(self) -> int:
        units = 0
        for r in self.regs:  # @line L6
            self.shade(r)
            units += 1
        for c, d in enumerate(self.dirty):  # @line L7
            if d:
                self.dirty[c] = False
                for x in self.cells_of(c):
                    if self.marked[x] and not self.is_free[x]:
                        self.scan(x)
                        units += 1
        while self.work:  # @line L8
            self.mark_step()
            units += 1
        self.phase, self.s = SWEEP, 0  # @line L9
        self.remark_pauses.append(units)
        return units

    def sweep_step(self) -> None:
        s = self.s
        if self.marked[s]:  # @line L10
            self.marked[s] = False
        elif not self.is_free[s]:  # @line L11
            self.fields[s] = [None] * len(self.fields[s])
            self.is_free[s] = True
            self.free.append(s)
        self.s += 1  # @line L12
        if self.s == self.H:
            self.phase = IDLE

    def collector_step(self) -> None:
        if self.phase == IDLE:
            if len(self.free) <= self.F:
                self.initial_mark()
        elif self.phase == MARK:
            if self.work:
                self.mark_step()
            else:
                self.phase = PRECLEAN
        elif self.phase == PRECLEAN:
            dirty = [c for c, d in enumerate(self.dirty) if d]
            if self.work:
                self.mark_step()
            elif dirty and self.preclean_budget > 0:
                self.preclean_budget -= 1
                self.preclean_step(dirty[0])
            else:
                self.remark()
        else:
            self.sweep_step()

    def finish_in_pause(self) -> None:
        """The fallback when the allocator finds no free cell."""
        if self.phase == IDLE:
            self.initial_mark()
        if self.phase in (MARK, PRECLEAN):
            self.remark()
        while self.phase == SWEEP:
            self.sweep_step()

    # The mutator.

    def write(self, x: int, f: int, y: int | None) -> None:
        self.fields[x][f] = y  # @line L13
        if self.barrier:
            self.dirty[x // self.C] = True  # @line L14

    def allocate(self) -> int:
        if not self.free:  # @line L15
            self.failures += 1
            self.finish_in_pause()
            if not self.free:  # the cycle kept only floating garbage: collect again
                self.finish_in_pause()
            if not self.free:
                raise OutOfMemory
        x = self.free.pop()  # @line L16
        self.is_free[x] = False
        self.fields[x] = [None] * len(self.fields[x])
        if self.phase in (MARK, PRECLEAN) or (self.phase == SWEEP and x >= self.s):
            self.marked[x] = True
        return x

    def reachable(self) -> set[int]:
        seen = {r for r in self.regs if r is not None}
        stack = list(seen)
        while stack:
            for y in self.fields[stack.pop()]:
                if y is not None and y not in seen:
                    seen.add(y)
                    stack.append(y)
        return seen


def mutator_step(heap: Heap, live: int, rng: random.Random) -> None:
    """One random mutator operation that keeps at most `live` cells reachable."""
    nf = len(heap.fields[0])
    held = [r for r in heap.regs if r is not None]
    op = rng.random()
    if op < 0.3 and len(heap.reachable()) < live:
        x = heap.allocate()
        if held and rng.random() < 0.7:
            heap.write(rng.choice(held), rng.randrange(nf), x)
        else:
            heap.regs[rng.randrange(len(heap.regs))] = x
    elif op < 0.6 and held:
        y = heap.fields[rng.choice(held)][rng.randrange(nf)]
        if y is not None:
            heap.regs[rng.randrange(len(heap.regs))] = y
    elif op < 0.9 and held:
        heap.write(rng.choice(held), rng.randrange(nf), rng.choice(held + [None]))
    else:
        heap.regs[rng.randrange(len(heap.regs))] = None


def apply(heap: Heap, op: tuple) -> None:
    """A mutator operation on registers: load, store or clear."""
    if op[0] == "load":  # ("load", i, j, f): r_i <- r_j.f
        _, i, j, f = op
        heap.regs[i] = heap.fields[heap.regs[j]][f]
    elif op[0] == "store":  # ("store", i, f, j): r_i.f <- r_j, or nil if j is None
        _, i, f, j = op
        heap.write(heap.regs[i], f, None if j is None else heap.regs[j])
    else:  # ("clear", i)
        heap.regs[op[1]] = None


def all_runs(heap: Heap, program: list[tuple]) -> tuple[int, int]:
    """Run the program against one whole collector cycle, in every interleaving.

    The cycle starts with the initial mark. Return (runs, runs in which a
    reachable cell was freed).
    """
    import copy

    heap.initial_mark()
    runs = lost = 0
    stack = [(heap, 0)]
    while stack:
        h, pc = stack.pop()
        if pc == len(program) and h.phase == IDLE:
            runs += 1
            lost += any(h.is_free[x] for x in h.reachable())
            continue
        if pc < len(program):
            g = copy.deepcopy(h)
            apply(g, program[pc])
            stack.append((g, pc + 1))
        if h.phase != IDLE:
            g = copy.deepcopy(h)
            g.collector_step()
            stack.append((g, pc))
    return runs, lost


def run(heap: Heap, live: int, ticks: int, rng: random.Random, collector_share: float = 0.5) -> int:
    """Interleave mutator and collector steps. Return the number of times a
    reachable cell was found on the free list or freed (0 for a correct collector)."""
    lost = 0
    for _ in range(ticks):
        if rng.random() < collector_share:
            heap.collector_step()
        else:
            mutator_step(heap, live, rng)
        if any(heap.is_free[x] for x in heap.reachable()):
            lost += 1
            break
    return lost
