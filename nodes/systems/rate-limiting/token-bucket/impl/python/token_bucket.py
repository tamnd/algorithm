# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/token-bucket/. The authors are listed in prov/PSJD1J.jsonl.

from fractions import Fraction
from typing import Union

Number = Union[int, Fraction]


class TokenBucket:
    """A token bucket policer with rate r and depth b.

    The bucket is full at time `start`. Time is an explicit number (int or
    Fraction) that the caller passes in; it must not go back.
    Refill is lazy: the tokens are brought up to date at each call.
    """

    def __init__(self, rate: Number, depth: Number, start: Number = 0) -> None:
        if rate <= 0 or depth <= 0:
            raise ValueError("rate and depth must be positive")
        self.rate = rate
        self.depth = depth
        self.tokens: Number = depth
        self.last: Number = start

    def allow(self, t: Number, size: Number = 1) -> bool:
        """Return True and take `size` tokens if the packet conforms at time t."""
        if t < self.last:
            raise ValueError("time went back")
        self.tokens = min(self.depth, self.tokens + self.rate * (t - self.last))  # @line L1
        self.last = t  # @line L2
        if self.tokens >= size:  # @line L3
            self.tokens -= size  # @line L4
            return True  # @line L5
        return False  # @line L6


def police(arrivals: list[tuple[Number, Number]], rate: Number, depth: Number) -> list[bool]:
    """Run a token bucket over (time, size) pairs in time order; return the decisions."""
    if not arrivals:
        return []
    bucket = TokenBucket(rate, depth, arrivals[0][0])
    return [bucket.allow(t, size) for t, size in arrivals]


def conforms(arrivals: list[tuple[Number, Number]], rate: Number, burst: Number) -> bool:
    """Brute-force test of the (r, b) arrival curve.

    For every pair i <= j, the sizes of packets i..j must add up to at most
    r (t_j - t_i) + b. These closed intervals are the tightest ones, so the
    test covers every interval of the time line.
    """
    n = len(arrivals)
    for i in range(n):
        total: Number = 0
        for j in range(i, n):
            total += arrivals[j][1]
            if total > rate * (arrivals[j][0] - arrivals[i][0]) + burst:
                return False
    return True
