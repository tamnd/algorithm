# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-subtraction/. The authors are listed in prov/EPV4TJ.jsonl.

import cmath
import math
import random

import pytest

from spectral_subtraction import dft, noise_estimate, periodic_hann, spectral_subtraction, subtract_bins


def test_bins_of_the_page_example() -> None:
    power = [10, 1, 3, 0.5, 25, 2]
    spec = [complex(math.sqrt(p), 0) for p in power]
    out = subtract_bins(spec, [1.0] * 6, alpha=2.0, beta=1 / 25)
    want = [8, 1 / 25, 1, 1 / 25, 23, 1 / 25]
    assert max(abs(abs(o) ** 2 - w) for o, w in zip(out, want)) < 1e-12


def test_dft_matches_definition() -> None:
    rng = random.Random(5601)
    for n in (2, 6, 8, 32):
        a = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        want = [sum(a[t] * cmath.exp(-2j * math.pi * k * t / n) for t in range(n)) for k in range(n)]
        assert max(abs(u - v) for u, v in zip(dft(a), want)) < 1e-12
        assert max(abs(u - v) for u, v in zip(dft(dft(a), inverse=True), a)) < 1e-12


def test_window_overlap_adds_to_one() -> None:
    for length in (4, 16, 64):
        w = periodic_hann(length)
        assert all(abs(w[n] + w[n + length // 2] - 1) < 1e-15 for n in range(length // 2))


def test_no_subtraction_reconstructs_the_input() -> None:
    rng = random.Random(5602)
    for length in (8, 32):
        y = [rng.gauss(0, 1) for _ in range(301)]
        out = spectral_subtraction(y, [1.0] * length, length, alpha=0.0, beta=0.0)
        assert len(out) == len(y)
        assert max(abs(a - b) for a, b in zip(out, y)) < 1e-12


def test_exact_floor_on_periodic_noise() -> None:
    """Noise with period H: every frame sees the same spectrum, equal to N_hat. With
    alpha = 2 each bin drops to the floor beta * N_hat, so the output is sqrt(beta) * y."""
    rng = random.Random(5603)
    length, hop = 32, 16
    cycle = [rng.gauss(0, 1) for _ in range(hop)]
    v = cycle * 40
    n_hat = noise_estimate(v, length)
    for frame in range(5):  # every interior frame has the same spectrum
        w = periodic_hann(length)
        spec = dft([w[n] * v[frame * hop + n] for n in range(length)])
        assert max(abs(abs(s) ** 2 - nh) for s, nh in zip(spec, n_hat)) < 1e-9
    y = v[:hop * 20]
    out = spectral_subtraction(y, n_hat, length, alpha=2.0, beta=0.01)
    inner = range(hop, len(y) - hop)  # the zero padding at the ends changes the outer frames
    assert max(abs(out[n] - 0.1 * y[n]) for n in inner) < 1e-9


def complex_gauss(rng, sigma2):
    s = math.sqrt(sigma2 / 2)
    return complex(rng.gauss(0, s), rng.gauss(0, s))


def test_white_noise_survival_and_residual_match_the_formula() -> None:
    """For |Y|^2 / sigma^2 ~ Exp(1): a bin survives above the floor with probability
    exp(-(alpha + beta)), and the mean output power is sigma^2 (beta + exp(-(alpha + beta)))."""
    rng = random.Random(5604)
    sigma2, count = 2.0, 200000
    for alpha, beta in ((1.0, 0.0), (2.0, 0.04), (4.0, 0.01)):
        spec = [complex_gauss(rng, sigma2) for _ in range(count)]
        out = subtract_bins(spec, [sigma2] * count, alpha, beta)
        alive = sum(1 for o in out if abs(o) ** 2 > beta * sigma2 * (1 + 1e-12)) / count
        power = sum(abs(o) ** 2 for o in out) / count
        assert abs(alive - math.exp(-(alpha + beta))) < 0.005
        assert abs(power / sigma2 - (beta + math.exp(-(alpha + beta)))) < 0.01


def test_full_pipeline_on_white_noise_leaves_the_predicted_floor() -> None:
    rng = random.Random(5605)
    length = 64
    v = [rng.gauss(0, 1) for _ in range(length * 400)]
    n_hat = noise_estimate(v, length)
    y = [rng.gauss(0, 1) for _ in range(length * 200)]
    alpha, beta = 2.0, 0.04
    out = spectral_subtraction(y, n_hat, length, alpha, beta)
    ratio = sum(o * o for o in out) / sum(s * s for s in y)
    # the overlap-add of two frames with Hann windows loses power in a way that depends on
    # correlation, so only the order of magnitude is checked: near beta + e^-(alpha + beta) = 0.17
    assert 0.05 < ratio < 0.25


def test_improves_snr_of_a_tone_in_noise() -> None:
    rng = random.Random(5606)
    length, total = 64, 64 * 100
    x = [math.cos(2 * math.pi * 8 * n / length) for n in range(total)]  # on bin 8
    n_hat = noise_estimate([rng.gauss(0, 0.5) for _ in range(length * 200)], length)
    y = [s + rng.gauss(0, 0.5) for s in x]
    out = spectral_subtraction(y, n_hat, length, alpha=2.0, beta=0.01)
    before = sum((a - b) ** 2 for a, b in zip(y, x))
    after = sum((a - b) ** 2 for a, b in zip(out, x))
    assert after < before / 4


def test_errors() -> None:
    with pytest.raises(ValueError):
        spectral_subtraction([0.0] * 10, [1.0] * 7, 7)
    with pytest.raises(ValueError):
        noise_estimate([0.0] * 3, 8)
