# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/related-key-attack/. The authors are listed in prov/3PCPX9.jsonl.
"""A related-key attack with shifted subkeys (the idea of Biham 1993) on a toy
Feistel cipher.

For study only: a teaching attack on a toy cipher. Nothing here is constant
time or fit for real use; for real data use AES from a validated library (for
example the Python package "cryptography").

The toy cipher, defined in this module only:
  * a 32-bit block (L, R) of two 16-bit halves and a 64-bit key made of four
    16-bit words w0, w1, w2, w3;
  * round i uses the subkey k_i = w_(i mod 4) and maps (L, R) to
    (R, L ^ f(R ^ k_i)), where f is one round of the Heys toy SPN without its
    key (S-boxes, then the bit transpose), a bijection on 16 bits;
  * ROUNDS = 32 rounds, and the output is (L_32, R_32) with no final swap.

The related key K* = (w1, w2, w3, w0) has the subkeys of K shifted by one
round. So E_K* applied to one round of P equals one round applied to E_K(P),
with the subkey w0 in both places. The attacker fixes the right half R0 of
m plaintexts under K and the left half (= R0) of m plaintexts under K*. A
"slid" pair turns up by the birthday paradox once m^2 is near 2^16, and each
slid pair gives w0 twice, once from the plaintexts and once from the
ciphertexts. Repeat with keys rotated by 1, 2 and 3 to get the next words.
"""

import random
from collections.abc import Callable

SBOX = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]
SBOX_INV = [SBOX.index(v) for v in range(16)]
ROUNDS = 32
MASK16 = 0xFFFF


def _perm_bits(x: int) -> int:
    y = 0
    for i in range(16):
        if (x >> (15 - i)) & 1:
            row, col = divmod(i, 4)
            y |= 1 << (15 - (4 * col + row))
    return y


_SUB = [sum(SBOX[(x >> (4 * k)) & 0xF] << (4 * k) for k in range(4)) for x in range(1 << 16)]
_SUB_INV = [sum(SBOX_INV[(x >> (4 * k)) & 0xF] << (4 * k) for k in range(4)) for x in range(1 << 16)]
_PERM = [_perm_bits(x) for x in range(1 << 16)]
F = [_PERM[_SUB[x]] for x in range(1 << 16)]
F_INV = [_SUB_INV[_PERM[y]] for y in range(1 << 16)]


def subkeys(key: list[int], rounds: int = ROUNDS) -> list[int]:
    return [key[i % 4] for i in range(rounds)]


def encrypt(p: int, key: list[int], rounds: int = ROUNDS) -> int:
    left, right = p >> 16, p & MASK16
    for k in subkeys(key, rounds):
        left, right = right, left ^ F[right ^ k]
    return (left << 16) | right


def rotate_key(key: list[int], j: int) -> list[int]:
    """The related key whose subkeys are those of `key` shifted by j rounds."""
    return key[j % 4:] + key[:j % 4]


def recover_first_word(enc: Callable[[int], int], enc_star: Callable[[int], int],
                       m: int, rng: random.Random) -> set[int]:
    """Candidates for the first subkey word, from m queries under each key."""
    r0 = rng.getrandbits(16)
    lefts = rng.sample(range(1 << 16), m)
    rights = rng.sample(range(1 << 16), m)
    # Under K: P = (L, r0). Index the ciphertexts by their right half b.
    by_b: dict[int, list[tuple[int, int]]] = {}
    for left in lefts:  # @line L1
        c = enc((left << 16) | r0)
        by_b.setdefault(c & MASK16, []).append((left, c >> 16))
    found = set()
    # Under K*: P* = (r0, X). A slid pair has C*_left = C_right.
    for x in rights:  # @line L2
        cs = enc_star((r0 << 16) | x)  # @line L3
        a_star, b_star = cs >> 16, cs & MASK16
        for left, a in by_b.get(a_star, []):  # @line L4
            w_from_p = F_INV[x ^ left] ^ r0  # @line L5
            w_from_c = F_INV[b_star ^ a] ^ a_star  # @line L6
            if w_from_p == w_from_c:  # @line L7
                found.add(w_from_p)
    return found  # @line L8


def recover_key(oracle: Callable[[int, int], int], m: int, rng: random.Random) -> list[int]:
    """oracle(j, p) encrypts p under the key rotated by j. Return w0..w3."""
    words = []
    for j in range(4):
        cands = set()
        while not cands:
            cands = recover_first_word(lambda p: oracle(j, p), lambda p: oracle(j + 1, p), m, rng)
        if len(cands) > 1:
            raise RuntimeError("more than one candidate; check with a known pair")
        words.append(cands.pop())
    return words
