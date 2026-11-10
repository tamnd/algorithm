# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/memory-coalescing/.

import random
from fractions import Fraction

from memory_coalescing import (aos_field, efficiency, expected_random, kernel_transactions, lines,
                               strided_formula, transactions, warp_addresses)


def test_unit_stride_needs_four_sectors():
    assert transactions(lambda l: l) == 4
    assert efficiency(lambda l: l) == 1
    assert len(lines(warp_addresses(lambda l: l))) == 1


def test_guide_example_of_a_large_stride():
    # Guide 2.3.4.1: lanes 32 or more bytes apart need 32 transactions, 1024 bytes, 12.5 percent.
    assert transactions(lambda l: 8 * l) == 32
    assert efficiency(lambda l: 8 * l) == Fraction(1, 8)


def test_strided_counts_match_the_formula():
    for word in (4, 8):
        for stride in range(1, 40):
            assert transactions(lambda l: stride * l, word=word) == strided_formula(stride, word)
    assert [strided_formula(s) for s in range(1, 9)] == [4, 8, 12, 16, 20, 24, 28, 32]


def test_misaligned_unit_stride_needs_five_sectors():
    for offset in range(0, 128, 4):
        expect = 4 if offset % 32 == 0 else 5
        assert transactions(lambda l: l, base=offset) == expect


def test_permutation_inside_a_segment_is_free():
    rng = random.Random(7)
    for _ in range(50):
        perm = list(range(32))
        rng.shuffle(perm)
        assert transactions(lambda l: perm[l]) == 4


def test_broadcast_needs_one_sector():
    assert transactions(lambda l: 0) == 1


def test_random_access_matches_the_expected_count():
    rng = random.Random(8)
    words = 1 << 16
    trials = 2000
    total = 0
    for _ in range(trials):
        idx = [rng.randrange(words) for _ in range(32)]
        total += transactions(lambda l: idx[l])
    mean = Fraction(total, trials)
    expect = expected_random(words // 8)
    assert abs(float(mean - expect)) < 0.05
    assert 31.9 < float(expect) < 32


def test_aos_against_soa():
    # Struct of three floats: reading one field has stride 3 words.
    assert transactions(aos_field(3)) == 12 and transactions(aos_field(1)) == 4
    assert efficiency(aos_field(3)) == Fraction(1, 3)


def test_whole_kernel_count():
    for n in (1, 32, 33, 1000):
        assert kernel_transactions(n, lambda i: i) == sum(
            transactions(lambda l: l, active=range(min(32, n - 32 * w))) for w in range(-(-n // 32)))
    assert kernel_transactions(1024, lambda i: i) == 128
    assert kernel_transactions(1024, lambda i: 2 * i) == 256
