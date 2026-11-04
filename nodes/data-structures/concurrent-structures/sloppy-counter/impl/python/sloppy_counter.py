# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sloppy-counter/. The authors are listed in prov/Y5EVC6.jsonl.

import threading
import time
from collections.abc import Generator
from typing import TypeVar

R = TypeVar("R")

SPIN = "spin"  # what a step generator yields while it waits for a lock

Steps = Generator[str | None, None, R]


def acquire(lock: threading.Lock) -> Generator[str | None, None, None]:
    """Take the lock, one try per step; yield SPIN while another holder has it."""
    while not lock.acquire(blocking=False):
        yield SPIN


def run(steps: "Steps[R]") -> R:
    """Run a step generator to its end in the calling thread and return its result."""
    while True:
        try:
            if next(steps) == SPIN:
                time.sleep(0)
        except StopIteration as stop:
            return stop.value


class SloppyCounter:
    """A counter with one local count per core and a global count.

    An increment adds 1 to the local count of its core under the lock of
    that core. When the local count reaches the threshold S, the increment
    moves it to the global count under the global lock. approximate() reads
    only the global count: it never exceeds the true count and is at most
    cores * (S - 1) below it. exact() takes every lock, local locks in index
    order and then the global lock, and returns the true count.

    The *_steps methods are generators that yield after each step on shared
    memory, for tests that choose the interleaving. The plain methods run the
    same steps and are safe to call from many threads.
    """

    def __init__(self, cores: int, threshold: int) -> None:
        if cores < 1 or threshold < 1:
            raise ValueError("cores and threshold must be at least 1")
        self.cores = cores
        self.threshold = threshold
        self.local = [0] * cores
        self.locks = [threading.Lock() for _ in range(cores)]
        self.global_count = 0
        self.global_lock = threading.Lock()

    def increment_steps(self, core: int) -> "Steps[None]":
        i = core % self.cores
        yield from acquire(self.locks[i])  # @line L1
        self.local[i] += 1  # @line L2
        yield None
        if self.local[i] >= self.threshold:  # @line L3
            yield from acquire(self.global_lock)  # @line L4
            self.global_count += self.local[i]  # @line L5
            yield None
            self.global_lock.release()  # @line L6
            self.local[i] = 0  # @line L7
            yield None
        self.locks[i].release()  # @line L8

    def approximate_steps(self) -> "Steps[int]":
        yield from acquire(self.global_lock)  # @line L9
        v = self.global_count  # @line L10
        yield None
        self.global_lock.release()  # @line L11
        return v  # @line L12

    def exact_steps(self) -> "Steps[int]":
        for lock in self.locks:  # @line L13
            yield from acquire(lock)
        yield from acquire(self.global_lock)  # @line L14
        v = self.global_count + sum(self.local)  # @line L15
        yield None
        self.global_lock.release()  # @line L16
        for lock in reversed(self.locks):
            lock.release()
        return v  # @line L17

    def increment(self, core: int) -> None:
        run(self.increment_steps(core))

    def approximate(self) -> int:
        """A value v with true - cores * (threshold - 1) <= v <= true."""
        return run(self.approximate_steps())

    def exact(self) -> int:
        return run(self.exact_steps())

    def max_error(self) -> int:
        return self.cores * (self.threshold - 1)

    def check_invariant(self) -> None:
        """At a quiet moment: no lock is held and each local count is below the threshold."""
        assert not self.global_lock.locked()
        assert not any(lock.locked() for lock in self.locks)
        assert all(0 <= c < self.threshold for c in self.local)
