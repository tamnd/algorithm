# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jpeg-2000/. The authors are listed in prov/APJT1C.jsonl.

import random

from jpeg_2000 import (
    dc_shift,
    decode_reversible,
    dequantize,
    dwt2_forward,
    dwt2_inverse,
    encode_reversible,
    lift53_forward,
    lift53_inverse,
    lift97_forward,
    lift97_inverse,
    quantize,
    rct_forward,
    rct_inverse,
    step_size,
    subbands,
    tiles,
    untile,
)


def test_worked_example_53() -> None:
    x = [10, 12, 14, 20, 30, 31, 32, 30]
    assert lift53_forward(x) == ([10, 14, 30, 32], [0, -2, 0, -2])
    assert lift53_inverse([10, 14, 30, 32], [0, -2, 0, -2]) == x
    # The predict step removes straight lines exactly, at the ends too for odd lengths.
    assert lift53_forward([5, 7, 9, 11, 13, 15, 17]) == ([5, 9, 13, 17], [0, 0, 0])
    assert lift53_forward([42]) == ([42], [])


def test_53_is_exactly_reversible_in_1d() -> None:
    rng = random.Random(1)
    for n in range(1, 41):
        for _ in range(30):
            x = [rng.randint(-5000, 5000) for _ in range(n)]
            lo, hi = lift53_forward(x)
            assert len(lo) == (n + 1) // 2 and len(hi) == n // 2
            assert lift53_inverse(lo, hi) == x


def make_images():
    rng = random.Random(2)
    yield [[4 * i + 2 * j for j in range(16)] for i in range(16)]  # gradient
    yield [[255 * ((i // 2 + j // 2) % 2) for j in range(13)] for i in range(11)]  # checkerboard
    for h, w in ((1, 1), (1, 9), (7, 1), (17, 23), (32, 32), (5, 64)):
        yield [[rng.randrange(256) for _ in range(w)] for _ in range(h)]


def test_53_multilevel_2d_is_exactly_reversible() -> None:
    for img in make_images():
        s = dc_shift(img, 8)
        for levels in range(0, 7):
            c = dwt2_forward(s, levels)
            assert all(isinstance(v, int) for row in c for v in row)
            assert dwt2_inverse(c, levels) == s


def test_subband_layout() -> None:
    bands = subbands(64, 64, 5)
    assert bands[0] == ("LL5", 0, 0, 2, 2)
    assert sum(r * c for _, _, _, r, c in bands) == 64 * 64
    assert len(bands) == 3 * 5 + 1
    odd = subbands(17, 23, 3)
    assert sum(r * c for _, _, _, r, c in odd) == 17 * 23
    # A gradient leaves zeros in all the high bands of level 1 except the last row and column,
    # where the symmetric extension breaks the straight line.
    c = dwt2_forward([[4 * i + 2 * j for j in range(8)] for i in range(8)], 1)
    assert [row[4:] for row in c[4:7]] == [[0, 0, 0, 0]] * 3
    assert [c[r][c0] for r in range(3) for c0 in range(4, 7)] == [0] * 9


def test_97_lifting() -> None:
    lo, hi = lift97_forward([1.0] * 16)
    assert all(abs(v - 1) < 1e-12 for v in lo) and all(abs(v) < 1e-12 for v in hi)
    lo, hi = lift97_forward([(-1.0) ** i for i in range(16)])
    assert all(abs(v) < 1e-12 for v in lo) and all(abs(abs(v) - 2) < 1e-12 for v in hi)
    # Four vanishing moments: cubics give 0 in the high band away from the ends.
    lo, hi = lift97_forward([0.5 * i ** 3 - 2 * i ** 2 + i for i in range(20)])
    assert all(abs(v) < 1e-8 for v in hi[1:8])
    # The analysis filters that the lifting steps produce.
    taps_lo, taps_hi = [], []
    for k in range(32):
        e = [0.0] * 32
        e[k] = 1.0
        a, b = lift97_forward(e)
        taps_lo.append(a[8])
        taps_hi.append(b[8])
    taps_lo = [round(v, 6) for v in taps_lo if abs(v) > 1e-12]
    taps_hi = [round(v, 6) for v in taps_hi if abs(v) > 1e-12]
    assert taps_lo == [0.026749, -0.016864, -0.078223, 0.266864, 0.602949, 0.266864, -0.078223, -0.016864, 0.026749]
    assert taps_hi == [0.091272, -0.057544, -0.591272, 1.115087, -0.591272, -0.057544, 0.091272]
    rng = random.Random(3)
    for n in range(1, 30):
        x = [rng.uniform(-100, 100) for _ in range(n)]
        assert max(abs(a - b) for a, b in zip(lift97_inverse(*lift97_forward(x)), x)) < 1e-9


def test_97_multilevel_2d() -> None:
    for img in make_images():
        f = [[float(v - 128) for v in row] for row in img]
        back = dwt2_inverse(dwt2_forward(f, 4, reversible=False), 4, reversible=False)
        assert max(abs(a - b) for r1, r2 in zip(back, f) for a, b in zip(r1, r2)) < 1e-9


def test_rct() -> None:
    assert rct_forward(255, 0, 0) == (63, 0, 255)
    red = dc_shift([[255, 0, 0]], 8)[0]  # pure red after the level shift
    assert red == [127, -128, -128]
    assert rct_forward(*red) == (-65, 0, 255) and rct_inverse(-65, 0, 255) == (127, -128, -128)
    vals = list(range(-128, 128, 5)) + [127]
    for r in vals:
        for g in vals:
            for b in vals:
                assert rct_inverse(*rct_forward(r, g, b)) == (r, g, b)


def test_tiles_and_lossless_path() -> None:
    rng = random.Random(4)
    h, w = 20, 27
    rgb = [[[rng.randrange(256) for _ in range(w)] for _ in range(h)] for _ in range(3)]
    parts = tiles(rgb[0], 8)
    assert len(parts) == 3 * 4 and untile(parts, h, w) == rgb[0]
    coded = encode_reversible(rgb, 8, 3, 8)
    assert decode_reversible(coded, 8, 3, h, w) == rgb


def test_dead_zone_quantizer() -> None:
    assert step_size(8, 0, 8) == 1.0
    assert step_size(10, 1024, 9) == 0.75
    assert [quantize(v, 2.0) for v in (-4.5, -1.9, 0.0, 1.9, 2.0, 5.9)] == [-2, 0, 0, 0, 1, 2]
    rng = random.Random(5)
    for _ in range(2000):
        y = rng.uniform(-50, 50)
        step = rng.choice((0.5, 1.0, 3.0))
        q = quantize(y, step)
        err = abs(y - dequantize(q, step))
        assert err < step and (q == 0 or err <= step / 2)
