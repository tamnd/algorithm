# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiqueue/. The authors are listed in prov/THZT7C.jsonl.

import heapq
import random
import threading
import time
from collections.abc import Generator
from typing import Any, TypeVar

R = TypeVar("R")

SPIN = "spin"  # what a step generator yields while it waits
EMPTY = "EMPTY"  # what delete-min returns when the whole MultiQueue is empty

Steps = Generator[str | None, None, R]


def run(steps: "Steps[R]") -> R:
    """Run a step generator to its end in the calling thread and return its result."""
    while True:
        try:
            if next(steps) == SPIN:
                time.sleep(0)
        except StopIteration as stop:
            return stop.value


class Heap:
    """One sequential binary heap with a lock and a cached minimum (None if empty)."""

    def __init__(self) -> None:
        self.items: list[Any] = []
        self.top: Any = None
        self.lock = threading.Lock()

    def push(self, x: Any) -> None:
        heapq.heappush(self.items, x)
        self.top = self.items[0]

    def pop(self) -> Any:
        x = heapq.heappop(self.items)
        self.top = self.items[0] if self.items else None
        return x


def smaller(a: Any, b: Any) -> bool:
    """Compare two cached minima, where None (an empty heap) is larger than all."""
    return b is None or (a is not None and a < b)


class MultiQueue:
    """The MultiQueue of Rihani, Sanders and Dementiev.

    c sequential heaps, each with its own lock. Insert puts the item into a
    random heap whose lock is free. Delete-min reads the cached minima of two
    random heaps and removes the minimum of the better one. When both are
    empty it scans all heaps under all locks, so that EMPTY is returned only
    when the whole structure is empty. Every shared access is one step.
    """

    def __init__(self, c: int, seed: int | None = None, rng: Any = None) -> None:
        if c < 1:
            raise ValueError("need at least one heap")
        self.c = c
        self.heaps = [Heap() for _ in range(c)]
        self.rng = rng if rng is not None else random.Random(seed)

    def insert_steps(self, x: Any) -> "Steps[None]":
        while True:  # @line L1
            q = self.heaps[self.rng.randrange(self.c)]
            if q.lock.acquire(blocking=False):
                break
            yield SPIN
        yield None
        q.push(x)  # @line L2
        yield None
        q.lock.release()  # @line L3
        return None

    def delete_min_steps(self) -> "Steps[Any]":
        while True:  # @line L4
            i, j = self.rng.randrange(self.c), self.rng.randrange(self.c)  # @line L5
            ti = self.heaps[i].top  # @line L6
            yield None
            tj = self.heaps[j].top
            yield None
            k = i if smaller(ti, tj) else j
            if ti is None and tj is None:  # @line L7
                return (yield from self._scan_steps())
            q = self.heaps[k]
            if q.lock.acquire(blocking=False):  # @line L8
                yield None
                if q.items:  # @line L9
                    x = q.pop()
                    yield None
                    q.lock.release()
                    return x
                q.lock.release()  # @line L10
            yield SPIN

    def _scan_steps(self) -> "Steps[Any]":
        for q in self.heaps:  # @line L11
            while not q.lock.acquire(blocking=False):
                yield SPIN
            yield None
        best = None  # @line L12
        for q in self.heaps:
            if q.items and (best is None or q.top < best.top):
                best = q
        x = EMPTY if best is None else best.pop()
        yield None
        for q in self.heaps:  # @line L13
            q.lock.release()
        return x

    def insert(self, x: Any) -> None:
        run(self.insert_steps(x))

    def delete_min(self) -> Any:
        return run(self.delete_min_steps())

    def items(self) -> list[Any]:
        return sorted(x for q in self.heaps for x in q.items)

    def check_invariant(self) -> None:
        for q in self.heaps:
            assert not q.lock.locked()
            assert q.top == (min(q.items) if q.items else None)
            for i in range(1, len(q.items)):
                assert q.items[(i - 1) // 2] <= q.items[i]
