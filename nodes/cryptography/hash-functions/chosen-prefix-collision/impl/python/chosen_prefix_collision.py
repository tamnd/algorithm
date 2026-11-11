# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chosen-prefix-collision/. The authors are listed in prov/41PGVW.jsonl.
"""A chosen-prefix collision on a TOY hash with a planted weakness.

For study only. The code is not constant time. The hash is a toy with a 32-bit
state, and its weakness is put there on purpose, so that the two phases of a
real chosen-prefix attack (a birthday phase, then near-collision blocks) show
up in a few lines. It says nothing about the cost of attacks on MD5 or SHA-1.
Do not use the toy to protect real data; use SHA-256 or SHA-3 from the
standard library, a FIPS 140 validated module, or libsodium.

The state is h = (t, u): t is the top 8 bits, u the low 24 bits. A block is 32
bits, b = (c, w) with c the top 8 bits and w the low 24 bits. With
z = mix(u, w):
    u' = z mod 2^24
    p  = (z >> 24) mod 4                 (a window of 2 bits of t)
    t' = t XOR k(z) XOR ((c mod 4) << 2p)
The planted weakness: t never feeds back into u, and the message can flip
the two bits of window p of t directly.
"""

M64 = (1 << 64) - 1
M24 = (1 << 24) - 1


def mix(u: int, w: int) -> int:
    z = ((u << 24) | w) & M64
    z = (z + 0x9E3779B97F4A7C15) & M64
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M64
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M64
    return z ^ (z >> 31)


def toy_compress(h: int, b: int) -> int:
    t, u = h >> 24, h & M24
    c, w = b >> 24, b & M24
    z = mix(u, w)
    p = (z >> 24) & 3
    t2 = t ^ ((z >> 26) & 0xFF) ^ ((c & 3) << (2 * p))
    return (t2 << 24) | (z & M24)


def chain(h: int, blocks: list[int]) -> int:
    for b in blocks:
        h = toy_compress(h, b)
    return h


IV = 0x01234567


def toy_hash(blocks: list[int]) -> int:
    """Merkle-Damgard with a final length block."""
    return toy_compress(chain(IV, blocks), len(blocks) & M24)


def birthday_phase(h1: int, h2: int) -> tuple[int, int, int, int, int]:
    """Find suffix blocks s1, s2 with equal u after them (24-bit birthday).

    Returns (s1, s2, new h1, new h2, number of compression calls).
    """
    left: dict[int, tuple[int, int]] = {}
    right: dict[int, tuple[int, int]] = {}
    i = calls = 0
    while True:
        a = toy_compress(h1, i)
        calls += 1
        if a & M24 in right:
            b, hb = right[a & M24]
            return i, b, a, hb, calls
        left[a & M24] = (i, a)
        bb = toy_compress(h2, i)
        calls += 1
        if bb & M24 in left:
            s1, ha = left[bb & M24]
            return s1, i, ha, bb, calls
        right[bb & M24] = (i, bb)
        i += 1


def near_collision_block(h1: int, h2: int, start: int = 0) -> tuple[int, int, int, int, int]:
    """With u1 == u2 and t1 != t2, find blocks that clear one nonzero 2-bit window of t1 XOR t2.

    Tries w until the window p chosen by the state holds a nonzero part of the
    difference, then sets c1 XOR c2 to that part. Returns (b1, b2, new h1, new h2, calls).
    """
    u = h1 & M24
    delta = (h1 ^ h2) >> 24
    w, calls = start, 0
    while True:
        z = mix(u, w & M24)
        calls += 1
        p = (z >> 24) & 3
        part = (delta >> (2 * p)) & 3
        if part:
            b1 = w & M24
            b2 = (part << 24) | (w & M24)
            return b1, b2, toy_compress(h1, b1), toy_compress(h2, b2), calls
        w += 1


def chosen_prefix_collision(p1: list[int], p2: list[int]) -> tuple[list[int], list[int], int]:
    """Given prefixes of equal block length, return suffixes S1, S2 with
    toy_hash(p1 + S1) == toy_hash(p2 + S2), and the number of compression calls."""
    if len(p1) != len(p2):
        raise ValueError("pad the prefixes to the same number of blocks first")
    h1, h2 = chain(IV, p1), chain(IV, p2)  # @line L1
    s1, s2, h1, h2, calls = birthday_phase(h1, h2)  # @line L2
    suf1, suf2 = [s1], [s2]
    rounds = 0
    while h1 != h2 and rounds < 64:  # @line L3
        b1, b2, h1, h2, c = near_collision_block(h1, h2, start=rounds << 16)  # @line L4
        suf1.append(b1)  # @line L5
        suf2.append(b2)  # @line L5
        calls += c
        rounds += 1
    if h1 != h2:
        raise RuntimeError("difference not cleared")
    return suf1, suf2, calls  # @line L6
