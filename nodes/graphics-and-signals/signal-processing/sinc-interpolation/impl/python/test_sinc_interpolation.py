# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sinc-interpolation/. The authors are listed in prov/CYHRAN.jsonl.

import math
import random

from sinc_interpolation import sinc_interpolate, sinc_interpolate_many, sinc_interpolate_one_sine


def sinc(u: float) -> float:
    return 1.0 if u == 0 else math.sin(math.pi * u) / (math.pi * u)


def sinc_sum(amps, shifts, t: float) -> float:
    """A band-limited signal: a finite sum of shifted sincs (band 1/2 Hz, rate 1 Hz)."""
    return sum(a * sinc(t - s) for a, s in zip(amps, shifts))


def test_returns_the_samples_at_the_sample_times() -> None:
    rng = random.Random(1)
    for _ in range(20):
        start = rng.randint(-10, 10)
        period = rng.choice([0.5, 1.0, 0.125, 2.0])
        samples = [rng.uniform(-1, 1) for _ in range(rng.randint(1, 30))]
        for j, v in enumerate(samples):
            assert sinc_interpolate(samples, start, period, (start + j) * period) == v
            assert sinc_interpolate_one_sine(samples, start, period, (start + j) * period) == v


def test_integer_shifts_are_reconstructed_everywhere() -> None:
    # sum of a_k sinc(t - k) has the samples a_k; the series has only these terms.
    rng = random.Random(2)
    shifts = list(range(-4, 5))
    amps = [rng.uniform(-1, 1) for _ in shifts]
    samples = [sinc_sum(amps, shifts, n) for n in range(-30, 31)]
    for j in range(-300, 301):
        t = j / 37
        assert abs(sinc_interpolate(samples, -30, 1.0, t) - sinc_sum(amps, shifts, t)) <= 1e-12


def test_off_grid_sincs_truncation_error_is_about_a_quarter_over_n() -> None:
    # The shifts are not integers, so the samples decay like 1/n and the
    # truncated series (|n| <= N) misses by a constant over N.
    rng = random.Random(5)
    shifts = [rng.uniform(-5, 5) for _ in range(6)]
    amps = [rng.uniform(-1, 1) for _ in range(6)]
    times = [-3 + j * 0.05 for j in range(121)]
    scaled = []
    for n_max in (100, 200, 400):
        samples = [sinc_sum(amps, shifts, n) for n in range(-n_max, n_max + 1)]
        got = sinc_interpolate_many(samples, -n_max, 1.0, times)
        worst = max(abs(g - sinc_sum(amps, shifts, t)) for g, t in zip(got, times))
        scaled.append(n_max * worst)
    assert all(0.24 <= s <= 0.26 for s in scaled)


def test_error_for_a_half_sample_shift_matches_two_over_pi_squared_n() -> None:
    # x(t) = sinc(t - 1/2): the tail terms all have one sign, and the error at
    # time t tends to 2 |sin(pi t)| / (pi^2 N).
    for n_max in (200, 800):
        samples = [sinc(n - 0.5) for n in range(-n_max, n_max + 1)]
        for t in (0.5, 0.25):
            err = abs(sinc_interpolate(samples, -n_max, 1.0, t) - sinc(t - 0.5))
            predicted = 2 * abs(math.sin(math.pi * t)) / (math.pi**2 * n_max)
            assert abs(err / predicted - 1) <= 0.01


def test_one_sine_form_agrees() -> None:
    rng = random.Random(3)
    samples = [rng.uniform(-1, 1) for _ in range(50)]
    for _ in range(200):
        t = rng.uniform(-30, 60) * 0.5
        a = sinc_interpolate(samples, -10, 0.5, t)
        b = sinc_interpolate_one_sine(samples, -10, 0.5, t)
        assert abs(a - b) <= 1e-10


def test_period_scales_time() -> None:
    # Samples at fs = 4 of sinc(4 t - 0.3) equal samples at fs = 1 of sinc(t - 0.3).
    samples = [sinc(n - 0.3) for n in range(-40, 41)]
    for t in (0.1, 0.37, -1.2):
        assert abs(sinc_interpolate(samples, -40, 0.25, t / 4) - sinc_interpolate(samples, -40, 1.0, t)) <= 1e-12


def test_bounded_samples_can_give_logarithmic_growth() -> None:
    # The sum of |sinc(1/2 - n)| over |n| <= N is about (2/pi)(ln N + gamma + 2 ln 2);
    # samples with the signs of these terms give an output of that size.
    gamma = 0.5772156649015329
    for n_max in (100, 1000, 10000):
        samples = [math.copysign(1.0, sinc(0.5 - n)) for n in range(-n_max, n_max + 1)]
        value = sinc_interpolate(samples, -n_max, 1.0, 0.5)
        assert abs(value - 2 / math.pi * (math.log(n_max) + gamma + 2 * math.log(2))) <= 0.01
