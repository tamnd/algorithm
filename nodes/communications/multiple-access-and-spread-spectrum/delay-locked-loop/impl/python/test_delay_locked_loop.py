# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delay-locked-loop/. The authors are listed in prov/WXMG9W.jsonl.

import math
import random

from delay_locked_loop import (
    correlate,
    discriminator,
    dll,
    mseq_autocorrelation,
    mseq_bits,
    received_block,
    s_curve,
    slope,
)

C31 = mseq_bits([5, 2, 0])
N = 31


def test_autocorrelation_matches_the_sampled_code() -> None:
    m = 31 * 64
    r = received_block(random.Random(0), C31, 0.0, m)
    for x in (0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 3.0, -0.5):
        got = correlate(r, C31, x).real
        assert abs(got - mseq_autocorrelation(x, N)) < 1e-12


def test_s_curve_is_linear_inside_the_early_late_window() -> None:
    delta = 0.5
    kd = slope(delta, N)
    assert abs(kd - 32 / 15) < 1e-12
    for eps in (-0.45, -0.3, -0.1, 0.0, 0.2, 0.4):
        assert abs(s_curve(eps, delta, N) - kd * eps) < 1e-12
    # Far from the peak both correlators see the floor and the output is zero.
    for eps in (1.6, 2.5, -3.0):
        assert s_curve(eps, delta, N) == 0.0


def test_sampled_discriminator_follows_the_s_curve() -> None:
    rng = random.Random(1)
    m = 499
    for eps in (-0.4, -0.2, 0.0, 0.1, 0.3):
        r = received_block(rng, C31, 10.0 + eps, m, 1.0, rng.uniform(0, 2 * math.pi))
        d = discriminator(correlate(r, C31, 10.0 - 0.5), correlate(r, C31, 10.0 + 0.5))
        assert abs(d - s_curve(eps, 0.5, N)) < 0.02


def test_converges_from_a_third_of_a_chip() -> None:
    rng = random.Random(2)
    m, tau = 499, 7.3
    blocks = (received_block(rng, C31, tau, m, 1.0, rng.uniform(0, 2 * math.pi)) for _ in range(30))
    hist = dll(blocks, C31, 7.0, 0.5, 0.5, slope(0.5, N))
    assert abs(tau - hist[0]) > 0.29
    assert all(abs(tau - h) < 0.02 for h in hist[10:])


def test_lag_of_a_first_order_loop_under_drift() -> None:
    rng = random.Random(3)
    m, v, g = 499, 0.004, 0.2
    taus = [5.0 + v * k for k in range(201)]
    blocks = (received_block(rng, C31, taus[k], m) for k in range(200))
    hist = dll(blocks, C31, 5.0, 0.5, g, slope(0.5, N))
    # The estimate after block k used the block with delay taus[k]; the lag settles at v (1 - g) / g.
    lags = [taus[k] - hist[k + 1] for k in range(100, 200)]
    expected = v * (1 - g) / g
    assert abs(sum(lags) / len(lags) - expected) < 0.005


def test_jitter_matches_the_linear_loop_theory() -> None:
    rng = random.Random(4)
    m, n0, delta, g, tau = 127, 2.0, 0.5, 0.2, 3.0
    kd = slope(delta, N)
    # Open loop: the noise of D / kd at zero error.
    v = []
    for _ in range(1500):
        r = received_block(rng, C31, tau, m, 1.0, rng.uniform(0, 2 * math.pi), n0)
        v.append(discriminator(correlate(r, C31, tau - delta), correlate(r, C31, tau + delta)) / kd)
    mean_v = sum(v) / len(v)
    var_v = sum((x - mean_v) ** 2 for x in v) / (len(v) - 1)
    assert abs(mean_v) < 0.01
    # Closed loop: eps(k + 1) = (1 - g) eps(k) - g v(k) has variance g var_v / (2 - g).
    blocks = (received_block(rng, C31, tau, m, 1.0, rng.uniform(0, 2 * math.pi), n0) for _ in range(2000))
    hist = dll(blocks, C31, tau, delta, g, kd)
    errs = [tau - h for h in hist[100:]]
    me = sum(errs) / len(errs)
    var_e = sum((x - me) ** 2 for x in errs) / (len(errs) - 1)
    ratio = var_e / (g * var_v / (2 - g))
    assert 0.5 < ratio < 2.0
