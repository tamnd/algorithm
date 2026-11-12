# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/size-classes/. The authors are listed in prov/3FJ7YX.jsonl.

from fractions import Fraction

import pytest

from size_classes import (
    geometric_classes,
    geometric_index,
    pow2_classes,
    round_up,
    worst_waste,
)


def test_example_lists() -> None:
    assert geometric_classes(4, 64) == [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 20, 24, 28, 32, 40, 48, 56, 64]
    assert pow2_classes(64) == [1, 2, 4, 8, 16, 32, 64]
    assert round_up(geometric_classes(4, 128), 65) == 80
    assert round_up(pow2_classes(128), 65) == 128
    with pytest.raises(ValueError):
        round_up([1, 2, 4], 5)
    with pytest.raises(ValueError):
        geometric_classes(3, 10)


def test_index_matches_search() -> None:
    for g in (1, 2, 4, 8):
        classes = geometric_classes(g, 1 << 14)
        for n in range(1, classes[-1] + 1):
            i = geometric_index(g, n)
            assert classes[i] == round_up(classes, n)


def test_geometric_bound_exhaustive() -> None:
    """If c[i+1] <= r c[i] for all i, every request n > c[0] wastes less than (r-1)/r of its block."""
    lists = [(1, pow2_classes(1 << 14))] + [(g, geometric_classes(g, 1 << 14)) for g in (1, 2, 4, 8, 16)]
    for g, classes in lists:
        tail = [c for c in classes if c >= g]  # sizes below g are all classes and waste nothing
        r = max(Fraction(b, a) for a, b in zip(tail, tail[1:]))
        for n in range(tail[0] + 1, classes[-1] + 1):
            c = round_up(classes, n)
            assert Fraction(c - n, c) < (r - 1) / r
        for n in range(1, tail[0] + 1):
            assert round_up(classes, n) == n


def test_ratio_and_tightness() -> None:
    for g in (1, 2, 4, 8):
        classes = geometric_classes(g, 1 << 16)
        tail = [c for c in classes if c >= g]
        r = max(Fraction(b, a) for a, b in zip(tail, tail[1:]))
        assert r == 1 + Fraction(1, g)
        # the bound 1/(g+1) is approached by the request just above a class
        assert 1 / (g + 1) - 0.01 < worst_waste(classes) < 1 / (g + 1)
    assert 0.49 < worst_waste(pow2_classes(1 << 16)) < 0.5
