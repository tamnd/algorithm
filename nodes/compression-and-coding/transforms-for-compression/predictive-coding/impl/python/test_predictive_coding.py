# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/predictive-coding/. The authors are listed in prov/5989T7.jsonl.

# Oracles: the worked examples of the page (computed by hand), the definition
# of MED as a median, k-th differences for the fixed predictors, the error
# bound step / 2 of closed-loop coding, round trips, and a lower empirical
# entropy of the residuals than of the samples on a smooth image built here.

import math
import random
from collections import Counter

from predictive_coding import (
    fixed_predictor,
    image_from_residuals,
    image_residuals,
    jpeg_lossless_decode,
    jpeg_lossless_encode,
    med,
    med_residuals,
    open_loop_encode,
    paeth,
    predictive_decode,
    predictive_encode,
    previous_sample,
)

IMG = [[50, 52, 54], [51, 53, 90], [52, 90, 92]]


def signed(r):
    return [[d - 65536 if d >= 32768 else d for d in row] for row in r]


def h0(v):
    c, n = Counter(v), len(v)
    return -sum(m / n * math.log2(m / n) for m in c.values())


def test_worked_image() -> None:
    assert jpeg_lossless_encode(IMG, 4)[0][0] == 65536 - 78
    assert signed(jpeg_lossless_encode(IMG, 4)) == [[-78, 2, 2], [1, 0, 35], [1, 36, -35]]
    assert signed(jpeg_lossless_encode(IMG, 1)) == [[-78, 2, 2], [1, 2, 37], [1, 38, 2]]
    assert med_residuals(IMG) == [[50, 2, 2], [1, 1, 36], [1, 37, 2]]
    assert med(90, 90, 53) == 90


def test_worked_dpcm() -> None:
    x = [10, 12, 15, 15, 14, 20, 30, 31]
    assert predictive_encode(x, previous_sample) == [10, 2, 3, 0, -1, 6, 10, 1]
    e = predictive_encode(x, previous_sample, 4)
    assert e == [3, 0, 1, 0, -1, 2, 3, 0]
    assert predictive_decode(e, previous_sample, 4) == [12, 12, 16, 16, 12, 20, 32, 32]
    eo = open_loop_encode(x, previous_sample, 4)
    assert predictive_decode(eo, previous_sample, 4) == [12, 16, 20, 20, 20, 28, 40, 40]


def test_t81_round_trips_and_boundaries() -> None:
    rng = random.Random(81)
    images = [[[0]], [[255]], [[7] * 5] * 4, [[rng.randrange(256) for _ in range(9)] for _ in range(6)]]
    images.append([[rng.randrange(65536) for _ in range(5)] for _ in range(4)])
    for img in images:
        p = 16 if max(max(r) for r in img) > 255 else 8
        for sel in range(1, 8):
            res = jpeg_lossless_encode(img, sel, p)
            assert all(0 <= d < 65536 for r in res for d in r)
            assert jpeg_lossless_decode(res, sel, p) == img
            assert res[0][0] == (img[0][0] - (1 << (p - 1))) % 65536
            assert all(res[0][j] == (img[0][j] - img[0][j - 1]) % 65536 for j in range(1, len(img[0])))
            assert all(res[i][0] == (img[i][0] - img[i - 1][0]) % 65536 for i in range(1, len(img)))


def test_med_is_a_median_and_paeth_picks_a_neighbour() -> None:
    for a in range(0, 12):
        for b in range(0, 12):
            for c in range(0, 12):
                assert med(a, b, c) == sorted([a, b, a + b - c])[1]
                assert paeth(a, b, c) in (a, b, c)
    rng = random.Random(2)
    img = [[rng.randrange(256) for _ in range(7)] for _ in range(5)]
    for pred in (med, paeth):
        assert image_from_residuals(image_residuals(img, pred), pred) == img


def test_fixed_predictors_are_differences() -> None:
    poly = [t * t for t in range(10)]
    assert predictive_encode(poly, fixed_predictor(2))[2:] == [2] * 8
    assert predictive_encode(poly, fixed_predictor(3))[3:] == [0] * 7
    rng = random.Random(9639)
    x = [rng.randrange(-1000, 1000) for _ in range(200)]
    for k in range(5):
        d = list(x)
        for _ in range(k):
            d = [d[i] - d[i - 1] for i in range(1, len(d))]
        e = predictive_encode(x, fixed_predictor(k))
        assert e[:k] == x[:k] and e[k:] == d
        assert predictive_decode(e, fixed_predictor(k)) == x


def test_closed_loop_error_bound_and_open_loop_drift() -> None:
    rng = random.Random(1952)
    for step in (1, 2, 3, 4, 7, 16):
        for _ in range(30):
            x = [rng.randrange(-500, 500) for _ in range(rng.randrange(0, 80))]
            for pred in (previous_sample, fixed_predictor(2)):
                y = predictive_decode(predictive_encode(x, pred, step), pred, step)
                assert len(y) == len(x)
                assert all(abs(u - v) <= step / 2 for u, v in zip(x, y))
    ramp = [3 * t for t in range(1000)]
    y = predictive_decode(open_loop_encode(ramp, previous_sample, 4), previous_sample, 4)
    assert y[-1] - ramp[-1] == 999  # each step adds an error of 1


def test_edge_inputs() -> None:
    for x in ([], [0], [5] * 100, [0] * 50 + [9] * 50):
        for k in range(5):
            assert predictive_decode(predictive_encode(x, fixed_predictor(k)), fixed_predictor(k)) == x
    assert predictive_encode([5] * 100, previous_sample)[1:] == [0] * 99


def test_residual_entropy_on_smooth_image() -> None:
    rng = random.Random(81)
    img = [[(2 * i + 3 * j) // 2 + rng.randrange(-2, 3) + 20 for j in range(64)] for i in range(64)]
    raw = h0([v for r in img for v in r])
    for sel in (1, 2, 4, 7):
        assert h0([d for r in jpeg_lossless_encode(img, sel) for d in r]) < raw - 3
    assert h0([d for r in med_residuals(img) for d in r]) < raw - 3
