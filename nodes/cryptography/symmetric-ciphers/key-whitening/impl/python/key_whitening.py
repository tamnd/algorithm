# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/key-whitening/. The authors are listed in prov/89MK42.jsonl.
"""Key whitening: the FX construction and the Even-Mansour cipher.

For study only. This code is not constant time, and the block here has only
16 bits, so the ciphers are toys and the tests break them. Do not use this
code to protect real data; use AES from a FIPS 140 validated module, or
libsodium.

FX: y = K2 XOR E_K(x XOR K1) for a block cipher E (DESX uses DES).
Even-Mansour: y = K2 XOR P(x XOR K1) for a public permutation P.
Cost: one call of E or P and two XORs of n bits for each block.
"""

import random
from typing import Callable

BlockCipher = Callable[[int, int], int]


def fx_encrypt(e: BlockCipher, k: int, k1: int, k2: int, x: int) -> int:
    """The FX construction of Kilian and Rogaway."""
    u = x ^ k1  # @line L1
    v = e(k, u)  # @line L2
    return v ^ k2  # @line L3


def fx_decrypt(d: BlockCipher, k: int, k1: int, k2: int, y: int) -> int:
    return d(k, y ^ k2) ^ k1


def public_permutation(n: int, seed: int) -> tuple[list[int], list[int]]:
    """A fixed random permutation of n-bit values and its inverse. Everyone, the attacker too, may call it."""
    p = list(range(1 << n))
    random.Random(seed).shuffle(p)
    inv = [0] * (1 << n)
    for i, v in enumerate(p):
        inv[v] = i
    return p, inv


def em_encrypt(p: list[int], k1: int, k2: int, x: int) -> int:
    """Even-Mansour: K2 XOR P(x XOR K1). The one-key variant has K1 = K2."""
    return p[x ^ k1] ^ k2


def em_decrypt(p_inv: list[int], k1: int, k2: int, y: int) -> int:
    return p_inv[y ^ k2] ^ k1
