# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/costas-loop/. The authors are listed in prov/J5XYD4.jsonl.

import cmath
import math
import random

from costas_loop import costas, detector, loop_gains

BPSK = [1 + 0j, -1 + 0j]
QPSK = [cmath.exp(1j * (math.pi / 4 + math.pi / 2 * m)) for m in range(4)]


def symbols(rng, mod, n):
    return [rng.choice(BPSK if mod == "bpsk" else QPSK) for _ in range(n)]


def noise_bandwidth(kp, ki):
    """B_L T of the linear second-order loop with gains kd kp and kd ki (closed form)."""
    b0, b1, a1, a2 = kp + ki, -kp, kp + ki - 2.0, 1.0 - kp
    return 0.5 * ((b0 * b0 + b1 * b1) * (1 + a2) - 2 * b0 * b1 * a1) / ((1 - a2) * ((1 + a2) ** 2 - a1 * a1))


def test_s_curves_without_noise() -> None:
    for i in range(-300, 301):
        d = i * math.pi / 300
        for a in BPSK:
            assert abs(detector(a * cmath.exp(1j * d), "bpsk") - 0.5 * math.sin(2 * d)) < 1e-12
        for a in QPSK:
            e = detector(a * cmath.exp(1j * d), "qpsk")
            # period pi/2: reduce d to [-pi/4, pi/4)
            dr = (d + math.pi / 4) % (math.pi / 2) - math.pi / 4
            if abs(abs(dr) - math.pi / 4) > 1e-9:
                assert abs(e - math.sqrt(2) * math.sin(dr)) < 1e-12


def test_bpsk_loop_equals_a_pll_on_the_squared_signal() -> None:
    # psi = 2 phi follows the PLL psi += kp E + S, S += ki E with E = Im(r^2 e^(-j psi)).
    rng = random.Random(11)
    sd = math.sqrt(0.05)
    r = [a * cmath.exp(0.7j) + complex(rng.gauss(0, sd), rng.gauss(0, sd)) for a in symbols(rng, "bpsk", 3000)]
    kp, ki = loop_gains(0.02, "bpsk")
    est = costas(r, kp, ki, "bpsk")
    psi, s = 0.0, 0.0
    for k, x in enumerate(r):
        assert abs(2 * est[k] - psi) < 1e-9
        e = (x * x * cmath.exp(-1j * psi)).imag
        s += ki * e
        psi += kp * e + s


def test_lock_from_0_7_rad_without_noise() -> None:
    rng = random.Random(1)
    for mod in ("bpsk", "qpsk"):
        kp, ki = loop_gains(0.02, mod)
        r = [a * cmath.exp(0.7j) for a in symbols(rng, mod, 1500)]
        est = costas(r, kp, ki, mod)
        assert max(abs(0.7 - p) for p in est[300:]) < 1e-3
        assert abs(0.7 - est[-1]) < 1e-9


def test_phase_ambiguity() -> None:
    rng = random.Random(1)
    # BPSK locks modulo pi, QPSK modulo pi/2, to the stable point nearest the start.
    for mod, th, target in [("bpsk", 2.0, 2.0 - math.pi), ("qpsk", 1.0, 1.0 - math.pi / 2)]:
        kp, ki = loop_gains(0.02, mod)
        r = [a * cmath.exp(1j * th) for a in symbols(rng, mod, 1500)]
        est = costas(r, kp, ki, mod)
        assert abs(est[-1] - target) < 1e-6


def test_frequency_offset_is_tracked() -> None:
    rng = random.Random(2)
    w = 2 * math.pi * 0.001
    for mod in ("bpsk", "qpsk"):
        kp, ki = loop_gains(0.02, mod)
        r = [a * cmath.exp(1j * (0.7 + w * k)) for k, a in enumerate(symbols(rng, mod, 2000))]
        est = costas(r, kp, ki, mod)
        assert max(abs(0.7 + w * k - est[k]) for k in range(600, 2000)) < 1e-4


def test_phase_error_variance_at_10_db() -> None:
    # Linear model, B_L T = 0.01: BPSK var = (B_L T / SNR)(1 + 1/(2 SNR)) (squaring loss);
    # QPSK with correct decisions var = B_L T / SNR. Accept a factor of 1.25 either way.
    snr = 10.0
    sd = math.sqrt(0.5 / snr)
    for mod, seed in (("bpsk", 3), ("qpsk", 4)):
        rng = random.Random(seed)
        kp, ki = loop_gains(0.01, mod)
        kd = 1.0 if mod == "bpsk" else math.sqrt(2.0)
        r = [a * cmath.exp(0.7j) + complex(rng.gauss(0, sd), rng.gauss(0, sd)) for a in symbols(rng, mod, 40000)]
        err = [0.7 - p for p in costas(r, kp, ki, mod)[2000:]]
        m = sum(err) / len(err)
        var = sum((e - m) ** 2 for e in err) / len(err)
        pred = noise_bandwidth(kd * kp, kd * ki) / snr
        if mod == "bpsk":
            pred *= 1 + 1 / (2 * snr)
        assert abs(m) < 0.01
        assert 0.8 < var / pred < 1.25
