# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rife-boorstyn-frequency-estimator/. The authors are listed in prov/749SAD.jsonl.

import cmath
import math
import random

from rife_boorstyn_frequency_estimator import crb, fft, periodogram, rb_estimate


def tone(rng, n, omega, snr=None, phi=0.0):
    sd = math.sqrt(0.5 / snr) if snr else 0.0
    return [cmath.exp(1j * (omega * t + phi)) + (complex(rng.gauss(0, sd), rng.gauss(0, sd)) if sd else 0j) for t in range(n)]


def wrap(x):
    return (x + math.pi) % (2 * math.pi) - math.pi


def test_fft_matches_the_direct_dft() -> None:
    rng = random.Random(1)
    for k in (1, 2, 8, 64, 128):
        x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(k)]
        X = fft(x)
        for i in range(k):
            d = sum(x[t] * cmath.exp(-2j * math.pi * i * t / k) for t in range(k))
            assert abs(X[i] - d) < 1e-9


def test_exact_without_noise() -> None:
    rng = random.Random(2)
    for _ in range(60):
        n = rng.randrange(4, 50)
        om = rng.uniform(-math.pi, math.pi)
        e = wrap(rb_estimate(tone(rng, n, om, phi=rng.uniform(-3, 3))) - om)
        assert abs(e) < 1e-7


def test_matches_a_dense_grid_search() -> None:
    # Brute force: the maximizer of P over a dense grid of 4000 points. The RB
    # estimate is at least as good and lies within one grid step of it.
    rng = random.Random(3)
    n, m = 16, 4000
    grid = [-math.pi + 2 * math.pi * i / m for i in range(m)]
    for _ in range(6):
        r = tone(rng, n, rng.uniform(-3, 3), snr=10 ** 0.2, phi=rng.uniform(-3, 3))
        est = rb_estimate(r)
        g = max(grid, key=lambda w: periodogram(r, w))
        assert periodogram(r, est) >= periodogram(r, g) - 1e-9
        assert abs(wrap(est - g)) < 2 * math.pi / m


def test_mse_against_the_crb() -> None:
    n, trials = 32, 150
    ratio = {}
    for snr_db in (-6, 0, 10):
        snr = 10 ** (snr_db / 10)
        rng = random.Random(2)
        se = 0.0
        for _ in range(trials):
            om = rng.uniform(-3, 3)
            e = wrap(rb_estimate(tone(rng, n, om, snr, rng.uniform(-3, 3))) - om)
            se += e * e
        ratio[snr_db] = se / trials / crb(n, snr)
    assert 0.75 < ratio[0] < 1.5
    assert 0.75 < ratio[10] < 1.35
    assert ratio[-6] > 20  # below the threshold: outliers at a wrong peak
