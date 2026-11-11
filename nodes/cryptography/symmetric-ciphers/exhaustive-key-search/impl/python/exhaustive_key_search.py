# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exhaustive-key-search/. The authors are listed in prov/BSXCZ6.jsonl.
"""Exhaustive key search: try each key against known plaintext and ciphertext pairs.

For study only. The code is not constant time, and the search runs only on a
toy cipher with a 16-bit key and a 16-bit block. Do not use the toy cipher to
protect real data; use AES from a FIPS 140 validated module or libsodium.

Cost: at most 2^k calls of the cipher on the first pair, where k is the key
length, plus a few calls for each key that passes the first pair.
"""

from typing import Callable

Cipher = Callable[[int, int], int]

# The 4-bit S-box of the Heys tutorial cipher, used here in a toy cipher.
TOY_S = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]
M16 = 0xFFFF
# Two S-boxes side by side on one byte, to make the toy cipher faster.
_S8 = [(TOY_S[b >> 4] << 4) | TOY_S[b & 0xF] for b in range(256)]


def _rotl(x: int, r: int) -> int:
    return ((x << r) | (x >> (16 - r))) & M16


def round_keys(key: int) -> list[int]:
    """Round key i is rotl(key, 3i + 1 mod 16) XOR a round constant."""
    return [_rotl(key, (3 * i + 1) % 16) ^ ((0x9E37 * (i + 1)) & M16) for i in range(7)]


def toy_encrypt(key: int, x: int) -> int:
    """A toy 6-round SPN with a 16-bit key and a 16-bit block. It is not secure.

    Each round XORs a round key, applies the S-box to the 4 nibbles, then the
    invertible linear map x -> x XOR rotl(x, 5) XOR rotl(x, 9).
    """
    rk = round_keys(key)
    for i in range(6):
        x ^= rk[i]
        x = (_S8[x >> 8] << 8) | _S8[x & 0xFF]
        x ^= ((x << 5) | (x >> 11)) & M16 ^ ((x << 9) | (x >> 7)) & M16
    return x ^ rk[6]


def key_search(encrypt: Cipher, pairs: list[tuple[int, int]], k: int) -> list[int]:
    """Return every k-bit key K with encrypt(K, x) = y for each pair (x, y)."""
    x1, y1 = pairs[0]
    found = []
    for key in range(1 << k):  # @line L1
        if encrypt(key, x1) != y1:  # @line L2
            continue
        if all(encrypt(key, x) == y for x, y in pairs[1:]):  # @line L3
            found.append(key)  # @line L4
    return found  # @line L5


def first_key(encrypt: Cipher, pairs: list[tuple[int, int]], k: int, order: list[int] | None = None) -> tuple[int | None, int]:
    """Stop at the first key that fits all pairs. Return the key and the number of keys tried."""
    keys = order if order is not None else range(1 << k)
    tried = 0
    for key in keys:
        tried += 1
        if all(encrypt(key, x) == y for x, y in pairs):
            return key, tried
    return None, tried
