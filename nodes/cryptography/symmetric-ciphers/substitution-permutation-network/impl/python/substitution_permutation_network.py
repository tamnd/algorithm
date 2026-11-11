# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/substitution-permutation-network/. The authors are listed in prov/H2EQ3A.jsonl.
"""The toy substitution-permutation network of the Heys tutorial (Cryptologia 2002).

For study only. This code is not constant time, and the toy cipher has a
16-bit block: it is not secure. Do not use it to protect real data; use AES
from a FIPS 140 validated module, or libsodium.

The block has 16 bits, numbered 1 to 16 from the most significant bit. There
are r rounds and r + 1 independent 16-bit round keys, as in the tutorial,
which uses no key schedule. Rounds 1 to r - 1 are key mixing, substitution
and permutation. Round r has no permutation, and a last key follows it.
Cost: r layers of 4 S-box lookups, r - 1 bit permutations and r + 1 XORs.
"""

SBOX = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]
INV_SBOX = [SBOX.index(v) for v in range(16)]
# Output bit PERM[i] receives input bit i (bits numbered 1 to 16). It is the transpose of a 4 x 4 bit matrix.
PERM = {i: 4 * ((i - 1) % 4) + (i - 1) // 4 + 1 for i in range(1, 17)}


def substitute(x: int, box: list[int]) -> int:
    """Apply the 4-bit S-box to each of the 4 nibbles."""
    return sum(box[(x >> s) & 0xF] << s for s in (0, 4, 8, 12))


def permute(x: int) -> int:
    """Move input bit i to output bit PERM[i]."""
    out = 0
    for i in range(1, 17):
        if (x >> (16 - i)) & 1:
            out |= 1 << (16 - PERM[i])
    return out


def encrypt(keys: list[int], x: int) -> int:
    """Encrypt a 16-bit block with r + 1 round keys, so with r = len(keys) - 1 rounds."""
    r = len(keys) - 1
    w = x  # @line L1
    for i in range(r - 1):  # @line L2
        u = w ^ keys[i]  # @line L3
        v = substitute(u, SBOX)  # @line L4
        w = permute(v)  # @line L5
    u = w ^ keys[r - 1]  # @line L6
    v = substitute(u, SBOX)  # @line L7
    return v ^ keys[r]  # @line L8


def decrypt(keys: list[int], y: int) -> int:
    """The inverse: the inverse S-box, the inverse permutation and the keys in reverse order."""
    r = len(keys) - 1
    w = substitute(y ^ keys[r], INV_SBOX) ^ keys[r - 1]
    for i in range(r - 2, -1, -1):
        w = substitute(permute(w), INV_SBOX) ^ keys[i]  # this PERM is its own inverse
    return w
