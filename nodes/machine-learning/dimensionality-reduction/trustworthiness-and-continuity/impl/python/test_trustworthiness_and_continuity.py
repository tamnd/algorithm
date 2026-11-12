# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trustworthiness-and-continuity/. The authors are listed in prov/B3SH8J.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from trustworthiness_and_continuity import (
    continuity,
    normalizer,
    rank_matrix,
    trustworthiness,
    trustworthiness_and_continuity,
)

LINE = [[float(v)] for v in range(7)]


def brute_force(x, y, k):
    """Exact T and C from the definition, with ranks found by counting closer points."""
    n = len(x)

    def rank(p, i, j):
        dij = math.dist(p[i], p[j])
        return 1 + sum(1 for l in range(n) if l not in (i, j) and (math.dist(p[i], p[l]), l) < (dij, j))

    def hood(p, i):
        return {j for j in range(n) if j != i and rank(p, i, j) <= k}

    pt = pc = 0
    for i in range(n):
        hx, hy = hood(x, i), hood(y, i)
        pt += sum(rank(x, i, j) - k for j in hy - hx)
        pc += sum(rank(y, i, j) - k for j in hx - hy)
    c = Fraction(2, n * k * (2 * n - 3 * k - 1))
    return 1 - c * pt, 1 - c * pc


def test_tear_example_from_the_page():
    y = [[0.0], [1.0], [2.0], [3.0], [10.0], [11.0], [12.0]]
    t, c = trustworthiness_and_continuity(LINE, y, 2)
    assert t == pytest.approx(46 / 49) and c == pytest.approx(46 / 49)
    assert brute_force(LINE, y, 2) == (Fraction(46, 49), Fraction(46, 49))


def test_fold_example_from_the_page():
    y = [[3.0], [1.0], [0.0], [2.0], [4.0], [5.0], [6.0]]
    assert brute_force(LINE, y, 2) == (Fraction(37, 49), Fraction(40, 49))
    assert trustworthiness(LINE, y, 2) == pytest.approx(37 / 49)
    assert continuity(LINE, y, 2) == pytest.approx(40 / 49)


def test_perfect_embedding_scores_one():
    rng = random.Random(0)
    x = [[rng.gauss(0, 1) for _ in range(5)] for _ in range(20)]
    # A rotation of two coordinates, a scale and a shift keep all ranks.
    c, s = math.cos(0.7), math.sin(0.7)
    y = [[2 * (c * p[0] - s * p[1]) + 1, 2 * (s * p[0] + c * p[1]), 2 * p[2], 2 * p[3], 2 * p[4]] for p in x]
    for k in range(1, 10):
        assert trustworthiness_and_continuity(x, x, k) == (1.0, 1.0)
        t, cc = trustworthiness_and_continuity(x, y, k)
        assert t == pytest.approx(1.0) and cc == pytest.approx(1.0)


def test_scores_lie_in_unit_interval_and_match_brute_force():
    rng = random.Random(1)
    for trial in range(30):
        n = rng.randint(5, 12)
        x = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(n)]
        y = [[rng.gauss(0, 1) for _ in range(2)] for _ in range(n)]
        for k in range(1, (n - 1) // 2 + 1):
            t, c = trustworthiness_and_continuity(x, y, k)
            bt, bc = brute_force(x, y, k)
            assert t == pytest.approx(float(bt), abs=1e-12)
            assert c == pytest.approx(float(bc), abs=1e-12)
            assert 0.0 <= t <= 1.0 and 0.0 <= c <= 1.0


def test_normalizer_is_the_largest_penalty_of_one_point():
    # For one point the penalty is sum of (r - k) over the k output neighbors outside the
    # input neighborhood; the maximum over all k-subsets of ranks 1..n-1 is k (2n - 3k - 1) / 2.
    for n in range(3, 11):
        for k in range(1, n):
            if 2 * k >= n:
                continue
            best = max(sum(r - k for r in sub if r > k) for sub in itertools.combinations(range(1, n), k))
            assert Fraction(best) == Fraction(k * (2 * n - 3 * k - 1), 2)
            assert normalizer(n, k) == pytest.approx(1 / (n * best))


def test_normalizer_fails_for_large_k():
    # For k > n/2 the top k ranks include ranks below k, so the formula is not the maximum.
    for n, k in ((6, 4), (7, 5), (9, 6)):
        best = max(sum(r - k for r in sub if r > k) for sub in itertools.combinations(range(1, n), k))
        assert best != Fraction(k * (2 * n - 3 * k - 1), 2)
    # At k = n/2 the formula still gives the maximum, but the source states k < n/2.
    best = max(sum(r - 3 for r in sub if r > 3) for sub in itertools.combinations(range(1, 6), 3))
    assert best == Fraction(3 * (12 - 9 - 1), 2)
    with pytest.raises(ValueError):
        normalizer(6, 3)


def test_ties_are_broken_by_index():
    x = [[0.0], [1.0], [-1.0], [2.0]]
    r = rank_matrix(x)
    assert r[0] == [0, 1, 2, 3]  # points 1 and 2 tie at distance 1; the smaller index ranks first
