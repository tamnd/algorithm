# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zero-forcing-mimo-detector/. The authors are listed in prov/Q1ZTZN.jsonl.

import math
import random

import pytest

import cbb
import constel
from zero_forcing_mimo_detector import (
    nearest,
    noise_gains,
    post_detection_snr,
    zf_detect,
    zf_matrix,
    zf_outputs,
)


def rayleigh(rng, m, n):
    return [[cbb.cn(rng, 1.0) for _ in range(n)] for _ in range(m)]


def test_example_on_the_page() -> None:
    h = [[2, 1], [1, 1]]
    y = [0.5, 0.6]
    bpsk = constel.pam(2)  # index 0 is +1, index 1 is -1
    z = zf_outputs(y, h)
    assert abs(z[0] - (-0.1)) < 1e-12 and abs(z[1] - 0.7) < 1e-12
    assert zf_detect(y, h, bpsk) == [1, 0]  # (-1, +1): both decisions wrong
    assert constel.ml_vector(y, h, bpsk) == [0, 1]  # ML finds the sent (+1, -1)
    g = noise_gains(h)
    assert abs(g[0] - 2) < 1e-12 and abs(g[1] - 5) < 1e-12
    snr = post_detection_snr(h, 1.0, 1.0)
    assert abs(cbb.db(1 / snr[0]) - 3.0103) < 1e-4 and abs(cbb.db(1 / snr[1]) - 6.9897) < 1e-4


def test_w_is_a_left_inverse_and_its_row_norms_are_the_noise_gains() -> None:
    rng = random.Random(1201)
    for _ in range(50):
        n = rng.randint(1, 4)
        m = rng.randint(n, 6)
        h = rayleigh(rng, m, n)
        w = zf_matrix(h)
        wh = cbb.matmul(w, h)
        for i in range(n):
            for k in range(n):
                assert abs(wh[i][k] - (1 if i == k else 0)) < 1e-9
        for k, g in enumerate(noise_gains(h)):
            assert abs(cbb.norm2(w[k]) - g) < 1e-9 * g


def test_noiseless_recovery_is_exact() -> None:
    rng = random.Random(1202)
    pts = constel.qam(16)
    for _ in range(100):
        n = rng.randint(1, 4)
        m = rng.randint(n, 6)
        h = rayleigh(rng, m, n)
        idx = [rng.randrange(16) for _ in range(n)]
        y = cbb.matvec(h, [pts[i] for i in idx])
        assert zf_detect(y, h, pts) == idx


def test_zf_is_ml_when_the_columns_are_orthogonal() -> None:
    # theorem 3: H^H H diagonal makes the ML metric separate per stream
    rng = random.Random(1206)
    pts = constel.qam(4)
    for _ in range(60):
        a, b = cbb.cn(rng, 1.0), cbb.cn(rng, 1.0)
        c = rng.uniform(0.3, 2.0)
        # columns (a, b, 0) and c (-conj(b), conj(a), 0) are orthogonal; the third column is e3
        h = [[a, -c * b.conjugate(), 0], [b, c * a.conjugate(), 0], [0, 0, rng.uniform(0.2, 1.5)]]
        idx = [rng.randrange(4) for _ in range(3)]
        y = cbb.awgn(rng, cbb.matvec(h, [pts[i] for i in idx]), 0.5)
        assert zf_detect(y, h, pts) == constel.ml_vector(y, h, pts)


def test_square_channel_uses_the_inverse() -> None:
    h = [[1, 2j], [0.5, -1 + 1j]]
    w, hinv = zf_matrix(h), cbb.inv(h)
    assert all(abs(w[i][k] - hinv[i][k]) < 1e-12 for i in range(2) for k in range(2))


def test_dependent_columns_and_wide_channels_are_rejected() -> None:
    with pytest.raises(ValueError):
        zf_matrix([[1, 2], [2, 4]])
    with pytest.raises(ValueError):
        zf_matrix([[1, 2, 3], [4, 5, 6]])


def test_nearest_breaks_ties_to_the_lowest_index() -> None:
    assert nearest(0j, constel.pam(2)) == 0
    assert nearest(0.2 - 0.9j, constel.qam(4)) == 1


def test_post_detection_snr_is_chi_square_with_2_times_m_minus_n_plus_1_degrees() -> None:
    # theorem: for i.i.d. CN(0, 1) entries, 1 / [(H^H H)^-1]_kk is Gamma(m - n + 1, 1),
    # so its mean and its variance are both m - n + 1
    rng = random.Random(1203)
    for m, n in ((2, 2), (3, 2), (4, 2)):
        d = m - n + 1
        trials = 1500
        vals = [1.0 / noise_gains(rayleigh(rng, m, n))[0] for _ in range(trials)]
        mean = sum(vals) / trials
        assert abs(mean - d) < 4.0 * math.sqrt(d / trials)


def mrc_bpsk_ber(snr: float, branches: int) -> float:
    # closed form: E[Q(sqrt(2 g))] for g ~ Gamma(branches, snr)
    mu = math.sqrt(snr / (1 + snr))
    a, b = (1 - mu) / 2, (1 + mu) / 2
    return a**branches * sum(math.comb(branches - 1 + k, k) * b**k for k in range(branches))


def test_bpsk_error_rate_matches_the_diversity_closed_form() -> None:
    # each ZF stream is BPSK on a channel with m - n + 1 Rayleigh branches
    rng = random.Random(1204)
    bpsk = constel.pam(2)
    for m, n, snr_db in ((2, 2, 10.0), (3, 2, 4.0)):
        snr = cbb.undb(snr_db)
        p = mrc_bpsk_ber(snr, m - n + 1)
        trials = math.ceil(150 / (p * n))
        errors = 0
        for _ in range(trials):
            h = rayleigh(rng, m, n)
            idx = [rng.randrange(2) for _ in range(n)]
            y = cbb.awgn(rng, cbb.matvec(h, [bpsk[i] for i in idx]), 1.0 / snr)
            errors += sum(a != b for a, b in zip(zf_detect(y, h, bpsk), idx))
        lo, hi = cbb.wilson(errors, trials * n)
        assert lo <= p <= hi


def test_most_decisions_match_ml_at_high_snr() -> None:
    # measured: 4-QAM, m = 4, n = 3, Es/N0 = 20 dB, seed 1205: at least 190 of 200 vectors agree with ML
    rng = random.Random(1205)
    pts = constel.qam(4)
    n0 = 1 / cbb.undb(20.0)
    agree = 0
    for _ in range(200):
        h = rayleigh(rng, 4, 3)
        idx = [rng.randrange(4) for _ in range(3)]
        y = cbb.awgn(rng, cbb.matvec(h, [pts[i] for i in idx]), n0)
        agree += zf_detect(y, h, pts) == constel.ml_vector(y, h, pts)
    assert agree >= 190
