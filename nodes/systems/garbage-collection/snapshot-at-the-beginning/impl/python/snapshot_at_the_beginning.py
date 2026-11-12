# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/snapshot-at-the-beginning/. The authors are listed in prov/4TDCX9.jsonl.

"""Snapshot-at-the-beginning marking with Yuasa's deletion barrier (1990).

Heap model: objects with integer names and k pointer fields each (an object
name or None). The mutator holds r registers, which are the roots. It runs a
fixed program of four operations:

    ("load", i, j, f)   register i <- field f of the object in register j
    ("store", i, f, j)  field f of the object in register i <- register j
    ("clear", i)        register i <- None
    ("alloc", i)        register i <- a new object with all fields None

An operation on a None register does nothing. BEGIN-CYCLE shades the roots in
one short pause. Then the collector runs one MARK-STEP per "C" of a schedule,
and the mutator runs one operation per "M". When the gray stack W is empty,
the next step frees every white object. There is no final rescan.

The barrier is "satb" (shade the old target before an overwrite, and allocate
new objects black), "none", or "dijkstra" (shade the new target, allocate
white, and rescan the roots at the end). The last one is here only to compare
the floating garbage of the two barriers on the same runs.
"""

from __future__ import annotations

import copy
from typing import Iterator

WHITE, GRAY, BLACK = 0, 1, 2
BARRIERS = ("satb", "none", "dijkstra")


class System:
    """A heap, a mutator program and an incremental marker with one barrier."""

    def __init__(self, fields: dict[int, list[int | None]], registers: list[int | None],
                 program: list[tuple], barrier: str = "satb", k: int = 2) -> None:
        if barrier not in BARRIERS:
            raise ValueError(f"unknown barrier {barrier}")
        self.fields = {x: list(fs) for x, fs in fields.items()}
        self.regs = list(registers)
        self.program = list(program)
        self.pc = 0
        self.barrier = barrier
        self.k = k
        self.next_name = max(self.fields, default=-1) + 1
        self.color: dict[int, int] = {}
        self.work: list[int] = []
        self.marking = False
        self.done = False
        self.freed: set[int] = set()
        self.lost: set[int] = set()  # reachable objects that the sweep freed
        self.floating = 0  # unreachable objects that the sweep kept
        self.remark_scans = 0  # objects scanned in a final pause (dijkstra only)
        self.used_freed = False
        self.snapshot = reachable(self.fields, self.regs)
        self.begin_cycle()

    def shade(self, y: int | None) -> None:
        if y is not None and self.color[y] == WHITE:
            self.color[y] = GRAY
            self.work.append(y)

    # The collector.

    def begin_cycle(self) -> None:
        self.color = {x: WHITE for x in self.fields}  # @line L8
        self.work = []
        for r in self.regs:  # @line L9
            self.shade(r)
        self.marking = True  # @line L10

    def scan(self, x: int) -> None:
        for y in self.fields[x]:  # @line L13
            self.shade(y)
        self.color[x] = BLACK  # @line L14

    def mark_step(self) -> None:
        if self.done:
            return
        if self.work:  # @line L11
            self.scan(self.work.pop())  # @line L12
            return
        if self.barrier == "dijkstra":  # the comparison barrier needs a final rescan
            for r in self.regs:
                self.shade(r)
            while self.work:
                self.scan(self.work.pop())
                self.remark_scans += 1
        self.marking = False  # @line L15
        live = reachable(self.fields, self.regs)
        for x in [x for x in self.fields if self.color[x] == WHITE]:  # @line L16
            if x in live:
                self.lost.add(x)
            del self.fields[x]
            self.freed.add(x)
        self.floating = sum(1 for x in self.fields if x not in live)
        self.sweep_pc = self.pc  # how much of the program ran before the sweep
        self.done = True

    # The mutator.

    def write(self, x: int, f: int, y: int | None) -> None:
        """Run the barrier, then store y in field f of x."""
        if self.marking and self.barrier == "satb":  # @line L1
            z = self.fields[x][f]  # @line L2
            if z is not None and self.color[z] == WHITE:  # @line L3
                self.color[z] = GRAY
                self.work.append(z)
        self.fields[x][f] = y  # @line L4
        if self.marking and self.barrier == "dijkstra":
            self.shade(y)

    def allocate(self) -> int:
        x = self.next_name  # @line L5
        self.next_name += 1
        self.fields[x] = [None] * self.k
        if self.marking:
            self.color[x] = BLACK if self.barrier == "satb" else WHITE  # @line L6
        return x  # @line L7

    def freed_use(self, *xs: int | None) -> bool:
        if any(x is not None and x in self.freed for x in xs):
            self.used_freed = True
            return True
        return False

    def mutator_step(self) -> None:
        if self.pc >= len(self.program):
            return
        op = self.program[self.pc]
        self.pc += 1
        if op[0] == "load":
            _, i, j, f = op
            if self.regs[j] is not None and not self.freed_use(self.regs[j]):
                self.regs[i] = self.fields[self.regs[j]][f]
        elif op[0] == "store":
            _, i, f, j = op
            if self.regs[i] is not None and not self.freed_use(self.regs[i], self.regs[j]):
                self.write(self.regs[i], f, self.regs[j])
        elif op[0] == "clear":
            self.regs[op[1]] = None
        elif op[0] == "alloc":
            self.regs[op[1]] = self.allocate()
        else:
            raise ValueError(f"unknown operation {op}")

    def run(self, schedule: str) -> "System":
        for c in schedule:
            if c == "M":
                self.mutator_step()
            elif c == "C":
                self.mark_step()
        while not self.done:
            self.mark_step()
        return self


def reachable(fields: dict[int, list[int | None]], regs: list[int | None]) -> set[int]:
    """Plain graph search from the registers: the reference answer."""
    seen = {r for r in regs if r is not None and r in fields}
    stack = list(seen)
    while stack:
        for y in fields[stack.pop()]:
            if y is not None and y in fields and y not in seen:
                seen.add(y)
                stack.append(y)
    return seen


def all_runs(start: System) -> Iterator[tuple[str, System]]:
    """Every interleaving of the mutator program with the collector steps."""
    stack = [("", start)]
    while stack:
        sched, s = stack.pop()
        if s.done:
            while s.pc < len(s.program):
                s.mutator_step()
            yield sched, s
            continue
        if s.pc < len(s.program):
            t = copy.deepcopy(s)
            t.mutator_step()
            stack.append((sched + "M", t))
        t = copy.deepcopy(s)
        t.mark_step()
        stack.append((sched + "C", t))
