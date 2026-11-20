# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sofi/. The authors are listed in prov/70NF24.jsonl.

import math
import random
from fractions import Fraction as F

from sofi import (
    cumulant,
    cumulant_by_partitions,
    lagged,
    markov_blinking,
    mean_image,
    simulate_movie,
    sofi_image,
)


def test_moment_formulas_match_partition_formula():
    rng = random.Random(1)
    for order in (2, 3, 4):
        xs = [[F(rng.randint(-5, 9)) for _ in range(12)] for _ in range(order)]
        assert cumulant(xs) == cumulant_by_partitions(xs)


def test_bernoulli_cumulants():
    s = [F(1)] * 3 + [F(0)] * 7  # the empirical law is Bernoulli(3/10)
    rho = F(3, 10)
    assert cumulant([s, s]) == rho * (1 - rho) == F(21, 100)
    assert cumulant([s, s, s]) == rho * (1 - rho) * (1 - 2 * rho) == F(84, 1000)
    k4 = rho * (1 - rho) * (1 - 6 * rho * (1 - rho))
    assert cumulant([s, s, s, s]) == k4 == F(-546, 10000)


def test_single_emitter_is_exact_and_background_free():
    rng = random.Random(2)
    blink = [F(rng.randint(0, 1)) for _ in range(40)]
    psf = [F(1, 9), F(1, 2), F(1), F(1, 2), F(1, 9)]
    eps, bg = F(7), F(3)
    movie = [[[bg + eps * u * st for u in psf]] for st in blink]
    for order in (2, 3, 4):
        img = sofi_image(movie, order)
        k = cumulant(lagged(blink, tuple(range(order))))
        for j, u in enumerate(psf):
            assert img[0][j] == u ** order * eps ** order * k


def test_lags_remove_white_noise():
    rng = random.Random(3)
    a, b, sigma = 0.2, 0.2, 0.5
    s = markov_blinking(rng, 40000, a, b)
    noisy = [v + rng.gauss(0.0, sigma) for v in s]
    rho = a / (a + b)
    var = rho * (1 - rho)
    lag1 = var * (1 - a - b)
    c0 = cumulant(lagged(noisy, (0, 0)))
    c1 = cumulant(lagged(noisy, (0, 1)))
    assert abs(c0 - (var + sigma ** 2)) < 0.02
    assert abs(c1 - lag1) < 0.02


def test_markov_lag_covariance():
    rng = random.Random(4)
    a, b = 0.1, 0.2
    s = markov_blinking(rng, 50000, a, b)
    rho = a / (a + b)
    assert abs(sum(s) / len(s) - rho) < 0.02
    assert abs(cumulant(lagged(s, (0, 1))) - rho * (1 - rho) * (1 - a - b)) < 0.015


def test_second_order_resolves_two_emitters():
    # Two emitters 2 sigma apart: the mean image has no dip between them,
    # the second order SOFI image has one.
    rng = random.Random(5)
    sigma = 2.0
    movie = simulate_movie(rng, (1, 15), [(0, 5, 1.0), (0, 9, 1.0)], sigma, 4000,
                           0.3, 0.3, background=2.0, noise=0.05)
    wf = mean_image(movie)[0]
    s2 = sofi_image(movie, 2)[0]
    assert wf[7] > wf[5] and wf[7] > wf[9]
    assert s2[7] < 0.85 * min(s2[5], s2[9])


def test_order_n_narrows_a_gaussian_by_sqrt_n():
    # One emitter: the SOFI image of order n is U^n times a constant, a
    # Gaussian of width sigma / sqrt(n).
    rng = random.Random(6)
    sigma = 1.5
    blink = markov_blinking(rng, 200, 0.3, 0.3)
    psf = [math.exp(-(j - 6) ** 2 / (2 * sigma ** 2)) for j in range(13)]
    movie = [[[u * st for u in psf]] for st in blink]
    for order in (2, 3, 4):
        img = sofi_image(movie, order)[0]
        for j in range(13):
            want = math.exp(-order * (j - 6) ** 2 / (2 * sigma ** 2))
            assert abs(img[j] / img[6] - want) < 1e-9
