# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/comb-pilot-channel-estimation/. The authors are listed in prov/VPF3QG.jsonl.

import math
import random

import cbb
from comb_pilot_channel_estimation import estimate, pilot_positions

S = 1 / math.sqrt(2)


def qpsk(rng: random.Random, n: int) -> list[complex]:
    return [complex(rng.choice((S, -S)), rng.choice((S, -S))) for _ in range(n)]


def channel(rng: random.Random, powers: tuple[float, ...], n: int) -> tuple[list[complex], list[complex]]:
    h = [cbb.cn(rng, p) for p in powers]
    return h, cbb.dft(h + [0j] * (n - len(h)))


def linear_reference(points: list[tuple[float, complex]], k: float) -> complex:
    """Piecewise linear interpolation by a search over the sorted points (a plain reference)."""
    for (u, a), (v, b) in zip(points, points[1:]):
        if u <= k <= v:
            return a + (b - a) * (k - u) / (v - u)
    raise ValueError("k outside the points")


def test_pilots_are_kept_and_spacing_one_is_plain_least_squares() -> None:
    rng = random.Random(1)
    n = 32
    _, hf = channel(rng, (0.5, 0.3, 0.2), n)
    x = qpsk(rng, n)
    y = cbb.awgn(rng, [a * b for a, b in zip(hf, x)], 0.1)
    assert max(abs(e - yk / xk) for e, yk, xk in zip(estimate(y, x, 1), y, x)) < 1e-12
    for d, k0 in ((4, 0), (4, 3), (8, 5)):
        ps = pilot_positions(n, d, k0)
        xp = [x[p] for p in ps]
        for order in (1, 2):
            est = estimate(y, xp, d, k0, order)
            assert max(abs(est[p] - y[p] / x[p]) for p in ps) < 1e-12


def test_linear_matches_a_reference_with_wrap_around() -> None:
    rng = random.Random(2)
    n, d, k0 = 32, 4, 2
    ps = pilot_positions(n, d, k0)
    y = [cbb.cn(rng, 1.0) for _ in range(n)]
    xp = qpsk(rng, len(ps))
    hp = [y[p] / x for p, x in zip(ps, xp)]
    # The pilots on an unrolled axis: the last one moved down by N and the first one moved up by N.
    points = [(ps[-1] - n, hp[-1])] + list(zip(ps, hp)) + [(ps[0] + n, hp[0])]
    est = estimate(y, xp, d, k0)
    for k in range(n):
        kk = k if k >= ps[0] - d else k + n
        assert abs(est[k] - linear_reference(points, kk)) < 1e-12


def test_error_bound_without_noise() -> None:
    # Theorem: |error| <= (D^2 / 8) max |H''| <= (pi^2 D^2 / (2 N^2)) sum of l^2 |h_l|.
    rng = random.Random(3)
    n = 64
    for d in (2, 4, 8):
        for _ in range(20):
            h, hf = channel(rng, (0.4, 0.3, 0.2, 0.1), n)
            est = estimate(hf, [1] * (n // d), d)
            bound = math.pi ** 2 * d * d / (2 * n * n) * sum(l * l * abs(c) for l, c in enumerate(h))
            assert max(abs(a - b) for a, b in zip(est, hf)) <= bound + 1e-12


def test_quadratic_has_less_bias_on_a_smooth_channel() -> None:
    # Measurement: 3 taps of power 0.5, 0.3, 0.2, N = 64, no noise, 30 channels.
    # D = 4: linear about 6.5e-4, quadratic about 9e-5 mean squared error.
    rng = random.Random(4)
    n, d = 64, 4
    e1 = e2 = 0.0
    for _ in range(30):
        _, hf = channel(rng, (0.5, 0.3, 0.2), n)
        a = estimate(hf, [1] * (n // d), d, order=1)
        b = estimate(hf, [1] * (n // d), d, order=2)
        e1 += sum(abs(u - v) ** 2 for u, v in zip(a, hf))
        e2 += sum(abs(u - v) ** 2 for u, v in zip(b, hf))
    assert e2 < e1 / 3


def test_noise_gain_on_a_flat_channel() -> None:
    # Closed form for a flat channel: at fraction t between two pilots the error is (1 - t) W_a + t W_b,
    # so the mean squared error over the spacing is mean of ((1 - t)^2 + t^2) N0 = 0.6875 N0 for D = 4.
    # Quadratic: mean of the squared Lagrange weights = 0.81543 N0. 400 symbols of N = 64, seed 5.
    rng = random.Random(5)
    n, d, n0, hval = 64, 4, 0.1, 0.7 - 0.2j
    f1 = sum((1 - r / d) ** 2 + (r / d) ** 2 for r in range(d)) / d
    f2 = 0.0
    for r in range(d):
        t = r / d
        f2 += ((t * (t - 1) / 2) ** 2 + ((1 - t) * (1 + t)) ** 2 + (t * (t + 1) / 2) ** 2) / d
    assert abs(f1 - 0.6875) < 1e-12
    assert abs(f2 - 0.81543) < 1e-5
    e1 = e2 = 0.0
    trials = 400
    for _ in range(trials):
        xp = qpsk(rng, n // d)
        y = [0j] * n
        for i, p in enumerate(range(0, n, d)):
            y[p] = hval * xp[i] + cbb.cn(rng, n0)
        a = estimate(y, xp, d, order=1)
        b = estimate(y, xp, d, order=2)
        e1 += sum(abs(u - hval) ** 2 for u in a)
        e2 += sum(abs(u - hval) ** 2 for u in b)
    assert 0.93 < e1 / (trials * n) / (f1 * n0) < 1.07
    assert 0.93 < e2 / (trials * n) / (f2 * n0) < 1.07
