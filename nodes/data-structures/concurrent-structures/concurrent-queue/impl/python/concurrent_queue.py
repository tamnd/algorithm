# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/concurrent-queue/. The authors are listed in prov/EBTAW1.jsonl.

import threading
import time
from collections.abc import Generator
from typing import Generic, TypeVar

T = TypeVar("T")
R = TypeVar("R")

EMPTY = object()  # the result of a dequeue on an empty queue
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


class _Node(Generic[T]):
    __slots__ = ("value", "next")

    def __init__(self, value: "T | None") -> None:
        self.value = value
        self.next: "_Node[T] | None" = None


class ConcurrentQueue(Generic[T]):
    """An unbounded FIFO queue that many threads can use, with one lock.

    The list starts with a sentinel node; head is the sentinel and tail is
    the last node. Each operation runs its sequential code while it holds
    the lock, so the queue is linearizable and deadlock-free. Each operation
    takes O(1) steps plus the time it waits for the lock.

    The *_steps methods return generators that yield after each step on
    shared memory, so a test can choose the interleaving. enqueue and
    dequeue run the same steps directly and are safe to call from threads.
    """

    def __init__(self) -> None:
        self.head: _Node[T] = _Node(None)
        self.tail: _Node[T] = self.head
        self.lock = threading.Lock()

    def enqueue_steps(self, x: T) -> "Steps[None]":
        n: _Node[T] = _Node(x)  # @line L1
        yield from acquire(self.lock)  # @line L2
        self.tail.next = n  # @line L3
        yield None
        self.tail = n  # @line L4
        yield None
        self.lock.release()  # @line L5

    def dequeue_steps(self) -> "Steps[object]":
        yield from acquire(self.lock)  # @line L6
        first = self.head.next  # @line L7
        yield None
        if first is None:  # @line L8
            self.lock.release()
            return EMPTY
        self.head = first  # @line L9
        yield None
        x = first.value  # @line L10
        first.value = None  # the node is the new sentinel; drop the reference
        self.lock.release()  # @line L11
        return x  # @line L12

    def enqueue(self, x: T) -> None:
        run(self.enqueue_steps(x))

    def dequeue(self) -> object:
        """Return the oldest item, or EMPTY when the queue has no item."""
        return run(self.dequeue_steps())

    def items(self) -> list[T]:
        """The items from the oldest to the newest. Call it only when no operation runs."""
        out: list[T] = []
        n = self.head.next
        while n is not None:
            out.append(n.value)  # type: ignore[arg-type]
            n = n.next
        return out

    def check_invariant(self) -> None:
        """Check, at a quiet moment, that tail is the last node and the lock is free."""
        n = self.head
        while n.next is not None:
            n = n.next
        assert n is self.tail
        assert not self.lock.locked()
