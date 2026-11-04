# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/external-queue/. The authors are listed in prov/HQ3Q31.jsonl.

from collections import deque
from typing import Generic, TypeVar

T = TypeVar("T")


class ExternalQueue(Generic[T]):
    """A FIFO queue whose middle part lives on a simulated disk in blocks of B.

    Memory holds two buffers of at most B items: `head`, the front of the
    queue, and `tail`, the back. A full tail is written to disk as one block;
    an empty head is refilled with the oldest block, or with the tail when
    the disk holds no block. Each item is written at most once and read at
    most once, so n operations make at most 2n / B transfers. `reads` and
    `writes` count the block transfers.
    """

    def __init__(self, block_size: int) -> None:
        if block_size < 1:
            raise ValueError("the block size must be at least 1")
        self.B = block_size
        self.head: deque[T] = deque()
        self.tail: list[T] = []
        self.disk: deque[list[T]] = deque()
        self.reads = 0
        self.writes = 0

    def enqueue(self, x: T) -> None:
        """Put x at the back of the queue."""
        self.tail.append(x)  # @line L1
        if len(self.tail) == self.B:  # @line L2
            self.disk.append(self.tail)  # @line L3
            self.writes += 1
            self.tail = []  # @line L4

    def dequeue(self) -> T:
        """Remove and return the front item. Raise IndexError if empty."""
        if not self.head:  # @line L5
            if self.disk:  # @line L6
                self.head = deque(self.disk.popleft())  # @line L7
                self.reads += 1
            else:
                if not self.tail:  # @line L8
                    raise IndexError("dequeue from an empty queue")
                self.head, self.tail = deque(self.tail), []  # @line L9
        return self.head.popleft()  # @line L10

    def front(self) -> T:
        """Return the front item without removing it."""
        x = self.dequeue()
        self.head.appendleft(x)
        return x

    def __len__(self) -> int:
        return len(self.head) + self.B * len(self.disk) + len(self.tail)

    def items(self) -> list[T]:
        """Return the items from the front to the back, without I/O counts."""
        return list(self.head) + [x for blk in self.disk for x in blk] + self.tail

    def check_invariant(self) -> None:
        """Raise AssertionError if a representation rule fails."""
        assert len(self.head) <= self.B
        assert len(self.tail) < self.B
        assert all(len(blk) == self.B for blk in self.disk)
