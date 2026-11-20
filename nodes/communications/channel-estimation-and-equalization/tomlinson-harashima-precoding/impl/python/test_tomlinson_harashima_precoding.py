# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tomlinson-harashima-precoding/. The authors are listed in prov/T1E2A7.jsonl.

import math
import random

import pytest

from tomlinson_harashima_precoding import (
    channel,
    mod,
    mod_real,
    pam,
    power_loss,
    ser_per_dimension,
    slice_real,
    thp_encode,
    thp_receive,
)


def wilson(k, n, z=3.29):
    p, z2 = k / n, z * z
    mid = (p + z2 / (2 * n)) / (1 + z2 / n)
    half = z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n)) / (1 + z2 / n)
    return mid - half, mid + half


def test_example_on_the_page() -> None:
    a = [3, -3, -3, 3, 3]
    x = thp_encode(a, [1, 0.5], 4)
    assert [v.real for v in x] == [3, 3.5, 3.25, 1.375, 2.3125]
    y = channel(x, [1, 0.5])
    assert [v.real for v in y] == [3, 5, 5, 3, 3]
    assert thp_receive(y, 1, 4, real=True) == [complex(v) for v in a]
    assert abs(10 * math.log10(power_loss(4)) - 0.280287) < 1e-6
    assert abs(10 * math.log10(power_loss(2)) - 1.249387) < 1e-6


def test_modulo_and_slicer() -> None:
    for v in (-4.0, -3.99, 0.0, 3.99, 4.0, 7.5, -12.25, 100.1):
        r = mod_real(v, 4)
        assert -4 <= r < 4 and abs((v - r) / 8 - round((v - r) / 8)) < 1e-12
    for m in (2, 3, 4, 8):
        for p in pam(m):
            for k in (-2, -1, 0, 1, 3):
                assert slice_real(p + 2 * m * k + 0.4, m) == p
                assert slice_real(p + 2 * m * k - 0.4, m) == p
    assert pam(4) == [3, 1, -1, -3]
    with pytest.raises(ValueError):
        pam(1)


def test_noiseless_recovery_on_random_channels() -> None:
    rng = random.Random(7301)
    for _ in range(30):
        m = rng.choice((2, 4, 8))
        taps = rng.randint(2, 5)
        cplx = rng.random() < 0.5
        h = [complex(rng.gauss(0, 1), rng.gauss(0, 1) if cplx else 0) for _ in range(taps)]
        pts = pam(m)
        a = [complex(rng.choice(pts), rng.choice(pts) if cplx else 0) for _ in range(200)]
        x = thp_encode(a, h, m)
        assert all(-m <= v.real < m and -m <= v.imag < m for v in x)
        y = channel(x, h)
        assert thp_receive(y, h[0], m, real=not cplx) == a


def test_received_minus_symbol_is_noise_modulo_2m() -> None:
    rng = random.Random(7302)
    h = [1, -0.9 + 0.3j, 0.4j]
    m = 4
    pts = pam(m)
    a = [complex(rng.choice(pts), rng.choice(pts)) for _ in range(500)]
    x = thp_encode(a, h, m)
    w = [complex(rng.gauss(0, 0.3), rng.gauss(0, 0.3)) for _ in a]
    y = [v + n for v, n in zip(channel(x, h), w)]
    for k in range(len(a)):
        d = mod(y[k] - a[k], m) - mod(w[k], m)
        assert abs(d.real) < 1e-9 or abs(abs(d.real) - 2 * m) < 1e-9
        assert abs(d.imag) < 1e-9 or abs(abs(d.imag) - 2 * m) < 1e-9


def test_transmit_power_is_near_the_uniform_power() -> None:
    # a measurement: on a dispersive channel the precoded samples are close to uniform on [-M, M)
    rng = random.Random(7303)
    m, n = 4, 40000
    a = [rng.choice(pam(m)) for _ in range(n)]
    x = thp_encode(a, [1, 0.9, 0.6], m)
    p = sum(v.real ** 2 for v in x) / n
    assert abs(p - m * m / 3) < 0.05 * m * m / 3
    assert p > (m * m - 1) / 3


def test_symbol_error_rate_matches_the_modulo_formula() -> None:
    rng = random.Random(7304)
    m, n, sigma = 4, 20000, 0.4
    pe = ser_per_dimension(m, sigma)
    assert abs(pe - 2 * 0.5 * math.erfc(1 / sigma / math.sqrt(2))) < 1e-9
    assert pe * n >= 100
    h = [1, 0.5]
    a = [complex(rng.choice(pam(m))) for _ in range(n)]
    y = [v + rng.gauss(0, sigma) for v in channel(thp_encode(a, h, m), h)]
    errors = sum(1 for p, q in zip(thp_receive(y, 1, m, real=True), a) if p != q)
    lo, hi = wilson(errors, n)
    assert lo <= pe <= hi


def test_input_checks() -> None:
    with pytest.raises(ValueError):
        thp_encode([1], [0, 1], 4)
    with pytest.raises(ValueError):
        thp_encode([1], [], 4)
