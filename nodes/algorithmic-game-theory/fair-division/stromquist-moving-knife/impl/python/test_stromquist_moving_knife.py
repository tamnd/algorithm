# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stromquist-moving-knife/. The authors are listed in prov/PK1D3M.jsonl.

import random
from fractions import Fraction

import pytest

from agtcake import cut, normalize, value
from stromquist_moving_knife import stromquist

F = Fraction


def positive_valuation(rng: random.Random, k: int, hi: int):
    return normalize([rng.randint(1, hi) for _ in range(k)])


def bisect(v, x):
    """The knife of v at sword position x, by the helper (independent of the slug file)."""
    return cut(v, x, value(v, x, 1) / 2)


def shout_gap(v, x, y):
    """min(V[0, x] - V[x, y], V[0, x] - V[y, 1]); the agent shouts when it is >= 0."""
    left = value(v, 0, x)
    return min(left - value(v, x, y), left - value(v, y, 1))


def check_run(vals, grid: int = 0):
    pieces, x, y, s = stromquist(vals)
    # connected pieces that cover [0, 1] in order
    assert pieces[s] == (0, x)
    assert sorted(pieces.values()) == [(0, x), (x, y), (y, 1)]
    assert 0 < x <= y <= 1
    # y is the median knife at x
    knives = [bisect(v, x) for v in vals]
    assert y == sorted(knives)[1]
    # envy-free, exactly
    for i in range(3):
        own = value(vals[i], *pieces[i])
        for j in range(3):
            assert own >= value(vals[i], *pieces[j])
    # x is the first moment: the shouter's gap is 0, nobody else's is positive
    assert shout_gap(vals[s], x, y) == 0
    for i in range(3):
        assert shout_gap(vals[i], x, y) <= 0 or i == s
        if i < s:
            assert shout_gap(vals[i], x, y) < 0
    # a second method: on a grid of sword positions before x, nobody shouts
    for t in range(1, grid):
        z = F(t, grid)
        if z >= x:
            break
        yz = sorted(bisect(v, z) for v in vals)[1]
        assert all(shout_gap(v, z, yz) < 0 for v in vals)
    return pieces, x, y, s


def test_page_example() -> None:
    vals = [normalize([1, 1, 1, 1]), normalize([2, 2, 1, 1]), normalize([1, 1, 1, 3])]
    pieces, x, y, s = check_run(vals, grid=60)
    assert (x, y, s) == (F(2, 7), F(9, 14), 1)
    assert [bisect(v, x) for v in vals] == [F(9, 14), F(15, 28), F(67, 84)]
    assert pieces == {1: (0, F(2, 7)), 0: (F(2, 7), F(9, 14)), 2: (F(9, 14), 1)}
    table = [[value(vals[i], *pieces[j]) for j in range(3)] for i in range(3)]
    assert table == [
        [F(5, 14), F(2, 7), F(5, 14)],
        [F(8, 21), F(8, 21), F(5, 21)],
        [F(5, 21), F(4, 21), F(4, 7)],
    ]


def test_identical_valuations_give_thirds() -> None:
    rng = random.Random(5)
    for _ in range(20):
        v = positive_valuation(rng, rng.randint(1, 8), 6)
        pieces, x, y, s = check_run([v, v, v])
        assert s == 0
        assert all(value(v, *pieces[i]) == F(1, 3) for i in range(3))


def test_random_valuations() -> None:
    rng = random.Random(31)
    for _ in range(60):
        k = rng.randint(1, 8)
        vals = [positive_valuation(rng, k, 6) for _ in range(3)]
        check_run(vals, grid=24)


def test_needs_positive_densities() -> None:
    with pytest.raises(ValueError):
        stromquist([normalize([1, 0]), normalize([1, 1]), normalize([1, 1])])
