# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/peak-to-average-power-ratio/. The authors are listed in prov/Z633YX.jsonl.

import math
import random

import cbb
from peak_to_average_power_ratio import ccdf_rule, fft, ofdm_oversampled, papr, papr_db

QPSK = [complex(a, b) / math.sqrt(2) for a in (1, -1) for b in (1, -1)]


def qpsk_block(rng, n):
    return [rng.choice(QPSK) for _ in range(n)]


def test_fft_matches_direct_dft():
    rng = random.Random(1)
    for n in (2, 8, 64):
        x = [cbb.cn(rng, 1.0) for _ in range(n)]
        assert max(abs(a - b) for a, b in zip(fft(x), cbb.dft(x))) < 1e-9
        assert max(abs(a / n - b) for a, b in zip(fft(x, inverse=True), cbb.idft(x))) < 1e-9


def test_nyquist_rate_is_the_unitary_inverse_dft():
    rng = random.Random(2)
    X = qpsk_block(rng, 16)
    assert max(abs(a - b) for a, b in zip(ofdm_oversampled(X, 1), cbb.uidft(X))) < 1e-9


def test_oversampling_keeps_the_nyquist_samples_and_the_power():
    rng = random.Random(3)
    for L in (2, 4, 8):
        X = [cbb.cn(rng, 1.0) for _ in range(32)]
        x1 = ofdm_oversampled(X, 1)
        xl = ofdm_oversampled(X, L)
        assert max(abs(xl[L * n] - x1[n]) for n in range(32)) < 1e-9
        assert abs(sum(abs(v) ** 2 for v in xl) / len(xl) - sum(abs(v) ** 2 for v in X) / 32) < 1e-9
        assert papr(xl) >= papr(x1) - 1e-12


def test_bound_n_and_its_equality_case():
    for n in (4, 16, 64):
        for L in (1, 4):
            assert abs(papr(ofdm_oversampled([1] * n, L)) - n) < 1e-9
    rng = random.Random(4)
    for _ in range(50):
        X = [cbb.cn(rng, 1.0) for _ in range(16)]
        for L in (1, 4):
            assert papr(ofdm_oversampled(X, L)) <= 16 + 1e-9


def test_small_examples_of_the_page():
    x = ofdm_oversampled([1, 1, 1, -1], 1)
    assert max(abs(a - b) for a, b in zip(x, [1, 1j, 1, -1j])) < 1e-12
    assert abs(papr(x) - 1.0) < 1e-12
    assert abs(papr_db(ofdm_oversampled([1, 1, 1, -1], 4)) - 2.323) < 1e-3
    assert abs(papr_db(ofdm_oversampled([1, 1, 1, 1], 4)) - 6.021) < 1e-3
    corner = (3 + 3j) / math.sqrt(10)
    assert abs(papr([corner], 1.0) - 1.8) < 1e-12


def test_check_value_of_the_rule():
    assert abs(ccdf_rule(10.0, 64) - 2.90e-3) < 5e-6


def test_rule_is_exact_for_gaussian_symbols_at_nyquist_rate():
    # The unitary DFT maps i.i.d. CN(0, 1) symbols to i.i.d. CN(0, 1) samples.
    rng = random.Random(7)
    trials, gamma = 1000, 10 ** 0.8
    k = sum(papr(ofdm_oversampled([cbb.cn(rng, 1.0) for _ in range(64)], 1), 1.0) > gamma for _ in range(trials))
    lo, hi = cbb.wilson(k, trials)
    assert lo <= ccdf_rule(gamma, 64) <= hi


def test_rule_underestimates_the_oversampled_qpsk_ccdf():
    rng = random.Random(1)
    trials, gamma = 1000, 10 ** 0.8
    k = sum(papr(ofdm_oversampled(qpsk_block(rng, 64), 4)) > gamma for _ in range(trials))
    lo, _ = cbb.wilson(k, trials)
    assert lo > ccdf_rule(gamma, 64)
