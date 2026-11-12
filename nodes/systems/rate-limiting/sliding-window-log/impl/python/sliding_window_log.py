# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-log/. The authors are listed in prov/JEWV9G.jsonl.

from collections import deque
from fractions import Fraction
from typing import Union

Number = Union[int, Fraction]


class SlidingWindowLog:
    """Admit a request at time t if fewer than `limit` admitted requests lie in (t - w, t].

    The log holds the times of the admitted requests that are still in the
    window, oldest first. Time is an explicit number; it must not go back.
    """

    def __init__(self, limit: int, window: Number) -> None:
        if limit < 1 or window <= 0:
            raise ValueError("need limit >= 1 and window > 0")
        self.limit = limit
        self.window = window
        self.log: deque = deque()
        self.now: Number | None = None

    def allow(self, t: Number) -> bool:
        if self.now is not None and t < self.now:
            raise ValueError("time went back")
        self.now = t
        while self.log and self.log[0] <= t - self.window:  # @line L1
            self.log.popleft()  # @line L2
        if len(self.log) < self.limit:  # @line L3
            self.log.append(t)  # @line L4
            return True  # @line L5
        return False  # @line L6


class SlidingWindowRing:
    """The same limiter with O(1) worst-case time: a ring of the last `limit` admitted times."""

    def __init__(self, limit: int, window: Number) -> None:
        if limit < 1 or window <= 0:
            raise ValueError("need limit >= 1 and window > 0")
        self.limit = limit
        self.window = window
        self.ring: list = [None] * limit
        self.head = 0  # slot of the oldest of the last `limit` admitted times

    def allow(self, t: Number) -> bool:
        oldest = self.ring[self.head]
        if oldest is not None and oldest > t - self.window:
            return False
        self.ring[self.head] = t
        self.head = (self.head + 1) % self.limit
        return True


def run(times: list[Number], limit: int, window: Number) -> list[bool]:
    """Decisions of a sliding window log for requests at the given times (in order)."""
    s = SlidingWindowLog(limit, window)
    return [s.allow(t) for t in times]


def fits(times: list[Number], limit: int, window: Number) -> bool:
    """Brute force: no `limit + 1` of the sorted times lie within less than `window` of each other."""
    ts = sorted(times)
    return all(ts[i + limit] - ts[i] >= window for i in range(len(ts) - limit))
