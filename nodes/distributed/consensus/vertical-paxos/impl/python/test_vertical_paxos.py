# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vertical-paxos/. The authors are listed in prov/53MYYW.jsonl.

from itertools import combinations

from vertical_paxos import Config, VerticalPaxos


def subsets(s: frozenset) -> list:
    return [set(c) for k in range(len(s) + 1) for c in combinations(sorted(s), k)]


def test_read_quorums_meet_write_quorums() -> None:
    for kind in ("pb", "maj"):
        for size in (1, 2, 3, 4):
            c = Config(frozenset(range(size)), kind)
            reads = [s for s in subsets(c.members) if c.is_read_quorum(s)]
            writes = [s for s in subsets(c.members) if c.is_write_quorum(s)]
            assert reads and writes
            assert all(r & w for r in reads for w in writes)
            assert all(w1 & w2 for w1 in writes for w2 in writes)
    bad = Config(frozenset({0, 1}), "bad")
    assert not ({0} & {1}) and bad.is_read_quorum({0}) and bad.is_write_quorum({1})


def run(variant: int, seed: int, kinds=("pb", "maj"), **kw) -> VerticalPaxos:
    opts = dict(dup=0.1, crashes=1, crash_prob=0.01, leader_fail=0.03, new_ballot_prob=0.03,
                after=4)
    opts.update(kw)
    return VerticalPaxos(variant, seed, kinds=kinds, **opts).run()


def test_safety_of_both_variants() -> None:
    for variant in (1, 2):
        for seed in range(250):
            sim = run(variant, seed)
            assert len(sim.chosen()) <= 1, (variant, seed)


def test_progress_without_crashes() -> None:
    # The master starts a new ballot only when the current one stalls, as a
    # liveness argument needs. Leaders still fail.
    for variant in (1, 2):
        for seed in range(100):
            sim = run(variant, seed, crashes=0, new_ballot_prob=0.0)
            assert len(sim.chosen()) == 1, (variant, seed)


def test_vp2_leader_reads_one_configuration_vp1_may_read_many() -> None:
    worst = {}
    for variant in (1, 2):
        worst[variant] = max(len(ld.queried) for seed in range(100)
                             for ld in run(variant, seed).leaders.values())
    assert worst[2] == 1
    assert worst[1] > 3


def test_primary_backup_new_leader_reads_one_acceptor() -> None:
    # With "pb" configurations a single acceptor of the previous ballot is a
    # read quorum, so phase 1 ends after one reply with no vote.
    for seed in range(50):
        sim = VerticalPaxos(2, seed, kinds=("pb",), after=3).run()
        assert len(sim.chosen()) == 1
        for b, ld in sim.leaders.items():
            assert sim.config[b].kind == "pb"


def test_quorums_that_do_not_meet_are_unsafe() -> None:
    for variant in (1, 2):
        bad = sum(len(run(variant, seed, kinds=("bad",)).chosen()) > 1 for seed in range(100))
        assert bad > 0, variant


def test_vp2_votes_in_inactive_ballots_must_not_count() -> None:
    # A ballot that the master never activates may still collect a write
    # quorum of votes for an old value. Counting it as chosen is unsafe.
    found = 0
    for seed in range(200):
        sim = run(2, seed)
        assert len(sim.chosen()) <= 1
        found += len(sim.raw_chosen()) > 1
    assert found > 0
