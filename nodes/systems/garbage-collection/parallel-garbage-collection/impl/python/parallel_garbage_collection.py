# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-garbage-collection/. The authors are listed in prov/02511Y.jsonl.

"""Parallel marking with work stealing and termination detection, in the style
of Endo, Taura and Yonezawa (1997) and Flood, Detlefs, Shavit and Zhang (2001).

This is a deterministic simulation of P collector threads, not a threaded
program. The heap is a list of cells, each a list of addresses or None. Time
runs in rounds; in each round every worker that has not terminated takes one
step, in an order drawn from a random.Random(seed) passed in. A step is atomic.

Each worker owns a deque. It pushes and pops gray cells at the bottom of its
own deque; an idle worker steals one cell from the top of the deque of a victim.
A cell is pushed only by the worker whose test-and-set of its mark bit succeeds,
so each reachable cell is scanned exactly once. A worker with nothing to do
offers to terminate by decrementing a shared count of active workers; it comes
back if it sees work in some deque, and all workers stop when the count is 0.
"""

from __future__ import annotations

import random
from collections import deque


class Marker:
    def __init__(self, heap: list[list[int | None]], roots: list[int], workers: int,
                 rng: random.Random, steal: bool = True) -> None:
        self.heap, self.P, self.rng, self.steal = heap, workers, rng, steal
        self.mark = [False] * len(heap)
        self.deques: list[deque[int]] = [deque() for _ in range(workers)]
        self.active = workers  # the shared count of workers that have not offered to stop
        self.idle = [False] * workers
        self.done = [False] * workers
        self.scanned = [0] * workers
        self.steals = 0
        self.rounds = 0
        for i, r in enumerate(roots):
            if self.test_and_set(r):
                self.deques[i % workers].append(r)

    def test_and_set(self, y: int) -> bool:
        """Atomic in the model: set the mark and report whether this call set it."""
        if self.mark[y]:
            return False
        self.mark[y] = True
        return True

    def step(self, i: int) -> None:
        d = self.deques[i]
        if self.idle[i]:
            if self.active == 0:  # @line L11
                self.done[i] = True
            elif any(self.deques):  # @line L10
                self.idle[i] = False
                self.active += 1
            return
        if d:  # @line L2
            x = d.pop()  # bottom
            self.scanned[i] += 1
            for y in self.heap[x]:  # @line L3
                if y is not None and self.test_and_set(y):  # @line L4
                    d.append(y)
            return
        victims = [v for v in range(self.P) if v != i and self.deques[v]]  # @line L5
        if self.steal and victims:  # @line L6
            v = self.rng.choice(victims)
            d.append(self.deques[v].popleft())  # @line L7
            self.steals += 1
            return
        self.idle[i] = True  # @line L8
        self.active -= 1  # @line L9

    def run(self, max_rounds: int = 10**6) -> list[bool]:
        while not all(self.done):  # @line L1
            self.rounds += 1
            if self.rounds > max_rounds:
                raise RuntimeError("no termination")
            order = [i for i in range(self.P) if not self.done[i]]
            self.rng.shuffle(order)
            for i in order:
                self.step(i)
            # Safety of termination: if some worker has stopped, all work is gone.
            if any(self.done):
                assert not any(self.deques) and self.active == 0
        return self.mark


def reachable(heap: list[list[int | None]], roots: list[int]) -> set[int]:
    seen = set(roots)
    stack = list(roots)
    while stack:
        for y in heap[stack.pop()]:
            if y is not None and y not in seen:
                seen.add(y)
                stack.append(y)
    return seen


def random_heap(n: int, fields: int, rng: random.Random, nil: float = 0.3) -> list[list[int | None]]:
    return [[None if rng.random() < nil else rng.randrange(n) for _ in range(fields)] for _ in range(n)]


def binary_tree(depth: int) -> list[list[int | None]]:
    n = 2 ** depth - 1
    return [[2 * i + 1 if 2 * i + 1 < n else None, 2 * i + 2 if 2 * i + 2 < n else None] for i in range(n)]


def linked_list(n: int) -> list[list[int | None]]:
    return [[i + 1 if i + 1 < n else None] for i in range(n)]
