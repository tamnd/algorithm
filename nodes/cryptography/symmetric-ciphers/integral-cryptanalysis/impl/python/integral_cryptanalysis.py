# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/integral-cryptanalysis/. The authors are listed in prov/9XG8MF.jsonl.
"""Integral (Square) cryptanalysis on a toy AES-like cipher.

For study only: a teaching attack on a toy cipher. Nothing here is constant
time or fit for real use; for real data use AES from a validated library (for
example the Python package "cryptography").

The toy cipher ("mini-Square" below) is defined in this module only. It has
the round structure of AES at a smaller scale:
  * the state is a 4x4 array of 4-bit cells (a 64-bit block); cell 4c + r is
    row r of column c;
  * SubCells applies the 4-bit S-box of Heys's tutorial to every cell;
  * ShiftRows rotates row r to the left by r places;
  * MixColumns multiplies each column by the circulant matrix (2 3 1 1) over
    GF(2^4) with the polynomial x^4 + x + 1;
  * AddRoundKey XORs a 64-bit round key. The R + 1 round keys are
    independent (there is no key schedule).
Encryption is AddRoundKey(K0), then R rounds; the last round has no
MixColumns, as in AES.

The 3-round distinguisher: take 16 plaintexts that differ only in cell 0,
where they take every value once. After 3 rounds every cell of the state
XORs to zero over the 16 texts ("balanced"). The 4-round attack guesses one
cell of K4 at a time, undoes the last SubCells on that cell and keeps the
guesses for which the sum is zero.
"""

import random

SBOX = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]
SBOX_INV = [SBOX.index(v) for v in range(16)]
MC = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]


def gf16_mul(a: int, b: int) -> int:
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        if a & 0x10:
            a ^= 0x13  # x^4 + x + 1
        b >>= 1
    return r


def sub_cells(s: list[int]) -> list[int]:
    return [SBOX[x] for x in s]


def shift_rows(s: list[int]) -> list[int]:
    return [s[4 * ((c + r) % 4) + r] for c in range(4) for r in range(4)]


def shift_rows_inv(s: list[int]) -> list[int]:
    return [s[4 * ((c - r) % 4) + r] for c in range(4) for r in range(4)]


def mix_columns(s: list[int]) -> list[int]:
    out = []
    for c in range(4):
        col = s[4 * c:4 * c + 4]
        for r in range(4):
            v = 0
            for j in range(4):
                v ^= gf16_mul(MC[r][j], col[j])
            out.append(v)
    return out


def add_key(s: list[int], k: list[int]) -> list[int]:
    return [a ^ b for a, b in zip(s, k)]


def encrypt(p: list[int], keys: list[list[int]], last_mix: bool = False) -> list[int]:
    """len(keys) - 1 rounds. last_mix=True keeps MixColumns in the last round."""
    s = add_key(p, keys[0])
    rounds = len(keys) - 1
    for r in range(1, rounds + 1):
        s = shift_rows(sub_cells(s))
        if r < rounds or last_mix:
            s = mix_columns(s)
        s = add_key(s, keys[r])
    return s


def lambda_set(rng: random.Random, active: int = 0) -> list[list[int]]:
    """16 plaintexts: cell `active` runs through all values, the rest is constant."""
    base = [rng.randrange(16) for _ in range(16)]
    out = []
    for v in range(16):
        p = list(base)
        p[active] = v
        out.append(p)
    return out


def xor_sum(states: list[list[int]]) -> list[int]:
    acc = [0] * 16
    for s in states:
        acc = [a ^ b for a, b in zip(acc, s)]
    return acc


def candidates_for_cell(ciphertexts: list[list[int]], cell: int) -> set[int]:
    """Guesses k of K4[cell] for which SBOX_INV[c ^ k] sums to zero."""
    out = set()
    for k in range(16):
        acc = 0
        for c in ciphertexts:
            acc ^= SBOX_INV[c[cell] ^ k]
        if acc == 0:
            out.add(k)
    return out


def recover_last_round_key(encrypt_oracle, rng: random.Random, max_sets: int = 8) -> tuple[list[int], int]:
    """Recover all 16 cells of K4 of the 4-round cipher. Return (key, sets used)."""
    cands = [set(range(16)) for _ in range(16)]  # @line L1
    used = 0
    while used < max_sets and any(len(c) > 1 for c in cands):  # @line L2
        pts = lambda_set(rng)  # @line L3
        cts = [encrypt_oracle(p) for p in pts]  # @line L4
        used += 1
        for cell in range(16):  # @line L5
            cands[cell] &= candidates_for_cell(cts, cell)  # @line L6
    if any(len(c) != 1 for c in cands):
        raise RuntimeError("the key is not determined; use more sets")
    return [next(iter(c)) for c in cands], used  # @line L7
