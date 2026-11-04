# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-lock-queue/. The authors are listed in prov/PMYQM4.jsonl.

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


class TwoLockQueue(Generic[T]):
    """The two-lock queue of Michael and Scott (1996).

    A linked list with a sentinel node. Enqueuers take tail_lock and touch
    only tail and the next field of the last node; dequeuers take head_lock
    and touch only head. So one enqueue and one dequeue run in parallel.
    The queue is linearizable and deadlock-free; each operation takes O(1)
    steps plus the wait for its lock.

    The *_steps methods are generators that yield after each step on shared
    memory, for tests that choose the interleaving. enqueue and dequeue run
    the same steps directly and are safe to call from many threads.
    """

    def __init__(self) -> None:
        self.head: _Node[T] = _Node(None)
        self.tail: _Node[T] = self.head
        self.head_lock = threading.Lock()
        self.tail_lock = threading.Lock()

    def enqueue_steps(self, x: T) -> "Steps[None]":
        node: _Node[T] = _Node(x)  # @line L1
        yield from acquire(self.tail_lock)  # @line L2
        self.tail.next = node  # @line L3
        yield None
        self.tail = node  # @line L4
        yield None
        self.tail_lock.release()  # @line L5

    def dequeue_steps(self) -> "Steps[object]":
        yield from acquire(self.head_lock)  # @line L6
        node = self.head  # @line L7
        new_head = node.next  # @line L8
        yield None
        if new_head is None:  # @line L9
            self.head_lock.release()
            return EMPTY
        x = new_head.value  # @line L10
        yield None
        self.head = new_head  # @line L11
        yield None
        new_head.value = None  # the node is the new sentinel; drop the reference
        self.head_lock.release()  # @line L12
        return x  # @line L13

    def enqueue(self, x: T) -> None:
        run(self.enqueue_steps(x))

    def dequeue(self) -> object:
        """Return the oldest item, or EMPTY when the queue has no item."""
        return run(self.dequeue_steps())

    def items(self) -> list[T]:
        """The items from the oldest to the newest, read at a quiet moment."""
        out: list[T] = []
        n = self.head.next
        while n is not None:
            out.append(n.value)  # type: ignore[arg-type]
            n = n.next
        return out

    def check_invariant(self) -> None:
        """At a quiet moment: tail is the last node of the list from head, no lock is held."""
        n = self.head
        while n.next is not None:
            n = n.next
        assert n is self.tail
        assert not self.head_lock.locked() and not self.tail_lock.locked()
