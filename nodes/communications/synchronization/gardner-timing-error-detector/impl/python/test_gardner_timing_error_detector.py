# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gardner-timing-error-detector/. The authors are listed in prov/9K1C0E.jsonl.

import cmath
import math
import random

from gardner_timing_error_detector import detector, gain_for_bandwidth, gardner_loop, s_curve_amplitude

BETA = 0.5
TAU = 0.3
QPSK = [cmath.exp(1j * (math.pi / 4 + m * math.pi / 2)) for m in range(4)]


def rc(t, b):
    """The raised cosine pulse with roll-off b and T = 1."""
    if abs(t) < 1e-12:
        return 1.0
    if abs(abs(t) - 1 / (2 * b)) < 1e-9:
        return math.pi / 4 * math.sin(math.pi / (2 * b)) / (math.pi / (2 * b))
    return math.sin(math.pi * t) / (math.pi * t) * math.cos(math.pi * b * t) / (1 - (2 * b * t) ** 2)


def rrc(t, b):
    """The root raised cosine pulse with roll-off b and T = 1."""
    if abs(t) < 1e-12:
        return 1 - b + 4 * b / math.pi
    if abs(abs(t) - 1 / (4 * b)) < 1e-9:
        return b / math.sqrt(2) * ((1 + 2 / math.pi) * math.sin(math.pi / (4 * b)) + (1 - 2 / math.pi) * math.cos(math.pi / (4 * b)))
    return (math.sin(math.pi * (1 - b) * t) + 4 * b * t * math.cos(math.pi * (1 + b) * t)) / (math.pi * t * (1 - (4 * b * t) ** 2))


def make_sampler(a, tau, n0=0.0, seed=0, theta=0.0, span=4, reach=8):
    """Matched filter output y(t) = e^(j theta) sum a_k g(t - k - tau) + v(t), g raised cosine.

    The noise is v(t) = sum_n w_n rrc(t - n h) with h = 1/2 and w_n i.i.d.
    CN(0, h n0). Since rrc has bandwidth (1 + beta)/2 < 1/(2h), v is stationary
    with autocorrelation n0 g(t - s): the matched filter output of white noise
    of density n0 (up to the cut of rrc at span symbols).
    """
    rot = cmath.exp(1j * theta)
    h = 0.5
    n_lo = int(-6 / h)
    w = None
    if n0 > 0:
        rng = random.Random(seed)
        sd = math.sqrt(h * n0 / 2)
        w = [complex(rng.gauss(0, sd), rng.gauss(0, sd)) for _ in range(int((len(a) + 12) / h))]
    reach_w = int(span / h)

    def sample(t):
        k0 = int(round(t - tau))
        acc = 0j
        for k in range(max(0, k0 - reach), min(len(a), k0 + reach + 1)):
            acc += a[k] * rc(t - k - tau, BETA)
        acc *= rot
        if w is not None:
            c = int(round(t / h))
            for n in range(c - reach_w, c + reach_w + 1):
                acc += w[n - n_lo] * rrc(t - n * h, BETA)
        return acc

    return sample


def qpsk(n, seed):
    rng = random.Random(seed)
    return [rng.choice(QPSK) for _ in range(n)]


def test_amplitude_closed_form():
    assert abs(s_curve_amplitude(0.5) - 0.2400843) < 1e-6
    # For small roll-off the amplitude is about beta / 2.
    assert abs(s_curve_amplitude(0.01) / 0.005 - 1) < 1e-3


def test_noise_model_has_unit_variance_at_any_offset():
    sample = make_sampler([0j] * 600, TAU, n0=1.0, seed=11)
    for off in (0.0, 0.25, 0.5):
        vals = [sample(k + off) for k in range(5, 595)]
        var = sum(abs(v) ** 2 for v in vals) / len(vals)
        # 590 samples that are nearly independent: the standard error is about 0.04.
        assert abs(var - 1.0) < 0.2


def test_exact_lock_on_alternating_data():
    # With a_k = (-1)^k the signal is cos(pi (t - tau)) and the error is
    # sin(2 pi (tau - tau_k)) exactly, so the loop has no self-noise.
    a = [(-1) ** k + 0j for k in range(400)]
    taus, _ = gardner_loop(make_sampler(a, TAU, reach=24), 360, kp=0.1)
    # What is left comes from cutting the pulse at 24 symbols.
    for t in taus[300:]:
        assert abs(t - TAU) < 1e-5


def test_detector_mean_matches_s_curve():
    a = qpsk(1300, 2)
    sample = make_sampler(a, TAU)
    amp = s_curve_amplitude(BETA)
    for delta in (-0.3, 0.1, 0.2):
        es = []
        for k in range(10, 1290):
            t = k + TAU - delta
            es.append(detector(sample(t - 1), sample(t - 0.5), sample(t)))
        mean = sum(es) / len(es)
        # The standard error of the mean is about 0.02 here.
        assert abs(mean - amp * math.sin(2 * math.pi * delta)) < 0.06


def test_carrier_phase_does_not_change_the_loop():
    a = qpsk(300, 4)
    t1, _ = gardner_loop(make_sampler(a, TAU), 250, kp=0.05)
    t2, _ = gardner_loop(make_sampler(a, TAU, theta=2.3), 250, kp=0.05)
    assert max(abs(x - y) for x, y in zip(t1, t2)) < 1e-9


def test_random_data_noiseless_settles_near_true_delay():
    a = qpsk(1700, 5)
    kd = 2 * math.pi * s_curve_amplitude(BETA)
    taus, _ = gardner_loop(make_sampler(a, TAU), 1650, kp=gain_for_bandwidth(0.0025, kd))
    tail = taus[800:]
    mean = sum(tail) / len(tail)
    assert abs(mean - TAU) < 0.003
    assert max(abs(t - TAU) for t in tail) < 0.006


def test_noise_variance_against_mcrb():
    snr = 10.0
    bl_t = 0.01
    xi = 1.0 / 12.0 + BETA ** 2 * (0.25 - 2.0 / math.pi ** 2)
    mcrb = bl_t / (4 * math.pi ** 2 * xi * snr)
    a = qpsk(2400, 6)
    sample = make_sampler(a, TAU, n0=1.0 / snr, seed=7)
    kd = 2 * math.pi * s_curve_amplitude(BETA)
    taus, _ = gardner_loop(sample, 2350, kp=gain_for_bandwidth(bl_t, kd))
    tail = taus[400:]
    mean = sum(tail) / len(tail)
    var = sum((t - mean) ** 2 for t in tail) / len(tail)
    assert 1.0 <= var / mcrb <= 4.0
