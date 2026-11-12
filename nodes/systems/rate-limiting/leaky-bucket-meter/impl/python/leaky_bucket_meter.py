# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/leaky-bucket-meter/. The authors are listed in prov/JQZSX6.jsonl.

from fractions import Fraction
from typing import Union

Number = Union[int, Fraction]


class LeakyBucketMeter:
    """A leaky bucket used as a meter (a policer), with leak rate r and size b.

    The bucket holds a level X in [0, b]. It leaks at rate r while it is not
    empty. A packet of size L conforms if pouring L into the bucket does not
    make it overflow. Time is an explicit number that the caller passes in;
    it must not go back. The leak is computed lazily at each call.
    """

    def __init__(self, rate: Number, size: Number, start: Number = 0) -> None:
        if rate <= 0 or size <= 0:
            raise ValueError("rate and size must be positive")
        self.rate = rate
        self.size = size
        self.level: Number = 0
        self.last: Number = start

    def allow(self, t: Number, length: Number = 1) -> bool:
        """Return True and pour `length` into the bucket if the packet conforms at time t."""
        if t < self.last:
            raise ValueError("time went back")
        self.level = max(0, self.level - self.rate * (t - self.last))  # @line L1
        self.last = t  # @line L2
        if self.level + length <= self.size:  # @line L3
            self.level += length  # @line L4
            return True  # @line L5
        return False  # @line L6


def police(arrivals: list[tuple[Number, Number]], rate: Number, size: Number) -> list[bool]:
    """Run a leaky bucket meter over (time, size) pairs in time order; return the decisions."""
    if not arrivals:
        return []
    meter = LeakyBucketMeter(rate, size, arrivals[0][0])
    return [meter.allow(t, length) for t, length in arrivals]


def conforms(arrivals: list[tuple[Number, Number]], rate: Number, burst: Number) -> bool:
    """Brute-force test of the arrival curve r * tau + b over every pair i <= j."""
    n = len(arrivals)
    for i in range(n):
        total: Number = 0
        for j in range(i, n):
            total += arrivals[j][1]
            if total > rate * (arrivals[j][0] - arrivals[i][0]) + burst:
                return False
    return True
