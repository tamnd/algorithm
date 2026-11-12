# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-garbage-collection/. The authors are listed in prov/RV18E3.jsonl.

"""Incremental mark-sweep paced by allocation: k units of collector work per allocation.

Heap model: H cells with the addresses 0 to H - 1, each with `fields` pointer
fields (an address or None) and a mark bit. Free cells are on a free list.
The mutator holds r registers (the roots). It loads, stores, clears registers
and allocates; at every moment at most L cells are reachable.

The collector has three phases: idle, mark and sweep. When an allocation
finds at most F free cells and the collector is idle, a short pause shades
the roots and starts the mark phase. After that, each allocation first does
k units of work: one unit scans one gray cell, or sweeps one cell. Marking
uses the snapshot-at-the-beginning deletion barrier, and cells allocated
during the cycle are marked (allocated black). The sweep frees the unmarked
cells and clears the marks of the others.

The pacing theorem of the page: with m = ceil((L + H) / k), F >= m and
H >= L + 2 m, no allocation ever finds the free list empty, and no
allocation does more than k units of work.
"""

from __future__ import annotations

import random

IDLE, MARK, SWEEP = "idle", "mark", "sweep"


class OutOfMemory(Exception):
    pass


class Heap:
    def __init__(self, size: int, registers: int, k: int, trigger: int, fields: int = 2) -> None:
        self.H, self.k, self.F = size, k, trigger
        self.fields: list[list[int | None]] = [[None] * fields for _ in range(size)]
        self.marked = [False] * size
        self.is_free = [True] * size
        self.free = list(range(size - 1, -1, -1))  # pop() gives the lowest address
        self.regs: list[int | None] = [None] * registers
        self.phase = IDLE
        self.work: list[int] = []
        self.s = 0  # the sweep pointer
        self.max_units = 0  # the most work done by one allocation
        self.root_pause = 0  # the most roots shaded in one start pause
        self.cycles = 0

    # The collector.

    def shade(self, y: int | None) -> None:
        if y is not None and not self.marked[y]:
            self.marked[y] = True
            self.work.append(y)

    def begin_cycle(self) -> None:
        for r in self.regs:  # @line L7
            self.shade(r)
        self.root_pause = max(self.root_pause, len(self.regs))
        self.phase = MARK
        self.cycles += 1

    def collect_work(self, k: int) -> int:
        u = 0  # @line L8
        while u < k and self.phase != IDLE:  # @line L9
            if self.phase == MARK and self.work:  # @line L10
                x = self.work.pop()  # @line L11
                for y in self.fields[x]:
                    self.shade(y)
                u += 1
            elif self.phase == MARK:
                self.phase, self.s = SWEEP, 0  # @line L12
            elif self.s < self.H:  # @line L13
                if self.marked[self.s]:  # @line L14
                    self.marked[self.s] = False
                elif not self.is_free[self.s]:  # @line L15
                    self.fields[self.s] = [None] * len(self.fields[self.s])
                    self.is_free[self.s] = True
                    self.free.append(self.s)
                self.s += 1  # @line L16
                u += 1
            else:
                self.phase = IDLE  # @line L17
        return u

    # The mutator.

    def allocate(self) -> int:
        if self.phase == IDLE and len(self.free) <= self.F:  # @line L1
            self.begin_cycle()
        units = self.collect_work(self.k) if self.phase != IDLE else 0  # @line L2
        self.max_units = max(self.max_units, units)
        if not self.free:  # @line L3
            raise OutOfMemory
        x = self.free.pop()  # @line L4
        self.is_free[x] = False
        self.fields[x] = [None] * len(self.fields[x])
        if self.phase == MARK or (self.phase == SWEEP and x >= self.s):  # @line L5
            self.marked[x] = True  # @line L6
        return x

    def write(self, x: int, f: int, y: int | None) -> None:
        if self.phase == MARK:  # @line L18
            self.shade(self.fields[x][f])
        self.fields[x][f] = y  # @line L19

    def reachable(self) -> set[int]:
        seen = {r for r in self.regs if r is not None}
        stack = list(seen)
        while stack:
            for y in self.fields[stack.pop()]:
                if y is not None and y not in seen:
                    seen.add(y)
                    stack.append(y)
        return seen


def pacing_bound(live: int, size: int, k: int) -> tuple[int, bool]:
    """Return m = ceil((L + H) / k) and whether H >= L + 2 m holds."""
    m = -(-(live + size) // k)
    return m, size >= live + 2 * m


def run_queue(heap: Heap, live: int, steps: int) -> None:
    """A FIFO queue of exactly `live` cells: allocate at the tail, drop the head.

    Register 0 is the head and register 1 the tail. Each step allocates one
    cell, so each step makes one cell garbage once the queue is full.
    """
    for _ in range(steps):
        if heap.regs[0] is not None and len(heap.reachable()) >= live:
            heap.regs[0] = heap.fields[heap.regs[0]][0]  # drop the head
        x = heap.allocate()
        if heap.regs[1] is None or heap.regs[0] is None:
            heap.regs[0] = heap.regs[1] = x
        else:
            heap.write(heap.regs[1], 0, x)
            heap.regs[1] = x
        live_now = heap.reachable()
        assert len(live_now) <= live
        assert not any(heap.is_free[x] for x in live_now), "a reachable cell is free"


def run_mutator(heap: Heap, live: int, steps: int, rng: random.Random) -> None:
    """A random mutator that keeps at most `live` cells reachable.

    It checks after every step that no reachable cell is on the free list.
    """
    nf = len(heap.fields[0])
    for _ in range(steps):
        held = [r for r in heap.regs if r is not None]
        op = rng.random()
        if op < 0.5 and len(heap.reachable()) < live:
            x = heap.allocate()
            if held:
                heap.write(rng.choice(held), rng.randrange(nf), x)
            else:
                heap.regs[rng.randrange(len(heap.regs))] = x
        elif op < 0.75 and held:
            src = rng.choice(held)
            y = heap.fields[src][rng.randrange(nf)]
            if y is not None:
                heap.regs[rng.randrange(len(heap.regs))] = y
        elif op < 0.95 and held:
            heap.write(rng.choice(held), rng.randrange(nf), rng.choice(held))
        else:
            heap.regs[rng.randrange(len(heap.regs))] = None
        live_now = heap.reachable()
        assert len(live_now) <= live
        assert not any(heap.is_free[x] for x in live_now), "a reachable cell is free"
