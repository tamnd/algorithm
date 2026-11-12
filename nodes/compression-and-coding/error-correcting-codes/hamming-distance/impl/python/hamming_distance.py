# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hamming-distance/. The authors are listed in prov/ZXVGP4.jsonl.
"""The Hamming distance between two words of the same length.

A word is any sequence over a finite alphabet, or a bit vector stored in a
Python integer (bit i is coordinate i). The distance is the number of
coordinates where the two words differ.
"""

from math import comb
from typing import Hashable, Sequence


def hamming_distance(x: Sequence[Hashable], y: Sequence[Hashable]) -> int:
    """The number of positions i with x[i] != y[i].

    Precondition: len(x) == len(y); a ValueError is raised otherwise, because
    the Hamming distance is not defined for words of different lengths.
    Cost: n symbol comparisons for words of length n.
    """
    if len(x) != len(y):
        raise ValueError("the Hamming distance needs two words of the same length")
    return sum(1 for a, b in zip(x, y) if a != b)


def hamming_distance_bits(a: int, b: int) -> int:
    """The Hamming distance of two bit vectors held in non-negative integers.

    The words differ exactly where a XOR b has a 1 bit, so the distance is the
    population count of a ^ b. Cost: one XOR and one popcount on n-bit integers.
    """
    if a < 0 or b < 0:
        raise ValueError("bit vectors are non-negative integers")
    return (a ^ b).bit_count()


def sphere_size(n: int, i: int, q: int) -> int:
    """The number of words of length n over q symbols at distance exactly i from a fixed word.

    Choose the i positions that change, and one of the q - 1 other symbols at each.
    """
    if not 0 <= i <= n:
        return 0
    return comb(n, i) * (q - 1) ** i


def ball_volume(n: int, r: int, q: int) -> int:
    """V_q(n, r): the number of words of length n over q symbols at distance at most r from a fixed word."""
    return sum(sphere_size(n, i, q) for i in range(0, min(r, n) + 1))
