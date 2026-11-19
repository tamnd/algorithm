# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unit-selection-synthesis/. The authors are listed in prov/V4WYB0.jsonl.

import itertools
import random

import pytest

from unit_selection_synthesis import (
    Target,
    Unit,
    candidates,
    join_cost,
    select_units,
    target_cost,
    total_cost,
)

PHONES = ["a", "b", "c"]


def random_database(rng, n_utts, length):
    units = []
    for utt in range(n_utts):
        phones = [rng.choice(PHONES) for _ in range(length)]
        for i, p in enumerate(phones):
            units.append(Unit(
                utt=utt, idx=i, phone=p,
                f0=float(rng.randint(90, 130)), dur=float(rng.randint(50, 90)),
                left=phones[i - 1] if i > 0 else "#",
                right=phones[i + 1] if i + 1 < length else "#",
                start=(float(rng.randint(0, 4)), float(rng.randint(0, 4))),
                end=(float(rng.randint(0, 4)), float(rng.randint(0, 4))),
            ))
    return units


def random_targets(rng, n, units):
    present = sorted({u.phone for u in units})
    phones = [rng.choice(present) for _ in range(n)]
    return [Target(p, float(rng.randint(90, 130)), float(rng.randint(50, 90)),
                   phones[i - 1] if i > 0 else "#", phones[i + 1] if i + 1 < n else "#")
            for i, p in enumerate(phones)]


def brute_force(targets, units, w=None):
    """All candidate sequences; the best by (cost, reversed index tuple)."""
    U = candidates(targets, units)
    best = None
    for idx in itertools.product(*[range(len(layer)) for layer in U]):
        seq = [U[i][k] for i, k in enumerate(idx)]
        c = total_cost(targets, seq) if w is None else total_cost(targets, seq, w)
        key = (c, tuple(reversed(idx)))
        if best is None or key < best[0]:
            best = (key, seq)
    return best[1], best[0][0]


def test_matches_brute_force_with_ties():
    rng = random.Random(1)
    for _ in range(40):
        units = random_database(rng, rng.randint(1, 3), rng.randint(2, 5))
        targets = random_targets(rng, rng.randint(1, 5), units)
        seq, cost = select_units(targets, units)
        bseq, bcost = brute_force(targets, units)
        assert cost == bcost
        assert seq == bseq
        assert total_cost(targets, seq) == cost


def test_wide_beam_equals_exact():
    rng = random.Random(2)
    for _ in range(30):
        units = random_database(rng, 3, 5)
        targets = random_targets(rng, rng.randint(1, 5), units)
        exact = select_units(targets, units)
        assert select_units(targets, units, beam=len(units)) == exact


def test_narrow_beam_can_fail():
    # Unit 0 of "a" fits its target exactly (cost 0) and unit 1 of "a" has
    # target cost 1, but unit 1 is followed by a matching "b" in the same
    # recording, so its join is free.
    units = [
        Unit(0, 0, "a", 100.0, 60.0, "#", "b", (0.0,), (0.0,)),
        Unit(1, 0, "a", 101.0, 60.0, "#", "b", (0.0,), (5.0,)),
        Unit(1, 1, "b", 120.0, 70.0, "a", "#", (5.0,), (0.0,)),
    ]
    targets = [Target("a", 100.0, 60.0, "#", "b"), Target("b", 120.0, 70.0, "a", "#")]
    exact_seq, exact = select_units(targets, units)
    assert exact == 1.0
    assert [(u.utt, u.idx) for u in exact_seq] == [(1, 0), (1, 1)]
    narrow_seq, narrow = select_units(targets, units, beam=1)
    assert [(u.utt, u.idx) for u in narrow_seq] == [(0, 0), (1, 1)]
    assert narrow == 0.0 + 25.0 + 20.0
    assert narrow > exact


def test_contiguous_stretch_is_preferred():
    # The database holds the whole target word in one recording and also
    # scattered copies with slightly better target costs but costly joins.
    word = ["c", "a", "b"]
    units = [Unit(0, i, p, 100.0, 60.0, "", "", (9.0,), (0.0,)) for i, p in enumerate(word)]
    units += [Unit(1 + i, 0, p, 100.0, 60.0, "", "", (3.0,), (3.0,)) for i, p in enumerate(word)]
    targets = [Target(p, 100.0, 60.0, "", "") for p in word]
    seq, cost = select_units(targets, units)
    assert [(u.utt, u.idx) for u in seq] == [(0, 0), (0, 1), (0, 2)]
    assert cost == 0.0


def test_weights_change_the_choice():
    units = [
        Unit(0, 0, "a", 100.0, 80.0),
        Unit(1, 0, "a", 130.0, 60.0),
    ]
    t = [Target("a", 100.0, 60.0)]
    w_f0 = {"f0": 1.0, "dur": 0.1, "ctx": 1.0, "spec": 1.0, "jf0": 1.0}
    w_dur = {"f0": 0.1, "dur": 1.0, "ctx": 1.0, "spec": 1.0, "jf0": 1.0}
    assert select_units(t, units, w_f0)[0][0].utt == 0
    assert select_units(t, units, w_dur)[0][0].utt == 1


def test_costs():
    u = Unit(0, 3, "a", 100.0, 60.0, "b", "c", (1.0, 2.0), (3.0, 4.0))
    v = Unit(0, 4, "d", 110.0, 50.0, "a", "e", (0.0, 0.0), (0.0, 0.0))
    x = Unit(2, 0, "d", 110.0, 50.0, "a", "e", (0.0, 0.0), (0.0, 0.0))
    assert target_cost(Target("a", 90.0, 70.0, "b", "x"), u) == 10.0 + 10.0 + 1.0
    assert target_cost(Target("z", 100.0, 60.0), u) == float("inf")
    assert join_cost(u, v) == 0.0
    assert join_cost(u, x) == 9.0 + 16.0 + 10.0


def test_errors_and_empty():
    units = [Unit(0, 0, "a", 100.0, 60.0)]
    assert select_units([], units) == ([], 0.0)
    with pytest.raises(ValueError):
        select_units([Target("b", 100.0, 60.0)], units)
    with pytest.raises(ValueError):
        select_units([Target("a", 100.0, 60.0)], units, beam=0)
