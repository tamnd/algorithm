# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dubins-spanier-moving-knife/. The authors are listed in prov/RTDGDA.jsonl.

import random
from fractions import Fraction

from agtcake import Oracle, normalize, piece_value, random_valuation, value
from dubins_spanier_moving_knife import dubins_spanier

F = Fraction


def check_partition(alloc, n) -> None:
    assert sorted(alloc) == list(range(n))
    assert all(len(alloc[i]) == 1 for i in range(n))
    ivs = sorted(alloc[i][0] for i in range(n))
    assert ivs[0][0] == 0 and ivs[-1][1] == 1
    for (a1, b1), (a2, b2) in zip(ivs, ivs[1:]):
        assert a1 <= b1 == a2 <= b2


def check_knife(vals, alloc) -> None:
    """Replay the knife with the true valuations, independent of the oracle.

    In each round the knife stops at x. Every waiting agent values [a, y] at
    less than 1/n for each y < x (here: at the midpoint of a and x, and just
    left of x), and the receiver values [a, x] at exactly 1/n.
    """
    n = len(vals)
    share = F(1, n)
    owner = {alloc[i][0]: i for i in range(n)}
    waiting = set(range(n))
    for a, x in sorted(owner)[:-1]:
        h = owner[(a, x)]
        assert value(vals[h], a, x) == share
        for j in waiting:
            assert value(vals[j], a, x) <= share
            if x > a:
                for y in (a + (x - a) / 2, x - (x - a) / 10**6):
                    assert value(vals[j], a, y) < share
            # ties go to the smallest index
            if value(vals[j], a, x) == share and x > a:
                assert h <= j
        waiting.remove(h)


def test_example() -> None:
    vals = [normalize(d) for d in ([1, 1, 1, 1], [0, 1, 1, 2], [2, 2, 0, 0], [1, 0, 0, 3])]
    o = Oracle(vals)
    alloc = dubins_spanier(o)
    assert alloc == {
        2: [(0, F(1, 8))],
        0: [(F(1, 8), F(3, 8))],
        1: [(F(3, 8), F(5, 8))],
        3: [(F(5, 8), 1)],
    }
    assert [piece_value(vals[i], alloc[i]) for i in range(4)] == [F(1, 4), F(1, 4), F(1, 4), F(3, 4)]
    assert piece_value(vals[1], alloc[3]) == F(5, 8)  # agent 2 envies agent 4
    assert o.cuts == [2, 3, 1, 3] and o.total_evals() == 0
    assert o.total() == 4 * 5 // 2 - 1
    check_knife(vals, alloc)


def test_random_valuations() -> None:
    rng = random.Random(99)
    for _ in range(150):
        n = rng.randint(1, 5)
        vals = [random_valuation(rng, rng.randint(1, 8), 6) for _ in range(n)]
        o = Oracle(vals)
        alloc = dubins_spanier(o)
        check_partition(alloc, n)
        check_knife(vals, alloc)
        for i in range(n):
            assert piece_value(vals[i], alloc[i]) >= F(1, n)
        assert o.total_evals() == 0
        assert o.total_cuts() == n * (n + 1) // 2 - 1


def test_identical_valuations() -> None:
    rng = random.Random(8)
    for n in range(1, 6):
        v = random_valuation(rng, 7, 3)
        alloc = dubins_spanier(Oracle([v] * n))
        check_partition(alloc, n)
        for i in range(n):
            assert piece_value(v, alloc[i]) == F(1, n)
        # all marks tie in each round, so agent 0 stops first, then agent 1, ...
        starts = [alloc[i][0][0] for i in range(n)]
        assert starts == sorted(starts)
