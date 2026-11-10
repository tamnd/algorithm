# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cheap-paxos/. The authors are listed in prov/DJBX02.jsonl.

from itertools import combinations

from cheap_paxos import CheapPaxos, Config, initial_config


def quorums(c: Config) -> list[frozenset]:
    g = sorted(c.members)
    return [frozenset(s) for k in range(len(g) + 1) for s in combinations(g, k)
            if c.is_quorum(frozenset(s))]


def test_quorums_intersect_in_every_reachable_config() -> None:
    for f in range(1, 4):
        c = initial_config(f)
        assert c.is_quorum(c.mains) and len(c.mains) == f + 1 and len(c.aux) == f
        for victim in sorted(c.mains)[:-1]:
            qs = quorums(c)
            assert all(a & b for a in qs for b in qs), (f, c)
            c = c.apply(("remove", victim))
        qs = quorums(c)
        assert all(a & b for a in qs for b in qs), (f, c)


def test_quorum_of_mains_meets_every_majority() -> None:
    # f + 1 mains out of 2f + 1 meet each majority, so a majority with no main
    # cannot exist.
    for f in range(1, 5):
        c = initial_config(f)
        for s in combinations(sorted(c.members), f + 1):
            assert set(s) & c.mains


def test_no_failure_keeps_auxiliaries_idle() -> None:
    for seed in range(30):
        sim = CheapPaxos(2, seed, dup=0.1).run()
        assert sim.done() and sim.consistent()
        assert sim.aux_messages == 0


def test_main_failure_uses_auxiliaries_then_reconfigures() -> None:
    for seed in range(30):
        sim = CheapPaxos(1, seed, n_commands=8)
        sim.crashed.add(1)  # one of the two mains is down from the start
        sim.run()
        log = sim.chosen_log()
        assert sim.done() and sim.consistent()
        assert ("remove", 1) in log
        assert sim.aux_messages > 0
        # After the change the auxiliary has forgotten the old slots.
        k = log.index(("remove", 1)) + 1
        assert sim.procs[2].forgot_below == k and not any(s < k for s in sim.procs[2].accepted)


def test_auxiliaries_rest_after_reconfiguration() -> None:
    sim = CheapPaxos(2, seed=3, n_commands=12)
    sim.crashed.add(2)
    sim.run()
    log = sim.chosen_log()
    k = log.index(("remove", 2)) + 1
    assert sim.procs[0].config(k).mains == frozenset({0, 1})
    assert not any(s >= k for s in sim.procs[3].accepted)  # no aux vote after the change
    assert not any(s >= k for s in sim.procs[4].accepted)


def test_safety_with_crashes_and_dueling_leaders() -> None:
    for seed in range(150):
        sim = CheapPaxos(2, seed, dup=0.1, crashes=2, crash_prob=0.005, duel_prob=0.01).run()
        assert sim.consistent(), seed  # chosen_log raises if a slot has two values
        assert sim.done(), seed
    for seed in range(100):
        sim = CheapPaxos(1, seed, dup=0.2, drop=0.05, crashes=1, crash_prob=0.005,
                         duel_prob=0.02, max_steps=3000).run()
        assert sim.consistent(), seed
