# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/core-svp-hardness/. The authors are listed in prov/AEJ0J4.jsonl.
"""Tests for the core-SVP calculator.

There are no official test vectors for a cost model. The reference figures
are Table 4 of the CRYSTALS-Kyber round 3 specification (version 3.01,
January 2021), primal attack only:

    Kyber512: d = 1003, b = 403, classical 118, quantum 107
    Kyber768: d = 1424, b = 625, classical 182, quantum 165
    Kyber1024: d = 1885, b = 877, classical 256, quantum 232

The Kyber script models the noise and the success condition in more detail
than the plain GSA formula here, so the tests allow a 1% error in b and an
error of 1 bit in the costs.
"""

import math

from core_svp_hardness import (
    cbd_sigma,
    core_svp_bits,
    delta_bkz,
    dual_advantage,
    dual_cost_bits,
    kyber_primal,
    primal_block_size,
    primal_succeeds,
)

TABLE4 = {
    "Kyber512": (2, 3, 403, 118, 107),
    "Kyber768": (3, 2, 625, 182, 165),
    "Kyber1024": (4, 2, 877, 256, 232),
}


def test_core_svp_bits_of_table_block_sizes():
    # 0.292 b and 0.265 b at the table's own b agree with its bits within 1.
    # (For example 0.292 * 403 = 117.7 and 0.265 * 625 = 165.6.)
    for _, (_, _, b, cl, qu) in TABLE4.items():
        bits = core_svp_bits(b)
        assert abs(bits["classical"] - cl) < 1
        assert abs(bits["quantum"] - qu) < 1


def test_kyber_primal_matches_table4():
    for name, (k, eta1, b_ref, cl, qu) in TABLE4.items():
        b, m = kyber_primal(k, eta1)
        assert abs(b - b_ref) <= 0.01 * b_ref, name
        assert 0 < m <= (k + 1) * 256
        bits = core_svp_bits(b)
        assert abs(bits["classical"] - cl) <= 1, name
        assert abs(bits["quantum"] - qu) <= 1, name


def test_delta_decreases_with_block_size():
    prev = delta_bkz(50)
    for b in range(51, 1000, 7):
        cur = delta_bkz(b)
        assert 1.0 < cur < prev
        prev = cur
    assert abs(delta_bkz(403) - 1.00396) < 1e-4


def test_condition_is_monotone_in_b():
    n, q, s, m = 512, 3329, cbd_sigma(3), 480
    ok = [primal_succeeds(n, q, s, m, b) for b in range(300, 600)]
    first = ok.index(True)
    assert all(ok[first:])


def test_more_noise_needs_larger_block():
    n, q = 512, 3329
    b1, _ = primal_block_size(n, q, 1.0, 2 * n)
    b2, _ = primal_block_size(n, q, 2.0, 2 * n)
    assert b2 > b1


def test_dual_advantage_range():
    a = dual_advantage(512, 3329, cbd_sigma(3), 500, 400)
    assert 0.0 < a < 4.0
    # A larger block size gives a shorter dual vector and a larger advantage.
    assert dual_advantage(512, 3329, cbd_sigma(3), 500, 450) > a


def test_dual_cost_is_close_to_primal_for_kyber512():
    # A sanity check of the model, not a figure from the specification.
    bits, b, m = dual_cost_bits(512, 3329, cbd_sigma(3), 768)
    assert 0.292 * 350 < bits < 0.292 * 450
    assert math.isfinite(bits)
