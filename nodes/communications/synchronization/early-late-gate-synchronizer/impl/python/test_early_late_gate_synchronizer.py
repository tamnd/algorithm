# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/early-late-gate-synchronizer/. The authors are listed in prov/Z897RY.jsonl.

import cmath
import math
import random

from early_late_gate_synchronizer import detector, early_late_gate, gain_for_bandwidth, s_curve

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


def test_exact_lock_on_alternating_data():
    # With a_k = (-1)^k the signal is cos(pi (t - tau)) and the error is
    # sin(2 pi d) sin(2 pi (tau - tau_k)) exactly, so the loop has no self-noise.
    a = [(-1) ** k + 0j for k in range(400)]
    sample = make_sampler(a, TAU)
    taus, _ = early_late_gate(sample, 360, kp=0.1)
    for t in taus[300:]:
        assert abs(t - TAU) < 1e-9


def test_detector_mean_matches_s_curve():
    a = qpsk(1300, 2)
    sample = make_sampler(a, TAU)
    for delta in (-0.3, 0.1, 0.2):
        es = [detector(sample, k + TAU - delta) for k in range(10, 1290)]
        mean = sum(es) / len(es)
        # The standard error of the mean is about 0.02 here.
        assert abs(mean - s_curve(delta, BETA)) < 0.06


def test_gate_half_width_one_half_gives_no_error_signal():
    a = qpsk(1300, 3)
    sample = make_sampler(a, TAU)
    es = [detector(sample, k + TAU - 0.2, d=0.5) for k in range(10, 1290)]
    assert abs(sum(es) / len(es)) < 0.04
    assert abs(s_curve(0.2, BETA, d=0.5)) < 1e-15


def test_carrier_phase_does_not_change_the_loop():
    a = qpsk(300, 4)
    t1, _ = early_late_gate(make_sampler(a, TAU), 250, kp=0.05)
    t2, _ = early_late_gate(make_sampler(a, TAU, theta=1.1), 250, kp=0.05)
    assert max(abs(x - y) for x, y in zip(t1, t2)) < 1e-9


def test_random_data_noiseless_settles_near_true_delay():
    a = qpsk(1700, 5)
    kd = math.pi * BETA * math.sin(2 * math.pi * 0.25)
    kp = gain_for_bandwidth(0.0025, kd)
    taus, _ = early_late_gate(make_sampler(a, TAU), 1650, kp=kp)
    tail = taus[800:]
    mean = sum(tail) / len(tail)
    assert abs(mean - TAU) < 0.006
    assert max(abs(t - TAU) for t in tail) < 0.015


def test_second_order_loop_tracks_clock_offset():
    # A sampler whose symbols drift by 1e-3 T per symbol: tau grows like a ramp.
    a = [(-1) ** k + 0j for k in range(700)]
    drift = 1e-3

    def sample(t):
        k0 = int(round(t))
        acc = 0j
        for k in range(max(0, k0 - 16), min(len(a), k0 + 17)):
            acc += a[k] * rc(t - k - TAU - drift * k, BETA)
        return acc

    taus, _ = early_late_gate(sample, 600, kp=0.1, ki=0.005)
    for k in range(450, 600):
        assert abs(taus[k] - (TAU + drift * k)) < 2e-3


def test_noise_variance_against_mcrb():
    snr = 10.0
    bl_t = 0.01
    xi = 1.0 / 12.0 + BETA ** 2 * (0.25 - 2.0 / math.pi ** 2)
    mcrb = bl_t / (4 * math.pi ** 2 * xi * snr)
    a = qpsk(2400, 6)
    sample = make_sampler(a, TAU, n0=1.0 / snr, seed=7)
    kd = math.pi * BETA
    taus, _ = early_late_gate(sample, 2350, kp=gain_for_bandwidth(bl_t, kd))
    tail = taus[400:]
    mean = sum(tail) / len(tail)
    var = sum((t - mean) ** 2 for t in tail) / len(tail)
    assert 1.0 <= var / mcrb <= 4.0
