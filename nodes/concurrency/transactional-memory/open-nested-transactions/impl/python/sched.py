# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/open-nested-transactions/. The authors are listed in prov/R3QGVQ.jsonl.
"""Deterministic scheduler for simulated processes.

A process is a Python generator. The code between two yields is one atomic
step, and a step makes one access to shared memory (or one short atomic
action, such as a compare-and-swap). A process can yield a guard, a function
with no arguments; it then takes its next step only when the guard returns
true. This models a process that waits for a condition without counting the
spins as steps.

Precondition: the processes share state only through objects that the
caller creates in `make`, and they do not use real threads.
Cost: a run of s steps costs O(s) plus the work of the steps. `explore`
replays each branch from the start, so it costs O(d) per node of the tree
of schedules, where d is the depth of the node.
"""

from __future__ import annotations

import random
from typing import Any, Callable, Iterator

Make = Callable[[], tuple[Any, list]]


class System:
    """A set of generator processes and their state."""

    def __init__(self, procs: list) -> None:
        self.procs = list(procs)
        self.guard: list[Any] = [None] * len(self.procs)
        self.done = [False] * len(self.procs)
        self.result: list[Any] = [None] * len(self.procs)
        self.error: list[Any] = [None] * len(self.procs)
        self.trace: list[int] = []

    def runnable(self) -> list[int]:
        """Return the processes that can take a step now."""
        out = []
        for p in range(len(self.procs)):
            if self.done[p]:
                continue
            g = self.guard[p]
            if g is None or g():
                out.append(p)
        return out

    def step(self, p: int) -> None:
        """Run one step of process p."""
        self.trace.append(p)
        try:
            self.guard[p] = next(self.procs[p])
        except StopIteration as stop:
            self.done[p] = True
            self.result[p] = stop.value
        except Exception as exc:  # the simulated process crashed
            self.done[p] = True
            self.error[p] = exc

    def finished(self) -> bool:
        return all(self.done)


def replay(make: Make, schedule: list[int]) -> tuple[Any, System]:
    """Build a fresh system and run the given steps."""
    ctx, procs = make()
    sys = System(procs)
    for p in schedule:
        sys.step(p)
    return ctx, sys


def explore(make: Make, max_steps: int = 200) -> Iterator[tuple[Any, System]]:
    """Yield (ctx, system) at the end of every schedule.

    A schedule ends when no process can take a step, or after max_steps
    steps (then `system.finished()` may be false).
    """
    stack: list[list[int]] = [[]]
    while stack:
        sched = stack.pop()
        ctx, sys = replay(make, sched)
        ready = sys.runnable()
        while len(ready) == 1 and len(sched) < max_steps:
            sys.step(ready[0])
            sched.append(ready[0])
            ready = sys.runnable()
        if not ready or len(sched) >= max_steps:
            yield ctx, sys
            continue
        for p in reversed(ready):
            stack.append(sched + [p])


def random_run(make: Make, rng: random.Random, max_steps: int = 10_000) -> tuple[Any, System]:
    """Run one schedule that picks a random runnable process at each step."""
    ctx, procs = make()
    sys = System(procs)
    for _ in range(max_steps):
        ready = sys.runnable()
        if not ready:
            break
        sys.step(rng.choice(ready))
    return ctx, sys


def run_schedule(make: Make, schedule: list[int], max_steps: int = 10_000) -> tuple[Any, System]:
    """Run the given steps (skipping a process that cannot run), then finish in round robin."""
    ctx, procs = make()
    sys = System(procs)
    for p in schedule:
        if p in sys.runnable():
            sys.step(p)
    count = 0
    while count < max_steps:
        ready = sys.runnable()
        if not ready:
            break
        for p in ready:
            if p in sys.runnable():
                sys.step(p)
                count += 1
    return ctx, sys
