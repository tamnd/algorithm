# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/amp-mimo-detection/. The authors are listed in prov/V4YK5H.jsonl.

import math
import random

import cbb
import constel
from amp_mimo_detection import amp, amp_detect, denoise, denoise_gaussian, state_evolution


def iid(rng, m, n):
    """An m by n channel with i.i.d. CN(0, 1/m) entries."""
    return [[cbb.cn(rng, 1.0 / m) for _ in range(n)] for _ in range(m)]


def test_denoiser_bpsk_closed_form() -> None:
    bpsk = constel.pam(2)
    for z in (0.3 - 0.2j, -1.1 + 0.5j, 2.0 + 0j, -0.05 + 1j):
        for s2 in (0.1, 0.5, 2.0):
            f, g = denoise(z, s2, bpsk)
            t = math.tanh(2 * z.real / s2)
            assert abs(f - t) < 1e-12
            assert abs(g - (1 - t * t)) < 1e-12


def test_denoiser_against_direct_posterior() -> None:
    pts = constel.qam(16)
    z, s2 = 0.4 - 0.7j, 0.3
    ws = [math.exp(-abs(z - a) ** 2 / s2) for a in pts]
    mean = sum(w * a for w, a in zip(ws, pts)) / sum(ws)
    var = sum(w * abs(a - mean) ** 2 for w, a in zip(ws, pts)) / sum(ws)
    f, g = denoise(z, s2, pts)
    assert abs(f - mean) < 1e-12 and abs(g - var) < 1e-12
    f, g = denoise(5 + 5j, 1e-6, pts)  # far away: no overflow, mass on the corner
    assert abs(f - pts[0]) < 1e-9 and g < 1e-9
    f, g = denoise_gaussian(1 + 1j, 0.5, 1.0)
    assert abs(f - (1 + 1j) / 1.5) < 1e-12 and abs(g - 0.5 / 1.5) < 1e-12


def test_example_on_the_page() -> None:
    h = [[2 / math.sqrt(5), 1 / math.sqrt(2)], [1 / math.sqrt(5), 1 / math.sqrt(2)]]
    y = [0.5, 0.6]
    bpsk = constel.pam(2)
    xhat, z, s2 = amp(y, h, bpsk, 0.25, iters=1)
    assert abs(z[0] - 1.0 / math.sqrt(5) * 1.6) < 1e-12
    assert abs(z[1] - 1.1 / math.sqrt(2)) < 1e-12
    assert abs(xhat[0] - math.tanh(2 * z[0].real / 1.25)) < 1e-12


def test_gaussian_prior_fixed_point_is_lmmse() -> None:
    rng = random.Random(2101)
    for _ in range(5):
        m, n = 24, 6
        h = iid(rng, m, n)
        x = [cbb.cn(rng, 1.0) for _ in range(n)]
        n0 = 0.2
        y = cbb.awgn(rng, cbb.matvec(h, x), n0)
        xa, _, s2 = amp(y, h, None, n0, iters=200)
        hh = cbb.herm(h)
        g = cbb.matmul(hh, h)
        for k in range(n):
            g[k][k] += n0
        xl = cbb.solve(g, cbb.matvec(hh, y))
        assert max(abs(a - b) for a, b in zip(xa, xl)) < 1e-8
        # the tracked variance solves s2 = N0 + beta Es s2 / (Es + s2)
        assert abs(s2 - (n0 + (n / m) * s2 / (1 + s2))) < 1e-9


def test_noiseless_recovery() -> None:
    rng = random.Random(2102)
    qpsk = constel.qam(4)
    ok = 0
    for _ in range(30):
        m, n = 32, 8
        h = iid(rng, m, n)
        idx = [rng.randrange(4) for _ in range(n)]
        y = cbb.matvec(h, [qpsk[i] for i in idx])
        if amp_detect(y, h, qpsk, 0.0, iters=15) == idx:
            ok += 1
    assert ok == 30


def test_agreement_with_ml_at_high_snr() -> None:
    # 4-QAM, n = 4 streams, m = 8 receive antennas, Es/N0 = 15 dB, seed 2103:
    # AMP agrees with brute-force ML on at least 95 of 100 vectors.
    rng = random.Random(2103)
    qpsk = constel.qam(4)
    n0 = cbb.undb(-15.0)
    agree = 0
    for _ in range(100):
        h = iid(rng, 8, 4)
        idx = [rng.randrange(4) for _ in range(4)]
        y = cbb.awgn(rng, cbb.matvec(h, [qpsk[i] for i in idx]), n0)
        if amp_detect(y, h, qpsk, n0, iters=15) == constel.ml_vector(y, h, qpsk):
            agree += 1
    assert agree >= 95


def test_effective_noise_matches_tracked_variance() -> None:
    # n = 32, m = 64 (beta = 0.5), 4-QAM, N0 = 0.25: the measured mean of |z_k - x_k|^2
    # is within 25 percent of the tracked s2 and of the state evolution value.
    rng = random.Random(2104)
    qpsk = constel.qam(4)
    m, n, n0, iters = 64, 32, 0.25, 6
    meas, track = 0.0, 0.0
    trials = 8
    for _ in range(trials):
        h = iid(rng, m, n)
        x = [qpsk[rng.randrange(4)] for _ in range(n)]
        y = cbb.awgn(rng, cbb.matvec(h, x), n0)
        _, z, s2 = amp(y, h, qpsk, n0, iters=iters)
        meas += sum(abs(a - b) ** 2 for a, b in zip(z, x)) / n
        # s2 returned is the next value; z used the previous one, so recompute by one more run
        _, _, s2prev = amp(y, h, qpsk, n0, iters=iters - 1)
        track += s2prev
    meas /= trials
    track /= trials
    se = state_evolution(qpsk, n0, n / m, iters - 1, 4000, random.Random(2105))[-1]
    assert abs(meas - track) / track < 0.25
    assert abs(meas - se) / se < 0.25
    assert n0 < se < n0 + (n / m)
