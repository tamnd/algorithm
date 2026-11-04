# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/disruptor-ring-buffer/. The authors are listed in prov/1JS632.jsonl.

import threading
import time
from collections.abc import Generator
from typing import Generic, TypeVar

T = TypeVar("T")
R = TypeVar("R")

SPIN = "spin"  # what a step generator yields while it waits

Steps = Generator[str | None, None, R]


def run(steps: "Steps[R]") -> R:
    """Run a step generator to its end in the calling thread and return its result."""
    while True:
        try:
            if next(steps) == SPIN:
                time.sleep(0)
        except StopIteration as stop:
            return stop.value


class Sequence:
    """A shared sequence number with atomic get, set and fetch-and-add (a lock simulates the hardware)."""

    def __init__(self, value: int = -1) -> None:
        self._value = value
        self._lock = threading.Lock()

    def get(self) -> int:
        with self._lock:
            return self._value

    def set(self, value: int) -> None:
        with self._lock:
            self._value = value

    def fetch_and_add(self, k: int) -> int:
        with self._lock:
            old = self._value
            self._value += k
            return old


class Consumer:
    """An event processor: its sequence is the last entry it has finished."""

    def __init__(self, name: str, deps: "list[Consumer]") -> None:
        self.name = name
        self.deps = deps
        self.seq = Sequence(-1)


class Disruptor(Generic[T]):
    """A Disruptor ring buffer: one pre-allocated ring, sequence numbers, no locks.

    Every consumer sees every published entry, in order. A consumer that
    depends on others sees an entry only after they have finished it.
    Producers claim sequence numbers, wait while the ring is full (gated by
    the slowest consumer), write the slot, and publish by moving the cursor
    in sequence order. With one producer no read-modify-write is needed.
    """

    def __init__(self, size: int) -> None:
        if size < 1 or size & (size - 1):
            raise ValueError("size must be a power of two")
        self.size = size
        self.mask = size - 1
        self.entries: list[T | None] = [None] * size
        self.claim = Sequence(0)  # the next sequence number to hand out
        self.cursor = Sequence(-1)  # the last published sequence number
        self.consumers: list[Consumer] = []

    def add_consumer(self, name: str, deps: "list[Consumer] | None" = None) -> Consumer:
        c = Consumer(name, list(deps or []))
        self.consumers.append(c)
        return c

    def publish_steps(self, x: T) -> "Steps[int]":
        s = self.claim.fetch_and_add(1)  # @line L1
        yield None
        while True:  # @line L2
            lowest = min((c.seq.get() for c in self.consumers), default=s)
            if s - self.size <= lowest:
                break
            yield SPIN
        yield None
        self.entries[s & self.mask] = x  # @line L3
        yield None
        while self.cursor.get() != s - 1:  # @line L4
            yield SPIN
        self.cursor.set(s)  # @line L5
        yield None
        return s

    def consume_steps(self, c: Consumer) -> "Steps[list[T]]":
        nxt = c.seq.get() + 1  # @line L6
        while True:  # @line L7
            avail = self.cursor.get()
            for d in c.deps:
                avail = min(avail, d.seq.get())
            if avail >= nxt:
                break
            yield SPIN
        yield None
        batch = [self.entries[s & self.mask] for s in range(nxt, avail + 1)]  # @line L8
        yield None
        c.seq.set(avail)  # @line L9
        yield None
        return batch  # type: ignore[return-value] # @line L10

    def publish(self, x: T) -> int:
        return run(self.publish_steps(x))

    def consume(self, c: Consumer) -> list[T]:
        return run(self.consume_steps(c))

    def check_invariant(self) -> None:
        """At a quiet moment: claim = cursor + 1, consumers behind their dependencies, nothing overwritten."""
        cur = self.cursor.get()
        assert self.claim.get() == cur + 1
        for c in self.consumers:
            assert -1 <= c.seq.get() <= cur
            assert cur - c.seq.get() <= self.size
            for d in c.deps:
                assert c.seq.get() <= d.seq.get()
