# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/decision-directed-carrier-recovery/. The authors are listed in prov/EVQ8KF.jsonl.

import cmath
import math
import random

import constel
from decision_directed_carrier_recovery import dd_detector, dd_loop, loop_gains, nearest

QPSK = constel.psk(4, math.pi / 4)
QAM16 = constel.qam(16)


def s_curve(deg, points):
    """The mean detector output without noise, over all points, at a phase error in degrees."""
    d = math.radians(deg)
    return sum(dd_detector(a * cmath.exp(1j * d), points) for a in points) / len(points)


def noise_bandwidth(kp, ki):
    b0, b1, a1, a2 = kp + ki, -kp, kp + ki - 2.0, 1.0 - kp
    return 0.5 * ((b0 * b0 + b1 * b1) * (1 + a2) - 2 * b0 * b1 * a1) / ((1 - a2) * ((1 + a2) ** 2 - a1 * a1))


def test_decisions_match_brute_force_ml() -> None:
    rng = random.Random(7)
    for pts in (QPSK, QAM16, constel.qam(64), constel.psk(8)):
        for _ in range(2000):
            z = complex(rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5))
            assert nearest(z, pts) == pts[constel.ml_detect(z, pts)]


def test_s_curves_without_noise() -> None:
    # QPSK: sin(delta) for |delta| < 45 degrees.
    for i in range(-449, 450):
        assert abs(s_curve(i / 10, QPSK) - math.sin(math.radians(i / 10))) < 1e-12
    # 16-QAM: sin(delta) while every decision is right, up to 16.87 degrees, where the
    # corner point crosses a boundary: arccos(2/(3 sqrt 2)) - 45 degrees.
    edge = math.degrees(math.acos(2 / (3 * math.sqrt(2)))) - 45
    assert abs(edge - 16.874) < 1e-3
    for i in range(-168, 169):
        assert abs(s_curve(i / 10, QAM16) - math.sin(math.radians(i / 10))) < 1e-12
    assert s_curve(16.9, QAM16) < 0.5 * math.sin(math.radians(16.9))
    # The mean output changes sign at arctan(1/3) = 18.435 degrees, and again between
    # 25 and 30 degrees, from negative to positive: a stable false lock point.
    assert s_curve(18.4, QAM16) > 0 > s_curve(18.47, QAM16)
    assert s_curve(25, QAM16) < 0 < s_curve(30, QAM16)


def test_lock_without_noise() -> None:
    kp, ki = loop_gains(0.02)
    for pts, th in ((QPSK, 0.7), (QAM16, 0.25)):
        rng = random.Random(1)
        r = [rng.choice(pts) * cmath.exp(1j * th) for _ in range(1500)]
        est, _ = dd_loop(r, pts, kp, ki)
        assert max(abs(th - p) for p in est[300:]) < 1e-3
        assert abs(th - est[-1]) < 1e-9


def test_qam_false_lock_and_the_data_aided_form() -> None:
    kp, ki = loop_gains(0.02)
    rng = random.Random(1)
    a = [rng.choice(QAM16) for _ in range(8000)]
    r = [x * cmath.exp(0.7j) for x in a]
    # Decision-directed from 0.7 rad (40 degrees): the loop settles near the false
    # lock point of about 28 degrees, and most decisions are wrong.
    est, dec = dd_loop(r, QAM16, kp, ki)
    tail = [0.7 - p for p in est[5000:]]
    assert 0.40 < min(tail) and max(tail) < 0.58
    assert abs(sum(tail) / len(tail) - 0.487) < 0.01  # 27.9 degrees
    assert sum(1 for x, y in zip(dec[5000:], a[5000:]) if x != y) > 2000
    # Data-aided: the known symbols give |a|^2 sin(delta), with no ambiguity at all.
    est, _ = dd_loop(r, QAM16, kp, ki, known=a)
    assert abs(0.7 - est[-1]) < 1e-9
    r2 = [x * cmath.exp(2.5j) for x in a[:3000]]
    est, _ = dd_loop(r2, QAM16, kp, ki, known=a[:3000])
    assert abs(2.5 - est[-1]) < 1e-9


def test_variance_against_the_linear_model() -> None:
    # With correct decisions the variance is B_L T / SNR. B_L T = 0.01; factor 1.25.
    kp, ki = loop_gains(0.01)
    bl = noise_bandwidth(kp, ki)
    for pts, snr_db, seed in ((QPSK, 10, 3), (QAM16, 20, 4)):
        snr = 10 ** (snr_db / 10)
        sd = math.sqrt(0.5 / snr)
        rng = random.Random(seed)
        r = [rng.choice(pts) * cmath.exp(0.2j) + complex(rng.gauss(0, sd), rng.gauss(0, sd)) for _ in range(30000)]
        err = [0.2 - p for p in dd_loop(r, pts, kp, ki, phi0=0.2)[0][1000:]]
        m = sum(err) / len(err)
        var = sum((e - m) ** 2 for e in err) / len(err)
        assert abs(m) < 0.01
        assert 0.8 < var / (bl / snr) < 1.25
