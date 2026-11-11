# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gost-28147-89/. The authors are listed in prov/QNHVZN.jsonl.
"""The GOST 28147-89 block cipher in the Magma form of RFC 8891.

For study only. This code is not constant time: the S-boxes are tables
indexed by secret nibbles, and Python itself leaks timing. Do not use it to
protect real data. Use a validated library that implements GOST R 34.12-2015
instead.

GOST 28147-89 (RFC 5830) leaves the eight 4-bit S-boxes open. Magma (GOST R
34.12-2015, RFC 8891) fixes them to the set id-tc26-gost-28147-param-Z and
reads the key and the block as big-endian integers. This module uses the
Magma conventions, so it passes the RFC 8891 examples. The round function
takes any S-box set. Cost: 32 Feistel rounds, each with one addition modulo
2^32, eight 4-bit S-box lookups and one rotation by 11.
"""

MASK32 = 0xFFFFFFFF

# RFC 8891 Section 4.1: Pi'_0, ..., Pi'_7 (the set id-tc26-gost-28147-param-Z).
SBOX_PARAM_Z = [
    [12, 4, 6, 2, 10, 5, 11, 9, 14, 8, 13, 7, 0, 3, 15, 1],
    [6, 8, 2, 3, 9, 10, 5, 12, 1, 14, 4, 7, 11, 13, 0, 15],
    [11, 3, 5, 8, 2, 15, 10, 13, 14, 1, 7, 4, 12, 9, 6, 0],
    [12, 8, 2, 1, 13, 4, 15, 6, 7, 0, 10, 5, 3, 14, 9, 11],
    [7, 15, 5, 10, 8, 1, 6, 13, 0, 9, 3, 14, 11, 4, 2, 12],
    [5, 13, 15, 6, 9, 2, 12, 10, 11, 7, 8, 1, 4, 3, 14, 0],
    [8, 14, 2, 5, 6, 9, 1, 12, 15, 4, 11, 0, 13, 10, 3, 7],
    [1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2],
]


def t(a: int, sbox: list[list[int]] = SBOX_PARAM_Z) -> int:
    """t(a_7||...||a_0) = Pi_7(a_7)||...||Pi_0(a_0); a_0 is the low nibble."""
    out = 0
    for i in range(8):
        out |= sbox[i][(a >> (4 * i)) & 0xF] << (4 * i)
    return out


def rotl(x: int, s: int) -> int:
    return ((x << s) | (x >> (32 - s))) & MASK32


def g(k: int, a: int, sbox: list[list[int]] = SBOX_PARAM_Z) -> int:
    """g[k](a) = t(a + k mod 2^32) <<< 11."""
    s = (a + k) & MASK32  # @line L4
    u = t(s, sbox)  # @line L5
    return rotl(u, 11)  # @line L6


def round_keys(key: bytes) -> list[int]:
    """K_1, ..., K_32: the 8 key words three times in order, then once in reverse."""
    if len(key) != 32:
        raise ValueError("the key must have 32 bytes")
    k = [int.from_bytes(key[4 * i:4 * i + 4], "big") for i in range(8)]  # @line L7
    return k * 3 + k[::-1]  # @line L8


def _crypt(block: int, keys: list[int], sbox: list[list[int]]) -> int:
    a1, a0 = block >> 32, block & MASK32
    for k in keys[:-1]:  # @line L1
        a1, a0 = a0, g(k, a0, sbox) ^ a1  # @line L2
    return ((g(keys[-1], a0, sbox) ^ a1) << 32) | a0  # @line L3


def encrypt_block(key: bytes, block: bytes, sbox: list[list[int]] = SBOX_PARAM_Z) -> bytes:
    if len(block) != 8:
        raise ValueError("the block must have 8 bytes")
    return _crypt(int.from_bytes(block, "big"), round_keys(key), sbox).to_bytes(8, "big")


def decrypt_block(key: bytes, block: bytes, sbox: list[list[int]] = SBOX_PARAM_Z) -> bytes:
    """Decryption is the same network with the round keys in reverse order."""
    if len(block) != 8:
        raise ValueError("the block must have 8 bytes")
    return _crypt(int.from_bytes(block, "big"), round_keys(key)[::-1], sbox).to_bytes(8, "big")
