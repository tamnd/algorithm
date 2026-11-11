# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slide-attack/. The authors are listed in prov/KDTCXR.jsonl.
"""The known-plaintext slide attack of Biryukov and Wagner (1999) on a toy
cipher with identical rounds.

For study only: a teaching attack on a toy cipher. Nothing here is constant
time or fit for real use; for real data use AES from a validated library (for
example the Python package "cryptography").

The toy cipher, defined in this module only, has a 16-bit block and a 16-bit
key k. Every round is the same keyed map

    F_k(x) = PERM(SUB(x ^ k)),

where SUB applies the 4-bit S-box of Heys's tutorial to each nibble and PERM
is the bit transpose of the same tutorial. Encryption is F_k applied r times,
for any r. A slid pair is a pair of plaintexts (P, P') with P' = F_k(P). Then
C' = F_k(C) too, because E_k(P') = F_k^r(F_k(P)) = F_k(F_k^r(P)) = F_k(C).
With m known pairs (P, C) there are m^2 ordered pairs, and each is slid with
probability 2^-16, so m near 2^8 gives a slid pair. The cost does not depend
on r.
"""

import random
from collections.abc import Callable

SBOX = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]
SBOX_INV = [SBOX.index(v) for v in range(16)]


def _perm_bits(x: int) -> int:
    y = 0
    for i in range(16):
        if (x >> (15 - i)) & 1:
            row, col = divmod(i, 4)
            y |= 1 << (15 - (4 * col + row))
    return y


SUB = [sum(SBOX[(x >> (4 * k)) & 0xF] << (4 * k) for k in range(4)) for x in range(1 << 16)]
SUB_INV = [sum(SBOX_INV[(x >> (4 * k)) & 0xF] << (4 * k) for k in range(4)) for x in range(1 << 16)]
PERM = [_perm_bits(x) for x in range(1 << 16)]  # an involution


def round_function(x: int, k: int) -> int:
    return PERM[SUB[x ^ k]]


def encrypt(p: int, k: int, rounds: int) -> int:
    for _ in range(rounds):
        p = PERM[SUB[p ^ k]]
    return p


def key_from_pair(p: int, p_next: int) -> int:
    """The only k with F_k(p) = p_next."""
    return p ^ SUB_INV[PERM[p_next]]


def slide_candidates(pairs: list[tuple[int, int]]) -> set[int]:
    """Keys suggested by ordered pairs that pass the ciphertext check."""
    found = set()  # @line L1
    for p, c in pairs:  # @line L2
        for q, d in pairs:  # @line L3
            # Assume q = F_k(p); then d = F_k(c) must hold.
            k = p ^ SUB_INV[PERM[q]]  # @line L4
            if PERM[SUB[c ^ k]] == d:  # @line L5
                found.add(k)
    return found


def recover_key(known: list[tuple[int, int]], check: Callable[[int], bool]) -> int | None:
    """Run the slide on the known pairs, then confirm each candidate key."""
    for k in sorted(slide_candidates(known)):  # @line L6
        if check(k):  # @line L7
            return k
    return None  # @line L8


def known_pairs(k: int, rounds: int, m: int, rng: random.Random) -> list[tuple[int, int]]:
    return [(p, encrypt(p, k, rounds)) for p in rng.sample(range(1 << 16), m)]
