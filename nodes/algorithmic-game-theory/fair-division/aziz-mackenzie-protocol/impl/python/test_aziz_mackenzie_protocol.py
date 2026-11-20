# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aziz-mackenzie-protocol/. The authors are listed in prov/3197Z9.jsonl.
# Tests of a toy for three agents. They do not test the protocol of Aziz and Mackenzie or its bound.

import random
from fractions import Fraction

import pytest

from agtcake import Oracle, normalize, piece_value, random_valuation
from aziz_mackenzie_protocol import (
    aziz_mackenzie_toy,
    cut_and_choose,
    dominates,
    dominates_value,
    piece_eval,
    trimming_round,
)

F = Fraction


def check_partition(alloc) -> None:
    """The pieces are disjoint and cover [0, 1]."""
    assert sorted(alloc) == [0, 1, 2]
    ivs = sorted(iv for i in range(3) for iv in alloc[i])
    assert ivs[0][0] == 0 and ivs[-1][1] == 1
    for (a1, b1), (a2, b2) in zip(ivs, ivs[1:]):
        assert a1 < b1 == a2 < b2


def check_envy_free(vals, alloc) -> None:
    for i in range(3):
        own = piece_value(vals[i], alloc[i])
        for j in range(3):
            assert own >= piece_value(vals[i], alloc[j])


def test_page_example_domination() -> None:
    # The row of agent 1 in the example: X_1 = 0.40, X_2 = 0.15, X_3 = X_4 = 0.20, R = 0.05.
    own = F(40, 100)
    others = [F(15, 100), F(20, 100), F(20, 100)]
    assert all(dominates_value(own, x, F(5, 100)) for x in others)
    # With V_1(R) = 0.30, agent 1 does not dominate agent 3.
    assert not dominates_value(own, F(20, 100), F(30, 100))


def test_round_makes_cutter_dominate_taker() -> None:
    rng = random.Random(8)
    for _ in range(100):
        vals = [random_valuation(rng, 6, 5) for _ in range(3)]
        o = Oracle(vals)
        give, rest, taker = trimming_round(o, [(F(0), F(1))], 1, 2, 0)
        alloc = {i: list(give[i]) for i in range(3)}
        for i in range(3):
            for j in range(3):
                assert piece_eval(o, i, alloc[i]) >= piece_eval(o, i, alloc[j])
        assert dominates(o, 1, taker, alloc, rest)


def test_cut_and_choose_gives_out_everything() -> None:
    rng = random.Random(4)
    for _ in range(50):
        vals = [random_valuation(rng, 5, 5) for _ in range(3)]
        o = Oracle(vals)
        rest = [(F(0), F(1, 3)), (F(1, 2), F(1))]
        give = cut_and_choose(o, rest, 0, 2)
        assert sorted(give) == [0, 2]
        assert sum(b - a for p in give.values() for a, b in p) == F(1, 3) + F(1, 2)
        assert piece_eval(o, 2, give[2]) >= piece_eval(o, 2, give[0])
        assert piece_eval(o, 0, give[0]) == piece_eval(o, 0, give[2])


def test_identical_valuations() -> None:
    rng = random.Random(3)
    for _ in range(20):
        v = random_valuation(rng, rng.randint(1, 8), 5)
        alloc, rounds = aziz_mackenzie_toy(Oracle([v, v, v]))
        check_partition(alloc)
        assert all(piece_value(v, alloc[i]) == F(1, 3) for i in range(3))


def test_random_valuations() -> None:
    rng = random.Random(2024)
    for _ in range(100):
        vals = [random_valuation(rng, rng.randint(1, 6), 5) for _ in range(3)]
        o = Oracle(vals)
        alloc, rounds = aziz_mackenzie_toy(o, max_rounds=12)
        check_partition(alloc)
        check_envy_free(vals, alloc)
        assert 1 <= rounds <= 13


def test_round_cap_uses_the_fallback() -> None:
    vals = [normalize([1, 2, 3, 1, 1, 2]), normalize([3, 1, 1, 2, 2, 1]), normalize([1, 1, 2, 3, 1, 2])]
    for cap in (1, 2, 3):
        alloc, rounds = aziz_mackenzie_toy(Oracle(vals), max_rounds=cap)
        assert rounds <= cap + 1
        check_partition(alloc)
        check_envy_free(vals, alloc)


def test_only_three_agents() -> None:
    v = normalize([1])
    with pytest.raises(ValueError):
        aziz_mackenzie_toy(Oracle([v, v]))
    with pytest.raises(ValueError):
        aziz_mackenzie_toy(Oracle([v, v, v]), max_rounds=0)
