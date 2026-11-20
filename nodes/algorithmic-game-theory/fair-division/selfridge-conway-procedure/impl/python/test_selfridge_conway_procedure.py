# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/selfridge-conway-procedure/. The authors are listed in prov/9GXB9K.jsonl.

import random
from fractions import Fraction

from agtcake import Oracle, normalize, piece_value, random_valuation
from selfridge_conway_procedure import selfridge_conway

F = Fraction


def check_partition(alloc) -> None:
    """The pieces are disjoint, cover [0, 1], and each has at most two intervals."""
    assert sorted(alloc) == [0, 1, 2]
    assert all(1 <= len(alloc[i]) <= 2 for i in range(3))
    ivs = sorted(iv for i in range(3) for iv in alloc[i])
    assert ivs[0][0] == 0 and ivs[-1][1] == 1
    for (a1, b1), (a2, b2) in zip(ivs, ivs[1:]):
        assert a1 <= b1 == a2 <= b2
    assert ivs[-1][0] <= ivs[-1][1]


def check_envy_free(vals, alloc) -> None:
    for i in range(3):
        own = piece_value(vals[i], alloc[i])
        for j in range(3):
            assert own >= piece_value(vals[i], alloc[j])


def run(vals):
    o = Oracle(vals)
    alloc = selfridge_conway(o)
    check_partition(alloc)
    check_envy_free(vals, alloc)
    assert o.total_cuts() <= 5
    assert o.total_evals() <= 12
    return o, alloc


def test_page_example() -> None:
    vals = [normalize([1] * 6), normalize([3, 1, 1, 1, 2, 4]), normalize([1, 2, 3, 3, 2, 1])]
    o, alloc = run(vals)
    assert alloc[0] == [(F(0), F(1, 3)), (F(17, 18), F(35, 36))]
    assert alloc[1] == [(F(2, 3), F(11, 12)), (F(11, 12), F(17, 18))]
    assert alloc[2] == [(F(1, 3), F(2, 3)), (F(35, 36), F(1))]
    table = [[piece_value(vals[i], alloc[j]) for j in range(3)] for i in range(3)]
    assert table == [
        [F(13, 36), F(5, 18), F(13, 36)],
        [F(7, 18), F(7, 18), F(2, 9)],
        [F(19, 72), F(2, 9), F(37, 72)],
    ]
    assert o.cuts == [2, 1, 2] and o.evals == [2, 6, 4]


def test_third_agent_takes_trimmed_piece() -> None:
    vals = [normalize([1] * 6), normalize([1, 1, 2, 2, 3, 3]), normalize([1, 1, 1, 2, 4, 3])]
    o, alloc = run(vals)
    # [2/3, 1] is trimmed to [2/3, 8/9]; the first chooser (agent 2 of the code)
    # takes it, so agent 1 of the code takes its second best piece [1/3, 2/3].
    assert alloc[2][0] == (F(2, 3), F(8, 9))
    assert alloc[1][0] == (F(1, 3), F(2, 3))
    assert alloc[0][0] == (F(0), F(1, 3))
    assert o.total_cuts() == 5 and o.cuts == [2, 3, 0]


def test_identical_valuations_need_no_trim() -> None:
    rng = random.Random(7)
    for _ in range(30):
        v = random_valuation(rng, rng.randint(1, 8), 5)
        o, alloc = run([v, v, v])
        assert o.total_cuts() == 2
        assert all(piece_value(v, alloc[i]) == F(1, 3) for i in range(3))


def test_random_valuations() -> None:
    rng = random.Random(2024)
    for _ in range(300):
        k = rng.randint(1, 8)
        vals = [random_valuation(rng, k, 6) for _ in range(3)]
        o, alloc = run(vals)
        # the cutter gets at least a third, as one of its own equal pieces
        assert piece_value(vals[0], alloc[0]) >= F(1, 3)


def test_trim_matches_second_best() -> None:
    rng = random.Random(11)
    for _ in range(200):
        vals = [random_valuation(rng, 8, 4) for _ in range(3)]
        o, alloc = run(vals)
        if o.total_cuts() == 5:
            # the agent with the trimmed piece holds it as its first interval,
            # and agent 1 of the code values it as its second best of the three.
            first = [alloc[i][0] for i in range(3)]
            v1 = sorted((piece_value(vals[1], [iv]) for iv in first), reverse=True)
            assert v1[0] == v1[1]
