# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boomerang-attack/. The authors are listed in prov/008RPY.jsonl.
"""The toy SPN of Heys, "A tutorial on linear and differential cryptanalysis",
Cryptologia 26(3), 2002.

For study only. This is a toy cipher with a 16-bit block. It has no security
at all and exists only to show attacks. For real data use AES from a validated
library (for example the Python package "cryptography").

Layout, as in the tutorial. A block is 16 bits; Heys numbers them 1 to 16 from
the left, so bit 1 is the most significant bit. The four S-boxes of a round
sit on bits 1-4, 5-8, 9-12 and 13-16 (nibble 1 is the leftmost). Rounds 1 to
3 are: XOR round key, S-box layer, bit permutation. Round 4 is: XOR round key
K4, S-box layer, XOR K5. The five 16-bit round keys are independent.
"""

# The S-box of the tutorial (the first row of DES S-box S1): input 0..F -> output.
SBOX = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]
SBOX_INV = [SBOX.index(v) for v in range(16)]


def _perm_bits(x: int) -> int:
    """The tutorial's permutation: bit 4r + c + 1 goes to bit 4c + r + 1 (a transpose)."""
    y = 0
    for i in range(16):  # i = 0 is Heys's bit 1 (the most significant bit)
        if (x >> (15 - i)) & 1:
            row, col = divmod(i, 4)
            y |= 1 << (15 - (4 * col + row))
    return y


PERM = [_perm_bits(x) for x in range(1 << 16)]  # the permutation is its own inverse
SUB = [sum(SBOX[(x >> (4 * k)) & 0xF] << (4 * k) for k in range(4)) for x in range(1 << 16)]
SUB_INV = [sum(SBOX_INV[(x >> (4 * k)) & 0xF] << (4 * k) for k in range(4)) for x in range(1 << 16)]


def nibble(x: int, i: int) -> int:
    """Nibble i of x, with i = 1 for the leftmost nibble (bits 1-4)."""
    return (x >> (4 * (4 - i))) & 0xF


def encrypt(p: int, keys: list[int]) -> int:
    """Encrypt with len(keys) - 1 rounds; the last round has no permutation."""
    x = p
    rounds = len(keys) - 1
    for r in range(rounds - 1):
        x = PERM[SUB[x ^ keys[r]]]
    return SUB[x ^ keys[rounds - 1]] ^ keys[rounds]


def decrypt(c: int, keys: list[int]) -> int:
    rounds = len(keys) - 1
    x = SUB_INV[c ^ keys[rounds]] ^ keys[rounds - 1]
    for r in range(rounds - 2, -1, -1):
        x = SUB_INV[PERM[x]] ^ keys[r]
    return x


def ddt() -> list[list[int]]:
    """Difference distribution table: ddt[a][b] = #{x : S(x) ^ S(x ^ a) = b}."""
    t = [[0] * 16 for _ in range(16)]
    for x in range(16):
        for a in range(16):
            t[a][SBOX[x] ^ SBOX[x ^ a]] += 1
    return t


def parity(x: int) -> int:
    return bin(x).count("1") & 1


def lat() -> list[list[int]]:
    """Linear approximation table: lat[a][b] = #{x : a.x = b.S(x)} - 8."""
    return [[sum(1 for x in range(16) if parity(a & x) == parity(b & SBOX[x])) - 8
             for b in range(16)] for a in range(16)]
