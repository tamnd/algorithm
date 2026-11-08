# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/halton-sequence/. The authors are listed in prov/MKABDE.jsonl.

import itertools
import math
import random
from fractions import Fraction as F

import pytest

from halton_sequence import (
    FIRST_PRIMES,
    HaltonStream,
    count_in_box,
    discrepancy_bound,
    halton,
    halton_points,
    radical_inverse,
    radical_inverse_float,
    radical_inverse_int,
    scrambled_radical_inverse,
    star_discrepancy_1d,
    star_discrepancy_2d,
)


def test_van_der_corput_base_2_and_3():
    assert [radical_inverse(i, 2) for i in range(8)] == [F(0), F(1, 2), F(1, 4), F(3, 4), F(1, 8), F(5, 8), F(3, 8), F(7, 8)]
    assert [radical_inverse(i, 3) for i in range(9)] == [F(k, 9) for k in (0, 3, 6, 1, 4, 7, 2, 5, 8)]
    assert radical_inverse(11, 2) == F(13, 16)  # 1011 -> 0.1101
    assert radical_inverse_int(0, 5) == (0, 1)


def test_halton_2_3_first_points():
    pts = halton_points(6, (2, 3))
    assert pts == [
        (F(0), F(0)),
        (F(1, 2), F(1, 3)),
        (F(1, 4), F(2, 3)),
        (F(3, 4), F(1, 9)),
        (F(1, 8), F(4, 9)),
        (F(5, 8), F(7, 9)),
    ]


def test_float_matches_exact():
    for b in (2, 3, 5, 7, 31):
        for i in range(2000):
            assert abs(radical_inverse_float(i, b) - float(radical_inverse(i, b))) < 1e-15


def test_stream_matches_direct():
    bases = (2, 3, 5, 7)
    for start in (0, 1, 26, 1000):
        st = HaltonStream(bases, start)
        for i in range(start, start + 500):
            assert st.next() == halton(i, bases)


def test_one_dimensional_stratification():
    # any b^k consecutive indices give each interval [j/b^k, (j+1)/b^k) exactly one point
    for b in (2, 3, 5):
        for k in (1, 2, 3):
            for start in (0, 7, 100):
                xs = [radical_inverse(i, b) for i in range(start, start + b ** k)]
                assert sorted(int(x * b ** k) for x in xs) == list(range(b ** k))


def test_two_dimensional_elementary_boxes():
    # N = 2^a 3^c consecutive points: each box of size 2^-a by 3^-c holds exactly one point
    for a, c in [(2, 1), (3, 2), (4, 2)]:
        n = 2 ** a * 3 ** c
        for start in (0, 5):
            pts = halton_points(n, (2, 3), start)
            cells = sorted((int(x * 2 ** a), int(y * 3 ** c)) for x, y in pts)
            assert cells == sorted(itertools.product(range(2 ** a), range(3 ** c)))


def test_elementary_box_counts_off_by_less_than_one():
    pts = halton_points(100, (2, 3, 5))
    for e in itertools.product(range(4), range(3), range(2)):
        m = 2 ** e[0] * 3 ** e[1] * 5 ** e[2]
        for a0 in range(2 ** e[0]):
            for a1 in range(3 ** e[1]):
                lows = (F(a0, 2 ** e[0]), F(a1, 3 ** e[1]), F(0))
                highs = (F(a0 + 1, 2 ** e[0]), F(a1 + 1, 3 ** e[1]), F(1, 5 ** e[2]))
                cnt = count_in_box(pts, lows, highs)
                assert abs(cnt - F(100, m)) < 1


def test_star_discrepancy_1d_values():
    assert star_discrepancy_1d([radical_inverse(i, 2) for i in range(4)]) == F(1, 4)
    assert star_discrepancy_1d([F(1, 2)]) == F(1, 2)
    # bound proved on the page, d = 1
    for n in (10, 100, 1000):
        xs = [radical_inverse(i, 2) for i in range(n)]
        assert star_discrepancy_1d(xs) <= discrepancy_bound(n, (2,))


