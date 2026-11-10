# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-heavy-hitters/. The authors are listed in prov/130NZR.jsonl.
"""Frequencies over a count-based window with error at most eps * W: Misra-Gries per block."""

import math
from collections import deque
from typing import Any, Dict, List


def mg_update(counters: Dict[Any, int], x: Any, k: int) -> None:
    """Misra-Gries with k counters: every count is under the true count by at most n / (k + 1)."""
    if x in counters:
        counters[x] += 1
    elif len(counters) < k:
        counters[x] = 1
    else:
        for y in list(counters):
            counters[y] -= 1
            if counters[y] == 0:
                del counters[y]


class WindowFrequencies:
    """Underestimates f(x) in the last w items by less than eps * w."""

    def __init__(self, w: int, eps: float) -> None:
        if w < 1 or not 0 < eps <= 1:
            raise ValueError("need w >= 1 and 0 < eps <= 1")
        self.w = w
        self.b = max(1, math.floor(eps * w / 2))  # block length
        self.k = math.ceil(2 / eps)  # counters per block
        self.t = 0
        self.cur: Dict[Any, int] = {}
        self.blocks: deque = deque()  # (first index, summary) of finished blocks

    def step(self, x: Any) -> None:
        self.t += 1  # @line L1
        mg_update(self.cur, x, self.k)
        if self.t % self.b == 0:  # @line L2
            self.blocks.append((self.t - self.b + 1, self.cur))  # @line L3
            self.cur = {}
        while self.blocks and self.blocks[0][0] <= self.t - self.w:  # @line L4
            self.blocks.popleft()

    def estimate(self, x: Any) -> int:
        return self.cur.get(x, 0) + sum(m.get(x, 0) for _, m in self.blocks)  # @line L5

    def heavy_hitters(self, phi: float, eps: float) -> List[Any]:
        """Items with estimate at least (phi - eps) * w."""
        keys = set(self.cur)
        for _, m in self.blocks:
            keys.update(m)
        return sorted((x for x in keys if self.estimate(x) >= (phi - eps) * self.w), key=repr)

    def words(self) -> int:
        return len(self.cur) + sum(len(m) for _, m in self.blocks)
