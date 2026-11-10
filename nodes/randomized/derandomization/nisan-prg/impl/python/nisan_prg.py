# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nisan-prg/. The authors are listed in prov/AGXJ9C.jsonl.

"""Nisan's generator for space-bounded computation.

A block is an element of GF(2^k), stored as an int below 2^k. The seed is a block x
and hash functions h_1, ..., h_ell, each a pair (a, b) that maps y to a*y + b in
GF(2^k). The output is 2^ell blocks, that is k * 2^ell bits.
"""

from typing import List, Sequence, Tuple

Hash = Tuple[int, int]

# An irreducible polynomial of degree k over GF(2), for k = 1 .. 8.
IRREDUCIBLE = {
    1: 0b11,
    2: 0b111,
    3: 0b1011,
    4: 0b10011,
    5: 0b100101,
    6: 0b1000011,
    7: 0b10000011,
    8: 0x11B,
}


def gf_mul(a: int, b: int, k: int, poly: int) -> int:
    """The product of a and b in GF(2^k) = GF(2)[t] / (poly)."""
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if (a >> k) & 1:
            a ^= poly
    return result


def apply_hash(h: Hash, y: int, k: int, poly: int) -> int:
    """h(y) = a*y + b in GF(2^k)."""
    a, b = h
    return gf_mul(a, y, k, poly) ^ b


def nisan_blocks(x: int, hs: Sequence[Hash], k: int, poly: int) -> List[int]:
    """The 2^ell output blocks of Nisan's generator on seed (x, h_1, ..., h_ell).

    hs[i - 1] is h_i. Block j is h_1^(j_1) o h_2^(j_2) o ... o h_ell^(j_ell) (x),
    where j_i is bit i of j, counted from 1 at the low end. Cost: 2^ell - 1 field
    multiplications."""
    ell = len(hs)
    blocks = [0] * (1 << ell)
    blocks[0] = x  # @line L1
    for j in range(1, 1 << ell):  # @line L2
        i = (j & -j).bit_length()  # @line L3
        blocks[j] = apply_hash(hs[i - 1], blocks[j - (1 << (i - 1))], k, poly)  # @line L4
    return blocks  # @line L5


def nisan_bits(x: int, hs: Sequence[Hash], k: int, poly: int) -> List[int]:
    """The output as k * 2^ell bits, block by block, low bit of each block first."""
    out = []
    for block in nisan_blocks(x, hs, k, poly):
        out.extend((block >> t) & 1 for t in range(k))
    return out


def seed_length(k: int, ell: int) -> int:
    """k bits for x and 2k bits for each of the ell hash functions."""
    return k * (2 * ell + 1)


def output_length(k: int, ell: int) -> int:
    return k * (1 << ell)
