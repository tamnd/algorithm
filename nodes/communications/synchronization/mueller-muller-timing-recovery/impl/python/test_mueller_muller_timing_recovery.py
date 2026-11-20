# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mueller-muller-timing-recovery/. The authors are listed in prov/BY94Z6.jsonl.

import cmath
import math
import random

from mueller_muller_timing_recovery import (
    detector,
    gain_for_bandwidth,
    mueller_muller,
    slicer,
    slope_raised_cosine,
)

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


def make_sampler(a, tau, n0=0.0, seed=0, span=4, reach=8):
    """Matched filter output y(t) = sum a_k g(t - k - tau) + v(t), g raised cosine.

    The noise is v(t) = sum_n w_n rrc(t - n h) with h = 1/2 and w_n i.i.d.
    CN(0, h n0). Since rrc has bandwidth (1 + beta)/2 < 1/(2h), v is stationary
    with autocorrelation n0 g(t - s): the matched filter output of white noise
    of density n0 (up to the cut of rrc at span symbols).
    """
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
        if w is not None:
            c = int(round(t / h))
            for n in range(c - reach_w, c + reach_w + 1):
                acc += w[n - n_lo] * rrc(t - n * h, BETA)
        return acc

    return sample


def qpsk(n, seed):
    rng = random.Random(seed)
    return [rng.choice(QPSK) for _ in range(n)]


def rc_derivative_at_one(b, eps=1e-6):
    return (rc(1 + eps, b) - rc(1 - eps, b)) / (2 * eps)


def test_slope_formula():
    for b in (0.1, 0.25, 0.35, 0.5, 0.75):
        assert abs(slope_raised_cosine(b) + 2 * rc_derivative_at_one(b)) < 1e-6
    assert abs(slope_raised_cosine(0.5) - math.pi / 2) < 1e-15


def test_slicer_is_nearest_point():
    rng = random.Random(1)
    for _ in range(200):
        y = complex(rng.gauss(0, 1), rng.gauss(0, 1))
        best = slicer(y, QPSK)
        assert all(abs(y - best) <= abs(y - p) for p in QPSK)


def test_decision_directed_lock_is_exact_without_noise():
    # At tau_k = tau the strobes are the symbols (raised cosine is a Nyquist
    # pulse), so e_k = Re{conj(a_{k-1}) a_k - conj(a_k) a_{k-1}} = 0: no self-noise.
    a = qpsk(700, 2)
    kp = gain_for_bandwidth(0.01, slope_raised_cosine(BETA))
    taus, ys, dec = mueller_muller(make_sampler(a, TAU), 650, kp, QPSK)
    for t in taus[500:]:
        # rc() takes its limit value within 1e-9 of t = 1/(2 beta), so 1e-8 is the floor here.
        assert abs(t - TAU) < 1e-8
    assert dec[500:650] == a[500:650]


def test_data_aided_lock_from_far_start():
    a = qpsk(700, 3)
    kp = gain_for_bandwidth(0.01, slope_raised_cosine(BETA))
    taus, _, _ = mueller_muller(make_sampler(a, TAU), 650, kp, QPSK, tau0=-0.15, known=a)
    for t in taus[600:]:
        # rc() takes its limit value within 1e-9 of t = 1/(2 beta), so 1e-8 is the floor here.
        assert abs(t - TAU) < 1e-8


def test_detector_mean_matches_s_curve():
    a = qpsk(1300, 4)
    sample = make_sampler(a, TAU)
    for delta in (0.1, 0.3, -0.2):
        es = []
        for k in range(10, 1290):
            t = k + TAU - delta
            es.append(detector(sample(t - 1), a[k - 1], sample(t), a[k]))
        mean = sum(es) / len(es)
        expected = rc(1 - delta, BETA) - rc(1 + delta, BETA)
        # The standard error of the mean is about 0.02 here.
        assert abs(mean - expected) < 0.06
    assert abs(rc(0.9, BETA) - rc(1.1, BETA) - 0.156597) < 1e-6
    assert abs(rc(0.7, BETA) - rc(1.3, BETA) - 0.457816) < 1e-6


def test_noise_variance_against_mcrb():
    # The detector noise is white with variance N0 per symbol (Nyquist pulse),
    # so a first-order loop has var = 2 B_L T N0 / K_D^2. Divided by the MCRB
    # this is 8 pi^2 xi / K_D^2 = 32 xi = 3.05 at beta = 0.5.
    snr = 10.0
    bl_t = 0.01
    xi = 1.0 / 12.0 + BETA ** 2 * (0.25 - 2.0 / math.pi ** 2)
    mcrb = bl_t / (4 * math.pi ** 2 * xi * snr)
    a = qpsk(2400, 6)
    sample = make_sampler(a, TAU, n0=1.0 / snr, seed=7)
    kd = slope_raised_cosine(BETA)
    taus, _, _ = mueller_muller(sample, 2350, gain_for_bandwidth(bl_t, kd), QPSK)
    tail = taus[400:]
    mean = sum(tail) / len(tail)
    var = sum((t - mean) ** 2 for t in tail) / len(tail)
    assert abs(32 * xi - 3.045) < 1e-3
    assert 1.5 <= var / mcrb <= 5.0
