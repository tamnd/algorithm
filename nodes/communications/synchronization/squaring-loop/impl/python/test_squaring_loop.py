# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/squaring-loop/. The authors are listed in prov/PVGB8C.jsonl.

import cmath
import math
import random

from squaring_loop import loop_gains, squaring_loop, variance_factor


def psk_samples(rng, m, phase0, theta, n, n0=0.0):
    sd = math.sqrt(n0 / 2)
    out = []
    for _ in range(n):
        a = cmath.exp(1j * (phase0 + 2 * math.pi * rng.randrange(m) / m))
        w = complex(rng.gauss(0, sd), rng.gauss(0, sd)) if n0 > 0 else 0j
        out.append(a * cmath.exp(1j * theta) + w)
    return out


def noise_bandwidth(kp, ki):
    b0, b1, a1, a2 = kp + ki, -kp, kp + ki - 2.0, 1.0 - kp
    return 0.5 * ((b0 * b0 + b1 * b1) * (1 + a2) - 2 * b0 * b1 * a1) / ((1 - a2) * ((1 + a2) ** 2 - a1 * a1))


def wrap(x, period):
    return (x + period / 2) % period - period / 2


def test_m2_equals_the_bpsk_costas_loop() -> None:
    rng = random.Random(11)
    r = psk_samples(rng, 2, 0.0, 0.7, 3000, n0=0.1)
    kp, ki = loop_gains(0.02)
    est = squaring_loop(r, 2, kp, ki)
    # The Costas recursion written out: e = I Q on z = r e^(-j phi), with the same gains.
    phi, s = 0.0, 0.0
    for k, x in enumerate(r):
        assert abs(est[k] - phi) < 1e-9
        z = x * cmath.exp(-1j * phi)
        e = z.real * z.imag
        s += ki * e
        phi += kp * e + s


def test_variance_factor_closed_forms() -> None:
    for n0 in (0.01, 0.1, 0.5):
        assert abs(variance_factor(2, n0) - n0 * (1 + n0 / 2)) < 1e-15
        assert abs(variance_factor(4, n0) - n0 * (1 + 4.5 * n0 + 6 * n0**2 + 1.5 * n0**3)) < 1e-15


def test_lock_without_noise_and_the_ambiguity() -> None:
    rng = random.Random(1)
    kp, ki = loop_gains(0.02)
    for m, phase0 in ((2, 0.0), (4, math.pi / 4), (8, 0.0)):
        r = psk_samples(rng, m, phase0, 0.7, 1500)
        est = squaring_loop(r, m, kp, ki, phase0)
        # The loop locks to theta modulo 2 pi / M, at the lock point nearest the start.
        target = 0.7 - 2 * math.pi / m * round(0.7 * m / (2 * math.pi))
        assert max(abs(target - p) for p in est[400:]) < 1e-3
        assert abs(target - est[-1]) < 1e-9
    # For 8-PSK, 0.7 rad is beyond pi/8, so the loop settles at 0.7 - pi/4.
    r = psk_samples(rng, 8, 0.0, 0.7, 1500)
    assert abs(squaring_loop(r, 8, kp, ki)[-1] - (0.7 - math.pi / 4)) < 1e-9


def test_frequency_offset_without_noise() -> None:
    rng = random.Random(2)
    kp, ki = loop_gains(0.02)
    w = 2 * math.pi * 0.0005
    r = [x * cmath.exp(1j * w * k) for k, x in enumerate(psk_samples(rng, 4, math.pi / 4, 0.3, 2500))]
    est = squaring_loop(r, 4, kp, ki, math.pi / 4)
    assert max(abs(wrap(0.3 + w * k - est[k], math.pi / 2)) for k in range(800, 2500)) < 1e-4


def test_variance_against_the_linear_model() -> None:
    # B_L T = 0.01; M = 2 and M = 4 at 10 dB, M = 4 at 6 dB. Factor 1.25 either way.
    kp, ki = loop_gains(0.01)
    bl = noise_bandwidth(kp, ki)
    for m, phase0, snr_db, seed in ((2, 0.0, 10, 1), (4, math.pi / 4, 10, 2), (4, math.pi / 4, 6, 3)):
        n0 = 10 ** (-snr_db / 10)
        rng = random.Random(seed)
        r = psk_samples(rng, m, phase0, 0.2, 40000, n0)
        err = [0.2 - p for p in squaring_loop(r, m, kp, ki, phase0)[2000:]]
        mean = sum(err) / len(err)
        var = sum((e - mean) ** 2 for e in err) / len(err)
        assert abs(mean) < 0.01
        assert 0.8 < var / (bl * variance_factor(m, n0)) < 1.25
