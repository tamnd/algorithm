# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/paxos-commit/. The authors are listed in prov/KZW5JY.jsonl.

from paxos_commit import PaxosCommit


def test_normal_case_message_count() -> None:
    for n in range(1, 7):
        for f in range(0, 4):
            sim = PaxosCommit(n, f, seed=n * 10 + f, crash_prob=0.0).run()
            assert sim.result() == "Committed"
            assert sum(sim.count.values()) == (n + 1) * (f + 3) - 2, (n, f)
            assert sim.recoveries == 0


def test_f_zero_is_two_phase_commit() -> None:
    # With F = 0 the single acceptor sits on the leader's node, so its 2b
    # message is local, and the first RM's BeginCommit travels with its 2a
    # message. What is left is the message pattern of Two-Phase Commit.
    for n in range(1, 8):
        sim = PaxosCommit(n, 0, seed=n, crash_prob=0.0).run()
        c = sim.count
        assert c["2b"] == 1 and c["BeginCommit"] == 1
        assert sum(c.values()) - c["2b"] - c["BeginCommit"] == 3 * n - 1


def test_one_abort_vote_aborts() -> None:
    for seed in range(40):
        sim = PaxosCommit(4, 1, seed, abort_prob=0.3, crash_prob=0.0).run()
        want = "Committed" if all(v == "Prepared" for v in sim.vote.values()) else "Aborted"
        assert sim.result() == want, seed


def test_safety_with_crashes_competing_leaders_and_early_timeouts() -> None:
    for n, f in ((3, 1), (4, 2)):
        for seed in range(80):
            sim = PaxosCommit(n, f, seed, abort_prob=0.1, n_leaders=3, dup=0.1,
                              leader_crash_prob=0.3, acc_crashes=f, rm_crash_prob=0.2,
                              crash_prob=0.01, timeout_prob=0.01).run()
            assert sim.consistent() and sim.valid(), (n, f, seed)
            assert sim.finished(), (n, f, seed)


def test_not_blocking_when_the_leader_and_f_acceptors_crash() -> None:
    for seed in range(40):
        sim = PaxosCommit(3, 1, seed, n_leaders=2, acc_crashes=1,
                          leader_crash_prob=0.5, crash_prob=0.05).run()
        assert sim.finished() and sim.consistent() and sim.valid(), seed


def test_f_zero_blocks_when_the_acceptor_crashes() -> None:
    blocked = 0
    for seed in range(40):
        sim = PaxosCommit(3, 0, seed, n_leaders=2, acc_crashes=1, crash_prob=0.05).run()
        assert sim.consistent() and sim.valid()
        blocked += not sim.finished()
    assert blocked > 0


def test_recovery_without_phase_1_is_unsafe() -> None:
    bad = sum(not PaxosCommit(3, 1, seed, n_leaders=2, timeout_prob=0.02,
                              unsafe_recovery=True).run().consistent()
              for seed in range(60))
    assert bad > 0
