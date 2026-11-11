# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multicollision-attack/. The authors are listed in prov/04D162.jsonl.
"""Joux multicollisions on a toy Merkle-Damgard hash, and the attack on H1(m) || H2(m).

For study only. The code is not constant time. The hash here is a toy with a
16 to 32-bit state, built only to show the attack. Do not use it to protect
real data; use SHA-256 or SHA-3 from the standard library, a FIPS 140
validated module, or libsodium.

Cost: t block collisions give 2^t messages with one digest, for about
t * 2^(n/2) calls of the compression function.
"""

from itertools import product

M64 = (1 << 64) - 1


def toy_compress(h: int, block: int, n: int, salt: int = 0) -> int:
    """A toy compression function {0,1}^n x {0,1}^32 -> {0,1}^n (a 64-bit mixer, top n bits kept)."""
    z = ((h << 32) | (block & 0xFFFFFFFF)) ^ (salt * 0xD6E8FEB86659FD93 & M64)
    z = (z + 0x9E3779B97F4A7C15) & M64
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M64
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M64
    z ^= z >> 31
    return z >> (64 - n)


def chain(h: int, blocks: list[int], n: int, salt: int = 0) -> int:
    for b in blocks:
        h = toy_compress(h, b, n, salt)
    return h


def md_hash(blocks: list[int], n: int, salt: int = 0, iv: int = 1) -> int:
    """Toy Merkle-Damgard hash of a list of 32-bit blocks, with a final length block."""
    return toy_compress(chain(iv, blocks, n, salt), len(blocks), n, salt)


def block_collision(h: int, n: int, salt: int = 0, start: int = 0) -> tuple[int, int, int]:
    """Birthday search for b != b2 with f(h, b) == f(h, b2). Returns (b, b2, new state)."""
    seen: dict[int, int] = {}
    b = start
    while True:
        v = toy_compress(h, b, n, salt)
        if v in seen:
            return seen[v], b, v
        seen[v] = b
        b += 1


def joux_multicollision(t: int, n: int, salt: int = 0, iv: int = 1, offset: int = 0) -> list[tuple[int, int]]:
    """Return t pairs of blocks; each of the 2^t ways to pick one block per pair gives the same digest.

    n is at most 32. offset picks a different region of blocks for the
    searches, to get a different multicollision.
    """
    h = iv  # @line L1
    pairs = []
    for i in range(t):  # @line L2
        start = ((offset * 64 + i) << 18) & 0xFFFFFFFF
        b, b2, h = block_collision(h, n, salt, start=start)  # @line L3
        pairs.append((b, b2))  # @line L4
    return pairs  # @line L5


def messages(pairs: list[tuple[int, int]]) -> list[list[int]]:
    """All 2^t messages of a multicollision."""
    return [list(choice) for choice in product(*pairs)]


def concat_collision(n1: int, n2: int, salt1: int = 1, salt2: int = 2) -> tuple[list[int], list[int], int]:
    """Collide H1(m) || H2(m), with H1 and H2 two toy MD hashes of n1 and n2 bits.

    Build a 2^t multicollision on H1 with t = n2/2 + 2, then look for a
    collision of H2 among its 2^t messages. Returns (m, m2, t).
    """
    t = n2 // 2 + 2
    for offset in range(1 << 10):
        pairs = joux_multicollision(t, n1, salt1, offset=offset)
        seen: dict[int, list[int]] = {}
        for m in messages(pairs):
            d = md_hash(m, n2, salt2)
            if d in seen:
                return seen[d], m, t
            seen[d] = m
        # no H2 collision among the 2^t messages (probability about e^(-8)): build a new multicollision
    raise RuntimeError("no collision found")
