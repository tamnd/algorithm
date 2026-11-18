# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/s3-texture-compression/. The authors are listed in prov/EBSNSC.jsonl.

"""Tests of the BC1 decoder and encoder.

The decoder is checked on the bit layout and on exact palettes. The encoder
is checked to be lossless on blocks whose colors lie on the palette of two
RGB565 endpoints, to choose the best index for its endpoints, and to have a
measured error on smooth blocks with noise.
"""

import random
from fractions import Fraction
from math import sqrt

from s3_texture_compression import (
    BITS_PER_TEXEL,
    decode_block,
    decode_texel,
    encode_block,
    encode_image,
    pack_block,
    palette,
    sq_err,
    unpack565,
)


def test_layout_and_rate():
    assert BITS_PER_TEXEL == 4
    rng = random.Random(1)
    for _ in range(200):
        c0, c1 = rng.randrange(65536), rng.randrange(65536)
        idx = [rng.randrange(4) for _ in range(16)]
        block = pack_block(c0, c1, idx)
        assert len(block) * 8 == 64
        pal = palette(c0, c1)
        assert decode_block(block) == [pal[k] for k in idx]


def test_known_block():
    red, blue = 0xF800, 0x001F
    block = pack_block(red, blue, [0, 1, 2, 3] * 4)
    assert block[:4] == bytes((0x00, 0xF8, 0x1F, 0x00))
    assert block[4:] == bytes((0xE4,) * 4)  # indices 0, 1, 2, 3 from the low bits up
    t = decode_block(block)
    assert t[0] == (1, 0, 0, 1) and t[1] == (0, 0, 1, 1)
    assert t[2] == (Fraction(2, 3), 0, Fraction(1, 3), 1)
    assert t[3] == (Fraction(1, 3), 0, Fraction(2, 3), 1)
    # Swap the endpoints: c0 <= c1 selects the 3-color mode with transparency.
    t = decode_block(pack_block(blue, red, [0, 1, 2, 3] * 4))
    assert t[2] == (Fraction(1, 2), 0, Fraction(1, 2), 1) and t[3] == (0, 0, 0, 0)


def test_palette_is_exact():
    rng = random.Random(2)
    for _ in range(300):
        c0, c1 = rng.randrange(65536), rng.randrange(65536)
        a, b = unpack565(c0), unpack565(c1)
        pal = palette(c0, c1)
        if c0 > c1:
            for j in range(3):
                assert pal[2][j] == Fraction(2, 3) * a[j] + Fraction(1, 3) * b[j]
                assert pal[3][j] == Fraction(1, 3) * a[j] + Fraction(2, 3) * b[j]
        else:
            assert pal[3] == (0, 0, 0, 0)
            assert all(pal[2][j] == (a[j] + b[j]) / 2 for j in range(3))


def test_lossless_on_palette_colors():
    rng = random.Random(3)
    done = 0
    while done < 200:
        c0, c1 = rng.randrange(65536), rng.randrange(65536)
        if c0 <= c1:
            continue
        pal = palette(c0, c1)
        idx = [0, 1] + [rng.randrange(4) for _ in range(14)]
        rng.shuffle(idx)
        colors = [tuple(float(x) for x in pal[k][:3]) for k in idx]
        out = decode_block(encode_block(colors))
        assert out == [pal[k] for k in idx]
        done += 1


def test_index_choice_is_best_for_the_endpoints():
    rng = random.Random(4)
    for _ in range(200):
        colors = [(rng.random(), rng.random(), rng.random()) for _ in range(16)]
        block = encode_block(colors)
        c0, c1 = block[0] | block[1] << 8, block[2] | block[3] << 8
        pal = palette(c0, c1)
        out = decode_block(block)
        for c, got in zip(colors, out):
            assert sq_err(c, got) <= min(sq_err(c, p) for p in pal[:4] if p[3] == 1) + 1e-15


def gradient_rmse(amplitude, seed=5, blocks=300):
    """RMSE in levels of 255 on diagonal gradient blocks with a little noise."""
    rng = random.Random(seed)
    total, count = 0.0, 0
    for _ in range(blocks):
        a = [rng.random() for _ in range(3)]
        b = [min(1.0, max(0.0, a[j] + rng.uniform(-amplitude, amplitude))) for j in range(3)]
        colors = []
        for y in range(4):
            for x in range(4):
                t = (x + y) / 6
                colors.append(tuple(min(1.0, max(0.0, a[j] + t * (b[j] - a[j]) + rng.gauss(0, 0.01)))
                                    for j in range(3)))
        out = decode_block(encode_block(colors))
        total += sum(sq_err(c, d) for c, d in zip(colors, out))
        count += 48
    return 255 * sqrt(total / count)


def test_measured_error_on_smooth_blocks():
    # Measurements of this encoder on this data, with seed 5: about 3.4 levels
    # for a low contrast and 11.5 for the full range. A gradient of 7 steps
    # has only 4 palette colors, so a high contrast costs more.
    assert gradient_rmse(0.15) < 4.5
    assert gradient_rmse(1.0) < 14.0


def test_random_access_and_determinism():
    rng = random.Random(6)
    w, h = 8, 12
    img = [[(rng.random(), rng.random(), rng.random()) for _ in range(w)] for _ in range(h)]
    blocks = encode_image(img, w, h)
    assert blocks == encode_image(img, w, h)
    assert len(blocks) == (w // 4) * (h // 4)
    for y in range(h):
        for x in range(w):
            full = decode_block(blocks[(y // 4) * 2 + x // 4])[4 * (y % 4) + x % 4]
            assert decode_texel(blocks, w, x, y) == full
