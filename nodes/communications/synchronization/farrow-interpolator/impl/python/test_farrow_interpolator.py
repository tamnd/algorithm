# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/farrow-interpolator/. The authors are listed in prov/9JVEXY.jsonl.

import math
import random

from farrow_interpolator import (
    CUBIC_LAGRANGE,
    farrow,
    impulse_response,
    nco_times,
    parabolic,
    resample,
)


def lagrange_direct(x, m, mu):
    """The Lagrange polynomial through (n, x[m + n]) for n = -1, 0, 1, 2, evaluated at mu."""
    nodes = (-1, 0, 1, 2)
    total = 0j
    for i, ni in enumerate(nodes):
        w = 1.0
        for k, nk in enumerate(nodes):
            if k != i:
                w *= (mu - nk) / (ni - nk)
        total += w * x[m + ni]
    return total


def test_exact_on_cubics():
    rng = random.Random(1)
    for _ in range(50):
        p = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(4)]

        def f(t):
            return ((p[3] * t + p[2]) * t + p[1]) * t + p[0]

        x = [f(n) for n in range(10)]
        for _ in range(10):
            t = rng.uniform(1, 7)
            m = math.floor(t)
            assert abs(farrow(x, m, t - m) - f(t)) < 1e-9


def test_matches_direct_lagrange():
    rng = random.Random(2)
    x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(40)]
    for _ in range(200):
        m = rng.randrange(1, 37)
        mu = rng.random()
        assert abs(farrow(x, m, mu) - lagrange_direct(x, m, mu)) < 1e-12


def test_passes_through_samples():
    rng = random.Random(3)
    x = [rng.gauss(0, 1) for _ in range(20)]
    for b in (CUBIC_LAGRANGE, parabolic(0.5), parabolic(0.43)):
        for m in range(1, 17):
            assert abs(farrow(x, m, 0.0, b) - x[m]) < 1e-15


def test_sinusoid_error_within_bound():
    f = 0.05
    w = 2 * math.pi * f
    bound = 3.0 / 128.0 * w ** 4
    x = [math.cos(w * n + 0.4) for n in range(80)]
    worst = 0.0
    for i in range(1, 7600):
        t = 1 + i / 100.0
        m = math.floor(t)
        if m + 2 >= len(x):
            break
        err = abs(farrow(x, m, t - m) - math.cos(w * t + 0.4))
        worst = max(worst, err)
    assert worst <= bound
    assert worst > 0.3 * bound


def test_parabolic_exact_on_lines_and_symmetric():
    rng = random.Random(4)
    for alpha in (0.5, 0.43, 0.0):
        b = parabolic(alpha)
        x = [2.0 - 0.7 * n for n in range(8)]
        for _ in range(20):
            t = rng.uniform(1, 5)
            m = math.floor(t)
            assert abs(farrow(x, m, t - m, b) - (2.0 - 0.7 * t)) < 1e-12
        for _ in range(20):
            t = rng.uniform(-2, 2)
            assert abs(impulse_response(t, b) - impulse_response(-t, b)) < 1e-12


def test_constant_input_gives_constant_output():
    for b in (CUBIC_LAGRANGE, parabolic(0.5), parabolic(0.43)):
        assert abs(sum(b[0]) - 1.0) < 1e-15
        for row in b[1:]:
            assert abs(sum(row)) < 1e-15
        x = [2.5] * 8
        for mu in (0.0, 0.1, 0.5, 0.99):
            assert abs(farrow(x, 3, mu, b) - 2.5) < 1e-14


def test_impulse_response_reproduces_output():
    rng = random.Random(5)
    x = [rng.gauss(0, 1) for _ in range(30)]
    for b in (CUBIC_LAGRANGE, parabolic(0.5)):
        for _ in range(50):
            t = rng.uniform(3, 25)
            m = math.floor(t)
            direct = sum(x[n] * impulse_response(t - n, b) for n in range(len(x)))
            assert abs(farrow(x, m, t - m, b) - direct) < 1e-12
    assert abs(impulse_response(0.0) - 1.0) < 1e-15
    for n in (-2, -1, 1, 2):
        assert abs(impulse_response(float(n))) < 1e-15


def test_resample_with_nco_times():
    f = 0.03
    x = [math.sin(2 * math.pi * f * n) for n in range(200)]
    times = nco_times(len(x), 1.37, 0.2)
    assert times[0] >= 1 and times[-1] <= len(x) - 3
    for a, b in zip(times, times[1:]):
        assert abs(b - a - 1.37) < 1e-9
    out = resample(x, times)
    bound = 3.0 / 128.0 * (2 * math.pi * f) ** 4
    for t, v in zip(times, out):
        assert abs(v - math.sin(2 * math.pi * f * t)) <= bound
