# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/luby-rackoff-theorem/. The authors are listed in prov/M3FGR1.jsonl.
"""The Luby-Rackoff construction: a Feistel network with random round functions.

For study only. This code is not constant time, and it uses Python's random
module, which is not a cryptographic generator. Do not use it to protect real
data; use AES from a FIPS 140 validated module, or libsodium.

The round functions and the ideal permutation are sampled lazily: a value is
drawn the first time it is needed and then kept. A round maps (L, R) to
(R, L XOR f(R)), and the output after r rounds is (L_r, R_r), with no swap.
"""

import random


class LazyFunction:
    """A random function from h-bit strings to h-bit strings."""

    def __init__(self, h: int, rng: random.Random) -> None:
        self.h, self.rng, self.table = h, rng, {}

    def __call__(self, x: int) -> int:
        if x not in self.table:
            self.table[x] = self.rng.getrandbits(self.h)
        return self.table[x]


class FeistelOracle:
    """Encryption and decryption under the r-round Feistel network with independent random round functions."""

    def __init__(self, rounds: int, h: int, rng: random.Random) -> None:
        self.h = h
        self.mask = (1 << h) - 1
        self.fs = [LazyFunction(h, rng) for _ in range(rounds)]

    def enc(self, x: int) -> int:
        left, right = x >> self.h, x & self.mask
        for f in self.fs:
            left, right = right, left ^ f(right)
        return (left << self.h) | right

    def dec(self, y: int) -> int:
        left, right = y >> self.h, y & self.mask
        for f in reversed(self.fs):
            left, right = right ^ f(left), left
        return (left << self.h) | right


class RandomPermutationOracle:
    """A random permutation of 2h-bit strings, sampled lazily, with its inverse."""

    def __init__(self, h: int, rng: random.Random) -> None:
        self.n = 2 * h
        self.rng = rng
        self.fwd: dict[int, int] = {}
        self.bwd: dict[int, int] = {}

    def _fresh(self, used: dict[int, int]) -> int:
        while True:
            v = self.rng.getrandbits(self.n)
            if v not in used:
                return v

    def enc(self, x: int) -> int:
        if x not in self.fwd:
            y = self._fresh(self.bwd)
            self.fwd[x], self.bwd[y] = y, x
        return self.fwd[x]

    def dec(self, y: int) -> int:
        if y not in self.bwd:
            x = self._fresh(self.fwd)
            self.fwd[x], self.bwd[y] = y, x
        return self.bwd[y]
