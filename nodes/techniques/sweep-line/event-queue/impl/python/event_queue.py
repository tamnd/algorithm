# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/event-queue/. The authors are listed in prov/324RJK.jsonl.

import heapq
from typing import Generic, Hashable, TypeVar

P = TypeVar("P", bound=Hashable)  # an event point, ordered by <, for example (x, y)
A = TypeVar("A")  # a payload, for example a segment that starts at the point


class EventQueue(Generic[P, A]):
    """The event queue of a sweep: a min-priority queue of distinct event points.

    An insert of a point that is already present does not make a second
    event: its payload joins the list of the existing event. A point is
    stored once in a binary heap and once as a key of a hash map from the
    point to its list of payloads. With m distinct points present, insert
    and pop_min do O(log m) comparisons of points, plus O(1) expected time
    for the hash map. The space is O(m + the number of payloads).
    """

    def __init__(self) -> None:
        self._heap: list[P] = []
        self._index: dict[P, list[A]] = {}

    def insert(self, p: P, payload: A | None = None) -> None:
        """Add event point p. If payload is not None, append it to the payloads of p."""
        if p in self._index:  # @line L1
            if payload is not None:
                self._index[p].append(payload)  # @line L2
        else:
            self._index[p] = [] if payload is None else [payload]  # @line L3
            heapq.heappush(self._heap, p)  # @line L4

    def pop_min(self) -> tuple[P, list[A]]:
        """Remove the smallest event point and return it with all its payloads.

        Precondition: the queue is not empty.
        """
        if not self._heap:
            raise IndexError("pop_min from an empty event queue")
        p = heapq.heappop(self._heap)  # @line L5
        payloads = self._index.pop(p)  # @line L6
        return p, payloads  # @line L7

    def contains(self, p: P) -> bool:
        """Return True if event point p is in the queue."""
        return p in self._index  # @line L8

    def is_empty(self) -> bool:
        """Return True if the queue holds no event point."""
        return not self._heap  # @line L9

    def __len__(self) -> int:
        """Return the number of distinct event points in the queue."""
        return len(self._heap)

    def check_invariant(self) -> None:
        """Check that the heap and the map hold the same distinct points and that the heap is ordered."""
        h = self._heap
        assert len(h) == len(self._index), "heap and index differ in size"
        assert set(h) == set(self._index), "heap and index hold different points"
        for i in range(1, len(h)):
            assert not (h[i] < h[(i - 1) // 2]), "heap order is broken"
