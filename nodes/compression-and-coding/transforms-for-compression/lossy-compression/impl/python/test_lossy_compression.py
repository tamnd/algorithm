# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lossy-compression/. The authors are listed in prov/JRTS3R.jsonl.

import math
import random

from lossy_compression import (
    binary_entropy,
    blahut_arimoto,
    hamming_matrix,
    mse,
    psnr,
    rd_bernoulli,
    rd_gaussian,
    rd_point_at,
    squared_error_matrix,
)


def test_psnr_example() -> None:
    x = [52, 55, 61, 66]
    y = [54, 55, 60, 70]
    assert mse(x, y) == 5.25
    assert abs(psnr(x, y) - 10 * math.log10(255 * 255 / 5.25)) < 1e-12
    assert abs(psnr(x, y) - 40.9292) < 1e-4
    assert psnr(x, x) == math.inf


def test_closed_forms() -> None:
    assert abs(rd_bernoulli(0.25, 0.1) - (binary_entropy(0.25) - binary_entropy(0.1))) < 1e-15
    assert abs(rd_bernoulli(0.25, 0.1) - 0.342283) < 1e-6
    assert rd_bernoulli(0.25, 0.25) == 0.0
    assert rd_bernoulli(0.5, 0.0) == 1.0
    assert abs(rd_gaussian(1.0, 0.25) - 1.0) < 1e-15
    assert rd_gaussian(4.0, 5.0) == 0.0
    # The 6.02 dB per bit rule: D(R) = var 2^(-2R), so SNR = 20 log10(2) R.
    for r in (1, 2, 3):
        d = 2.0 ** (-2 * r)
        assert abs(rd_gaussian(1.0, d) - r) < 1e-12
        assert abs(10 * math.log10(1.0 / d) - 6.0206 * r) < 1e-3


def test_blahut_arimoto_bernoulli() -> None:
    for p in (0.1, 0.3, 0.5):
        for beta in (0.5, 1.0, 2.0, 3.0, 5.0):
            r, d, _ = blahut_arimoto([1 - p, p], hamming_matrix(2), beta)
            assert abs(r - rd_bernoulli(p, d)) < 1e-6
            if 1 / (1 + math.exp(beta)) < min(p, 1 - p):
                # Where the curve is above 0, its point of slope -beta (in
                # nats) has D = 1 / (1 + e^beta) for Hamming distortion.
                assert abs(d - 1 / (1 + math.exp(beta))) < 1e-6
            else:
                assert r < 1e-6 and abs(d - min(p, 1 - p)) < 1e-6


def test_blahut_arimoto_gaussian() -> None:
    h, k = 0.25, 24  # a grid on [-6, 6] that stands in for the Gaussian
    xs = [i * h for i in range(-k, k + 1)]
    w = [math.exp(-x * x / 2) for x in xs]
    s = sum(w)
    p = [v / s for v in w]
    var = sum(a * x * x for a, x in zip(p, xs))
    dm = squared_error_matrix(xs, xs)
    for beta in (1.0, 4.0):
        r, d, _ = blahut_arimoto(p, dm, beta, iters=3000, tol=1e-10)
        assert abs(r - rd_gaussian(var, d)) < 1e-3
        assert abs(d - 1 / (2 * beta)) < 1e-3


def test_target_distortion() -> None:
    r, d = rd_point_at([0.75, 0.25], hamming_matrix(2), 0.1)
    assert abs(d - 0.1) < 1e-6
    assert abs(r - rd_bernoulli(0.25, 0.1)) < 1e-5


def test_rd_is_convex_and_decreasing_random_sources() -> None:
    rng = random.Random(7)
    for _ in range(5):
        k = rng.randint(2, 4)
        w = [rng.random() + 0.05 for _ in range(k)]
        s = sum(w)
        p = [v / s for v in w]
        pts = [blahut_arimoto(p, hamming_matrix(k), b)[:2] for b in (0.5, 1.0, 2.0, 4.0, 8.0)]
        pts.sort(key=lambda t: t[1])
        for (r1, d1), (r2, d2) in zip(pts, pts[1:]):
            assert d1 <= d2 + 1e-12 and r1 >= r2 - 1e-9
        hp = -sum(v * math.log2(v) for v in p)
        for r, _ in pts:
            assert -1e-12 <= r <= hp + 1e-9
