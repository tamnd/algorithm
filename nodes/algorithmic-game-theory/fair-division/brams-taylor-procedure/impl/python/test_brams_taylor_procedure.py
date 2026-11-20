# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brams-taylor-procedure/. The authors are listed in prov/MN3VTM.jsonl.
# Tests of a toy for three agents. They do not test the protocol of Brams and Taylor for n agents.

import random
from fractions import Fraction

import pytest

from agtcake import Oracle, normalize, piece_value, random_valuation
from brams_taylor_procedure import (
    advantage,
    brams_taylor_toy,
    has_advantage,
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


def test_page_example_advantage() -> None:
    # Alice values C at 1/3, the piece A' of Charlie at 1/4 and the leftover Y at 1/12.
    assert has_advantage(F(1, 3), F(1, 4), F(1, 12))
    # She values the piece B of Bob at 1/3, so she has no advantage over Bob.
    assert not has_advantage(F(1, 3), F(1, 3), F(1, 12))


def test_round_gives_cutter_an_advantage() -> None:
    rng = random.Random(5)
    for _ in range(100):
        vals = [random_valuation(rng, 6, 5) for _ in range(3)]
        o = Oracle(vals)
        rest = [(F(0), F(1))]
        give, new_rest, taker = trimming_round(o, rest, 0, 1, 2)
        alloc = {i: list(give[i]) for i in range(3)}
        # the round is envy-free on the pieces it gives out
        for i in range(3):
            for j in range(3):
                assert piece_eval(o, i, alloc[i]) >= piece_eval(o, i, alloc[j])
        assert advantage(o, 0, taker, alloc, new_rest)
        gain = piece_eval(o, 0, alloc[0]) - piece_eval(o, 0, alloc[taker])
        assert gain == piece_eval(o, 0, new_rest)


def test_identical_valuations_end_after_one_round() -> None:
    rng = random.Random(3)
    for _ in range(20):
        v = random_valuation(rng, rng.randint(1, 8), 5)
        o = Oracle([v, v, v])
        alloc, rounds = brams_taylor_toy(o)
        assert rounds == 1
        check_partition(alloc)
        assert all(piece_value(v, alloc[i]) == F(1, 3) for i in range(3))


def test_random_valuations() -> None:
    rng = random.Random(2024)
    for _ in range(60):
        vals = [random_valuation(rng, rng.randint(1, 6), 5) for _ in range(3)]
        o = Oracle(vals)
        alloc, rounds = brams_taylor_toy(o, max_rounds=12)
        check_partition(alloc)
        check_envy_free(vals, alloc)
        assert 1 <= rounds <= 12


def test_round_cap_uses_the_fallback() -> None:
    vals = [normalize([1, 2, 3, 1, 1, 2]), normalize([3, 1, 1, 2, 2, 1]), normalize([1, 1, 2, 3, 1, 2])]
    for cap in (1, 2, 3):
        o = Oracle(vals)
        alloc, rounds = brams_taylor_toy(o, max_rounds=cap)
        assert rounds <= cap
        check_partition(alloc)
        check_envy_free(vals, alloc)


def test_only_three_agents() -> None:
    v = normalize([1])
    with pytest.raises(ValueError):
        brams_taylor_toy(Oracle([v, v]))
    with pytest.raises(ValueError):
        brams_taylor_toy(Oracle([v, v, v]), max_rounds=0)
