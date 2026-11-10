# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-hyperloglog/. The authors are listed in prov/XQTWXT.jsonl.
"""Sliding HyperLogLog of Chabchoub and Hebrail over a time-based window.

There are m = 2^b registers. Register j keeps a list of pairs (time, rank),
oldest first, with ranks that strictly decrease: the list of future possible
maxima. A query for the last w <= W time units takes, in each register, the
largest rank among the pairs with time >= now - w, and applies the
HyperLogLog estimate to these m values.
"""

import hashlib
import math
from collections import deque
from typing import Deque, Hashable, List, Optional, Tuple

HASH_BITS = 64


def seeded_hash(item: Hashable, seed: int) -> int:
    """A 64-bit hash of str(item), keyed by the seed (BLAKE2b)."""
    key = seed.to_bytes(8, "little", signed=False)
    digest = hashlib.blake2b(str(item).encode("utf-8"), digest_size=8, key=key).digest()
    return int.from_bytes(digest, "big")


def split_hash(h: int, b: int) -> Tuple[int, int]:
    """The register index (first b bits) and the rank rho of the other 64 - b bits."""
    rest_bits = HASH_BITS - b
    j = h >> rest_bits
    rest = h & ((1 << rest_bits) - 1)
    return j, rest_bits - rest.bit_length() + 1


def alpha(m: int) -> float:
    if m == 16:
        return 0.673
    if m == 32:
        return 0.697
    if m == 64:
        return 0.709
    return 0.7213 / (1 + 1.079 / m)


def hll_estimate(registers: List[int]) -> float:
    """The HyperLogLog estimate, with linear counting for small values."""
    m = len(registers)
    raw = alpha(m) * m * m / sum(2.0 ** -r for r in registers)  # @line L7
    zeros = registers.count(0)
    if raw <= 2.5 * m and zeros > 0:  # @line L8
        return m * math.log(m / zeros)
    return raw  # @line L9


class SlidingHyperLogLog:
    """Distinct count over the items with timestamps in [now - w, now], for w <= W."""

    def __init__(self, b: int, window: float, seed: int = 0) -> None:
        if not 4 <= b <= 16 or window <= 0:
            raise ValueError("need 4 <= b <= 16 and window > 0")
        self.b = b
        self.m = 1 << b
        self.window = window
        self.seed = seed
        self.lists: List[Deque[Tuple[float, int]]] = [deque() for _ in range(self.m)]
        self.now: Optional[float] = None

    def update(self, time: float, item: Hashable) -> None:
        """Read item at the given time; times must not decrease (lines L1 to L4)."""
        if self.now is not None and time < self.now:
            raise ValueError("timestamps must not decrease")
        self.now = time
        j, r = split_hash(seeded_hash(item, self.seed), self.b)  # @line L1
        lfpm = self.lists[j]
        while lfpm and lfpm[0][0] < time - self.window:  # @line L2
            lfpm.popleft()
        while lfpm and lfpm[-1][1] <= r:  # @line L3
            lfpm.pop()
        lfpm.append((time, r))  # @line L4

    def registers(self, w: Optional[float] = None, now: Optional[float] = None) -> List[int]:
        """The m register values of HyperLogLog on the items in [now - w, now] (lines L5, L6)."""
        if w is None:
            w = self.window
        if not 0 <= w <= self.window:
            raise ValueError("w must be in [0, W]")
        if now is None:
            now = self.now if self.now is not None else 0
        elif self.now is not None and now < self.now:
            raise ValueError("now must not be before the last item")
        out = []
        for lfpm in self.lists:  # @line L5
            best = 0
            for t, r in lfpm:  # @line L6
                if t >= now - w:
                    best = r
                    break
            out.append(best)
        return out

    def query(self, w: Optional[float] = None, now: Optional[float] = None) -> float:
        """Estimate the number of distinct items in [now - w, now] (lines L5 to L9)."""
        return hll_estimate(self.registers(w, now))

    def pairs(self) -> int:
        """The number of stored pairs."""
        return sum(len(lfpm) for lfpm in self.lists)


def plain_hll_registers(items, b: int, seed: int = 0) -> List[int]:
    """The registers of HyperLogLog run on the given items, with the same hash."""
    regs = [0] * (1 << b)
    for item in items:
        j, r = split_hash(seeded_hash(item, seed), b)
        regs[j] = max(regs[j], r)
    return regs
