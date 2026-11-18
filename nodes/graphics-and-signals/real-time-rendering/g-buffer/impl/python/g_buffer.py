# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/g-buffer/. The authors are listed in prov/P04D18.jsonl.

"""A G-buffer texel with an octahedral normal, after Cigolle et al. (2014).

The octahedral map projects a unit vector onto the octahedron
|x| + |y| + |z| = 1, keeps the upper half as it is, and folds the lower half
out over the four corners of the square [-1, 1]^2. The square is then stored
as two signed normalized integers of b bits each.

The texel layout is an example, not a standard: three 32-bit words, with the
base color and the metallic value in unorm8, the normal in two snorm16 values
and the roughness in unorm8. The depth is kept in the depth buffer.
"""

import math

Vec3 = tuple[float, float, float]


def sign_not_zero(x: float) -> float:
    """+1 for x >= 0 and -1 for x < 0. The fold needs sign(0) = +1."""
    return 1.0 if x >= 0.0 else -1.0


def normalize(v: Vec3) -> Vec3:
    length = math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
    return (v[0] / length, v[1] / length, v[2] / length)


def oct_encode(n: Vec3) -> tuple[float, float]:
    """Map a nonzero vector to a point of the square [-1, 1]^2."""
    s = abs(n[0]) + abs(n[1]) + abs(n[2])  # @line L1
    u, v = n[0] / s, n[1] / s  # @line L2
    if n[2] < 0.0:  # @line L3
        u, v = (1.0 - abs(v)) * sign_not_zero(u), (1.0 - abs(u)) * sign_not_zero(v)
    return u, v  # @line L4


def oct_decode(u: float, v: float) -> Vec3:
    """Map a point of the square back to a unit vector."""
    z = 1.0 - abs(u) - abs(v)  # @line L5
    if z < 0.0:  # @line L6
        u, v = (1.0 - abs(v)) * sign_not_zero(u), (1.0 - abs(u)) * sign_not_zero(v)
    return normalize((u, v, z))  # @line L7


def quantize_snorm(x: float, bits: int) -> int:
    """Store x in [-1, 1] as a signed integer of the given width."""
    m = (1 << (bits - 1)) - 1
    return round(max(-1.0, min(1.0, x)) * m)  # @line L8


def dequantize_snorm(q: int, bits: int) -> float:
    m = (1 << (bits - 1)) - 1
    return max(-1.0, q / m)  # @line L9


def encode_normal(n: Vec3, bits: int) -> tuple[int, int]:
    u, v = oct_encode(n)
    return quantize_snorm(u, bits), quantize_snorm(v, bits)


def decode_normal(q: tuple[int, int], bits: int) -> Vec3:
    return oct_decode(dequantize_snorm(q[0], bits), dequantize_snorm(q[1], bits))


def encode_normal_best(n: Vec3, bits: int) -> tuple[int, int]:
    """Try the four integer neighbors of the encoded point and keep the one
    that decodes closest to n. Cigolle et al. call this the precise encoding."""
    u, v = oct_encode(n)
    m = (1 << (bits - 1)) - 1
    best = None
    best_dot = -2.0
    for qu in (math.floor(u * m), math.floor(u * m) + 1):
        for qv in (math.floor(v * m), math.floor(v * m) + 1):
            q = (max(-m, min(m, qu)), max(-m, min(m, qv)))
            d = decode_normal(q, bits)
            dot = d[0] * n[0] + d[1] * n[1] + d[2] * n[2]
            if dot > best_dot:
                best, best_dot = q, dot
    return best


def unorm8(x: float) -> int:
    return round(max(0.0, min(1.0, x)) * 255.0)


def pack_texel(albedo: Vec3, normal: Vec3, roughness: float, metallic: float) -> tuple[int, int, int]:
    """The geometry pass writes one texel: three 32-bit words."""
    r, g, b = (unorm8(c) for c in albedo)
    word0 = r | (g << 8) | (b << 16) | (unorm8(metallic) << 24)  # @line L10
    qu, qv = encode_normal(normal, 16)
    word1 = (qu & 0xFFFF) | ((qv & 0xFFFF) << 16)  # @line L11
    word2 = unorm8(roughness)  # @line L12
    return word0, word1, word2


def to_signed16(x: int) -> int:
    return x - 0x10000 if x & 0x8000 else x


def unpack_texel(words: tuple[int, int, int]) -> tuple[Vec3, Vec3, float, float]:
    """The lighting pass reads the texel back."""
    word0, word1, word2 = words
    albedo = tuple((word0 >> s & 0xFF) / 255.0 for s in (0, 8, 16))  # @line L13
    metallic = (word0 >> 24 & 0xFF) / 255.0
    q = (to_signed16(word1 & 0xFFFF), to_signed16(word1 >> 16 & 0xFFFF))
    normal = decode_normal(q, 16)  # @line L14
    roughness = (word2 & 0xFF) / 255.0
    return albedo, normal, roughness, metallic  # @line L15
