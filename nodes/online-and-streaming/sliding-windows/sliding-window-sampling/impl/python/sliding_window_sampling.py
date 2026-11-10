# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-sampling/. The authors are listed in prov/Z8FFSE.jsonl.
"""Uniform samples of a sliding window: priority sampling and the two-bucket method."""

import random
from collections import deque
from typing import Any, Optional


class PrioritySampler:
    """One uniform sample of the items with timestamp in (t - T, t].

    Each item gets a random priority; the sample is the item of highest
    priority in the window. The deque keeps the items whose priority is
    higher than that of every later item.
    """

    def __init__(self, length: float, rng: Optional[random.Random] = None) -> None:
        if length <= 0:
            raise ValueError("window length must be positive")
        self.length = length
        self.rng = rng or random.Random()
        self.d: deque = deque()  # (timestamp, item, priority)

    def insert(self, ts: Any, x: Any) -> None:
        p = self.rng.random()  # @line L1
        d = self.d
        while d and d[-1][2] < p:  # @line L2
            d.pop()
        d.append((ts, x, p))  # @line L3

    def sample(self, t: Any) -> Optional[Any]:
        d = self.d
        while d and d[0][0] <= t - self.length:  # @line L4
            d.popleft()
        if not d:  # @line L5
            return None
        return d[0][1]  # @line L6


class BucketSampler:
    """One uniform sample of the last w items with O(1) memory in the worst case.

    The stream is cut into buckets of w items. prev is a uniform sample of
    the last full bucket, cur a reservoir sample of the current one.
    """

    def __init__(self, w: int, rng: Optional[random.Random] = None) -> None:
        if w < 1:
            raise ValueError("window size must be at least 1")
        self.w = w
        self.rng = rng or random.Random()
        self.t = 0
        self.j = 0  # items in the current bucket
        self.cur: Optional[tuple] = None  # (index, item)
        self.prev: Optional[tuple] = None

    def step(self, x: Any) -> None:
        self.t += 1
        self.j += 1
        if self.rng.randrange(self.j) == 0:  # reservoir step with probability 1/j
            self.cur = (self.t, x)
        if self.j == self.w:  # the bucket is full
            self.prev, self.cur, self.j = self.cur, None, 0

    def sample_index(self) -> Optional[int]:
        if self.prev is not None and self.prev[0] > self.t - self.w:
            return self.prev[0]
        return None if self.cur is None else self.cur[0]

    def sample(self) -> Optional[Any]:
        if self.prev is not None and self.prev[0] > self.t - self.w:
            return self.prev[1]
        return None if self.cur is None else self.cur[1]
