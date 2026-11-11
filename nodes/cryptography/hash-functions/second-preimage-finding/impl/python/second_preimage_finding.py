# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/second-preimage-finding/. The authors are listed in prov/033D0B.jsonl.
"""Second preimages on a toy Merkle-Damgard hash: brute force, and the long-message attack
of Kelsey and Schneier (2005) with an expandable message.

For study only. The code is not constant time. The hash is a toy with a 16 to
24-bit state, built only to show the attacks. Do not use it to protect real
data; use SHA-256 or SHA-3 from the standard library, a FIPS 140 validated
module, or libsodium.
"""

M64 = (1 << 64) - 1


def toy_compress(h: int, block: int, n: int) -> int:
    """A toy compression function {0,1}^n x {0,1}^32 -> {0,1}^n (a 64-bit mixer, top n bits kept)."""
    z = ((h << 32) | (block & 0xFFFFFFFF)) & M64
    z = (z + 0x9E3779B97F4A7C15) & M64
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M64
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M64
    z ^= z >> 31
    return z >> (64 - n)


class ToyMD:
    """A Merkle-Damgard hash with an n-bit state, 32-bit blocks and a final length block."""

    def __init__(self, n: int, iv: int = 1) -> None:
        self.n, self.iv, self.calls = n, iv, 0

    def f(self, h: int, b: int) -> int:
        self.calls += 1
        return toy_compress(h, b, self.n)

    def chaining_values(self, blocks: list[int]) -> list[int]:
        """[h_0, h_1, ..., h_L]: the state before and after each block."""
        hs = [self.iv]
        for b in blocks:
            hs.append(self.f(hs[-1], b))
        return hs

    def digest(self, blocks: list[int]) -> int:
        return self.f(self.chaining_values(blocks)[-1], len(blocks))


def brute_force_second_preimage(md: ToyMD, blocks: list[int], max_tries: int = 1 << 26) -> list[int]:
    """Generic attack: try one-block messages until one has the same digest. About 2^n calls."""
    target = md.digest(blocks)
    for b in range(max_tries):
        cand = [b]
        if cand != blocks and md.digest(cand) == target:
            return cand
    raise RuntimeError("not found")


def _collide(md: ToyMD, h_short: int, h_long: int, tag: int) -> tuple[int, int, int]:
    """Find blocks b, b2 with f(h_short, b) == f(h_long, b2), by a two-list birthday search."""
    left: dict[int, int] = {}
    right: dict[int, int] = {}
    i = 0
    while True:
        b = (tag << 24) | i
        u = md.f(h_short, b)
        if u in right:
            return b, right[u], u
        left[u] = b
        v = md.f(h_long, b)
        if v in left:
            return left[v], b, v
        right[v] = b
        i += 1


def expandable_message(md: ToyMD, h0: int, k: int) -> tuple[list[tuple[list[int], list[int]]], int]:
    """A (k, k + 2^k - 1) expandable message from state h0.

    Piece i (i = 0 .. k-1) is a pair (short, long): one block, or 2^i dummy
    blocks and one block, both leading to the same state. Returns the pieces
    and the final state. Cost: about k 2^(n/2 + 1) + 2^k calls of f.
    """
    pieces = []
    h = h0
    for i in range(k):
        dummy = [0xD0000000 | i] * (1 << i)
        q = h
        for d in dummy:
            q = md.f(q, d)
        b, b2, h = _collide(md, h, q, 0x40 + i)
        pieces.append(([b], dummy + [b2]))
    return pieces, h


def expand(pieces: list[tuple[list[int], list[int]]], length: int) -> list[int]:
    """The message of the given length, k <= length <= k + 2^k - 1."""
    k = len(pieces)
    extra = length - k
    if not 0 <= extra < 1 << k:
        raise ValueError("length out of range")
    out: list[int] = []
    for i, (short, long) in enumerate(pieces):
        out += long if extra >> i & 1 else short
    return out


def kelsey_schneier(md: ToyMD, blocks: list[int], k: int) -> list[int]:
    """A second preimage of a long message of L blocks, k + 1 <= L.

    1. Build a (k, k + 2^k - 1) expandable message from the IV.
    2. Find a linking block B from its final state to some h_j, k + 1 <= j <= min(L, k + 2^k).
    3. Return the expandable message of length j - 1, then B, then blocks j + 1 .. L.
    """
    big_l = len(blocks)
    hs = md.chaining_values(blocks)
    pieces, h_exp = expandable_message(md, md.iv, k)
    targets = {hs[j]: j for j in range(k + 1, min(big_l, k + (1 << k)) + 1)}
    b = 0
    while True:
        v = md.f(h_exp, 0xB0000000 | b)
        if v in targets:
            j = targets[v]
            return expand(pieces, j - 1) + [0xB0000000 | b] + blocks[j:]
        b += 1
