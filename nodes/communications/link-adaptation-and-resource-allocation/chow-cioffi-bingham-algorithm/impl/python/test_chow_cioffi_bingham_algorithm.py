# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chow-cioffi-bingham-algorithm/. The authors are listed in prov/KRYPZ8.jsonl.

import math
import random

import pytest

from chow_cioffi_bingham_algorithm import chow_cioffi_bingham, loading_power, optimal_power


def check_output(snr, target, gap, budget, bits, energy, margin, b_max=None):
    assert sum(bits) == target
    assert min(bits) >= 0
    if b_max is not None:
        assert max(bits) <= b_max
    assert abs(sum(energy) - budget) < 1e-9 * budget
    for b, e, s in zip(bits, energy, snr):
        if b == 0:
            assert e == 0
        else:
            assert abs(s * e / (gap * (2**b - 1)) - margin) < 1e-9 * margin


def test_page_example() -> None:
    snr = [20, 9, 5, 1.5]
    bits, energy, margin, rounds = chow_cioffi_bingham(snr, 8)
    assert bits == [3, 2, 2, 1] and rounds == 3
    assert abs(loading_power(snr, bits) - 1.95) < 1e-12
    assert abs(margin - 4 / 1.95) < 1e-12
    assert abs(optimal_power(snr, 8) - 101 / 60) < 1e-12
    assert abs(10 * math.log10(1.95 / (101 / 60)) - 0.638) < 1e-3
    check_output(snr, 8, 1.0, 4.0, bits, energy, margin)


def test_targets_budget_and_equal_margin() -> None:
    rng = random.Random(41)
    for _ in range(300):
        n = rng.randint(1, 64)
        snr = [rng.expovariate(1 / 1000) + 0.5 for _ in range(n)]
        gap = 10 ** (rng.uniform(0, 10) / 10)
        b_max = rng.choice([None, 15])
        target = rng.randint(1, 6 * n)
        budget = rng.uniform(1, 100)
        bits, energy, margin, rounds = chow_cioffi_bingham(snr, target, gap, budget, b_max=b_max)
        assert 1 <= rounds <= 10
        check_output(snr, target, gap, budget, bits, energy, margin, b_max)


def test_never_better_than_the_optimum_and_close_on_average() -> None:
    rng = random.Random(42)
    losses = []
    for _ in range(200):
        n = rng.randint(16, 64)
        snr = [rng.expovariate(1 / 1000) + 0.5 for _ in range(n)]
        gap = 10 ** 0.98
        target = rng.randint(n, 6 * n)
        bits, _, _, _ = chow_cioffi_bingham(snr, target, gap)
        ratio = loading_power(snr, bits, gap) / optimal_power(snr, target, gap)
        assert ratio >= 1 - 1e-12
        losses.append(10 * math.log10(ratio))
    assert sum(losses) / len(losses) < 0.3


def test_one_round_when_rounding_hits_the_target() -> None:
    snr = [3.0, 15.0, 63.0]
    bits, _, margin, rounds = chow_cioffi_bingham(snr, 2 + 4 + 6)
    assert bits == [2, 4, 6] and rounds == 1
    assert abs(margin - 3 / 3) < 1e-12


def test_fix_up_after_max_count() -> None:
    snr = [20, 9, 5, 1.5]
    bits, _, _, rounds = chow_cioffi_bingham(snr, 8, max_count=1)
    assert rounds == 1 and bits == [4, 2, 2, 0]
    assert abs(loading_power(snr, bits) - optimal_power(snr, 8)) < 1e-12
    bits, _, _, rounds = chow_cioffi_bingham(snr, 5, max_count=1)
    assert rounds == 1 and sum(bits) == 5


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        chow_cioffi_bingham([], 1)
    with pytest.raises(ValueError):
        chow_cioffi_bingham([1, 0], 1)
    with pytest.raises(ValueError):
        chow_cioffi_bingham([1, 2], 31, b_max=15)
    with pytest.raises(ValueError):
        chow_cioffi_bingham([1e-9], 1, gap=1e9)
    bits, energy, margin, _ = chow_cioffi_bingham([5, 7], 0)
    assert bits == [0, 0] and energy == [0.0, 0.0] and margin == math.inf
