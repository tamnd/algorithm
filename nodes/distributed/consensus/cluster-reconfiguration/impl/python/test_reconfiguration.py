# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cluster-reconfiguration/. The authors are listed in prov/3KQHHP.jsonl.

import itertools

from reconfiguration import Model, always_meet, ongaro_scenario

U = range(1, 6)
SETS = [frozenset(c) for k in range(1, 6) for c in itertools.combinations(U, k)]


def test_direct_switch_can_have_disjoint_majorities() -> None:
    old, new = frozenset({1, 2, 3}), frozenset({1, 2, 3, 4, 5})
    assert not always_meet(old, new)       # {1, 2} and {3, 4, 5}
    assert not always_meet(frozenset({1, 2}), frozenset({3, 4, 5}))


def test_joint_quorums_meet_old_and_new() -> None:
    for old in SETS:
        for new in SETS:
            joint = (old, new)
            assert always_meet(joint, old) and always_meet(joint, new)
            assert always_meet(joint, joint)


def test_single_server_changes_keep_majorities_overlapping() -> None:
    for c in SETS:
        for x in U:
            d = c - {x} if x in c else c | {x}
            if d:
                assert always_meet(c, d), (c, d)


def test_joint_consensus_is_safe() -> None:
    for noop in (False, True):
        changes = 0
        for seed in range(500):
            m = Model(seed, "joint", noop).run(150)
            assert not m.violation, (noop, seed)
            changes += m.changes
        assert changes > 100


def test_single_server_changes_with_the_noop_rule_are_safe() -> None:
    changes = 0
    for seed in range(500):
        m = Model(seed, "single", True).run(150)
        assert not m.violation, seed
        changes += m.changes
    assert changes > 100


def test_direct_switch_is_unsafe() -> None:
    bad = sum(Model(seed, "direct", False).run(150).violation for seed in range(500))
    assert bad > 0


def test_ongaro_2015_bug_and_its_fix() -> None:
    out = ongaro_scenario(noop_rule=False)
    assert out["c_remove_committed"] and out["leader1_again"] and out["violation"]
    out = ongaro_scenario(noop_rule=True)
    assert out["c_remove_committed"]
    assert not out["leader1_again"] and not out["violation"]
