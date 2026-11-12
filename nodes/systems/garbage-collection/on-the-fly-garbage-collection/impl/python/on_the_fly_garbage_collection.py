# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/on-the-fly-garbage-collection/. The authors are listed in prov/R73E8Z.jsonl.

"""On-the-fly mark-sweep with handshakes, in the style of Doligez, Leroy and
Gonthier (1993, 1994).

This is a model, not a runtime. There is one shared heap of H cells with
`fields` pointer fields each, several mutator threads, each with its own
registers (its roots), and one collector. A scheduler runs one step at a time.
No step stops all the threads: the collector posts a status, and each thread
answers it alone, at a safe point between two of its own operations.

The collector posts sync1, then sync2, then async. A thread that answers async
shades its own registers. The collector waits until every thread has answered
each status, then traces the gray cells and sweeps. The write barrier depends on
the status of the thread: in sync1 and sync2 it shades the old and the new value;
in async, while the collector is marking, it shades the old value.

A store takes two steps, as on real hardware: first the thread reads the
collector's marking flag, then it shades and stores. The collector can run
between the two steps. Loads, register clears and allocations are one step.
"""

from __future__ import annotations

import copy
import random

SYNC1, SYNC2, ASYNC = "sync1", "sync2", "async"
IDLE, HANDSHAKE, TRACE, SWEEP = "idle", "handshake", "trace", "sweep"


class Thread:
    def __init__(self, registers: int) -> None:
        self.regs: list[int | None] = [None] * registers
        self.status = ASYNC
        self.seen = 0  # the last post this thread has answered
        self.program: list[tuple] = []
        self.pc = 0
        self.flag: bool | None = None  # the marking flag read by a store in progress


class System:
    def __init__(self, size: int, threads: int, registers: int, fields: int = 2,
                 handshakes: tuple[str, ...] = (SYNC1, SYNC2, ASYNC),
                 barrier: bool = True, trigger: int = 0) -> None:
        self.H, self.F = size, trigger
        self.fields: list[list[int | None]] = [[None] * fields for _ in range(size)]
        self.marked = [False] * size
        self.is_free = [True] * size
        self.free = list(range(size - 1, -1, -1))
        self.threads = [Thread(registers) for _ in range(threads)]
        self.handshakes, self.barrier = handshakes, barrier
        self.phase = IDLE
        self.status = ASYNC  # the status the collector has posted
        self.epoch = 0  # the number of posts so far
        self.hs = 0  # index of the posted handshake
        self.work: list[int] = []
        self.s = 0
        self.cycles = 0

    # Shared helpers.

    def marking(self) -> bool:
        """The flag the barrier reads: true from the post of async to the end of tracing."""
        return (self.phase == HANDSHAKE and self.status == ASYNC) or self.phase == TRACE

    def shade(self, y: int | None) -> None:
        if self.phase in (HANDSHAKE, TRACE) and y is not None and not self.marked[y]:
            self.marked[y] = True
            self.work.append(y)

    # The collector.

    def post(self, status: str) -> None:
        self.status = status  # @line L1
        self.epoch += 1

    def all_answered(self) -> bool:
        return all(t.seen == self.epoch for t in self.threads)  # @line L2

    def collector_can_step(self) -> bool:
        return self.phase != HANDSHAKE or self.all_answered()

    def collector_step(self) -> None:
        if self.phase == IDLE:
            self.phase, self.hs = HANDSHAKE, 0
            self.cycles += 1
            self.post(self.handshakes[0])
        elif self.phase == HANDSHAKE:
            if self.hs + 1 < len(self.handshakes):
                self.hs += 1
                self.post(self.handshakes[self.hs])
            else:
                self.phase = TRACE
        elif self.phase == TRACE:
            if self.work:  # @line L3
                x = self.work.pop()
                for y in self.fields[x]:  # @line L4
                    self.shade(y)
            else:
                self.phase, self.s = SWEEP, 0  # @line L5
        else:
            s = self.s
            if self.marked[s]:  # @line L6
                self.marked[s] = False
            elif not self.is_free[s]:  # @line L7
                self.fields[s] = [None] * len(self.fields[s])
                self.is_free[s] = True
                self.free.append(s)
            self.s += 1  # @line L8
            if self.s == self.H:
                self.phase = IDLE

    # The mutator threads.

    def can_answer(self, m: int) -> bool:
        t = self.threads[m]
        return t.seen != self.epoch and t.flag is None

    def answer(self, m: int) -> None:
        """A safe point of thread m: take the posted status."""
        t = self.threads[m]
        t.status, t.seen = self.status, self.epoch  # @line L9
        if t.status == ASYNC and self.phase == HANDSHAKE:
            for r in t.regs:  # @line L10
                self.shade(r)

    def store_read_flag(self, m: int) -> None:
        self.threads[m].flag = self.marking()  # @line L11

    def store_finish(self, m: int, x: int, f: int, y: int | None) -> None:
        t = self.threads[m]
        if self.barrier and t.status in (SYNC1, SYNC2):  # @line L12
            self.shade(self.fields[x][f])
            self.shade(y)
        elif self.barrier and t.flag:  # @line L13
            self.shade(self.fields[x][f])
        self.fields[x][f] = y  # @line L14
        t.flag = None

    def allocate(self, m: int) -> int | None:
        if not self.free:
            return None  # the thread waits for the sweep
        x = self.free.pop()
        self.is_free[x] = False
        self.fields[x] = [None] * len(self.fields[x])
        t = self.threads[m]
        answered = t.seen == self.epoch
        if (answered and t.status == ASYNC and self.marking()) or (self.phase == SWEEP and x >= self.s):
            self.marked[x] = True  # @line L15
        return x

    def mutator_step(self, m: int) -> None:
        """Run the next step of the program of thread m."""
        t = self.threads[m]
        op = t.program[t.pc]
        if op[0] == "load":  # ("load", i, j, f): r_i <- r_j.f
            _, i, j, f = op
            t.regs[i] = None if t.regs[j] is None else self.fields[t.regs[j]][f]
        elif op[0] == "clear":
            t.regs[op[1]] = None
        elif op[0] == "alloc":
            x = self.allocate(m)
            if x is None:
                return
            t.regs[op[1]] = x
        elif t.flag is None:  # ("store", i, f, j): r_i.f <- r_j, or nil if j is None
            self.store_read_flag(m)
            return
        else:
            _, i, f, j = op
            if t.regs[i] is None:
                t.flag = None
            else:
                self.store_finish(m, t.regs[i], f, None if j is None else t.regs[j])
        t.pc += 1

    def reachable(self) -> set[int]:
        seen = {r for t in self.threads for r in t.regs if r is not None}
        stack = list(seen)
        while stack:
            for y in self.fields[stack.pop()]:
                if y is not None and y not in seen:
                    seen.add(y)
                    stack.append(y)
        return seen

    def lost(self) -> bool:
        return any(self.is_free[x] for x in self.reachable())

    def choices(self) -> list[tuple[str, int]]:
        out = []
        if self.collector_can_step():
            out.append(("c", 0))
        for m, t in enumerate(self.threads):
            if self.can_answer(m):
                out.append(("a", m))
            if t.pc < len(t.program):
                out.append(("m", m))
        return out

    def do(self, choice: tuple[str, int]) -> None:
        kind, m = choice
        if kind == "c":
            self.collector_step()
        elif kind == "a":
            self.answer(m)
        else:
            self.mutator_step(m)


