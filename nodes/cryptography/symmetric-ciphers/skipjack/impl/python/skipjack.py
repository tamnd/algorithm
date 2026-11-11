# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/skipjack/. The authors are listed in prov/F2V5M9.jsonl.
"""SKIPJACK (NSA, declassified 1998): encryption and decryption.

For study only. This code is not constant time: the F-table is indexed by
secret bytes, and Python itself leaks timing. Do not use it to protect real
data; an 80-bit key and a 64-bit block are too small today. Use AES from a
validated library (for example the Python package "cryptography") instead.

The names follow "SKIPJACK and KEA Algorithm Specifications", Version 2.0,
29 May 1998. A block is four 16-bit words w1..w4, and the 80-bit
cryptovariable is ten bytes cv0..cv9. Cost: 32 steps, each with one
G-permutation (4 F-table lookups) and one or two XORs.
"""

# Specification Section II.B.7, the F-table, row by row (high nibble = row).
F = bytes.fromhex(
    "a3 d7 09 83 f8 48 f6 f4 b3 21 15 78 99 b1 af f9"
    "e7 2d 4d 8a ce 4c ca 2e 52 95 d9 1e 4e 38 44 28"
    "0a df 02 a0 17 f1 60 68 12 b7 7a c3 e9 fa 3d 53"
    "96 84 6b ba f2 63 9a 19 7c ae e5 f5 f7 16 6a a2"
    "39 b6 7b 0f c1 93 81 1b ee b4 1a ea d0 91 2f b8"
    "55 b9 da 85 3f 41 bf e0 5a 58 80 5f 66 0b d8 90"
    "35 d5 c0 a7 33 06 65 69 45 00 94 56 6d 98 9b 76"
    "97 fc b2 c2 b0 fe db 20 e1 eb d6 e4 dd 47 4a 1d"
    "42 ed 9e 6e 49 3c cd 43 27 d2 07 d4 de c7 67 18"
    "89 cb 30 1f 8d c6 8f aa c8 74 dc c9 5d 5c 31 a4"
    "70 88 61 2c 9f 0d 2b 87 50 82 54 64 26 7d 03 40"
    "34 4b 1c 73 d1 c4 fd 3b cc fb 7f ab e6 3e 5b a5"
    "ad 04 23 9c 14 51 22 f0 29 79 71 7e ff 8c 0e e2"
    "0c ef bc 72 75 6f 37 a1 ec d3 8e 62 8b 86 10 e8"
    "08 77 11 be 92 4f 24 c5 32 36 9d cf f3 a6 bb ac"
    "5e 6c a9 13 57 25 b5 e3 bd a8 3a 01 05 59 2a 46"
)

# Section II.B.4: 8 steps of rule A, 8 of rule B, 8 of A, 8 of B.
RULES = "A" * 8 + "B" * 8 + "A" * 8 + "B" * 8


def g(word: int, k: int, cv: bytes) -> int:
    """The G-permutation for step k + 1: a 4-round Feistel network on two bytes."""
    g1, g2 = word >> 8, word & 0xFF
    g3 = F[g2 ^ cv[(4 * k) % 10]] ^ g1  # @line L7
    g4 = F[g3 ^ cv[(4 * k + 1) % 10]] ^ g2  # @line L8
    g5 = F[g4 ^ cv[(4 * k + 2) % 10]] ^ g3  # @line L9
    g6 = F[g5 ^ cv[(4 * k + 3) % 10]] ^ g4  # @line L10
    return (g5 << 8) | g6  # @line L11


def g_inv(word: int, k: int, cv: bytes) -> int:
    g5, g6 = word >> 8, word & 0xFF
    g4 = F[g5 ^ cv[(4 * k + 3) % 10]] ^ g6
    g3 = F[g4 ^ cv[(4 * k + 2) % 10]] ^ g5
    g2 = F[g3 ^ cv[(4 * k + 1) % 10]] ^ g4
    g1 = F[g2 ^ cv[(4 * k) % 10]] ^ g3
    return (g1 << 8) | g2


def encrypt_steps(key: bytes, block: bytes) -> list[tuple[int, int, int, int]]:
    """All 33 states (w1, w2, w3, w4): the input and the state after each step."""
    if len(key) != 10 or len(block) != 8:
        raise ValueError("the key must have 10 bytes and the block 8 bytes")
    w = tuple(int.from_bytes(block[2 * i:2 * i + 2], "big") for i in range(4))
    states = [w]
    for k, rule in enumerate(RULES):  # @line L1
        w1, w2, w3, w4 = w
        counter = k + 1
        if rule == "A":  # @line L2
            gw = g(w1, k, key)
            w = (gw ^ w4 ^ counter, gw, w2, w3)  # @line L3
        else:  # @line L4
            w = (w4, g(w1, k, key), w1 ^ w2 ^ counter, w3)  # @line L5
        states.append(w)
    return states  # @line L6


def _pack(w: tuple[int, int, int, int]) -> bytes:
    return b"".join(x.to_bytes(2, "big") for x in w)


def encrypt_block(key: bytes, block: bytes) -> bytes:
    return _pack(encrypt_steps(key, block)[-1])


def decrypt_block(key: bytes, block: bytes) -> bytes:
    if len(key) != 10 or len(block) != 8:
        raise ValueError("the key must have 10 bytes and the block 8 bytes")
    w1, w2, w3, w4 = (int.from_bytes(block[2 * i:2 * i + 2], "big") for i in range(4))
    for k in range(31, -1, -1):
        counter = k + 1
        x1 = g_inv(w2, k, key)
        if RULES[k] == "A":
            w1, w2, w3, w4 = x1, w3, w4, w1 ^ w2 ^ counter
        else:
            w1, w2, w3, w4 = x1, x1 ^ w3 ^ counter, w4, w1
    return _pack((w1, w2, w3, w4))
