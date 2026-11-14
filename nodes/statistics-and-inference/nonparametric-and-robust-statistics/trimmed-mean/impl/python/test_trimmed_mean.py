# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trimmed-mean/. The authors are listed in prov/4F0CN9.jsonl.

import random
from fractions import Fraction

import pytest

from trimmed_mean import select, trim_count, trimmed_mean, winsorized_variance


def by_sorting(xs, g):
    """Oracle: sort, cut g values from each end, average exactly."""
    s = sorted(xs)
    kept = s[g:len(s) - g]
    return sum(kept, Fraction(0)) / len(kept)


def test_small_samples_by_hand() -> None:
    # sorted: 1 1 2 3 3 4 5 5 6 9; g = 2 keeps 2 3 3 4 5 5, sum 22.
    xs = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    assert trimmed_mean(xs, Fraction(1, 5)) == Fraction(22, 6)
    # g = 0 is the mean, 39 / 10.
    assert trimmed_mean(xs, 0) == Fraction(39, 10)
    # g = 4 keeps 3 and 4.
    assert trimmed_mean(xs, g=4) == Fraction(7, 2)
    # (2, 4, 4, 5, 7, 9, 30) with g = 1 keeps 4 4 5 7 9.
    assert trimmed_mean([2, 4, 4, 5, 7, 9, 30], g=1) == Fraction(29, 5)
    # the example of the page
    # sorted: 1 3 4 5 6 7 8 10 12 95; g = 2 keeps 4 5 6 7 8 10, sum 40.
    assert trimmed_mean([12, 7, 3, 95, 5, 8, 6, 1, 10, 4], Fraction(1, 5)) == Fraction(20, 3)


def test_trim_count_is_exact() -> None:
    assert trim_count(100, 0.29) == 29
    assert trim_count(10, 0.1) == 1
    assert trim_count(7, 0.1) == 0
    assert trim_count(20, Fraction(1, 4)) == 5
    with pytest.raises(ValueError):
        trim_count(10, 0.5)


def test_against_sorting_random() -> None:
    rng = random.Random(1)
    for _ in range(400):
        n = rng.randint(1, 40)
        xs = [rng.randint(-5, 5) for _ in range(n)]  # many ties
        g = rng.randint(0, (n - 1) // 2)
        assert trimmed_mean(xs, g=g, seed=rng.randint(0, 10**6)) == by_sorting(xs, g)


def test_select_postcondition() -> None:
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(1, 30)
        a = [rng.randint(0, 6) for _ in range(n)]
        lo = rng.randint(0, n - 1)
        hi = rng.randint(lo, n - 1)
        k = rng.randint(lo, hi)
        before = list(a)
        select(a, lo, hi, k, rng)
        assert a[:lo] == before[:lo] and a[hi + 1:] == before[hi + 1:]
        assert sorted(a[lo:hi + 1]) == sorted(before[lo:hi + 1])
        assert all(v <= a[k] for v in a[lo:k]) and all(v >= a[k] for v in a[k + 1:hi + 1])


def test_input_not_changed_and_float_data() -> None:
    xs = [0.5, 2.25, -1.0, 7.5, 3.0]
    copy = list(xs)
    assert trimmed_mean(xs, g=1) == pytest.approx((0.5 + 2.25 + 3.0) / 3)
    assert xs == copy


def test_empirical_breakdown() -> None:
    # Move k points to a huge value t. The trimmed mean stays in the range of the
    # clean points for k <= g, and grows without bound for k = g + 1.
    rng = random.Random(3)
    n, g = 20, 4
    clean = [rng.randint(0, 100) for _ in range(n)]
    for t in (10**6, 10**12, 10**30):
        for k in range(0, g + 2):
            ys = clean[:n - k] + [t] * k
            v = trimmed_mean(ys, g=g)
            lo, hi = min(clean[:n - k]), max(clean[:n - k])
            if k <= g:
                assert lo <= v <= hi
            else:
                assert v >= Fraction(t, n - 2 * g)
    # The mean (g = 0) breaks with one point.
    assert trimmed_mean(clean[:-1] + [10**30], g=0) > 10**28


def test_winsorized_variance_small() -> None:
    # g = 1 on (1, 2, 3, 4, 100): Winsorized sample (2, 2, 3, 4, 4), mean 3, variance 4 / 4.
    assert winsorized_variance([1, 2, 3, 4, 100], 1) == 1


def test_errors() -> None:
    with pytest.raises(ValueError):
        trimmed_mean([1, 2], g=1)
    with pytest.raises(ValueError):
        trimmed_mean([], 0)
