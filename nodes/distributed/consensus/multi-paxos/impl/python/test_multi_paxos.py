# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-paxos/. The authors are listed in prov/5TRQGX.jsonl.

from multi_paxos import NOOP, MultiPaxos, lease_overlap, slots_agree, steady_state_delays


def flush(sim: MultiPaxos, pred) -> None:
    keep, todo = [], []
    for item in sim.net.queue:
        (todo if pred(*item) else keep).append(item)
    sim.net.queue = keep
    for dst, msg in todo:
        sim.deliver(dst, msg)


def drain(sim: MultiPaxos) -> None:
    while sim.net.queue:
        flush(sim, lambda d, m: True)


def test_slot_agreement_random_faults() -> None:
    for seed in range(120):
        sim = MultiPaxos(3, 3, seed, drop=0.1, dup=0.1, crash_prob=0.005,
                         timeout_prob=0.03, stable_after=600)
        r = sim.run()
        assert slots_agree(r), seed
        assert sim.done(), seed  # every command sent after stabilization is applied


def test_slot_agreement_five_acceptors() -> None:
    for seed in range(60):
        sim = MultiPaxos(5, 2, seed, n_learners=3, drop=0.2, dup=0.2, crash_prob=0.01,
                         timeout_prob=0.05, stable_after=800)
        r = sim.run()
        assert slots_agree(r), seed
        assert sim.done(), seed


def test_gap_is_filled_with_noop() -> None:
    sim = MultiPaxos(3, 2, seed=0)
    l0, l1 = sim.leaders
    l0.start(sim.net)
    flush(sim, lambda d, m: m[0] == "PREPARE" and m[1] == l0.ballot)
    flush(sim, lambda d, m: m[0] == "PROMISE")
    for c in ("a", "b", "c"):
        l0.propose(sim.net, c)
    # Slot 0 reaches all acceptors, slot 1 is lost, slot 2 reaches A2 only.
    flush(sim, lambda d, m: m[0] == "ACCEPT" and m[2] == 0)
    flush(sim, lambda d, m: m[0] == "ACCEPT" and m[2] == 2 and d == ("A", 2))
    sim.net.queue = [q for q in sim.net.queue if q[1][0] != "ACCEPT"]
    sim.crashed.add(("L", 0))
    l1.start(sim.net)
    flush(sim, lambda d, m: m[0] == "PREPARE" and d[1] in (1, 2))
    flush(sim, lambda d, m: m[0] == "PROMISE")
    assert l1.active and l1.next_slot == 3
    drain(sim)
    r = sim.result()
    assert r.chosen == {0: {"a"}, 1: {NOOP}, 2: {"c"}}
    assert all(l.applied == ["a", NOOP, "c"] for l in sim.learners)


def test_new_leader_keeps_chosen_value() -> None:
    sim = MultiPaxos(3, 2, seed=0)
    l0, l1 = sim.leaders
    l0.start(sim.net)
    flush(sim, lambda d, m: m[0] == "PREPARE" and m[1] == l0.ballot)
    flush(sim, lambda d, m: m[0] == "PROMISE")
    l0.propose(sim.net, "x")
    flush(sim, lambda d, m: m[0] == "ACCEPT" and d[1] in (0, 1))  # x is chosen in slot 0
    sim.net.queue = []
    l1.start(sim.net)
    flush(sim, lambda d, m: m[0] == "PREPARE" and d[1] in (1, 2))
    flush(sim, lambda d, m: m[0] == "PROMISE")
    l1.propose(sim.net, "y")
    drain(sim)
    assert sim.result().chosen == {0: {"x"}, 1: {"y"}}
    assert all(l.applied == ["x", "y"] for l in sim.learners)


def test_two_delays_in_steady_state() -> None:
    assert steady_state_delays(3, 2) == 2
    assert steady_state_delays(5, 5) == 2


def test_lease_safe_under_bounded_drift() -> None:
    for seed in range(20):
        assert not lease_overlap(rho=0.01, true_rho=0.01, lease=10.0, seed=seed)
        assert not lease_overlap(rho=0.2, true_rho=0.15, lease=10.0, seed=seed)


def test_lease_unsafe_when_drift_exceeds_bound() -> None:
    assert any(lease_overlap(rho=0.01, true_rho=0.3, lease=10.0, seed=s) for s in range(20))
    # The leader that ignores drift (rho = 0) and uses the full lease is unsafe.
    assert any(lease_overlap(rho=0.0, true_rho=0.05, lease=10.0, seed=s) for s in range(20))
