# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monotonic-deque/. The authors are listed in prov/S8NDWC.jsonl.

from collections import deque
from typing import Generic, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


class MonotonicDeque(Generic[T]):
    """A queue with a minimum query: push at the back, pop at the front, min.

    The deque holds (position, item) pairs of the strict suffix minima of the
    queue, so the items increase from the front to the back and the front is
    the minimum. push costs O(1) amortized, pop and min cost O(1) worst case.
    pop does not return the item, because not every item is stored.
    """

    def __init__(self) -> None:
        self.d: deque[tuple[int, T]] = deque()  # @line L1
        self.h = 0
        self.t = 0

    def push(self, x: T) -> None:
        """Append x at the back of the queue. Cost O(1) amortized."""
        d = self.d
        while d and not d[-1][1] < x:  # @line L2: back item >= x
            d.pop()  # @line L3
        d.append((self.t, x))  # @line L4
        self.t += 1  # @line L5

    def pop(self) -> None:
        """Remove the oldest item. Precondition: the queue is not empty. Cost O(1)."""
        if self.h >= self.t:
            raise IndexError("pop from an empty queue")
        if self.d[0][0] == self.h:  # @line L6
            self.d.popleft()
        self.h += 1  # @line L7

    def min(self) -> T:
        """Return the least item of the queue (the newest one on ties). Cost O(1)."""
        if self.h >= self.t:
            raise IndexError("min of an empty queue")
        return self.d[0][1]  # @line L8

    def __len__(self) -> int:
        return self.t - self.h

    def check_invariant(self) -> None:
        """Check the parts of the invariant that do not need the popped items."""
        pos = [j for j, _ in self.d]
        items = [x for _, x in self.d]
        assert all(self.h <= j < self.t for j in pos)
        assert all(a < b for a, b in zip(pos, pos[1:]))
        assert all(a < b for a, b in zip(items, items[1:]))
        assert (len(self) == 0) == (len(self.d) == 0)
        if self.d:
            assert pos[-1] == self.t - 1


def sliding_min(a: list[T], k: int) -> list[T]:
    """Return the minimum of each window a[r - k + 1 .. r], for k - 1 <= r < len(a).

    Precondition: k >= 1. Cost Theta(len(a)) time and O(k) extra space.
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    q: MonotonicDeque[T] = MonotonicDeque()
    out: list[T] = []
    for r in range(len(a)):
        q.push(a[r])
        if len(q) > k:
            q.pop()
        if r >= k - 1:
            out.append(q.min())
    return out
