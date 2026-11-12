# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spiht/. The authors are listed in prov/0AFRWT.jsonl.

import math
import random

import pytest

from spiht import (
    Trees,
    compress,
    decompress,
    s_forward,
    s_inverse,
    spiht_decode,
    spiht_encode,
    wavelet_forward,
    wavelet_inverse,
)


def example() -> list:
    c = [[0] * 8 for _ in range(8)]
    c[0][0], c[0][1], c[1][0], c[1][1] = 26, 6, -3, 2
    c[0][2], c[0][3], c[0][4] = 13, -12, -9
    return c


def nonzero(m):
    return {(i, j): v for i, row in enumerate(m) for j, v in enumerate(row) if v}


def test_worked_example() -> None:
    c = example()
    bits, n_max, snaps = spiht_encode(c, 2)
    assert n_max == 4 and len(bits) == 85
    passes = ["10000000", "00011011000011110000001", "100000000000000110", "1110000000000010001", "00000000000101010"]
    ends = [s[4] for s in snaps]
    assert ["".join(map(str, bits[a:b])) for a, b in zip([0] + ends, ends)] == passes
    assert snaps[1][2] == [(1, 0, 0), (1, 1, 0), (0, 3, 0), (1, 2, 0), (1, 3, 0)]  # LIS after plane 3, all type A
    assert snaps[1][3] == [(0, 0), (0, 2), (0, 3), (0, 4)]  # LSP after plane 3
    expected = [
        {(0, 0): 24},
        {(0, 0): 28, (0, 2): 12, (0, 3): -12, (0, 4): -12},
        {(0, 0): 26, (0, 1): 6, (0, 2): 14, (0, 3): -14, (0, 4): -10},
        {(0, 0): 27, (0, 1): 7, (0, 2): 13, (0, 3): -13, (0, 4): -9, (1, 0): -3, (1, 1): 3},
        nonzero(c),
    ]
    for end, want in zip(ends, expected):
        assert nonzero(spiht_decode(bits[:end], 8, 8, 2, n_max)[0]) == want
    assert len(bits) < 64 * 5 + 7  # plain bit planes would need 327 bits


def test_trees_cover_every_coefficient_once() -> None:
    for rows, cols, levels in ((8, 8, 2), (16, 32, 3), (32, 16, 1)):
        t = Trees(rows, cols, levels)
        parents = {}
        for i in range(rows):
            for j in range(cols):
                for ch in t.offspring(i, j):
                    assert ch not in parents
                    parents[ch] = (i, j)
        roots = set(t.roots())
        assert all((i, j) in parents or (i, j) in roots for i in range(rows) for j in range(cols))
        assert not any(r in parents for r in roots)
        assert sum(1 for r in roots if not t.offspring(*r)) == len(roots) // 4
    with pytest.raises(ValueError):
        Trees(12, 16, 2)


def test_s_transform_is_reversible() -> None:
    rng = random.Random(1)
    for _ in range(200):
        x = [rng.randint(-300, 300) for _ in range(2 * rng.randint(1, 10))]
        assert s_inverse(*s_forward(x)) == x
    assert s_forward([7, 4]) == ([5], [3])  # floor((7 + 4) / 2) and 7 - 4
    for rows, cols, levels in ((8, 8, 2), (16, 32, 3), (32, 16, 1)):
        img = [[rng.randrange(256) for _ in range(cols)] for _ in range(rows)]
        assert wavelet_inverse(wavelet_forward(img, levels), levels) == img


def scene(rows: int, cols: int, seed: int) -> list:
    """A smooth gradient with a bright disc, some noise, and a checkerboard patch."""
    rng = random.Random(seed)
    out = []
    for i in range(rows):
        row = []
        for j in range(cols):
            v = 60 + 1.5 * i + 0.8 * j + rng.gauss(0, 3)
            if (i - rows / 2) ** 2 + (j - cols / 3) ** 2 < (rows / 4) ** 2:
                v += 70
            if i < rows // 4 and j >= 3 * cols // 4:
                v += 40 * ((i // 2 + j // 2) % 2)
            row.append(max(0, min(255, int(v))))
        out.append(row)
    return out


def coded_images():
    rng = random.Random(2)
    yield wavelet_forward(scene(64, 64, 1), 4), 4
    yield wavelet_forward(scene(32, 64, 3), 3), 3
    yield [[rng.randint(-40, 40) for _ in range(16)] for _ in range(16)], 2
    yield [[int(rng.expovariate(0.1)) * rng.choice((-1, 1)) for _ in range(32)] for _ in range(32)], 3


def test_decoder_state_equals_encoder_state_and_lossless() -> None:
    for coef, levels in coded_images():
        rows, cols = len(coef), len(coef[0])
        bits, n_max, snaps = spiht_encode(coef, levels)
        est, n, dsnaps = spiht_decode(bits, rows, cols, levels, n_max)
        assert dsnaps == snaps  # the same LIP, LIS, LSP and position after every pass
        assert est == coef and n == -1


def test_full_image_round_trip_and_zero_image() -> None:
    img = scene(64, 64, 4)
    bits, n_max = compress(img, 4)
    assert decompress(bits, 64, 64, 4, n_max) == img
    assert len(bits) < 64 * 64 * (n_max + 1)  # far fewer than one bit per coefficient per plane
    zero = [[0] * 16 for _ in range(16)]
    bits, n_max, snaps = spiht_encode(zero, 2)
    assert (bits, n_max, snaps) == ([], -1, [])
    assert spiht_decode([], 16, 16, 2, -1)[0] == zero


def max_err(a, b):
    return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def mse(a, b):
    return sum((x - y) ** 2 for ra, rb in zip(a, b) for x, y in zip(ra, rb)) / (len(a) * len(a[0]))


def test_figures_on_the_page() -> None:
    c = example()
    bits, n_max, snaps = spiht_encode(c, 2)
    sse = [mse(spiht_decode(bits[: s[4]], 8, 8, 2, n_max)[0], c) * 64 for s in snaps]
    assert sse == [447, 63, 19, 4, 0]
    img = scene(64, 64, 1)
    bits, n_max = compress(img, 4)
    assert (n_max, len(bits)) == (7, 20672)
    for bpp, want in ((0.25, 21.66), (0.5, 28.57), (1, 30.66), (2, 36.36)):
        rec = decompress(bits[: int(bpp * 4096)], 64, 64, 4, n_max)
        assert abs(10 * math.log10(255 ** 2 / mse(rec, img)) - want) < 0.01


def test_every_prefix_decodes_within_bound() -> None:
    for coef, levels in coded_images():
        rows, cols = len(coef), len(coef[0])
        bits, n_max, snaps = spiht_encode(coef, levels)
        step = max(1, len(bits) // 100)
        for k in list(range(0, len(bits), step)) + [len(bits)]:
            est, n, _ = spiht_decode(bits[:k], rows, cols, levels, n_max)
            assert max_err(est, coef) <= (2 ** (n + 1) - 1 if n >= 0 else 0)


def test_error_after_each_pass() -> None:
    for coef, levels in coded_images():
        rows, cols = len(coef), len(coef[0])
        bits, n_max, snaps = spiht_encode(coef, levels)
        prev = None
        for n, _, _, lsp, end in snaps:
            est = spiht_decode(bits[:end], rows, cols, levels, n_max)[0]
            assert max_err(est, coef) <= max(2 ** n - 1, 0)
            assert set(lsp) == {(i, j) for i in range(rows) for j in range(cols) if abs(coef[i][j]) >= 2 ** n}
            e = mse(est, coef)
            assert prev is None or e <= prev  # observed on these images, not a theorem
            prev = e
