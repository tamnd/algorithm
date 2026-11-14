# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hodges-lehmann-estimator/. The authors are listed in prov/WF6BA7.jsonl.

import random
from fractions import Fraction
from statistics import median

import pytest

from hodges_lehmann_estimator import (
    count_le, hodges_lehmann, hodges_lehmann_shift, select_sum,
)


def naive_hl(xs):
    """Oracle: list all n(n + 1)/2 Walsh averages, sort, take the median."""
    n = len(xs)
    walsh = [Fraction(xs[i] + xs[j], 2) for i in range(n) for j in range(i, n)]
    return median(walsh)


def naive_shift(xs, ys):
    return median([Fraction(y - x) for x in xs for y in ys])


def test_small_by_hand() -> None:
    # Walsh averages of (1, 2, 9): 1, 1.5, 5, 2, 5.5, 9 -> sorted 1 1.5 2 5 5.5 9, median 3.5.
    assert hodges_lehmann([1, 2, 9]) == Fraction(7, 2)
    # (0, 1): averages 0, 0.5, 1, median 0.5.
    assert hodges_lehmann([0, 1]) == Fraction(1, 2)
    assert hodges_lehmann([5]) == 5
    # The example of the page.
    assert hodges_lehmann([3, 7, 1, 20, 4]) == 5
    # Shift: x = (1, 2), y = (4, 9): differences 3 8 2 7, median 5.
    assert hodges_lehmann_shift([1, 2], [4, 9]) == 5


def test_against_all_walsh_averages() -> None:
    rng = random.Random(11)
    for _ in range(300):
        n = rng.randint(1, 40)
        xs = [rng.randint(-20, 20) for _ in range(n)]
        assert hodges_lehmann(xs, seed=rng.randint(0, 10**6)) == naive_hl(xs)


def test_shift_against_all_differences() -> None:
    rng = random.Random(12)
    for _ in range(200):
        m, n = rng.randint(1, 25), rng.randint(1, 25)
        xs = [rng.randint(-9, 9) for _ in range(m)]
        ys = [rng.randint(-9, 9) for _ in range(n)]
        assert hodges_lehmann_shift(xs, ys, seed=rng.randint(0, 10**6)) == naive_shift(xs, ys)


def test_every_rank_of_select() -> None:
    rng = random.Random(13)
    for _ in range(40):
        n = rng.randint(1, 15)
        x = sorted(rng.randint(0, 8) for _ in range(n))
        cells = sorted(x[i] + x[j] for i in range(n) for j in range(i, n))
        for k in range(1, len(cells) + 1):
            assert select_sum(x, x, list(range(n)), k, rng) == cells[k - 1]


def test_count_le_matches_brute_force() -> None:
    rng = random.Random(14)
    for _ in range(200):
        n = rng.randint(1, 12)
        x = sorted(rng.randint(0, 10) for _ in range(n))
        v = rng.randint(-1, 21)
        c, _ = count_le(x, x, list(range(n)), v)
        assert c == sum(1 for i in range(n) for j in range(i, n) if x[i] + x[j] <= v)
        c, _ = count_le(x, x, list(range(n)), v, strict=True)
        assert c == sum(1 for i in range(n) for j in range(i, n) if x[i] + x[j] < v)


def test_large_input_is_fast_and_correct() -> None:
    rng = random.Random(15)
    xs = [rng.gauss(0.0, 1.0) for _ in range(2000)]
    est = hodges_lehmann(xs)
    walsh = sorted((xs[i] + xs[j]) / 2 for i in range(0, 2000, 1) for j in range(i, 2000))
    assert est == pytest.approx((walsh[len(walsh) // 2 - 1] + walsh[len(walsh) // 2]) / 2, abs=1e-12)


def test_tukey_identity() -> None:
    # W+ (sum of the ranks of |d_i| over d_i > 0) equals #{i <= j : d_i + d_j > 0}.
    rng = random.Random(16)
    for _ in range(200):
        n = rng.randint(1, 15)
        mags = rng.sample(range(1, 100), n)
        d = [m if rng.random() < 0.5 else -m for m in mags]
        order = sorted(range(n), key=lambda i: abs(d[i]))
        rank = {i: r + 1 for r, i in enumerate(order)}
        w_plus = sum(rank[i] for i in range(n) if d[i] > 0)
        pairs = sum(1 for i in range(n) for j in range(i, n) if d[i] + d[j] > 0)
        assert w_plus == pairs


def finite_breakdown_count(n):
    total = n * (n + 1) // 2
    need = (total + 1) // 2
    return next(m for m in range(n + 1) if total - (n - m) * (n - m + 1) // 2 >= need)


def test_empirical_breakdown() -> None:
    # Move k points to a huge t: bounded for k < m*, unbounded at k = m*.
    rng = random.Random(17)
    for n in (5, 10, 20):
        mstar = finite_breakdown_count(n)
        clean = [rng.randint(0, 50) for _ in range(n)]
        for t in (10**9, 10**18):
            for k in range(mstar + 1):
                ys = clean[:n - k] + [t] * k
                v = hodges_lehmann(ys)
                if k < mstar:
                    assert min(clean[:n - k]) <= v <= max(clean[:n - k])
                else:
                    assert v >= Fraction(t, 4)
    assert [finite_breakdown_count(n) for n in (5, 10, 20, 100)] == [2, 4, 6, 30]


def test_errors() -> None:
    with pytest.raises(ValueError):
        hodges_lehmann([])
    with pytest.raises(ValueError):
        hodges_lehmann_shift([], [1])
