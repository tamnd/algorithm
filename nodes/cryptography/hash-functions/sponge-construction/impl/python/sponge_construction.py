# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sponge-construction/. The authors are listed in prov/12K42P.jsonl.
"""The sponge construction over any permutation, with streaming absorb and squeeze, and the
generic inner-collision attack on a toy sponge with a small capacity.

For study only. This code is not constant time and is not for real data. Use
hashlib.sha3_256 or hashlib.shake_128, OpenSSL or XKCP instead.

A permutation is a callable on bytes of length b (the width in bytes). The rate
is r bytes and the capacity is c = b - r bytes. The padding is the multi-rate
pad10*1 on bytes: a first byte that holds domain bits and the first 1 bit,
zeros, and a last 1 bit in 0x80. The suffix 0x1F with Keccak-f[1600] and
r = 168 gives SHAKE128.
"""

import random


class Sponge:
    def __init__(self, perm, width: int, rate: int, suffix: int = 0x01) -> None:
        assert 0 < rate < width
        self.perm, self.width, self.rate, self.suffix = perm, width, rate, suffix
        self.state = bytes(width)  # @line L1
        self.buf = b""
        self.squeezing = False
        self.out = b""

    def _absorb_block(self, block: bytes) -> None:
        mixed = bytes(a ^ b for a, b in zip(self.state[: self.rate], block)) + self.state[self.rate:]  # @line L4
        self.state = self.perm(mixed)  # @line L5

    def absorb(self, data: bytes) -> None:
        """Absorb more input. May be called many times, with pieces of any length."""
        assert not self.squeezing, "the sponge has started to squeeze"
        self.buf += data
        while len(self.buf) >= self.rate:  # @line L3
            self._absorb_block(self.buf[: self.rate])
            self.buf = self.buf[self.rate:]

    def _finish(self) -> None:
        last = bytearray(self.buf) + bytes([self.suffix])  # @line L2
        last += b"\x00" * ((-len(last)) % self.rate)
        last[-1] |= 0x80
        for i in range(0, len(last), self.rate):
            self._absorb_block(bytes(last[i:i + self.rate]))
        self.out = self.state[: self.rate]
        self.squeezing = True

    def squeeze(self, n: int) -> bytes:
        """The next n output bytes. May be called many times."""
        if not self.squeezing:
            self._finish()
        res = b""
        while len(res) < n:  # @line L6
            if not self.out:
                self.state = self.perm(self.state)  # @line L7
                self.out = self.state[: self.rate]
            take = min(n - len(res), len(self.out))
            res += self.out[:take]  # @line L8
            self.out = self.out[take:]
        return res


# Keccak-f[1600] as a permutation of 200 bytes, for the tests against SHAKE128.
_MASK = (1 << 64) - 1
_RC = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
    0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
    0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
    0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
    0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
]
_RHO = [0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39, 41, 45, 15, 21, 8, 18, 2, 61, 56, 14]


def _rotl(x: int, s: int) -> int:
    return ((x << s) | (x >> (64 - s))) & _MASK if s else x


def keccak_f1600(state: bytes) -> bytes:
    a = [int.from_bytes(state[8 * i:8 * i + 8], "little") for i in range(25)]
    for rc in _RC:
        c = [a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20] for x in range(5)]
        d = [c[(x - 1) % 5] ^ _rotl(c[(x + 1) % 5], 1) for x in range(5)]
        a = [a[i] ^ d[i % 5] for i in range(25)]
        b = [0] * 25
        for x in range(5):
            for y in range(5):
                b[y + 5 * ((2 * x + 3 * y) % 5)] = _rotl(a[x + 5 * y], _RHO[x + 5 * y])
        a = [b[i] ^ (~b[(i % 5 + 1) % 5 + i - i % 5] & b[(i % 5 + 2) % 5 + i - i % 5] & _MASK) for i in range(25)]
        a[0] ^= rc
    return b"".join(x.to_bytes(8, "little") for x in a)


def shake128_sponge() -> Sponge:
    return Sponge(keccak_f1600, 200, 168, 0x1F)


def toy_permutation(seed: int = 7):
    """A random permutation of 16-bit states (2 bytes), as a table. Width 2 bytes: r = 1, c = 1."""
    table = list(range(1 << 16))
    random.Random(seed).shuffle(table)

    def perm(state: bytes) -> bytes:
        return table[int.from_bytes(state, "big")].to_bytes(2, "big")

    return perm


def state_after(perm, width: int, rate: int, msg: bytes) -> bytes:
    """The full state after absorbing msg, before padding (msg must be whole blocks)."""
    s = Sponge(perm, width, rate)
    s.absorb(msg)
    assert not s.buf
    return s.state


def inner_collision_attack(perm, width: int = 2, rate: int = 1, seed: int = 3):
    """Find two different messages with the same full state, in about 2^(4c) tries for c capacity bytes.
    Step 1: find two 2-block messages whose capacity parts agree (birthday on c bytes).
    Step 2: append blocks that cancel the difference in the rate part."""
    rng = random.Random(seed)
    seen: dict[bytes, bytes] = {}
    tries = 0
    while True:
        m = bytes(rng.getrandbits(8) for _ in range(2 * rate))
        tries += 1
        st = state_after(perm, width, rate, m)
        inner = st[rate:]
        if inner in seen and seen[inner] != m:
            m0 = seen[inner]
            s0 = state_after(perm, width, rate, m0)
            fix = bytes(a ^ b for a, b in zip(s0[:rate], st[:rate]))
            return m0 + bytes(rate), m + fix, tries
        seen[inner] = m
