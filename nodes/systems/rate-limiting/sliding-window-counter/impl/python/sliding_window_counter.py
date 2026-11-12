# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-counter/. The authors are listed in prov/5CM6Z2.jsonl.

from fractions import Fraction
from math import floor
from typing import Union

Number = Union[int, Fraction]


class SlidingWindowCounter:
    """Approximate a sliding window of length w by two fixed-window counters.

    At time t in window k = floor(t / w), with f = (t - k w) / w, the estimate
    of the requests in (t - w, t] is prev * (1 - f) + cur. A request passes if
    the estimate plus one is at most `limit`. Time must not go back.
    """

    def __init__(self, limit: int, window: Number) -> None:
        if limit < 1 or window <= 0:
            raise ValueError("need limit >= 1 and window > 0")
        self.limit = limit
        self.window = window
        self.k: int | None = None
        self.prev = 0
        self.cur = 0

    def estimate(self, t: Number) -> Fraction:
        """Roll the windows forward to time t and return the estimate."""
        k = floor(Fraction(t) / self.window)  # @line L1
        if self.k is not None and k < self.k:
            raise ValueError("time went back")
        if self.k is not None and k == self.k + 1:  # @line L2
            self.prev, self.cur = self.cur, 0
        elif self.k is None or k > self.k + 1:  # @line L3
            self.prev, self.cur = 0, 0
        self.k = k
        f = (Fraction(t) - k * self.window) / self.window  # @line L4
        return self.prev * (1 - f) + self.cur

    def allow(self, t: Number) -> bool:
        if self.estimate(t) + 1 <= self.limit:  # @line L5
            self.cur += 1  # @line L6
            return True  # @line L7
        return False  # @line L8


def run(times: list[Number], limit: int, window: Number) -> list[bool]:
    """Decisions of a sliding window counter for requests at the given times (in order)."""
    s = SlidingWindowCounter(limit, window)
    return [s.allow(t) for t in times]


def max_in_window(times: list[Number], length: Number) -> int:
    """Largest number of the given times in one half-open interval (s - length, s]."""
    ts = sorted(times)
    best, i = 0, 0
    for j in range(len(ts)):
        while ts[i] <= ts[j] - length:
            i += 1
        best = max(best, j - i + 1)
    return best
