# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bit-plane-coding/. The authors are listed in prov/8GXKH4.jsonl.

"""Bit-plane coding of signed integers (for example quantized transform
coefficients) as an embedded bit stream, its decoder for any prefix, and
Gray-code bit planes of unsigned samples.

The coder sends the magnitudes plane by plane from the most significant
plane down, and the sign of a value right after its first 1 bit. Every
prefix of the stream decodes. Encoding and decoding cost O(n P) for n
values and P planes.
"""

from typing import List, Sequence, Tuple


def num_planes(values: Sequence[int]) -> int:
    """The number of magnitude planes needed: bit length of the largest |v|."""
    return max((abs(v) for v in values), default=0).bit_length()


def encode(values: Sequence[int], planes: int) -> List[int]:
    """Embedded bit-plane stream: magnitude bits, plane by plane, signs on first 1."""
    out: List[int] = []
    for p in range(planes - 1, -1, -1):  # @line L1
        for v in values:  # @line L2
            m = abs(v)
            b = (m >> p) & 1  # @line L3
            out.append(b)  # @line L4
            if b and m >> (p + 1) == 0:  # @line L5
                out.append(1 if v < 0 else 0)  # first 1 bit: the sign follows
    return out  # @line L6


def decode(bits: Sequence[int], n: int, planes: int, midpoint: bool = True) -> Tuple[List[int], List[int]]:
    """Decode any prefix of the stream of n values.

    Returns (estimates, known) where known[i] is the lowest plane whose bit
    of value i was read (planes if none). With midpoint=True a value known
    to be nonzero gets half of its first unknown plane, 2^(p-1), added to
    its magnitude, which is the middle of its interval of uncertainty.
    """
    mag = [0] * n
    neg = [False] * n
    known = [planes] * n
    pos = 0
    for p in range(planes - 1, -1, -1):  # @line L7
        for i in range(n):
            if pos >= len(bits):
                return _estimate(mag, neg, known, midpoint), known
            b = bits[pos]
            pos += 1
            if b:
                if mag[i] == 0:
                    if pos >= len(bits):  # the sign was cut off: treat the bit as unread
                        return _estimate(mag, neg, known, midpoint), known
                    neg[i] = bits[pos] == 1
                    pos += 1
                mag[i] |= 1 << p
            known[i] = p
    return _estimate(mag, neg, known, midpoint), known


def _estimate(mag: List[int], neg: List[bool], known: List[int], midpoint: bool) -> list:
    out = []
    for m, s, p in zip(mag, neg, known):
        v = m + (2 ** (p - 1) if midpoint and m and p > 0 else 0)  # @line L8
        out.append(-v if s else v)
    return out


def gray(v: int) -> int:
    """Binary-reflected Gray code of v."""
    return v ^ (v >> 1)


def gray_inverse(g: int) -> int:
    """Inverse of gray: the prefix XOR of the bits from the top."""
    v = 0
    while g:
        v ^= g
        g >>= 1
    return v


def bit_planes(samples: Sequence[int], planes: int, use_gray: bool = False) -> List[List[int]]:
    """The bit planes of unsigned samples, most significant first."""
    vals = [gray(s) if use_gray else s for s in samples]
    return [[(v >> p) & 1 for v in vals] for p in range(planes - 1, -1, -1)]


def from_bit_planes(planes_list: Sequence[Sequence[int]], use_gray: bool = False) -> List[int]:
    """Inverse of bit_planes."""
    planes = len(planes_list)
    n = len(planes_list[0]) if planes else 0
    vals = [sum(planes_list[k][i] << (planes - 1 - k) for k in range(planes)) for i in range(n)]
    return [gray_inverse(v) for v in vals] if use_gray else vals
