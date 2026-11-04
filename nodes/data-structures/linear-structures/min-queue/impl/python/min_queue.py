# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/min-queue/. The authors are listed in prov/VVXG5M.jsonl.

from collections import deque
from typing import Generic, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


class _MinStack(Generic[T]):
    """A stack of pairs (x, least item at or below x)."""

    def __init__(self) -> None:
        self.s: list[tuple[T, T]] = []

    def __len__(self) -> int:
        return len(self.s)

    def push(self, x: T) -> None:
        m = x if not self.s or x < self.s[-1][1] else self.s[-1][1]
        self.s.append((x, m))

    def pop(self) -> T:
        return self.s.pop()[0]

    def min(self) -> T:
        return self.s[-1][1]


class MinQueue(Generic[T]):
    """A FIFO queue with a min query, built from two stacks with minimum.

    The front of the queue is the top of `out`; the back is the top of
    `inp`. enqueue, dequeue and min cost O(1) amortized: each item is pushed
    and popped at most twice. dequeue costs O(n) in the worst case.
    """

    def __init__(self) -> None:
        self.inp: _MinStack[T] = _MinStack()
        self.out: _MinStack[T] = _MinStack()
        self.moves = 0  # items moved by line L4, for tests

    def __len__(self) -> int:
        return len(self.inp) + len(self.out)

    def enqueue(self, x: T) -> None:
        """Add x at the back. Cost O(1)."""
        self.inp.push(x)  # @line L1

    def dequeue(self) -> T:
        """Remove and return the front item. Precondition: not empty. Cost O(1) amortized."""
        if len(self) == 0:
            raise IndexError("dequeue from an empty queue")
        if len(self.out) == 0:  # @line L2
            while len(self.inp) > 0:  # @line L3
                self.out.push(self.inp.pop())  # @line L4
                self.moves += 1
        return self.out.pop()  # @line L5

    def min(self) -> T:
        """Return the least item. Precondition: not empty. Cost O(1)."""
        if len(self) == 0:
            raise IndexError("min of an empty queue")
        if len(self.inp) == 0:  # @line L6
            return self.out.min()
        if len(self.out) == 0:  # @line L7
            return self.inp.min()
        a, b = self.inp.min(), self.out.min()  # @line L8
        return b if b < a else a

    def to_list(self) -> list[T]:
        """The items from the front to the back."""
        return [x for x, _ in reversed(self.out.s)] + [x for x, _ in self.inp.s]


class MonotonicMinQueue(Generic[T]):
    """The deque variant: keep only the items that can still become the minimum.

    Each entry is (x, t) with t the arrival number. The values in the deque
    increase strictly from the front, so the front is the minimum.
    enqueue costs O(1) amortized; dequeue and min cost O(1).
    """

    def __init__(self) -> None:
        self.d: deque[tuple[T, int]] = deque()
        self.items: deque[T] = deque()  # the full queue, to return the dequeued item
        self.arrived = 0
        self.left = 0

    def enqueue(self, x: T) -> None:
        while self.d and not self.d[-1][0] < x:  # drop back items >= x
            self.d.pop()
        self.d.append((x, self.arrived))
        self.items.append(x)
        self.arrived += 1

    def dequeue(self) -> T:
        if self.d and self.d[0][1] == self.left:
            self.d.popleft()
        self.left += 1
        return self.items.popleft()

    def min(self) -> T:
        return self.d[0][0]
