# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forward-error-correction/. The authors are listed in prov/8PQV2E.jsonl.

import math
import random

from forward_error_correction import (
    HAMMING_CHECKS, HAMMING_ROWS, asymptotic_gain_hard_db, asymptotic_gain_soft_db, coded_ber,
    coding_gain_db, decode, decoded_ber, encode, required_ebn0_db, simulate_ber, syndrome,
    syndrome_table, uncoded_ber,
)

REP3_ROWS = [0b111]
REP3_CHECKS = [0b011, 0b101]


def test_hamming_code_and_decoder() -> None:
    assert all(syndrome(HAMMING_CHECKS, r) == 0 for r in HAMMING_ROWS)
    words = [encode(HAMMING_ROWS, m) for m in range(16)]
    assert len(set(words)) == 16
    assert min(w.bit_count() for w in words if w) == 3
    table = syndrome_table(HAMMING_CHECKS, 7)
    assert sorted(e.bit_count() for e in table.values()) == [0] + [1] * 7  # a perfect code
    for m in range(16):
        c = encode(HAMMING_ROWS, m)
        assert decode(HAMMING_CHECKS, table, c, 4) == m
        for i in range(7):
            assert decode(HAMMING_CHECKS, table, c ^ (1 << i), 4) == m


def test_uncoded_reference() -> None:
    # uncoded BPSK needs about 9.6 dB for a bit error rate of 1e-5
    assert abs(required_ebn0_db(uncoded_ber, 1e-5) - 9.59) < 0.005
    assert abs(uncoded_ber(0.0) - 0.0786) < 1e-4


def test_exact_ber_against_simulation() -> None:
    rng = random.Random(5)
    for ebn0 in (2.0, 4.0):
        exact = coded_ber(HAMMING_CHECKS, 7, 4, ebn0)
        sim = simulate_ber(HAMMING_ROWS, HAMMING_CHECKS, 7, 4, ebn0, 20000, rng)
        assert abs(sim - exact) < 5 * math.sqrt(exact / 80000) + 0.002


def test_ber_is_below_block_error_rate() -> None:
    for p in (1e-4, 1e-2, 0.1, 0.3):
        block = 1 - (1 - p) ** 7 - 7 * p * (1 - p) ** 6
        ber = decoded_ber(HAMMING_CHECKS, 7, 4, p)
        assert 0 < ber <= block


def test_coding_gain() -> None:
    gain = coding_gain_db(HAMMING_CHECKS, 7, 4, 1e-5)
    assert 0.40 < gain < 0.42
    assert abs(required_ebn0_db(lambda x: coded_ber(HAMMING_CHECKS, 7, 4, x), 1e-5) - 9.17) < 0.01
    # at high error rates the code loses: the rate penalty outweighs the correction
    assert coding_gain_db(HAMMING_CHECKS, 7, 4, 1e-2) < 0
    assert coded_ber(HAMMING_CHECKS, 7, 4, 5.8) > uncoded_ber(5.8)
    assert coded_ber(HAMMING_CHECKS, 7, 4, 5.9) < uncoded_ber(5.9)
    # the gain grows toward the hard-decision asymptotic value 10 log10(R (t + 1))
    assert abs(asymptotic_gain_soft_db(7, 4, 3) - 2.34) < 0.005
    assert abs(asymptotic_gain_hard_db(7, 4, 3) - 0.58) < 0.005
    g6, g9 = coding_gain_db(HAMMING_CHECKS, 7, 4, 1e-6), coding_gain_db(HAMMING_CHECKS, 7, 4, 1e-9)
    assert gain < g6 < g9 < asymptotic_gain_hard_db(7, 4, 3)


def test_repetition_code_loses() -> None:
    # the [3, 1, 3] code with hard decisions has asymptotic gain 10 log10(2/3) < 0
    assert all(syndrome(REP3_CHECKS, r) == 0 for r in REP3_ROWS)
    assert coding_gain_db(REP3_CHECKS, 3, 1, 1e-5) < 0
    assert abs(asymptotic_gain_hard_db(3, 1, 3) - 10 * math.log10(2 / 3)) < 1e-12
    assert abs(asymptotic_gain_soft_db(3, 1, 3)) < 1e-12
