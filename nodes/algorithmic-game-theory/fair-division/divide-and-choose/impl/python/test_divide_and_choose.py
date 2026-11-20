# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/divide-and-choose/. The authors are listed in prov/EWY1RW.jsonl.

import random
from fractions import Fraction

import pytest

from agtcake import Oracle, cut, normalize, piece_value, random_valuation, value
from divide_and_choose import divide_and_choose

F = Fraction


# ---------------------------------------------------------------- the helper


def test_normalize() -> None:
    assert normalize([1, 1, 1, 1]) == [1, 1, 1, 1]
    assert normalize([3, 1, 0, 0]) == [3, 1, 0, 0]
    assert normalize([2, 0]) == [2, 0]
    assert normalize([1, 2, 3]) == [F(1, 2), F(1), F(3, 2)]
    for bad in ([], [0, 0], [1, -1]):
        with pytest.raises(ValueError):
            normalize(bad)


def test_value_by_hand() -> None:
    v = normalize([3, 1, 0, 0])
    assert value(v, 0, 1) == 1
    assert value(v, 0, F(1, 4)) == F(3, 4)
    assert value(v, F(1, 8), F(3, 8)) == F(3, 8) + F(1, 8)
    assert value(v, F(1, 2), 1) == 0
    assert value(v, F(1, 3), F(1, 3)) == 0
    with pytest.raises(ValueError):
        value(v, F(1, 2), F(1, 4))


def test_cut_by_hand() -> None:
    v = normalize([3, 1, 0, 0])
    assert cut(v, 0, F(1, 2)) == F(1, 6)
    assert cut(v, 0, F(3, 4)) == F(1, 4)
    assert cut(v, 0, 1) == F(1, 2)  # the least point, not 1
    assert cut(v, F(1, 2), F(1, 100)) is None
    assert cut(v, F(1, 2), 0) == F(1, 2)
    w = normalize([1, 0, 1])
    assert cut(w, 0, F(1, 2)) == F(1, 3)  # the least x, at the start of the zero segment
    assert cut(w, 0, F(1, 2) + F(1, 10)) == F(2, 3) + F(1, 15)


def test_cut_and_value_invert_each_other() -> None:
    rng = random.Random(20240101)
    for _ in range(300):
        k = rng.randint(1, 8)
        v = random_valuation(rng, k, 5)
        assert sum(v) == k and value(v, 0, 1) == 1
        a = F(rng.randint(0, 24), 24)
        rest = value(v, a, 1)
        t = rest * F(rng.randint(0, 12), 12)
        x = cut(v, a, t)
        assert x is not None and a <= x <= 1
        assert value(v, a, x) == t
        # x is the least such point: a little to the left the value is smaller
        if x > a:
            assert value(v, a, x - (x - a) / 1000) < t
        assert cut(v, a, rest + F(1, 1000)) is None
        b = a + (1 - a) * F(rng.randint(0, 10), 10)
        y = cut(v, a, value(v, a, b))
        assert y is not None and y <= b and value(v, y, b) == 0


def test_piece_value_and_additivity() -> None:
    rng = random.Random(7)
    for _ in range(100):
        v = random_valuation(rng, rng.randint(1, 8), 4)
        pts = sorted(F(rng.randint(0, 30), 30) for _ in range(3))
        a, b, c = pts
        assert value(v, a, c) == value(v, a, b) + value(v, b, c)
        assert piece_value(v, [(0, a), (b, 1)]) == 1 - value(v, a, b)


def test_oracle_counts() -> None:
    o = Oracle([normalize([1, 1]), normalize([1, 3])])
    assert o.n == 2
    assert o.eval_query(1, 0, F(1, 2)) == F(1, 4)
    assert o.cut_query(1, 0, F(1, 4)) == F(1, 2)
    assert o.cut_query(0, 0, F(1, 2)) == F(1, 2)
    assert o.evals == [0, 1] and o.cuts == [1, 1]
    assert o.total_evals() == 1 and o.total_cuts() == 2 and o.total() == 3


# ---------------------------------------------------------------- divide and choose


def check(vals, alloc) -> None:
    """Both pieces cover the cake, the cutter gets 1/2, and nobody envies."""
    a, b = alloc[0], alloc[1]
    ends = sorted(a + b)
    assert ends[0][0] == 0 and ends[-1][1] == 1 and ends[0][1] == ends[1][0]
    assert piece_value(vals[0], a) == F(1, 2)
    for i in (0, 1):
        own = piece_value(vals[i], alloc[i])
        other = piece_value(vals[i], alloc[1 - i])
        assert own >= other
        assert own >= F(1, 2)
        # brute force over the two pieces: the chooser has a best one
    assert piece_value(vals[1], b) == max(piece_value(vals[1], a), piece_value(vals[1], b))


def test_example() -> None:
    vals = [normalize([3, 1, 0, 0]), normalize([1, 1, 1, 1])]
    o = Oracle(vals)
    alloc = divide_and_choose(o)
    assert alloc[0] == [(0, F(1, 6))]
    assert alloc[1] == [(F(1, 6), 1)]
    assert piece_value(vals[1], alloc[1]) == F(5, 6)
    assert o.cuts == [1, 0] and o.evals == [0, 1]
    check(vals, alloc)


def test_identical_valuations() -> None:
    rng = random.Random(11)
    for _ in range(50):
        v = random_valuation(rng, rng.randint(1, 8), 6)
        alloc = divide_and_choose(Oracle([v, v]))
        assert piece_value(v, alloc[0]) == piece_value(v, alloc[1]) == F(1, 2)


def test_random_valuations() -> None:
    rng = random.Random(12345)
    for _ in range(400):
        vals = [random_valuation(rng, rng.randint(1, 8), 6) for _ in range(2)]
        o = Oracle(vals)
        alloc = divide_and_choose(o)
        check(vals, alloc)
        assert o.total() == 2


def test_roles_swapped() -> None:
    vals = [normalize([3, 1, 0, 0]), normalize([1, 1, 1, 1])]
    alloc = divide_and_choose(Oracle(vals), cutter=1, chooser=0)
    assert alloc[1] == [(F(1, 2), 1)] and alloc[0] == [(0, F(1, 2))]
    assert piece_value(vals[0], alloc[0]) == 1
