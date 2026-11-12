# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fixed-window-counter/. The authors are listed in prov/WERYMV.jsonl.

from fractions import Fraction
from math import floor
from typing import Union

Number = Union[int, Fraction]


class FixedWindowCounter:
    """Admit at most `limit` requests in each aligned window [k w, (k + 1) w).

    The state is the index of the current window and the number of requests
    admitted in it. Time is an explicit number; it must not go back.
    """

    def __init__(self, limit: int, window: Number) -> None:
        if limit < 1 or window <= 0:
            raise ValueError("need limit >= 1 and window > 0")
        self.limit = limit
        self.window = window
        self.k: int | None = None
        self.count = 0

    def allow(self, t: Number) -> bool:
        k = floor(Fraction(t) / self.window)  # @line L1
        if self.k is not None and k < self.k:
            raise ValueError("time went back")
        if k != self.k:  # @line L2
            self.k, self.count = k, 0
        if self.count < self.limit:  # @line L3
            self.count += 1  # @line L4
            return True  # @line L5
        return False  # @line L6


def run(times: list[Number], limit: int, window: Number) -> list[bool]:
    """Decisions of a fixed window counter for requests at the given times (in order)."""
    f = FixedWindowCounter(limit, window)
    return [f.allow(t) for t in times]


def max_in_window(times: list[Number], length: Number) -> int:
    """Largest number of the given times in one half-open interval [s, s + length)."""
    ts = sorted(times)
    best, j = 0, 0
    for i in range(len(ts)):
        while j < len(ts) and ts[j] < ts[i] + length:
            j += 1
        best = max(best, j - i)
    return best
