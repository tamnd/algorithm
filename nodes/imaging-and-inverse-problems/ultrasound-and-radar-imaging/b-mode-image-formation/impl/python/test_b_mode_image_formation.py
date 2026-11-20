# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/b-mode-image-formation/. The authors are listed in prov/P3DHGZ.jsonl.

import math
import random

from b_mode_image_formation import (analytic_signal, b_mode, envelope, log_compress, sample_depths, scan_convert,
                                    simulate_sector_lines)

N, FS, F0, SIGMA, T0 = 64, 40.0, 5.0, 0.1, 6.5
DEG = math.pi / 180
ANGLES = [(-20 + 2 * k) * DEG for k in range(21)]


def test_real_part_is_the_input() -> None:
    rng = random.Random(5501)
    for n in (64, 45):
        x = [rng.uniform(-1, 1) for _ in range(n)]
        a = analytic_signal(x)
        assert all(abs(v.real - xi) < 1e-12 for v, xi in zip(a, x))


def test_envelope_of_a_whole_number_of_cycles_is_constant() -> None:
    x = [1.5 * math.cos(2 * math.pi * 8 * q / N + 0.3) for q in range(N)]
    assert all(abs(e - 1.5) < 1e-12 for e in envelope(x))


def test_envelope_of_a_gaussian_pulse() -> None:
    x = [math.exp(-((q / FS - 0.8) ** 2) / (2 * SIGMA ** 2)) * math.cos(2 * math.pi * F0 * (q / FS - 0.8))
         for q in range(N)]
    g = [math.exp(-((q / FS - 0.8) ** 2) / (2 * SIGMA ** 2)) for q in range(N)]
    assert max(abs(a - b) for a, b in zip(envelope(x), g)) < 2e-3


def test_depth_axis_is_half_the_two_way_path() -> None:
    d = sample_depths(N, T0, FS)
    assert abs(d[0] - 1.54 * 6.5 / 2) < 1e-12
    assert abs(d[1] - d[0] - 1.54 / (2 * FS)) < 1e-12


def test_log_compression_levels() -> None:
    assert log_compress([[1.0, 0.1, 0.01, 0.001, 0.0]], 40) == [[255, 128, 0, 0, 0]]
    # gray levels depend only on ratios to the brightest value
    assert log_compress([[3.0, 0.3], [0.03, 0.0]], 60) == log_compress([[1.0, 0.1], [0.01, 0.0]], 60)


def test_scan_conversion_is_exact_for_bilinear_functions() -> None:
    depths = sample_depths(N, T0, FS)

    def f(r, th):
        return 2 + 0.5 * r + 3 * th + r * th

    polar = [[f(r, th) for r in depths] for th in ANGLES]
    xs = [-1.2, -0.37, 0.0, 0.41, 1.1]
    zs = [5.2, 5.55, 6.0]
    out = scan_convert(polar, ANGLES, depths, xs, zs)
    for i, z in enumerate(zs):
        for j, x in enumerate(xs):
            assert abs(out[i][j] - f(math.hypot(x, z), math.atan2(x, z))) < 1e-9


def test_pixels_outside_the_sector_are_zero() -> None:
    depths = sample_depths(N, T0, FS)
    polar = [[1.0] * N for _ in ANGLES]
    out = scan_convert(polar, ANGLES, depths, [-4.0, 0.0, 4.0], [1.0, 5.5, 9.0])
    assert out == [[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]]


def test_point_scatterer_appears_at_its_place() -> None:
    lines = simulate_sector_lines(ANGLES, N, T0, FS, F0, SIGMA, [(5.6, 4 * DEG, 1.0)], 2 * DEG)
    img = b_mode(lines, 40, t0=T0, fs=FS)
    depths = sample_depths(N, T0, FS)
    xs = [round(-1.5 + 0.1 * k, 10) for k in range(31)]
    zs = [round(5.0 + 0.05 * k, 10) for k in range(25)]
    sc = scan_convert(img, ANGLES, depths, xs, zs)
    v, i, j = max((v, i, j) for i, row in enumerate(sc) for j, v in enumerate(row))
    assert (zs[i], xs[j]) == (5.6, 0.4)
    assert v > 240


def test_tgc_balances_attenuation() -> None:
    # 5 dB/mm one way is 10 dB per mm of depth on the two-way path
    lines = simulate_sector_lines(ANGLES, N, T0, FS, F0, SIGMA, [(5.3, 0.0, 1.0), (5.9, 0.0, 1.0)], 2 * DEG, 5.0)
    depths = sample_depths(N, T0, FS)
    q1 = min(range(N), key=lambda q: abs(depths[q] - 5.3))
    q2 = min(range(N), key=lambda q: abs(depths[q] - 5.9))
    raw = b_mode(lines, 40, 0.0, T0, FS)[10]
    fixed = b_mode(lines, 40, 10.0, T0, FS)[10]
    assert max(raw[q1 - 3:q1 + 4]) - max(raw[q2 - 3:q2 + 4]) > 30
    assert abs(max(fixed[q1 - 3:q1 + 4]) - max(fixed[q2 - 3:q2 + 4])) <= 1
