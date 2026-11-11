# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bkw-algorithm/. The authors are listed in prov/R2MHB2.jsonl.
"""Tests for the BKW algorithm on toy LPN instances.

BKW is a cryptanalytic algorithm with no official test vectors. The
oracle is the secret used to make the samples: 500 random instances with
a fixed seed must give it back, and larger runs with n = 24 and n = 32
must too. Other tests check the reduction step and the bias formula.
"""

import random

from bkw_algorithm import (
    bias_after,
    bkw,
    lpn_samples,
    parity,
    reduce_block,
    solve_block_majority,
    solve_block_wht,
)


def test_reduce_block_clears_block_and_keeps_relation():
    rng = random.Random(1)
    samples, s = lpn_samples(16, 2000, 0.0, rng)
    R = reduce_block(samples, 1, 4)
    assert len(R) >= 2000 - 16
    for x, y in R:
        assert (x >> 4) & 0xF == 0
        assert y == parity(x & s)


def test_noiseless_is_exact():
    rng = random.Random(2)
    for _ in range(30):
        samples, s = lpn_samples(16, 1024, 0.0, rng)
        assert bkw(samples, 4, 4) == s


def test_random_instances_against_secret():
    rng = random.Random(3)
    wins = 0
    for _ in range(500):
        tau = rng.choice((0.0, 0.03, 0.05))
        samples, s = lpn_samples(12, 1024, tau, rng)
        wins += bkw(samples, 3, 4) == s
    assert wins >= 497


def test_n24_tau_005():
    rng = random.Random(4)
    for _ in range(3):
        samples, s = lpn_samples(24, 1 << 14, 0.05, rng)
        assert bkw(samples, 3, 8) == s


def test_n32_wht_final_step():
    rng = random.Random(5)
    samples, s = lpn_samples(32, 1 << 14, 0.05, rng)
    assert bkw(samples, 4, 8, final="wht") == s


def test_bias_squares_per_level():
    tau = 0.05
    d = 1 - 2 * tau
    assert abs(bias_after(tau, 0) - d) < 1e-12
    for k in range(1, 5):
        assert abs(bias_after(tau, k) - bias_after(tau, k - 1) ** 2) < 1e-12
    # Empirical check at two levels: the error rate of reduced samples.
    # One run varies a lot, because many outputs share a representative,
    # so the test averages 8 runs.
    rng = random.Random(6)
    rates = []
    for _ in range(8):
        samples, s = lpn_samples(24, 1 << 14, tau, rng)
        R = reduce_block(reduce_block(samples, 0, 8), 1, 8)
        rates.append(sum(y != parity(x & s) for x, y in R) / len(R))
    want = (1 - bias_after(tau, 2)) / 2  # about 0.172
    assert abs(sum(rates) / len(rates) - want) < 0.025


def test_wht_and_majority_agree_on_clean_block():
    rng = random.Random(7)
    samples, s = lpn_samples(8, 4000, 0.0, rng)  # each unit vector about 15 times
    assert solve_block_majority(samples, 0, 8) == solve_block_wht(samples, 0, 8) == s
