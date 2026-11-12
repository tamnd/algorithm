# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clock/. The authors are listed in prov/Z35MNC.jsonl.

from collections.abc import Hashable, Iterable


class Clock:
    """The CLOCK (second chance) policy on a cache of k frames.

    The frames form a circle with one reference bit each and a hand that
    points at the oldest load. A request sets the bit of its page, also the
    request that loads the page, as the hardware does. A miss moves the hand
    past pages whose bit is set, clearing each bit, and evicts the first page
    whose bit is clear. load_bit=0 gives the variant that loads a page with a
    clear bit; it is not k-competitive (see the tests).
    """

    def __init__(self, k: int, load_bit: int = 1) -> None:
        if k < 1:
            raise ValueError("the cache size k must be at least 1")
        if load_bit not in (0, 1):
            raise ValueError("load_bit must be 0 or 1")
        self.k = k
        self.load_bit = load_bit
        self.frames: list[Hashable] = []
        self.ref: list[int] = []
        self.where: dict[Hashable, int] = {}
        self.hand = 0
        self.evicted: Hashable | None = None

    def __contains__(self, p: Hashable) -> bool:
        return p in self.where

    def __len__(self) -> int:
        return len(self.frames)

    def contents(self) -> set[Hashable]:
        return set(self.frames)

    def access(self, p: Hashable) -> bool:
        """Serve one request. Return True on a hit, False on a miss."""
        self.evicted = None
        if p in self.where:  # @line L1
            self.ref[self.where[p]] = 1  # @line L2
            return True  # @line L3
        if len(self.frames) < self.k:  # @line L4
            self.where[p] = len(self.frames)  # @line L5
            self.frames.append(p)
            self.ref.append(self.load_bit)
            return False  # @line L6
        while self.ref[self.hand] == 1:  # @line L7
            self.ref[self.hand] = 0  # @line L8
            self.hand = (self.hand + 1) % self.k  # @line L9
        q = self.frames[self.hand]  # @line L10
        del self.where[q]
        self.evicted = q
        self.frames[self.hand] = p  # @line L11
        self.ref[self.hand] = self.load_bit
        self.where[p] = self.hand
        self.hand = (self.hand + 1) % self.k  # @line L12
        return False  # @line L13


def clock_hits(trace: Iterable[Hashable], k: int, load_bit: int = 1) -> list[bool]:
    """Run CLOCK with k frames on the trace. Return one hit flag per request."""
    cache = Clock(k, load_bit)
    return [cache.access(p) for p in trace]
