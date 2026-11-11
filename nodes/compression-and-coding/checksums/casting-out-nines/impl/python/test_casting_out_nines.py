# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/casting-out-nines/. The authors are listed in prov/SXWWDF.jsonl.

import random

import pytest

from casting_out_nines import (
    check_addition,
    check_addition11,
    check_multiplication,
    check_multiplication11,
    excess9,
    excess11,
)


def test_page_example() -> None:
    a, b = 3248, 1765
    assert a * b == 5732720
    assert (excess9(a), excess9(b), excess9(a * b)) == (8, 1, 8)
    assert check_multiplication(a, b, 5732720)
    # A slip that swaps two adjacent digits of the product passes the nines check
    # but fails the elevens check.
    assert check_multiplication(a, b, 5723720)
    assert not check_multiplication11(a, b, 5723720)
    # A slip of one digit is caught.
    assert not check_multiplication(a, b, 5732820)


def test_edges() -> None:
    assert excess9(0) == 0 and excess9(9) == 0 and excess9(18) == 0 and excess9(8) == 8
    assert excess11(0) == 0 and excess11(11) == 0 and excess11(10) == 10
    with pytest.raises(ValueError):
        excess9(-1)


def test_excess_against_mod() -> None:
    rng = random.Random(14101)
    for _ in range(2000):
        x = rng.choice([rng.randrange(100), rng.randrange(10**6), rng.randrange(10**40)])
        assert excess9(x) == x % 9
        assert excess11(x) == x % 11


def test_correct_results_always_pass() -> None:
    rng = random.Random(14102)
    for _ in range(1000):
        a, b = rng.randrange(10**12), rng.randrange(10**12)
        assert check_addition(a, b, a + b) and check_multiplication(a, b, a * b)
        assert check_addition11(a, b, a + b) and check_multiplication11(a, b, a * b)


def test_missed_errors_are_exactly_multiples_of_9() -> None:
    # Every wrong product c of x * y with 0 <= x, y < 30 and 0 <= c < 1000.
    missed = 0
    expected = 0
    for x in range(30):
        for y in range(30):
            t = x * y
            for c in range(1000):
                if c == t:
                    continue
                got = check_multiplication(x, y, c)
                assert got == ((c - t) % 9 == 0)
                missed += got
                expected += (c - t) % 9 == 0
            # the same rule for sums
            for c in range(0, 100):
                if c != x + y:
                    assert check_addition(x, y, c) == ((c - x - y) % 9 == 0)
    assert missed == expected == 99260  # of 900 * 999 = 899100 wrong products


def test_nines_and_elevens_together_miss_only_multiples_of_99() -> None:
    missed = 0
    for x in range(30):
        for y in range(30):
            t = x * y
            for c in range(1000):
                if c != t:
                    both = check_multiplication(x, y, c) and check_multiplication11(x, y, c)
                    assert both == ((c - t) % 99 == 0)
                    missed += both
    assert missed == 8258


def test_digit_transpositions_and_nine_shifts() -> None:
    rng = random.Random(14103)
    for _ in range(1000):
        a, b = rng.randrange(1, 10**6), rng.randrange(1, 10**6)
        s = list(str(a * b))
        i, j = sorted(rng.sample(range(len(s)), 2)) if len(s) > 1 else (0, 0)
        s[i], s[j] = s[j], s[i]
        wrong = int("".join(s))
        assert check_multiplication(a, b, wrong)  # any permutation of the digits passes
        if j == i + 1 and s[i] != s[j]:
            assert not check_multiplication11(a, b, wrong)  # adjacent swap fails mod 11
        k = rng.randrange(1, 1000)
        assert check_multiplication(a, b, a * b + 9 * k)
        assert check_multiplication(a, b, a * b * 10)  # a dropped or extra 0 is missed
        assert not check_multiplication(a, b, a * b + rng.choice([1, 2, 3, 4, 5, 6, 7, 8]))
