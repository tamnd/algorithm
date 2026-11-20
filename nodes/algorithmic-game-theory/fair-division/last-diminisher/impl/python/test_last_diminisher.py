# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/last-diminisher/. The authors are listed in prov/VJGVJA.jsonl.

import random
from fractions import Fraction

from agtcake import Oracle, normalize, piece_value, random_valuation, value
from last_diminisher import last_diminisher

F = Fraction


def check_partition(alloc, n) -> list:
    """The pieces are single intervals that tile [0, 1] from left to right."""
    assert sorted(alloc) == list(range(n))
    ivs = sorted(alloc[i][0] for i in range(n))
    assert all(len(alloc[i]) == 1 for i in range(n))
    assert ivs[0][0] == 0 and ivs[-1][1] == 1
    for (a1, b1), (a2, b2) in zip(ivs, ivs[1:]):
        assert a1 <= b1 == a2 <= b2
    return ivs


def check_rounds(vals, alloc) -> None:
    """Replay the rounds with the true valuations.

    In each round, the receiver values its piece at exactly 1/n, and every
    agent that is still waiting values that piece at most 1/n.
    """
    n = len(vals)
    share = F(1, n)
    owner = {alloc[i][0]: i for i in range(n)}
    waiting = set(range(n))
    for iv in sorted(owner)[:-1]:
        i = owner[iv]
        assert piece_value(vals[i], [iv]) == share
        for j in waiting - {i}:
            assert piece_value(vals[j], [iv]) <= share
        waiting.remove(i)


def test_example() -> None:
    vals = [normalize([1, 1, 1, 1]), normalize([2, 1, 1, 0]), normalize([3, 1, 0, 0])]
    o = Oracle(vals)
    alloc = last_diminisher(o)
    assert alloc == {2: [(0, F(1, 9))], 1: [(F(1, 9), F(11, 36))], 0: [(F(11, 36), 1)]}
    assert [piece_value(vals[i], alloc[i]) for i in range(3)] == [F(25, 36), F(1, 3), F(1, 3)]
    # agent 3 envies agent 2: proportional, not envy-free
    assert piece_value(vals[2], alloc[1]) == F(17, 36)
    assert o.evals == [0, 2, 1] and o.cuts == [2, 2, 1]
    assert o.total() == 3 * 3 - 1  # every agent trims in every round


def test_identical_valuations() -> None:
    rng = random.Random(3)
    for n in range(1, 6):
        v = random_valuation(rng, 6, 5)
        o = Oracle([v] * n)
        alloc = last_diminisher(o)
        check_partition(alloc, n)
        for i in range(n):
            assert piece_value(v, alloc[i]) == F(1, n)
        assert o.total_cuts() == n - 1  # nobody trims
        assert o.total_evals() == n * (n - 1) // 2


def test_random_valuations() -> None:
    rng = random.Random(2024)
    for _ in range(150):
        n = rng.randint(1, 5)
        vals = [random_valuation(rng, rng.randint(1, 8), 6) for _ in range(n)]
        o = Oracle(vals)
        alloc = last_diminisher(o)
        check_partition(alloc, n)
        check_rounds(vals, alloc)
        for i in range(n):
            assert piece_value(vals[i], alloc[i]) >= F(1, n)
        assert o.total_evals() == n * (n - 1) // 2
        assert n - 1 <= o.total_cuts() <= n * (n + 1) // 2 - 1
        assert o.total() <= n * n - 1 if n > 1 else o.total() == 0


def test_worst_case_reaches_bound() -> None:
    # agent i puts more weight to the left than every agent before it
    for n in range(2, 6):
        vals = [normalize([2 ** (i * (n - j)) for j in range(n)]) for i in range(n)]
        o = Oracle(vals)
        alloc = last_diminisher(o)
        check_partition(alloc, n)
        for i in range(n):
            assert piece_value(vals[i], alloc[i]) >= F(1, n)
        assert o.total() == n * n - 1


def test_two_agents_is_cut_and_trim() -> None:
    rng = random.Random(5)
    for _ in range(50):
        vals = [random_valuation(rng, 5, 4) for _ in range(2)]
        alloc = last_diminisher(Oracle(vals))
        left = min(alloc, key=lambda i: alloc[i][0][0])
        x = alloc[left][0][1]
        assert value(vals[left], 0, x) == F(1, 2)
        assert value(vals[1 - left], 0, x) <= F(1, 2)
