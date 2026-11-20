# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/viterbi-viterbi-phase-estimation/. The authors are listed in prov/VA0M3B.jsonl.

import cmath
import math
import random

from viterbi_viterbi_phase_estimation import objective, unwrap, vv_estimate, wrap

Q0 = math.pi / 4  # QPSK points at pi/4 + i pi/2


def psk_block(rng, m, n, theta, snr=None, phase0=0.0):
    sd = math.sqrt(0.5 / snr) if snr else 0.0
    out = []
    for _ in range(n):
        a = cmath.exp(1j * (2 * math.pi * rng.randrange(m) / m + phase0))
        w = complex(rng.gauss(0, sd), rng.gauss(0, sd)) if sd else 0j
        out.append(a * cmath.exp(1j * theta) + w)
    return out


def test_exact_without_noise() -> None:
    rng = random.Random(1)
    for m, phase0 in ((2, 0.0), (4, Q0), (4, 0.0), (8, 0.0)):
        for _ in range(50):
            th = rng.uniform(-math.pi / m, math.pi / m) * 0.999
            r = psk_block(rng, m, 16, th, phase0=phase0)
            for p in (0, 1, 2, m):
                assert abs(vv_estimate(r, m, p, phase0) - th) < 1e-9


def test_ambiguity_modulo_two_pi_over_m() -> None:
    rng = random.Random(2)
    r = psk_block(rng, 4, 16, 1.0, phase0=Q0)
    assert abs(vv_estimate(r, 4, 2, Q0) - (1.0 - math.pi / 2)) < 1e-9
    r = psk_block(rng, 2, 16, 2.0)
    assert abs(vv_estimate(r, 2, 2) - (2.0 - math.pi)) < 1e-9


def test_maximizes_the_objective_against_a_grid() -> None:
    # Brute force: the best of 4000 grid points in one period cannot beat the closed form.
    rng = random.Random(3)
    for m, phase0, p in ((4, Q0, 2), (4, Q0, 0), (8, 0.0, 1), (2, 0.0, 2)):
        r = psk_block(rng, m, 24, 0.1, snr=10 ** 0.3, phase0=phase0)
        t = vv_estimate(r, m, p, phase0)
        period = 2 * math.pi / m
        grid = [-period / 2 + period * i / 4000 for i in range(4000)]
        g = max(grid, key=lambda x: objective(r, m, x, p, phase0))
        best = objective(r, m, t, p, phase0)
        assert best >= objective(r, m, g, p, phase0) - 1e-12
        assert abs(wrap(g - t, period)) <= period / 4000


def test_mse_against_the_mcrb() -> None:
    # QPSK, N = 32, MCRB = 1/(2 N SNR). At 10 dB all nonlinearities are close to it;
    # at 5 dB, p = 1 or 2 is clearly better than the plain fourth power p = 4.
    n, trials = 32, 600
    ratio = {}
    for snr_db in (5, 10):
        snr = 10 ** (snr_db / 10)
        mcrb = 1 / (2 * n * snr)
        for p in (1, 2, 4):
            rng = random.Random(4)
            se = 0.0
            for _ in range(trials):
                th = rng.uniform(-0.3, 0.3)
                e = wrap(vv_estimate(psk_block(rng, 4, n, th, snr, Q0), 4, p, Q0) - th, math.pi / 2)
                se += e * e
            ratio[snr_db, p] = se / trials / mcrb
    for p in (1, 2, 4):
        assert 0.9 < ratio[10, p] < 1.8
    assert ratio[10, 2] < 1.35
    assert ratio[5, 2] < 0.8 * ratio[5, 4]
    assert ratio[5, 1] < 0.8 * ratio[5, 4]
    assert ratio[5, 2] > 1.5


def test_unwrap_tracks_a_drifting_phase() -> None:
    # Blocks of 32 QPSK symbols with a phase ramp over 3 rad, beyond the range pi/4.
    rng = random.Random(5)
    ests, truth = [], []
    for b in range(60):
        th = 0.05 * b
        truth.append(th)
        ests.append(vv_estimate(psk_block(rng, 4, 32, th, 10.0, Q0), 4, 2, Q0))
    assert max(ests) < math.pi / 4
    u = unwrap(ests, 4)
    assert max(abs(a - b) for a, b in zip(u, truth)) < 0.2