def test_star_discrepancy_2d_against_bound_and_random():
    rng = random.Random(1)
    results = {}
    for n in (16, 64, 128):
        pts = halton_points(n, (2, 3))
        d = star_discrepancy_2d(pts)
        assert d <= discrepancy_bound(n, (2, 3))
        results[n] = d
        rnd = [(F(rng.randrange(2 ** 20), 2 ** 20), F(rng.randrange(2 ** 20), 2 ** 20)) for _ in range(n)]
        assert d < star_discrepancy_2d(rnd)
    assert results[128] < results[16]


def test_star_discrepancy_2d_small_exact():
    # first 4 points of Halton (2,3): (0,0), (1/2,1/3), (1/4,2/3), (3/4,1/9)
    # boxes [0, 3/4 + e) x [0, 2/3 + e) hold all 4 points with volume tending to 1/2
    pts = halton_points(4, (2, 3))
    assert star_discrepancy_2d(pts) == F(1, 2)
    G = 288
    grid = max(abs(F(count_in_box(pts, (0, 0), (F(a, G), F(c, G))), 4) - F(a * c, G * G))
               for a in range(1, G + 1, 3) for c in range(1, G + 1, 3))
    assert F(49, 100) < grid <= F(1, 2)


def test_qmc_integration_beats_monte_carlo():
    f = lambda x, y: x * y  # integral 1/4
    n = 4096
    pts = halton_points(n, (2, 3), start=1)
    qmc_err = abs(sum(float(x * y) for x, y in pts) / n - 0.25)
    assert qmc_err < 1e-3
    rng = random.Random(7)
    mc_errs = []
    for _ in range(5):
        mc_errs.append(abs(sum(rng.random() * rng.random() for _ in range(n)) / n - 0.25))
    assert qmc_err < sorted(mc_errs)[2]


def test_correlation_in_large_coprime_bases():
    # for i < 29, phi_29(i) = i/29 and phi_31(i) = i/31: the first points lie on a line through 0
    for i in range(29):
        x, y = halton(i, (29, 31))
        assert x == F(i, 29) and y == F(i, 31)
        assert y * 31 == x * 29
    # a digit scrambling with nontrivial permutations breaks the line
    rng = random.Random(3)
    perms29 = [[0] + rng.sample(range(1, 29), 28) for _ in range(4)]
    perms31 = [[0] + rng.sample(range(1, 31), 30) for _ in range(4)]
    xs = [scrambled_radical_inverse(i, 29, perms29) for i in range(1, 29)]
    ys = [scrambled_radical_inverse(i, 31, perms31) for i in range(1, 29)]
    assert any(y * 31 != x * 29 for x, y in zip(xs, ys))
    # scrambling keeps one-dimensional stratification
    assert sorted(int(scrambled_radical_inverse(i, 29, perms29) * 29) for i in range(29)) == list(range(29))


def test_edge_cases_and_errors():
    assert halton(0, FIRST_PRIMES[:10]) == (F(0),) * 10
    assert all(0 <= x < 1 for x in halton(10 ** 12, FIRST_PRIMES[:5]))
    with pytest.raises(ValueError):
        radical_inverse(3, 1)
    with pytest.raises(ValueError):
        radical_inverse(-1, 2)
    with pytest.raises(ValueError):
        HaltonStream((2, 1))
    # radical inverse is a bijection from {0..b^k - 1} onto {j / b^k}
    assert sorted(radical_inverse(i, 7) * 49 for i in range(49)) == list(range(49))


def test_chi_square_uniform_marginals():
    # 2000 points in base 5, 10 bins: stratification makes chi-square tiny (threshold 21.67 is the 1% point for 9 df)
    n, bins = 2000, 10
    counts = [0] * bins
    for i in range(n):
        counts[int(radical_inverse(i, 5) * bins)] += 1
    chi2 = sum((c - n / bins) ** 2 / (n / bins) for c in counts)
    assert chi2 < 21.67
    assert chi2 < 0.5
