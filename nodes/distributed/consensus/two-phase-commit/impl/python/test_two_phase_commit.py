# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-phase-commit/. The authors are listed in prov/S2MVM5.jsonl.

import itertools
import random

from two_phase_commit import ABORT, COMMIT, UNCERTAIN, TwoPC

ALL_YES = {1: True, 2: True, 3: True}


def test_all_yes_commits() -> None:
    t = TwoPC(ALL_YES)
    t.start()
    t.deliver_all()
    assert all(t.decision[i] == COMMIT for i in range(4))
    assert t.log[0] == [COMMIT, "end"]
    assert all(t.log[p] == ["prepared", COMMIT] for p in (1, 2, 3))


def test_one_no_aborts() -> None:
    t = TwoPC({1: True, 2: False, 3: True})
    t.start()
    t.deliver_all()
    assert all(t.decision[i] == ABORT for i in range(4))


def blocked_run(naive: bool = False) -> TwoPC:
    """All vote yes. The coordinator forces COMMIT to its log and crashes before it sends it."""
    t = TwoPC(ALL_YES, naive_termination=naive)
    t.start()
    while t.inflight and 0 not in t.decision:
        t.deliver(0)
    assert t.log[0] == [COMMIT]
    t.crash(0)  # the COMMIT messages are lost with it
    for _ in range(10):
        for p in (1, 2, 3):
            t.timeout(p)
        t.deliver_all()
    return t


def test_coordinator_crash_blocks_the_participants() -> None:
    t = blocked_run()
    assert all(t.state(p) == UNCERTAIN for p in (1, 2, 3))  # blocked, holding their locks
    assert t.inflight == []  # nothing more can happen until the coordinator recovers
    t.recover(0)
    t.deliver_all()
    assert all(t.decision[p] == COMMIT for p in (1, 2, 3))


def test_giving_up_while_blocked_is_unsafe() -> None:
    t = blocked_run(naive=True)
    assert all(t.decision[p] == ABORT for p in (1, 2, 3))
    t.recover(0)  # the log says COMMIT
    t.deliver_all()
    assert t.decision[0] == COMMIT and t.check() == "agreement"


def test_commit_reaches_one_participant_that_crashes() -> None:
    """P1 commits and crashes, and the coordinator crashes. P2 and P3 cannot tell commit from abort."""
    for naive in (False, True):
        t = TwoPC(ALL_YES, naive_termination=naive)
        t.start()
        while 0 not in t.decision:
            t.deliver(0)
        k = next(k for k, m in enumerate(t.inflight) if m[1] == 1)
        t.deliver(k)  # COMMIT reaches P1 only
        assert t.decision[1] == COMMIT
        t.crash(1)
        t.crash(0)
        for _ in range(5):
            t.timeout(2)
            t.timeout(3)
            t.deliver_all()
        if naive:
            assert t.decision[2] == ABORT and t.check() == "agreement"
        else:
            assert t.state(2) == UNCERTAIN and t.state(3) == UNCERTAIN
            t.recover(1)
            t.timeout(2)
            t.timeout(3)
            t.deliver_all()  # P1's log has COMMIT, so P2 and P3 learn it from P1
            assert t.decision[2] == t.decision[3] == COMMIT and t.check() is None


def test_participant_that_did_not_vote_may_abort_alone() -> None:
    t = TwoPC(ALL_YES)
    t.timeout(2)  # P2 never got PREPARE
    t.start()
    t.deliver_all()
    assert all(t.decision[i] == ABORT for i in range(4))


def test_random_runs_are_safe_and_terminate() -> None:
    for seed in range(600):
        rng = random.Random(seed)
        n = rng.randrange(1, 5)
        votes = {p: rng.random() < 0.85 for p in range(1, n + 1)}
        t = TwoPC(votes, seed=seed)
        t.random_run(rng.randrange(5, 60), crash_p=rng.choice([0.0, 0.05, 0.15]))
        assert t.check() is None, seed
        assert len(t.decision) == n + 1, seed  # all recover, so all decide
        if COMMIT in t.decision.values():
            assert all(votes.values())


def test_no_failures_and_all_yes_means_commit() -> None:
    for n, seed in itertools.product(range(1, 5), range(20)):
        t = TwoPC({p: True for p in range(1, n + 1)}, seed=seed)
        t.start()
        while t.inflight:
            t.deliver(t.rng.randrange(len(t.inflight)))
        assert set(t.decision.values()) == {COMMIT}
