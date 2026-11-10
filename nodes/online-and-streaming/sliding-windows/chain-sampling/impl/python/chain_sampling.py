# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chain-sampling/. The authors are listed in prov/MV8B8B.jsonl.

import random
from collections import deque
from typing import Generic, TypeVar

T = TypeVar("T")


class ChainSampler(Generic[T]):
    """One uniform sample from the last W items of a stream (Babcock, Datar and Motwani).

    chain[0] is the sample. chain[j + 1] is the successor of chain[j]: an
    index chosen uniformly in chain[j].index + 1 .. chain[j].index + W when
    chain[j] joined the chain. `want` is the successor index of the last
    element, which has not arrived yet. All randomness goes through
    rng.randrange, so a test can enumerate every outcome.
    """

    def __init__(self, w: int, rng: random.Random) -> None:
        if w < 1:
            raise ValueError("the window size must be at least 1")
        self.w = w
        self.rng = rng
        self.t = 0
        self.chain: deque[tuple[int, T]] = deque()
        self.want = 0

    def step(self, x: T) -> None:
        """Read the next stream item x."""
        w = self.w
        self.t += 1  # @line L1
        t = self.t
        if t == self.want:  # @line L2
            self.chain.append((t, x))  # @line L3
            self.want = t + 1 + self.rng.randrange(w)
        if self.chain and self.chain[0][0] == t - w:  # @line L4
            self.chain.popleft()  # @line L5
        elif self.rng.randrange(min(t, w)) == 0:  # @line L6
            self.chain = deque([(t, x)])  # @line L7
            self.want = t + 1 + self.rng.randrange(w)

    def sample(self) -> T:
        """The sampled item. Precondition: at least one item was read."""
        return self.chain[0][1]  # @line L8

    def sample_index(self) -> int:
        return self.chain[0][0]

    def check_invariant(self) -> None:
        idx = [i for i, _ in self.chain]
        assert idx and self.t - self.w < idx[0] <= self.t
        assert all(0 < b - a <= self.w for a, b in zip(idx, idx[1:]))
        assert idx[-1] <= self.t < self.want <= idx[-1] + self.w
