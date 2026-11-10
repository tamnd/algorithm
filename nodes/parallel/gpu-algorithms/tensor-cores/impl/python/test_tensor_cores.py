# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tensor-cores/. The authors are listed in prov/65S74S.jsonl.
import random
from fractions import Fraction as F

from tensor_cores import (BF16, FP16, FP32, TF32, dot, max_finite, mma, mma_count,
                          padding_efficiency, peak_flops, ridge_point, round_to,
                          tile_intensity, unit_roundoff)


def test_round_to_is_nearest_and_idempotent():
    rng = random.Random(3)
    for fmt in (FP16, BF16, TF32, FP32):
        u = unit_roundoff(fmt)
        tiny = F(2) ** fmt[1]
        for _ in range(300):
            x = F(rng.randrange(1, 10 ** 6), rng.randrange(1, 10 ** 6)) * rng.choice([1, -1])
            r = round_to(x, fmt)
            assert round_to(r, fmt) == r
            if tiny <= abs(x) <= max_finite(fmt):
                assert abs(r - x) <= u * abs(x)


def test_round_to_worked_values():
    assert round_to(F(1, 10), FP16) == F(819, 8192)
    assert round_to(F(1, 10), TF32) == F(819, 8192)
    assert round_to(F(1, 10), BF16) == F(205, 2048)
    assert max_finite(FP16) == 65504
    assert round_to(65519, FP16) == 65504
    assert round_to(65520, FP16) == float("inf")          # the tie rounds to 65536, which overflows
    assert round_to(F(1, 2 ** 25), FP16) == 0             # half the smallest subnormal, tie to even
    assert unit_roundoff(FP16) == F(1, 2048) and unit_roundoff(BF16) == F(1, 256)


def test_mma_is_exact_on_small_integers():
    rng = random.Random(4)
    A = [[rng.randrange(-8, 9) for _ in range(16)] for _ in range(16)]
    B = [[rng.randrange(-8, 9) for _ in range(16)] for _ in range(16)]
    C = [[rng.randrange(-100, 101) for _ in range(16)] for _ in range(16)]
    D = mma(A, B, C, FP16, FP32)
    for i in range(16):
        for j in range(16):
            assert D[i][j] == C[i][j] + sum(A[i][t] * B[t][j] for t in range(16))


def test_accumulator_precision():
    ones = [1] * 4096
    assert dot(ones, ones, FP16, FP16) == 2048          # 2048 + 1 rounds back to 2048
    assert dot(ones, ones, FP16, FP32) == 4096
    rng = random.Random(5)
    x = [F(rng.randrange(1, 1001), 1000) for _ in range(1024)]
    y = [F(rng.randrange(1, 1001), 1000) for _ in range(1024)]
    xr, yr = [round_to(v, FP16) for v in x], [round_to(v, FP16) for v in y]
    exact = sum(a * b for a, b in zip(xr, yr))
    d16, d32 = dot(x, y, FP16, FP16), dot(x, y, FP16, FP32)
    assert d16 == F(1961, 8)
    assert d32 == F(247.58416748046875)
    assert abs(d16 - exact) / exact > F(9, 1000)
    assert abs(d32 - exact) / exact < F(1, 10 ** 6)
    k, u = 1024, unit_roundoff(FP32)
    assert abs(d32 - exact) <= k * u / (1 - k * u) * exact   # the classic bound for a sum of k terms


def test_tiles_and_peaks():
    assert mma_count(4096, 4096, 4096) == 256 ** 3
    assert mma_count(1000, 1000, 1000) == 63 ** 3
    assert padding_efficiency(1000, 1000, 1000) == F(125, 126) ** 3
    assert mma_count(32, 8, 16, (32, 8, 16)) == 1
    assert peak_flops(640, 64, 1530 * 10 ** 6) == 125_337_600_000_000
    assert peak_flops(432, 256, 1410 * 10 ** 6) == 311_869_440_000_000
    assert tile_intensity(16) == 8 and tile_intensity(128) == 64
    assert ridge_point(312 * 10 ** 12, 2 * 10 ** 12) == 156