def key(s: System) -> tuple:
    return (tuple(map(tuple, s.fields)), tuple(s.marked), tuple(s.is_free), tuple(s.free),
            tuple((tuple(t.regs), t.status, t.seen, t.pc, t.flag) for t in s.threads),
            s.phase, s.status, s.epoch, s.hs, tuple(s.work), s.s)


def all_runs(system: System) -> tuple[int, int]:
    """Every interleaving of the thread programs with one collector cycle.

    Return (runs, runs that free a reachable cell). The cycle may start at any
    point of the programs. Equal states are counted once, with the number of
    schedules that reach the end from them, so the count is the number of
    schedules.
    """
    start = system.cycles

    def children(s: System) -> list[System]:
        out = []
        for ch in s.choices():
            if ch[0] == "c" and s.phase == IDLE and s.cycles > start:
                continue  # one cycle only
            g = copy.deepcopy(s)
            g.do(ch)
            out.append(g)
        return out

    memo: dict[tuple, tuple[int, int]] = {}
    stack: list[tuple[System, bool]] = [(system, False)]
    while stack:
        s, expanded = stack.pop()
        k = key(s)
        if k in memo:
            continue
        if s.phase == IDLE and s.cycles > start and all(t.pc == len(t.program) for t in s.threads):
            memo[k] = (1, int(s.lost()))
            continue
        kids = children(s)
        if not expanded:
            stack.append((s, True))
            stack.extend((g, False) for g in kids if key(g) not in memo)
        else:
            memo[k] = (sum(memo[key(g)][0] for g in kids), sum(memo[key(g)][1] for g in kids))
    return memo[key(system)]


def random_run(system: System, live: int, ticks: int, rng: random.Random) -> int:
    """Random threads that keep at most `live` cells reachable. Register 0 of
    every thread holds the shared cell 0. Return the tick at which a reachable
    cell was freed, or -1."""
    nf = len(system.fields[0])
    nr = len(system.threads[0].regs)
    for tick in range(ticks):
        if system.phase == IDLE and len(system.free) <= system.F:
            system.collector_step()
        chs = [ch for ch in system.choices() if not (ch[0] == "c" and system.phase == IDLE)]
        idle = [m for m, t in enumerate(system.threads) if t.pc == len(t.program)]
        for m in idle:
            chs.append(("new", m))
        ch = rng.choice(chs)
        if ch[0] == "new":
            t = system.threads[ch[1]]
            held = [i for i in range(nr) if t.regs[i] is not None]
            x = rng.random()
            if x < 0.25 and len(system.reachable()) < live:
                op = ("alloc", rng.randrange(1, nr))
            elif x < 0.55:
                op = ("load", rng.randrange(1, nr), rng.choice(held), rng.randrange(nf))
            elif x < 0.9:
                op = ("store", rng.choice(held), rng.randrange(nf), rng.choice(held + [None]))
            else:
                op = ("clear", rng.randrange(1, nr))
            if op[0] == "load" and system.fields[t.regs[op[2]]][op[3]] is None:
                op = ("clear", op[1])
            t.program, t.pc = [op], 0
        else:
            system.do(ch)
        if system.lost():
            return tick
    return -1
