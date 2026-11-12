# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/calinski-harabasz-index/. The authors are listed in prov/8Z3PGC.jsonl.

import random
from fractions import Fraction

import pytest

from calinski_harabasz_index import calinski_harabasz, scatter_matrices, trace

POINTS = [(0, 0), (2, 0), (1, 3), (8, 0), (10, 0), (9, 3), (4, 8), (6, 8), (5, 11)]
GOOD = [0, 0, 0, 1, 1, 1, 2, 2, 2]
MERGED = [0, 0, 0, 0, 0, 0, 1, 1, 1]


def test_total_scatter_splits_exactly() -> None:
    rng = random.Random(6)
    for _ in range(100):
        n = rng.randrange(2, 12)
        d = rng.randrange(1, 4)
        pts = [tuple(rng.randrange(-9, 10) for _ in range(d)) for _ in range(n)]
        lab = [rng.randrange(4) for _ in range(n)]
        W, B, T = scatter_matrices(pts, lab)
        assert all(T[s][t] == W[s][t] + B[s][t] for s in range(d) for t in range(d))


def test_example() -> None:
    W, B, T = scatter_matrices(POINTS, GOOD)
    assert W == [[6, 0], [0, 18]] and B == [[96, 0], [0, 128]] and T == [[102, 0], [0, 146]]
    assert calinski_harabasz(POINTS, GOOD) == Fraction(28)
    W, B, T = scatter_matrices(POINTS, MERGED)
    assert trace(W) == 120 and trace(B) == 128
    assert calinski_harabasz(POINTS, MERGED) == Fraction(112, 15)


def test_one_dimensional_is_anova_f() -> None:
    # d = 1: CH is the F statistic of a one-way analysis of variance.
    xs = [(1,), (2,), (3,), (7,), (8,), (12,)]
    lab = [0, 0, 0, 1, 1, 2]
    ssw = Fraction(2) + Fraction(1, 2) + 0
    grand = Fraction(33, 6)
    ssb = 3 * (2 - grand) ** 2 + 2 * (Fraction(15, 2) - grand) ** 2 + (12 - grand) ** 2
    assert calinski_harabasz(xs, lab) == (ssb / 2) / (ssw / 3)


def test_invariances() -> None:
    rng = random.Random(1)
    for _ in range(50):
        n = rng.randrange(4, 12)
        pts = [(rng.randrange(20), rng.randrange(20)) for _ in range(n)]
        lab = [i % 3 for i in range(n)]
        try:
            ch = calinski_harabasz(pts, lab)
        except ValueError:
            continue
        moved = [(3 * y - 7, -3 * x + 1) for x, y in pts]  # rotate by 90 degrees, scale by 3, shift
        assert calinski_harabasz(moved, lab) == ch


def test_undefined_cases() -> None:
    with pytest.raises(ValueError):
        calinski_harabasz(POINTS, [0] * 9)
    with pytest.raises(ValueError):
        calinski_harabasz(POINTS, list(range(9)))
