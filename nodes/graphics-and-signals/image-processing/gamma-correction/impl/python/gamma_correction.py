# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gamma-correction/. The authors are listed in prov/FDBZJX.jsonl.

"""Gamma encoding and decoding: the plain power law and the sRGB transfer function.

Values are in [0, 1]. The sRGB curve of IEC 61966-2-1 is a straight line of
slope 12.92 near black and a 1/2.4 power above it. On the straight segment
the functions accept a Fraction and return an exact Fraction.
"""

from fractions import Fraction

ENCODE_BREAK = Fraction(31308, 10000000)  # 0.0031308, linear light
DECODE_BREAK = Fraction(4045, 100000)  # 0.04045, encoded value
SLOPE = Fraction(1292, 100)  # 12.92
A = Fraction(55, 1000)  # 0.055


def power_encode(linear, gamma: float = 2.2):
    """V = L^(1/gamma)."""
    return linear ** (1 / gamma)


def power_decode(encoded, gamma: float = 2.2):
    """L = V^gamma."""
    return encoded**gamma


def srgb_encode(linear):
    """Linear light in [0, 1] to the sRGB encoded value in [0, 1]."""
    if linear <= ENCODE_BREAK:
        return SLOPE * linear
    return float(1 + A) * float(linear) ** (1 / 2.4) - float(A)


def srgb_decode(encoded):
    """sRGB encoded value in [0, 1] to linear light in [0, 1]."""
    if encoded <= DECODE_BREAK:
        return encoded / SLOPE
    return ((float(encoded) + float(A)) / float(1 + A)) ** 2.4


def decode_table(bits: int = 8) -> list[float]:
    """Linear light for each code 0 .. 2^bits - 1, as a lookup table."""
    top = (1 << bits) - 1
    return [float(srgb_decode(Fraction(c, top))) for c in range(top + 1)]


def encode_to_code(linear, bits: int = 8) -> int:
    """Linear light to the nearest sRGB code, halves up."""
    top = (1 << bits) - 1
    v = srgb_encode(linear) * top
    return min(top, max(0, int(float(v) + 0.5)))


def mean_in_linear_light(codes: list[int], bits: int = 8) -> int:
    """Average 8-bit sRGB codes the right way: decode, average, encode."""
    table = decode_table(bits)
    return encode_to_code(sum(table[c] for c in codes) / len(codes), bits)
