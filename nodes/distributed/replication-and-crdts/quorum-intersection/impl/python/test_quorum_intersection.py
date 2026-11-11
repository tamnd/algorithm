# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quorum-intersection/. The authors are listed in prov/6YJE35.jsonl.

from fractions import Fraction

from quorum_intersection import (all_meet, counting_bound, failure_probability, grid, load,
                                 masking_threshold, min_intersection, naor_wool_lower_bound,
                                 threshold)


def test_r_plus_w_greater_than_n_is_exactly_the_condition() -> None:
    for n in range(1, 8):
        for r in range(1, n + 1):
            for w in range(1, n + 1):
                m = min_intersection(threshold(n, r), threshold(n, w))
                assert m == counting_bound(n, r, w)  # the counting bound is tight
                assert (m >= 1) == (r + w > n)


def test_2w_greater_than_n_is_exactly_write_write_intersection() -> None:
    for n in range(1, 8):
        for w in range(1, n + 1):
            ws = threshold(n, w)
            assert all_meet(ws, ws) == (2 * w > n)


def test_page_example_numbers() -> None:
    # N = 5, R = 2, W = 4: one common server; 2W = 8 > 5
    assert min_intersection(threshold(5, 2), threshold(5, 4)) == 1
    assert all_meet(threshold(5, 4), threshold(5, 4))
    # N = 4, R = 3, W = 2: reads meet writes, but two writes can miss each other
    assert all_meet(threshold(4, 3), threshold(4, 2))
    assert not all_meet(threshold(4, 2), threshold(4, 2))


def test_grid_quorums() -> None:
    for k in range(2, 5):
        n = k * k
        g = grid(k)
        assert all(len(q) == 2 * k - 1 for q in g)
        assert all_meet(g, g, 2)  # a row and a column of another quorum meet in 2 places
        assert load(n, g) == Fraction(2 * k - 1, n)
        assert load(n, g) >= naor_wool_lower_bound(n, g)


def test_load_of_majority_and_star_and_the_lower_bound() -> None:
    for n in range(1, 10):
        maj = threshold(n, n // 2 + 1)
        assert load(n, maj) == Fraction(n // 2 + 1, n)
        assert load(n, maj) >= naor_wool_lower_bound(n, maj)
    # the star: every quorum holds server 0
    star = [frozenset({0, i}) for i in range(1, 6)]
    assert all_meet(star, star)
    assert load(6, star) == 1


def test_failure_probability_majority_beats_grid() -> None:
    p = Fraction(1, 10)
    assert failure_probability(9, threshold(9, 5), p) < failure_probability(9, grid(3), p)
    # majority of 9 fails when 5 or more servers fail
    from math import comb
    exact = sum(comb(9, i) * p ** i * (1 - p) ** (9 - i) for i in range(5, 10))
    assert failure_probability(9, threshold(9, 5), p) == exact
    assert round(float(exact), 5) == 0.00089
    assert round(float(failure_probability(9, grid(3), p)), 4) == 0.0333


def test_masking_quorums_need_n_greater_than_4f() -> None:
    for f in range(0, 4):
        for n in range(1, 18):
            q = masking_threshold(n, f)
            assert (q is not None) == (n >= 4 * f + 1)
            if q is not None and n <= 12:
                assert all_meet(threshold(n, q), threshold(n, q), 2 * f + 1)
