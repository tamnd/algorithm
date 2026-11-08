# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lemire-bounded-integers/. The authors are listed in prov/N47W7S.jsonl.

import pytest

from lemire_bounded_integers import (
    accepted_outputs,
    division_rejection,
    lemire_bounded,
    lemire_bounded_counted,
    rejected_words,
    splitmix64,
    word_stream,
)


@pytest.mark.parametrize("w", [1, 2, 3, 4, 5, 6, 7, 8])
def test_exactly_uniform_by_enumeration(w):
    for s in range(1, (1 << w) + 1):
        counts = accepted_outputs(s, w)
        assert sorted(counts) == list(range(s))
        assert set(counts.values()) == {(1 << w) // s}
        assert len(rejected_words(s, w)) == (1 << w) % s


def test_worked_example_w8_s6():
    assert rejected_words(6, 8) == [0, 43, 128, 171]
    assert lemire_bounded_counted(6, word_stream([200]), 8) == (4, 1, 0)
    assert lemire_bounded_counted(6, word_stream([43, 0, 85]), 8) == (1, 3, 1)
    assert lemire_bounded_counted(6, word_stream([42]), 8) == (0, 1, 0)  # low = 252


def test_power_of_two_and_extreme_ranges():
    w = 32
    top = (1 << w) - 1
    # s = 1: always 0, never rejects.
    for x in (0, 1, top):
        assert lemire_bounded_counted(1, word_stream([x]), w)[:2] == (0, 1)
    # s = 2^w: the word itself; the low half is always 0, so the (trivial) division runs.
    for x in (0, 12345, top):
        assert lemire_bounded_counted(1 << w, word_stream([x]), w) == (x, 1, 1)
    # s a power of two: the top bits, never a rejection.
    for x in (0, 1, top, 0x80000000):
        assert lemire_bounded(1 << 10, word_stream([x]), w) == x >> 22
    # s = 2^(w-1) + 1: about half the words are rejected.
    s = (1 << (w - 1)) + 1
    assert ((1 << w) % s) == (1 << (w - 1)) - 1


def test_bad_ranges_rejected():
    for s in (0, -3, (1 << 8) + 1):
        with pytest.raises(ValueError):
            lemire_bounded(s, word_stream([1]), 8)


def test_divisions_are_rare_for_small_ranges():
    rnd = splitmix64(1)
    divisions = 0
    n = 20000
    for _ in range(n):
        v, _, d = lemire_bounded_counted(1000, rnd, 64)
        assert 0 <= v < 1000
        divisions += d
    assert divisions <= 1  # probability of a division is s / 2^64 per call
    rnd = splitmix64(2)
    assert all(division_rejection(1000, rnd, 64)[2] == 2 for _ in range(100))


def test_expected_draws_for_worst_case_range():
    # s = 3 * 2^30 with w = 32: 2^32 mod s = 2^30, so a quarter of the words are rejected.
    s, w = 3 << 30, 32
    rnd32 = splitmix64(3)
    total = 0
    n = 20000
    for _ in range(n):
        v, draws, _ = lemire_bounded_counted(s, lambda: rnd32() >> 32, w)
        assert 0 <= v < s
        total += draws
    mean = total / n
    assert abs(mean - 4 / 3) < 0.03  # expected draws 2^32 / (2^32 - 2^30) = 4/3


def test_chi_square_small_range():
    rnd = splitmix64(4)
    s, n = 7, 14000
    counts = [0] * s
    for _ in range(n):
        counts[lemire_bounded(s, rnd, 64)] += 1
    chi2 = sum((c - n / s) ** 2 / (n / s) for c in counts)
    assert chi2 < 22.46  # 0.999 quantile of chi-square with 6 degrees of freedom


def test_same_distribution_as_division_method_by_enumeration():
    w = 6
    for s in range(1, 1 << w):
        t = (1 << w) % s
        classic = {}
        for x in range(1 << w):
            if x >= ((1 << w) - s) % s:
                classic[x % s] = classic.get(x % s, 0) + 1
        assert classic == accepted_outputs(s, w)
        assert t == ((1 << w) - s) % s
