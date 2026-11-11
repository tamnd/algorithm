# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/source-coding-theorem/. The authors are listed in prov/53WS0H.jsonl.

import itertools
import math
import random
from fractions import Fraction
from math import comb

import pytest

from source_coding_theorem import (
    TypicalSetCode, bernoulli_entropy, best_fixed_length_success, measured_error_rate, rank_fixed_weight,
    shannon_block_rate, unrank_fixed_weight,
)

P = 0.1
H = bernoulli_entropy(P)  # 0.4690 bits per symbol


def test_rank_is_a_bijection() -> None:
    for n in range(0, 9):
        for k in range(n + 1):
            seqs = [list(x) for x in itertools.product((0, 1), repeat=n) if sum(x) == k]
            ranks = [rank_fixed_weight(x) for x in seqs]
            assert ranks == list(range(comb(n, k)))  # lexicographic order
            for r, x in enumerate(seqs):
                assert unrank_fixed_weight(n, k, r) == x


def test_round_trip_on_typical_sequences() -> None:
    code = TypicalSetCode(60, P, 0.7)
    rng = random.Random(1)
    sent = 0
    for _ in range(300):
        x = [1 if rng.random() < P else 0 for _ in range(60)]
        idx = code.encode(x)
        if idx is not None:
            assert 0 <= idx < 2 ** code.bits
            assert code.decode(idx) == x
            sent += 1
    assert sent > 200


def test_rate_never_exceeds_target_by_a_bit() -> None:
    for R in (0.5, 0.6, 0.8):
        for n in (20, 100, 500):
            code = TypicalSetCode(n, P, R)
            assert code.bits <= math.ceil(n * R)


def test_error_vanishes_above_entropy() -> None:
    for R in (0.6, 0.8):
        errs = [TypicalSetCode(n, P, R).error_probability() for n in (50, 100, 200, 500, 1000)]
        assert all(a > b for a, b in zip(errs, errs[1:]))
        assert errs[-1] < 1e-4


def test_page_values() -> None:
    assert TypicalSetCode(200, P, 0.6).error_probability() == pytest.approx(0.04388176, abs=1e-8)
    assert TypicalSetCode(1000, P, 0.6).error_probability() == pytest.approx(1.7405e-05, rel=1e-3)
    assert float(best_fixed_length_success(1000, Fraction(1, 10), 400)) == pytest.approx(0.0193782, abs=1e-7)


def test_measured_error_matches_exact() -> None:
    code = TypicalSetCode(200, P, 0.6)
    exact = code.error_probability()
    trials = 2000
    measured = measured_error_rate(code, trials, seed=7)
    sd = math.sqrt(exact * (1 - exact) / trials)
    assert abs(measured - exact) < 4 * sd


def test_every_code_fails_below_entropy() -> None:
    # The best code with 2^(floor(nR)) codewords, R < H, succeeds with probability tending to 0.
    for R in (0.3, 0.4):
        succ = [float(best_fixed_length_success(n, Fraction(1, 10), math.floor(n * R))) for n in (50, 100, 200, 500, 1000)]
        assert all(a > b for a, b in zip(succ, succ[1:]))
        assert succ[-1] < 0.02


def test_best_code_succeeds_above_entropy() -> None:
    succ = float(best_fixed_length_success(1000, Fraction(1, 10), 600))
    assert succ > 1 - 1e-6


def test_variable_length_block_bounds() -> None:
    for p in (Fraction(1, 10), Fraction(1, 3), Fraction(1, 2)):
        h = bernoulli_entropy(float(p))
        for n in range(1, 21):
            rate = shannon_block_rate(n, p)
            assert h - 1e-12 <= rate < h + 1 / n
