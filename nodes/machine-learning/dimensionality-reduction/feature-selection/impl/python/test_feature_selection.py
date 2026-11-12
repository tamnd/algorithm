# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/feature-selection/. The authors are listed in prov/MFR8P0.jsonl.

from fractions import Fraction
from itertools import combinations
import random

import pytest

from feature_selection import (
    backward_stepwise,
    best_subset,
    entropy,
    forward_stepwise,
    mrmr,
    mutual_information,
    rss,
)

# y = x1 + x2 exactly, but x3 alone is closer to y than x1 or x2 alone.
X = [[1, 0, 1], [0, 1, 1], [0, 0, 1]]
Y = [1, 1, 0]


def test_rss_is_exact_and_handles_dependent_columns() -> None:
    assert rss(X, Y, []) == 2
    assert [rss(X, Y, [j]) for j in range(3)] == [1, 1, Fraction(2, 3)]
    assert rss(X, Y, [0, 1]) == 0
    assert rss(X, Y, [0, 1, 2]) == 0
    x = [[1, 2, 3], [2, 4, 1], [0, 0, 5], [1, 2, 0]]  # column 1 is twice column 0
    y = [1, 2, 3, 4]
    assert rss(x, y, [0, 1]) == rss(x, y, [0])
    assert rss(x, y, [1, 0, 2]) == rss(x, y, [0, 2])


def test_greedy_forward_selection_is_not_optimal() -> None:
    path = forward_stepwise(X, Y, 2)
    assert path == [(2, Fraction(2, 3)), (0, Fraction(1, 2))]
    assert best_subset(X, Y, 2) == ((0, 1), Fraction(0))
    assert backward_stepwise(X, Y, 2) == [0, 1]


def test_forward_against_brute_force_on_random_data() -> None:
    rng = random.Random(7)
    strictly_worse = 0
    for _ in range(60):
        n, d = 6, 5
        x = [[rng.randint(-3, 3) for _ in range(d)] for _ in range(n)]
        y = [rng.randint(-3, 3) for _ in range(n)]
        for k in range(1, d + 1):
            path = forward_stepwise(x, y, k)
            subset, best = best_subset(x, y, k)
            assert rss(x, y, [j for j, _ in path]) == path[-1][1]
            assert path[-1][1] >= best
            assert best == min(rss(x, y, s) for s in combinations(range(d), k))
            strictly_worse += path[-1][1] > best
        assert forward_stepwise(x, y, 1)[0][1] == best_subset(x, y, 1)[1]  # one step is exact
    assert strictly_worse > 0


def test_forward_is_optimal_for_orthogonal_columns() -> None:
    rng = random.Random(3)
    x = [[2, 0, 0, 0], [0, 1, 0, 0], [0, 0, 3, 0], [0, 0, 0, 1], [0, 0, 0, 0]]
    for _ in range(20):
        y = [rng.randint(-5, 5) for _ in range(5)]
        for k in range(5):
            got = forward_stepwise(x, y, k)
            assert (got[-1][1] if got else rss(x, y, [])) == best_subset(x, y, k)[1]


def test_mutual_information() -> None:
    a = [0, 0, 1, 1]
    b = [0, 1, 0, 1]
    assert entropy(a) == pytest.approx(1.0)
    assert mutual_information(a, a) == pytest.approx(1.0)
    assert mutual_information(a, b) == pytest.approx(0.0)
    assert mutual_information(a, [2 * p + q for p, q in zip(a, b)]) == pytest.approx(1.0)


def test_mrmr_skips_a_redundant_copy() -> None:
    a = [0] * 8 + [1] * 8
    b = [0, 0, 0, 0, 1, 1, 1, 1] * 2
    y = [2 * p + q for p, q in zip(a, b)]
    noisy_b = [1 - v if i % 4 == 0 else v for i, v in enumerate(b)]
    noise = [0, 1] * 8
    feats = [a, a[:], noisy_b, noise]
    relevance = [mutual_information(f, y) for f in feats]
    assert relevance[0] == relevance[1] == pytest.approx(1.0)
    assert 0 < relevance[2] < 1 and relevance[3] == pytest.approx(0.0)
    top2_by_relevance = sorted(range(4), key=lambda j: -relevance[j])[:2]
    assert sorted(top2_by_relevance) == [0, 1]  # both copies of a
    assert mrmr(feats, y, 2) == [0, 2]


def test_bad_k() -> None:
    with pytest.raises(ValueError):
        best_subset(X, Y, 4)
    with pytest.raises(ValueError):
        forward_stepwise(X, Y, -1)
