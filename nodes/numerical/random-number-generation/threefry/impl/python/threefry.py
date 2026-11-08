# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/threefry/. The authors are listed in prov/SS4JEM.jsonl.

"""Threefry counter-based generators (Salmon, Moraes, Dror and Shaw, 2011), as in Random123.

The rounds are those of the Threefish block cipher (Skein hash function), with Random123's
rotation constants for the 2-word and 32-bit variants, and without Threefish's tweak.
"""

ROTATIONS = {
    (2, 64): [(16,), (42,), (12,), (31,), (16,), (32,), (24,), (21,)],
    (4, 64): [(14, 16), (52, 57), (23, 40), (5, 37), (25, 33), (46, 12), (58, 22), (32, 32)],
    (2, 32): [(13,), (15,), (26,), (6,), (17,), (29,), (16,), (24,)],
    (4, 32): [(10, 26), (11, 21), (13, 27), (23, 5), (6, 20), (17, 11), (25, 10), (18, 20)],
}
PARITY = {64: 0x1BD11BDAA9FC1A22, 32: 0x1BD11BDA}

MASK64 = (1 << 64) - 1
C240 = PARITY[64]
ROT2X64 = [r for (r,) in ROTATIONS[(2, 64)]]


def rotl(x: int, r: int, w: int) -> int:
    mask = (1 << w) - 1
    return ((x << r) | (x >> (w - r))) & mask


def threefry2x64(ctr: list[int], key: list[int], rounds: int = 20) -> list[int]:
    """Threefry2x64-R: a 128-bit counter and a 128-bit key to 128 output bits."""
    x0, x1 = ctr[0] & MASK64, ctr[1] & MASK64
    k0, k1 = key[0] & MASK64, key[1] & MASK64
    ks = [k0, k1, k0 ^ k1 ^ C240]  # @line L1
    x0, x1 = (x0 + ks[0]) & MASK64, (x1 + ks[1]) & MASK64  # @line L2
    for r in range(rounds):  # @line L3
        x0 = (x0 + x1) & MASK64  # @line L4
        x1 = rotl(x1, ROT2X64[r % 8], 64) ^ x0
        if r % 4 == 3:  # @line L5
            s = (r + 1) // 4  # @line L6
            x0 = (x0 + ks[s % 3]) & MASK64
            x1 = (x1 + ks[(s + 1) % 3] + s) & MASK64
    return [x0, x1]  # @line L7


def _pairs(n: int, r: int):
    """The (a, b) word pairs mixed in round r: b is rotated and added into a."""
    if n == 2:
        return [(0, 1)]
    return [(0, 1), (2, 3)] if r % 2 == 0 else [(0, 3), (2, 1)]


def threefry(n: int, w: int, ctr: list[int], key: list[int], rounds: int = 20, rot=None) -> list[int]:
    """Threefry{n}x{w}-R for n in (2, 4) and w in (32, 64); rot overrides the rotation table."""
    mask = (1 << w) - 1
    rot = rot if rot is not None else ROTATIONS[(n, w)]
    if len(ctr) != n or len(key) != n:
        raise ValueError("need n counter words and n key words")
    ks = [k & mask for k in key]
    parity = PARITY.get(w, 0)
    for k in ks:
        parity ^= k
    ks.append(parity & mask)
    x = [(c + k) & mask for c, k in zip(ctr, ks)]
    for r in range(rounds):
        for (a, b), d in zip(_pairs(n, r), rot[r % 8]):
            x[a] = (x[a] + x[b]) & mask
            x[b] = rotl(x[b], d, w) ^ x[a]
        if r % 4 == 3:
            s = (r + 1) // 4
            for i in range(n):
                x[i] = (x[i] + ks[(s + i) % (n + 1)]) & mask
            x[n - 1] = (x[n - 1] + s) & mask
    return x


def threefry_inverse(n: int, w: int, out: list[int], key: list[int], rounds: int = 20, rot=None) -> list[int]:
    """Undo threefry for a known key, round by round in reverse order."""
    mask = (1 << w) - 1
    rot = rot if rot is not None else ROTATIONS[(n, w)]
    ks = [k & mask for k in key]
    parity = PARITY.get(w, 0)
    for k in ks:
        parity ^= k
    ks.append(parity & mask)
    x = list(out)
    for r in reversed(range(rounds)):
        if r % 4 == 3:
            s = (r + 1) // 4
            x[n - 1] = (x[n - 1] - s) & mask
            for i in range(n):
                x[i] = (x[i] - ks[(s + i) % (n + 1)]) & mask
        for (a, b), d in reversed(list(zip(_pairs(n, r), rot[r % 8]))):
            x[b] = rotl(x[b] ^ x[a], w - d, w)
            x[a] = (x[a] - x[b]) & mask
    return [(v - k) & mask for v, k in zip(x, ks)]


class Threefry2x64Stream:
    """Counter mode: block i is threefry2x64((i mod 2^64, i div 2^64), key)."""

    def __init__(self, key: list[int], start: int = 0, rounds: int = 20):
        self.key = [k & MASK64 for k in key]
        self.counter = start
        self.rounds = rounds
        self.buf: list[int] = []

    def next64(self) -> int:
        if not self.buf:
            c = self.counter
            self.buf = threefry2x64([c & MASK64, c >> 64], self.key, self.rounds)[::-1]
            self.counter = (c + 1) % (1 << 128)
        return self.buf.pop()
