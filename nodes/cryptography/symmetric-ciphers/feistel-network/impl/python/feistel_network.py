# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/feistel-network/. The authors are listed in prov/NQ29ZT.jsonl.
"""A generic balanced Feistel network on blocks of 2h bits.

For study only. This code is not constant time, and a Feistel network with a
toy round function is not a secure cipher. Do not use it to protect real data;
use AES from a FIPS 140 validated module, or libsodium.

The output is (R_r, L_r), with the halves swapped after the last round, as in
DES. Then decryption is the same network with the round keys in reverse order.
Cost: r calls of the round function F and r XORs of h bits.
"""

from typing import Callable

RoundFunction = Callable[[int, int], int]


def feistel(f: RoundFunction, keys: list[int], block: int, h: int) -> int:
    """Run the network with round keys keys[0], keys[1], ... on a block of 2h bits."""
    mask = (1 << h) - 1
    left, right = block >> h, block & mask  # @line L1
    for k in keys:  # @line L2
        prev_left = left
        left = right  # @line L3
        right = prev_left ^ (f(k, left) & mask)  # @line L4
    return (right << h) | left  # @line L5


def feistel_inverse(f: RoundFunction, keys: list[int], block: int, h: int) -> int:
    """The inverse: the same network, with the round keys in reverse order."""
    return feistel(f, keys[::-1], block, h)


def toy_round_function(k: int, r: int) -> int:
    """A round function on 16-bit halves that is not a permutation: (r AND k) loses information."""
    return ((r & k) ^ ((r * r) >> 3) ^ (k >> 1)) & 0xFFFF
