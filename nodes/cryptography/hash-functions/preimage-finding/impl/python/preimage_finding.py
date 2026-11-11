# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/preimage-finding/. The authors are listed in prov/HTNXXE.jsonl.
"""Preimages on a toy two-block hash: brute force, and a meet in the middle
attack that works because the toy compression function can be run backwards.

For study only. The code is not constant time. The hash is a toy with an n-bit
state (n from 12 to 32), built to show the attacks. Do not use it to protect
real data; use SHA-256 or SHA-3 from the standard library, a FIPS 140 validated
module, or libsodium.

The toy compression function is g(h, m) = E_m(h), where E is a small invertible
mixer keyed by the 32-bit block m. With no feed-forward, anyone can compute
h = E_m^-1(y). The Davies-Meyer form g(h, m) = E_m(h) XOR h blocks this.
"""

import random

M64 = (1 << 64) - 1


def _splitmix(x: int) -> int:
    z = (x + 0x9E3779B97F4A7C15) & M64
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M64
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M64
    return z ^ (z >> 31)


class ToyCipherHash:
    """H(m1, m2) = g(g(IV, m1), m2) on an n-bit state, with g(h, m) = E_m(h)."""

    ROUNDS = 4

    def __init__(self, n: int, iv: int = 1, feed_forward: bool = False) -> None:
        if not 12 <= n <= 32 or n % 2:
            raise ValueError("n must be even, from 12 to 32")
        self.n, self.mask = n, (1 << n) - 1
        self.iv, self.feed_forward = iv & self.mask, feed_forward
        self.a = 0x9E3779B9 & self.mask | 1
        self.a_inv = pow(self.a, -1, 1 << n)
        self.calls = 0

    def _keys(self, m: int) -> list[int]:
        return [_splitmix((m << 3) | i) & self.mask for i in range(self.ROUNDS)]

    def enc(self, h: int, m: int) -> int:
        self.calls += 1
        for k in self._keys(m):
            h = (h + k) & self.mask
            h ^= h >> (self.n // 2)  # self-inverse on n bits
            h = (h * self.a) & self.mask
        return h

    def dec(self, y: int, m: int) -> int:
        self.calls += 1
        for k in reversed(self._keys(m)):
            y = (y * self.a_inv) & self.mask
            y ^= y >> (self.n // 2)
            y = (y - k) & self.mask
        return y

    def g(self, h: int, m: int) -> int:
        out = self.enc(h, m)
        return out ^ h if self.feed_forward else out

    def digest(self, m1: int, m2: int) -> int:
        return self.g(self.g(self.iv, m1), m2)


def brute_force_preimage(hf: ToyCipherHash, target: int, rng: random.Random) -> tuple[int, int]:
    """Try random two-block messages until one hashes to target. About 2^n tries."""
    while True:
        m1, m2 = rng.getrandbits(32), rng.getrandbits(32)
        if hf.digest(m1, m2) == target:
            return m1, m2


def mitm_preimage(hf: ToyCipherHash, target: int, rng: random.Random) -> tuple[int, int, int]:
    """Meet in the middle: store 2^(n/2) forward states g(IV, m1), then run
    backwards from target with random m2 until a state matches. About 2^(n/2+1)
    calls of E and 2^(n/2) memory. Needs feed_forward = False.
    Returns (m1, m2, number of stored states)."""
    if hf.feed_forward:
        raise ValueError("the backward step needs an invertible g")
    forward: dict[int, int] = {}
    for _ in range(1 << (hf.n // 2)):
        m1 = rng.getrandbits(32)
        forward[hf.g(hf.iv, m1)] = m1
    while True:
        m2 = rng.getrandbits(32)
        mid = hf.dec(target, m2)
        if mid in forward:
            return forward[mid], m2, len(forward)
