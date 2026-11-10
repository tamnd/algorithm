# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/three-phase-commit/. The authors are listed in prov/DSVH0K.jsonl.

import itertools
import random

from three_phase_commit import A, C, P, W, ThreePC

YES3 = {1: True, 2: True, 3: True}


def test_no_failures() -> None:
    t = ThreePC(YES3)
    t.run(10)
    assert [s[0] for s in t.trace[:5]] == [W, W, P, P, C]
    assert set(t.state.values()) == {C}
    t = ThreePC({1: True, 2: False, 3: True})
    t.run(10)
    assert set(t.state.values()) == {A}


def test_precommit_reaches_one_participant_then_both_crash() -> None:
    # round 2: the coordinator sends PRE-COMMIT to P1 only and crashes; round 3: P1 moves to p and crashes
    t = ThreePC(YES3, crashes={0: (2, 1), 1: (3, 0)})
    t.run(20)
    assert t.state[1] == P and t.state[2] == t.state[3] == A  # no survivor is in p, so abort
    assert t.safe()


def test_commit_reaches_one_participant_then_both_crash() -> None:
    # round 4: the coordinator sends COMMIT to P1 only and crashes; round 5: P1 commits and crashes
    t = ThreePC(YES3, crashes={0: (4, 1), 1: (5, 0)})
    t.run(20)
    assert t.state[1] == C and t.state[2] == t.state[3] == C  # the survivors are in p, so commit
    assert t.safe()


def test_new_leader_crashes_during_termination() -> None:
    t = ThreePC({1: True, 2: True, 3: True, 4: True}, crashes={0: (2, 1), 1: (4, 2)})
    t.run(30)
    assert t.safe() and t.live_undecided() == []


def check_all(votes: dict[int, bool], plan: dict[int, tuple[int, int]]) -> None:
    t = ThreePC(votes, crashes=plan)
    t.run(25)
    assert t.safe(), (votes, plan, t.state)
    assert t.live_undecided() == [], (votes, plan, t.state)  # non-blocking


def test_all_patterns_of_one_and_two_crashes() -> None:
    options = [(r, k) for r in range(8) for k in range(4)]
    for votes in ({1: True, 2: True, 3: True}, {1: True, 2: True, 3: False}):
        for who in range(4):
            for o in options:
                check_all(votes, {who: o})
        for a, b in itertools.combinations(range(4), 2):
            for oa, ob in itertools.product(options, repeat=2):
                check_all(votes, {a: oa, b: ob})


def test_random_crashes_with_more_processes() -> None:
    for seed in range(1500):
        rng = random.Random(seed)
        n = rng.randrange(1, 6)
        votes = {p: rng.random() < 0.8 for p in range(1, n + 1)}
        who = rng.sample(range(n + 1), rng.randrange(n + 1))  # at least one process stays up
        check_all(votes, {i: (rng.randrange(12), rng.randrange(n + 1)) for i in who})


def test_partition_breaks_safety() -> None:
    # round 2: the coordinator sends PRE-COMMIT, but a partition {C, P1} | {P2, P3} starts in that round
    t = ThreePC(YES3, partition=(2, [{0, 1}, {2, 3}]))
    t.run(12)
    assert t.state == {0: C, 1: C, 2: A, 3: A}
    assert not t.safe()


def test_random_partitions_sometimes_break_safety() -> None:
    bad = 0
    for seed in range(300):
        rng = random.Random(seed)
        procs = list(range(4))
        rng.shuffle(procs)
        cut = rng.randrange(1, 4)
        t = ThreePC(YES3, partition=(rng.randrange(6), [set(procs[:cut]), set(procs[cut:])]))
        t.run(20)
        bad += not t.safe()
    assert bad > 0
