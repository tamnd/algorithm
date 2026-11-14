# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-axis-printing-decomposition/. The authors are listed in prov/N5ERYT.jsonl.

import random

from multi_axis_printing_decomposition import (
    DIRECTIONS,
    beam_decompose,
    cuts,
    dot,
    exhaustive_min_parts,
    gallows,
    is_base,
    simulate,
    support_block,
    tee,
    unsupported,
)


def random_model(rng, p):
    return frozenset((x, y, z) for x in range(5) for y in range(2) for z in range(5) if rng.random() < p)


def test_support_block_is_the_layer_below() -> None:
    for d in DIRECTIONS.values():
        v = (3, -2, 5)
        block = support_block(v, d)
        assert len(set(block)) == 9
        assert all(dot(w, d) == dot(v, d) - 1 for w in block)
        assert all(max(abs(w[i] - v[i]) for i in range(3)) == 1 for w in block)


def test_tee_needs_three_parts() -> None:
    m = tee()
    assert len(m) == 56
    assert len(unsupported(m, (0, 0, 1))) == 12  # the arm undersides beyond the 45 degree rule
    plan = beam_decompose(m)
    assert [(d, len(p)) for d, p in plan] == [("+z", 32), ("-x", 12), ("+x", 12)]
    assert simulate(m, plan) == (True, "ok")
    assert exhaustive_min_parts(m) == 3


def test_gallows_needs_two_parts() -> None:
    m = gallows()
    plan = beam_decompose(m)
    assert [(d, len(p)) for d, p in plan] == [("+z", 28), ("+x", 20)]
    assert simulate(m, plan) == (True, "ok")
    assert exhaustive_min_parts(m) == 2


def test_every_cut_is_support_free_by_direct_test() -> None:
    rng = random.Random(11)
    for _ in range(80):
        m = random_model(rng, 0.6)
        for name, d in DIRECTIONS.items():
            for _, c, part, rest in cuts(m, name):
                assert part | rest == m and not (part & rest)
                assert all(dot(v, d) >= c for v in part) and all(dot(v, d) < c for v in rest)
                # direct overhang test: print rest, then part layer by layer
                assert simulate(m, [("+z", rest), (name, part)])[1] != "parts overlap"
                solid = set(rest)
                for v in sorted(part, key=lambda v: dot(v, d)):
                    assert any(w in solid for w in support_block(v, d))
                    solid.add(v)


def test_beam_plans_pass_the_print_simulation() -> None:
    rng = random.Random(7)
    found = 0
    for _ in range(200):
        m = random_model(rng, 0.5)
        if not m:
            continue
        best = exhaustive_min_parts(m, 4)
        plan = beam_decompose(m, width=4, max_cuts=3)
        if plan is None:
            assert best is None
            continue
        found += 1
        ok, msg = simulate(m, plan)
        assert ok, msg
        assert best is not None and len(plan) >= best
        assert len(plan) == best  # width 4 is enough on this test set
    assert found > 150


def test_simulation_rejects_bad_plans() -> None:
    m = tee()
    assert not simulate(m, [("+z", m)])[0]  # overhangs
    plan = beam_decompose(m)
    assert not simulate(m, list(reversed(plan)))[0]  # wrong order
    base, left, right = plan
    assert not simulate(m, [base, left])[0]  # does not cover the model


def test_a_hanging_voxel_has_no_plan() -> None:
    # a rod of two voxels hangs under the end of an arm. The lower voxel has
    # only one neighbor, directly above it, and -z is not allowed.
    m = frozenset({(0, 0, z) for z in range(4)} | {(x, 0, 3) for x in range(1, 4)} | {(3, 0, 2), (3, 0, 1)})
    assert not is_base(m)
    assert beam_decompose(m, width=8, max_cuts=4) is None
    assert exhaustive_min_parts(m, 5) is None
