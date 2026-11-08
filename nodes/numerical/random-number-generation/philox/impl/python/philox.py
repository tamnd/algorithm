# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/philox/. The authors are listed in prov/JXHPPT.jsonl.

"""Philox counter-based generators (Salmon, Moraes, Dror and Shaw, 2011), as in Random123."""

# Multipliers and Weyl key increments of Random123.
CONSTANTS = {
    (2, 32): ([0xD256D193], [0x9E3779B9]),
    (4, 32): ([0xD2511F53, 0xCD9E8D57], [0x9E3779B9, 0xBB67AE85]),
    (2, 64): ([0xD2B74407B1CE6E93], [0x9E3779B97F4A7C15]),
    (4, 64): ([0xD2E7470EE14C6C93, 0xCA5A826395121157], [0x9E3779B97F4A7C15, 0xBB67AE8584CAA73B]),
}

M0_32, M1_32 = 0xD2511F53, 0xCD9E8D57
W0_32, W1_32 = 0x9E3779B9, 0xBB67AE85
MASK32 = 0xFFFFFFFF


def philox4x32(ctr: list[int], key: list[int], rounds: int = 10) -> list[int]:
    """Philox4x32-R: four 32-bit counter words and two 32-bit key words to four output words."""
    x0, x1, x2, x3 = (c & MASK32 for c in ctr)
    k0, k1 = (k & MASK32 for k in key)
    for _ in range(rounds):  # @line L1
        p0 = M0_32 * x0  # @line L2
        h0, l0 = p0 >> 32, p0 & MASK32
        p1 = M1_32 * x2  # @line L3
        h1, l1 = p1 >> 32, p1 & MASK32
        x0, x1, x2, x3 = h1 ^ x1 ^ k0, l1, h0 ^ x3 ^ k1, l0  # @line L4
        k0, k1 = (k0 + W0_32) & MASK32, (k1 + W1_32) & MASK32  # @line L5
    return [x0, x1, x2, x3]  # @line L6


def philox(n: int, w: int, ctr: list[int], key: list[int], rounds: int = 10, consts=None) -> list[int]:
    """Philox{n}x{w}-R for n in (2, 4); consts = (multipliers, increments) overrides the table."""
    mult, weyl = consts if consts is not None else CONSTANTS[(n, w)]
    mask = (1 << w) - 1
    x = [c & mask for c in ctr]
    k = [v & mask for v in key]
    if len(x) != n or len(k) != n // 2:
        raise ValueError("need n counter words and n/2 key words")
    for _ in range(rounds):
        if n == 2:
            p = mult[0] * x[0]
            x = [(p >> w) ^ x[1] ^ k[0], p & mask]
        else:
            p0, p1 = mult[0] * x[0], mult[1] * x[2]
            x = [(p1 >> w) ^ x[1] ^ k[0], p1 & mask, (p0 >> w) ^ x[3] ^ k[1], p0 & mask]
        k = [(ki + wi) & mask for ki, wi in zip(k, weyl)]
    return x


def philox_inverse(n: int, w: int, out: list[int], key: list[int], rounds: int = 10, consts=None) -> list[int]:
    """Invert philox for a known key: each multiplier is odd, so it is invertible modulo 2^w."""
    mult, weyl = consts if consts is not None else CONSTANTS[(n, w)]
    mask = (1 << w) - 1
    inv = [pow(m, -1, 1 << w) for m in mult]
    keys = []
    k = [v & mask for v in key]
    for _ in range(rounds):
        keys.append(k)
        k = [(ki + wi) & mask for ki, wi in zip(k, weyl)]
    y = list(out)
    for k in reversed(keys):
        if n == 2:
            x0 = (y[1] * inv[0]) & mask
            hi = (mult[0] * x0) >> w
            y = [x0, y[0] ^ hi ^ k[0]]
        else:
            x0 = (y[3] * inv[0]) & mask
            x2 = (y[1] * inv[1]) & mask
            h0, h1 = (mult[0] * x0) >> w, (mult[1] * x2) >> w
            y = [x0, y[0] ^ h1 ^ k[0], x2, y[2] ^ h0 ^ k[1]]
    return y


class Philox4x32Stream:
    """Counter mode: block i is philox4x32(i as a 128-bit counter, key); words are used in order."""

    def __init__(self, key: list[int], start: int = 0, rounds: int = 10):
        self.key = [k & MASK32 for k in key]
        self.counter = start
        self.rounds = rounds
        self.buf: list[int] = []

    def next32(self) -> int:
        if not self.buf:
            c = self.counter
            ctr = [(c >> (32 * i)) & MASK32 for i in range(4)]
            self.buf = philox4x32(ctr, self.key, self.rounds)[::-1]
            self.counter = (c + 1) % (1 << 128)
        return self.buf.pop()

    def random(self) -> float:
        return self.next32() / 2**32
