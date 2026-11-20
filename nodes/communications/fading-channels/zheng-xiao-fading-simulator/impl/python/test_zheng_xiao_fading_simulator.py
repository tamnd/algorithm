# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zheng-xiao-fading-simulator/. The authors are listed in prov/97VH88.jsonl.

import math
import random

from zheng_xiao_fading_simulator import (
    draw_parameters,
    fourth_moment,
    gains,
    j0,
    theta_average,
    zheng_xiao,
)

M = 8


def j0_series(x):
    """J0 by its power series, a second method for small x."""
    s, t, k = 0.0, 1.0, 0
    while abs(t) > 1e-18 or k < 5:
        s += t
        k += 1
        t *= -(x / 2.0) ** 2 / (k * k)
    return s


def test_angles_cover_a_quarter_circle() -> None:
    rng = random.Random(9701)
    for _ in range(100):
        alpha, psi, phi = draw_parameters(M, rng)
        assert len(alpha) == len(psi) == len(phi) == M
        assert all(0.0 <= a <= math.pi / 2 for a in alpha)
        steps = [alpha[n + 1] - alpha[n] for n in range(M - 1)]
        assert all(abs(s - 2 * math.pi / (4 * M)) < 1e-12 for s in steps)


def test_exact_autocorrelation_over_theta() -> None:
    # the theorem: the average over theta is J0(x) for any M, even M = 1
    for m in (1, 2, 8):
        for ft in (0.1, 0.38274, 1.0, 3.0, 10.0):
            x = 2 * math.pi * ft
            assert abs(theta_average(m, x) - j0(x)) < 1e-9
    for x in (0.5, 2.0, 5.0):
        assert abs(j0(x) - j0_series(x)) < 1e-10


def test_ensemble_power_and_autocorrelation() -> None:
    rng = random.Random(9702)
    trials = 4000
    fd = 1.0
    lags = [0.1, 0.25, 0.5, 1.0, 5.0]
    acc = [0j] * len(lags)
    cross = 0.0
    power = 0.0
    for _ in range(trials):
        h = zheng_xiao(M, fd, [3.0] + [3.0 + t for t in lags], rng)
        power += abs(h[0]) ** 2
        cross += h[1].real * h[0].imag
        for k in range(len(lags)):
            acc[k] += h[k + 1] * h[0].conjugate()
    assert abs(power / trials - 1.0) < 0.07
    assert abs(cross / trials) < 0.05  # the quadratures are uncorrelated at any lag
    for k, t in enumerate(lags):
        assert abs(acc[k] / trials - j0(2 * math.pi * fd * t)) < 0.07


def test_fourth_moment_shows_the_2006_correction() -> None:
    # E|h|^4 = 2 for Rayleigh fading. The phase per sinusoid gives 2 - 1/(2M) = 1.9375,
    # one common phase gives 3 - 3/(2M) = 2.8125 at t = 0.
    assert fourth_moment(M, False) == 1.9375 and fourth_moment(M, True) == 2.8125
    # 12000 draws: the standard error is about 0.04 per-path and 0.09 common, and the two means differ by 0.875.
    trials = 12000
    for common, tol, seed in ((False, 0.15, 9703), (True, 0.35, 9704)):
        rng = random.Random(seed)
        s = 0.0
        for _ in range(trials):
            alpha, psi, phi = draw_parameters(M, rng, common_phase=common)
            h = gains(1.0, [0.0], alpha, psi, phi)[0]
            s += abs(h) ** 4
        assert abs(s / trials - fourth_moment(M, common)) < tol


def test_omega_scales_power() -> None:
    rng = random.Random(9705)
    alpha, psi, phi = draw_parameters(M, rng)
    a = gains(2.0, [0.0, 0.1, 0.7], alpha, psi, phi, omega=1.0)
    b = gains(2.0, [0.0, 0.1, 0.7], alpha, psi, phi, omega=4.0)
    assert all(abs(q - 2 * p) < 1e-12 for p, q in zip(a, b))
