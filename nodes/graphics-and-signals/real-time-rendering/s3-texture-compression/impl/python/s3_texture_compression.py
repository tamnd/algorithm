# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/s3-texture-compression/. The authors are listed in prov/EBSNSC.jsonl.

"""S3 texture compression, the basic RGB format: decoder and a simple encoder.

A block codes 4 x 4 texels in 64 bits:
- bytes 0-1: color0, an RGB565 word, little endian (red in bits 15..11,
  green in bits 10..5, blue in bits 4..0);
- bytes 2-3: color1, the same;
- bytes 4-7: a 32-bit little-endian word of 16 indices of 2 bits; texel
  i = 4 y + x uses bits 2i and 2i + 1.

If color0 > color1 as unsigned numbers, the palette is color0, color1,
(2 color0 + color1) / 3 and (color0 + 2 color1) / 3. Otherwise it is color0,
color1, (color0 + color1) / 2 and transparent black.

The decoder returns exact Fractions in [0, 1], with the 5-bit and 6-bit
values divided by 31 and 63. Hardware rounds the thirds and the expansion to
8 bits in slightly different ways, so a bit-exact match with one GPU needs
its own rounding rule. The encoder is a range fit along the principal axis
of the block, which is fast but not optimal; its error is measured in the tests.
"""

from fractions import Fraction

BLOCK_BITS = 64
TEXELS = 16
BITS_PER_TEXEL = Fraction(BLOCK_BITS, TEXELS)  # 4 bits per texel


def unpack565(word):
    """RGB565 word -> (r, g, b) as exact Fractions in [0, 1]."""
    r, g, b = (word >> 11) & 31, (word >> 5) & 63, word & 31
    return (Fraction(r, 31), Fraction(g, 63), Fraction(b, 31))


def pack565(rgb):
    """(r, g, b) in [0, 1] -> the nearest RGB565 word."""
    r, g, b = (min(max(c, 0.0), 1.0) for c in rgb)
    return (int(round(r * 31)) << 11) | (int(round(g * 63)) << 5) | int(round(b * 31))


def palette(c0, c1):
    """The four RGBA palette entries of a block with endpoint words c0 and c1."""
    a, b = unpack565(c0), unpack565(c1)
    if c0 > c1:  # @line L3
        p2 = tuple((2 * x + y) / 3 for x, y in zip(a, b))
        p3 = tuple((x + 2 * y) / 3 for x, y in zip(a, b))
        return [a + (1,), b + (1,), p2 + (1,), p3 + (1,)]
    mid = tuple((x + y) / 2 for x, y in zip(a, b))  # @line L4
    return [a + (1,), b + (1,), mid + (1,), (0, 0, 0, 0)]


def decode_block(block):
    """8 bytes -> 16 RGBA texels in raster order, as exact Fractions."""
    if len(block) != 8:
        raise ValueError("a BC1 block has 8 bytes")
    c0 = block[0] | (block[1] << 8)  # @line L1
    c1 = block[2] | (block[3] << 8)
    bits = block[4] | (block[5] << 8) | (block[6] << 16) | (block[7] << 24)
    pal = palette(c0, c1)  # @line L2
    return [pal[(bits >> (2 * i)) & 3] for i in range(TEXELS)]  # @line L5


def pack_block(c0, c1, indices):
    bits = 0
    for i, k in enumerate(indices):
        bits |= (k & 3) << (2 * i)
    return bytes((c0 & 255, c0 >> 8, c1 & 255, c1 >> 8,
                  bits & 255, (bits >> 8) & 255, (bits >> 16) & 255, bits >> 24))


def principal_axis(colors, iterations=24):
    """The dominant eigenvector of the 3 x 3 covariance, by power iteration."""
    n = len(colors)
    mean = [sum(c[a] for c in colors) / n for a in range(3)]
    cov = [[sum((c[a] - mean[a]) * (c[b] - mean[b]) for c in colors) for b in range(3)] for a in range(3)]
    # Start from the axis with the largest variance. In rare cases this start
    # is orthogonal to the dominant eigenvector, and the iteration ends on
    # another eigenvector. That axis still gives a valid, if worse, encoding.
    v = [0.0, 0.0, 0.0]
    v[max(range(3), key=lambda a: cov[a][a])] = 1.0
    for _ in range(iterations):
        w = [sum(cov[a][b] * v[b] for b in range(3)) for a in range(3)]
        norm = max(abs(x) for x in w)
        if norm == 0:
            return mean, [1.0, 0.0, 0.0]
        v = [x / norm for x in w]
    return mean, v


def sq_err(rgb, entry):
    return sum((float(x) - float(y)) ** 2 for x, y in zip(rgb, entry[:3]))


def nearest_indices(colors, pal, count):
    return [min(range(count), key=lambda k: sq_err(c, pal[k])) for c in colors]


def encode_block(colors):
    """16 RGB colors in [0, 1] -> 8 bytes in the 4-color mode (range fit)."""
    if len(colors) != TEXELS:
        raise ValueError("a BC1 block has 16 texels")
    mean, axis = principal_axis(colors)  # @line L6
    proj = [sum((c[a] - mean[a]) * axis[a] for a in range(3)) for c in colors]
    lo = colors[min(range(TEXELS), key=lambda i: proj[i])]  # @line L7
    hi = colors[max(range(TEXELS), key=lambda i: proj[i])]
    c0, c1 = pack565(hi), pack565(lo)  # @line L8
    if c0 < c1:
        c0, c1 = c1, c0
    if c0 == c1:
        return pack_block(c0, c1, [0] * TEXELS)
    idx = nearest_indices(colors, palette(c0, c1), 4)  # @line L9
    return pack_block(c0, c1, idx)  # @line L10


def encode_image(pixels, width, height):
    """Encode an image (rows of RGB tuples) whose sides are multiples of 4."""
    if width % 4 or height % 4:
        raise ValueError("the sides must be multiples of 4")
    out = []
    for by in range(0, height, 4):
        for bx in range(0, width, 4):
            out.append(encode_block([pixels[by + y][bx + x] for y in range(4) for x in range(4)]))
    return out


def decode_texel(blocks, width, x, y):
    """Random access: decode only the block that holds texel (x, y)."""
    block = blocks[(y // 4) * (width // 4) + x // 4]
    return decode_block(block)[4 * (y % 4) + x % 4]
