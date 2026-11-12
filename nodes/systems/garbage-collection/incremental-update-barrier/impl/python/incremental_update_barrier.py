# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-update-barrier/. The authors are listed in prov/PCHTN8.jsonl.

"""Incremental update write barriers on an interleaved mutator and marker.

Heap model: objects with integer names and k pointer fields each (an object
name or None). The mutator holds r registers, which are the roots. It runs a
fixed program of four operations:

    ("load", i, j, f)   register i <- field f of the object in register j
    ("store", i, f, j)  field f of the object in register i <- register j
    ("clear", i)        register i <- None
    ("alloc", i)        register i <- a new object with all fields None

An operation on a None register does nothing. The collector is an incremental
tricolor marker. Its unit of work is one MARK-STEP. When the gray stack W is
empty, the next step is the FINAL-REMARK: the mutator is stopped, the roots
are shaded again, W is drained, and every white object is freed.

The barrier is "dijkstra" (shade the new target, Dijkstra et al. 1978),
"steele" (make a black source gray again, Steele 1975) or "none".
A schedule is a string of "M" (run the next mutator operation) and "C" (run
one collector step). Registers are not covered by the barrier, which is why
the final remark must scan them again.
"""

from __future__ import annotations

import copy
from typing import Iterator

WHITE, GRAY, BLACK = 0, 1, 2
BARRIERS = ("dijkstra", "steele", "none")


class System:
    """A heap, a mutator program and an incremental marker with one barrier."""

    def __init__(self, fields: dict[int, list[int | None]], registers: list[int | None],
                 program: list[tuple], barrier: str = "dijkstra", k: int = 2) -> None:
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
        self.remark_scans = 0  # objects scanned inside the final pause
        self.used_freed = False  # the mutator touched a freed object after the sweep
        self.begin_cycle()

    # The collector.

    def shade(self, y: int | None) -> None:
        if y is not None and self.color[y] == WHITE:
            self.color[y] = GRAY
            self.work.append(y)

    def begin_cycle(self) -> None:
        self.color = {x: WHITE for x in self.fields}  # @line L7
        self.work = []
        for r in self.regs:  # @line L8
            self.shade(r)
        self.marking = True  # @line L9

    def scan(self, x: int) -> None:
        for y in self.fields[x]:  # @line L12
            self.shade(y)
        self.color[x] = BLACK  # @line L13

    def mark_step(self) -> None:
        if self.done:
            return
        if self.work:  # @line L10
            x = self.work.pop()  # @line L11
            self.scan(x)
        else:
            self.final_remark()  # @line L14

    def final_remark(self) -> None:
        for r in self.regs:  # @line L15
            self.shade(r)
        while self.work:  # @line L16
            self.scan(self.work.pop())
            self.remark_scans += 1
        self.marking = False  # @line L17
        live = reachable(self.fields, self.regs)
        for x in [x for x in self.fields if self.color[x] == WHITE]:  # @line L18
            if x in live:
                self.lost.add(x)
            del self.fields[x]
            self.freed.add(x)
        self.floating = sum(1 for x in self.fields if x not in live)
        self.done = True

    # The mutator.

    def write(self, x: int, f: int, y: int | None) -> None:
        """Store y in field f of x, then run the barrier."""
        if self.barrier == "steele":
            self.write_steele(x, f, y)
            return
        self.fields[x][f] = y  # @line L1
        if self.barrier == "dijkstra" and self.marking and y is not None \
                and self.color[y] == WHITE:  # @line L2
            self.color[y] = GRAY  # @line L3
            self.work.append(y)

    def write_steele(self, x: int, f: int, y: int | None) -> None:
        self.fields[x][f] = y  # @line L4
        if self.marking and self.color[x] == BLACK and y is not None \
                and self.color[y] == WHITE:  # @line L5
            self.color[x] = GRAY  # @line L6
            self.work.append(x)

    def freed_use(self, *xs: int | None) -> bool:
        """True if an operand is a freed object; the model then skips the operation."""
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
            if self.freed_use(self.regs[i], self.regs[j]):
                return
            if self.regs[i] is not None:
                self.write(self.regs[i], f, self.regs[j])
        elif op[0] == "clear":
            self.regs[op[1]] = None
        elif op[0] == "alloc":
            x = self.next_name
            self.next_name += 1
            self.fields[x] = [None] * self.k
            if not self.done:
                self.color[x] = WHITE  # new objects are white under incremental update
            self.regs[op[1]] = x
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
