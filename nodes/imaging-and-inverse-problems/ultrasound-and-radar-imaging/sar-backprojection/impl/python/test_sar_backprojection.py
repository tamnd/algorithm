# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sar-backprojection/. The authors are listed in prov/KA63T0.jsonl.

import math
import random

from sar_backprojection import backproject, backproject_exact, image_grid, simulate_compressed, upsample

F0, B, FS, T0, N = 300e6, 100e6, 120e6, 2 * 370 / 3.0e8, 64
STRAIGHT = [(-40.0 + 1.25 * p, 0.0, 0.0) for p in range(64)]
TARGETS = [(0.0, 400.0, 1.0), (5.0, 410.0, 0.5)]
XS = [-2.5 + 0.625 * i for i in range(9)]
YS = [397.5 + 0.625 * i for i in range(9)]
PIX = image_grid(XS, YS)


def curved_path(seed):
    rng = random.Random(seed)
    return [(x, 2.0 * math.sin(x / 15.0) + rng.uniform(-0.5, 0.5), rng.uniform(-0.3, 0.3)) for x, _, _ in STRAIGHT]


def test_point_target_focuses_with_gain_equal_to_the_pulse_count() -> None:
    data = simulate_compressed(STRAIGHT, TARGETS, F0, B, FS, T0, N)
    img = backproject(data, STRAIGHT, PIX, F0, FS, T0)
    best = max(range(len(PIX)), key=lambda i: abs(img[i]))
    assert PIX[best] == (0.0, 400.0)
    assert abs(img[best] - 64) < 0.02 * 64  # phase near 0 too


def test_matches_brute_force_exact_interpolation() -> None:
    data = simulate_compressed(STRAIGHT, TARGETS, F0, B, FS, T0, N)
    fast = backproject(data, STRAIGHT, PIX, F0, FS, T0)
    slow = backproject_exact(data, STRAIGHT, PIX, F0, B, FS, T0)
    assert max(abs(a - b) for a, b in zip(fast, slow)) < 0.01 * 64


def test_any_flight_path_focuses_when_it_is_known() -> None:
    path = curved_path(1)
    data = simulate_compressed(path, TARGETS, F0, B, FS, T0, N)
    right = backproject(data, path, [(0.0, 400.0), (5.0, 410.0)], F0, FS, T0)
    assert abs(right[0] - 64) < 0.03 * 64
    assert abs(right[1] - 32) < 0.03 * 64
    wrong = backproject(data, STRAIGHT, PIX, F0, FS, T0)
    assert max(abs(v) for v in wrong) < 0.3 * 64


def test_azimuth_resolution_is_lambda_r_over_2l() -> None:
    data = simulate_compressed(STRAIGHT, TARGETS[:1], F0, B, FS, T0, N)
    cut = [abs(v) for v in backproject(data, STRAIGHT, [(0.25 * k, 400.0) for k in range(13)], F0, FS, T0)]
    first_null = min(range(13), key=lambda k: cut[k])
    lam, length = 3.0e8 / F0, 64 * 1.25
    assert abs(0.25 * first_null - lam * 400.0 / (2 * length)) <= 0.25
    assert cut[first_null] < 0.03 * cut[0]


def test_linear_in_the_data() -> None:
    d1 = simulate_compressed(STRAIGHT, TARGETS[:1], F0, B, FS, T0, N)
    d2 = simulate_compressed(STRAIGHT, TARGETS[1:], F0, B, FS, T0, N)
    both = [[a + b for a, b in zip(r1, r2)] for r1, r2 in zip(d1, d2)]
    i1 = backproject(d1, STRAIGHT, PIX, F0, FS, T0)
    i2 = backproject(d2, STRAIGHT, PIX, F0, FS, T0)
    i12 = backproject(both, STRAIGHT, PIX, F0, FS, T0)
    assert max(abs(a + b - c) for a, b, c in zip(i1, i2, i12)) < 1e-9


def test_upsample_keeps_the_samples() -> None:
    rng = random.Random(3)
    row = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(16)]
    fine = upsample(row, 4)
    assert max(abs(fine[4 * j] - row[j]) for j in range(16)) < 1e-9
