# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/paxos/. The authors are listed in prov/7W88GQ.jsonl.

from paxos import Paxos, majority, run_paxos, safe


def deliver_matching(px: Paxos, pred) -> None:
    """Deliver, in queue order, every queued message that pred accepts."""
    keep = []
    todo = []
    for item in px.net.queue:
        (todo if pred(*item) else keep).append(item)
    px.net.queue = keep
    for dst, msg in todo:
        px.deliver(dst, msg)


def test_majority() -> None:
    assert [majority(n) for n in range(1, 8)] == [1, 2, 2, 3, 3, 4, 4]


def test_worked_example() -> None:
    # Three acceptors. P0 proposes x, P1 proposes y.
    px = Paxos(3, ["x", "y"], seed=0)
    p0, p1 = px.proposers
    p0.start(px.net)
    deliver_matching(px, lambda d, m: m[0] == "PREPARE" and d[1] in (0, 1))
    deliver_matching(px, lambda d, m: m[0] == "PROMISE")
    assert p0.phase == 2
    deliver_matching(px, lambda d, m: m[0] == "ACCEPT" and d[1] in (0, 1))
    assert [a.vv for a in px.acceptors] == ["x", "x", None]
    px.net.queue = [q for q in px.net.queue if q[1][0] != "PREPARE"]  # P0's PREPARE to A2 is lost
    p1.start(px.net)
    assert p1.ballot == (1, 1) and p1.ballot > p0.ballot
    deliver_matching(px, lambda d, m: m[0] == "PREPARE" and d[1] in (1, 2))
    deliver_matching(px, lambda d, m: m[0] == "PROMISE" and d == ("P", 1))
    # P1 heard of x, accepted at ballot (1, 0), so it must propose x and not y.
    deliver_matching(px, lambda d, m: m[0] == "ACCEPT" and m[1] == (1, 1))
    assert [a.vv for a in px.acceptors] == ["x", "x", "x"]
    deliver_matching(px, lambda d, m: True)
    r = px.result(0)
    assert r.chosen == {"x"} and set(r.learned.values()) == {"x"}


def test_broken_rule_example() -> None:
    # The same schedule, but P1 ignores the accepted value: y is chosen too.
    px = Paxos(3, ["x", "y"], seed=0, follow_rule=False)
    p0, p1 = px.proposers
    p0.start(px.net)
    deliver_matching(px, lambda d, m: m[0] == "PREPARE" and d[1] in (0, 1))
    deliver_matching(px, lambda d, m: m[0] == "PROMISE")
    deliver_matching(px, lambda d, m: m[0] == "ACCEPT" and d[1] in (0, 1))
    px.net.queue = [q for q in px.net.queue if q[1][0] != "PREPARE"]
    p1.start(px.net)
    deliver_matching(px, lambda d, m: m[0] == "PREPARE" and d[1] in (1, 2))
    deliver_matching(px, lambda d, m: m[0] == "PROMISE" and d == ("P", 1))
    deliver_matching(px, lambda d, m: m[0] == "ACCEPT" and m[1] == (1, 1))
    r = px.result(0)
    assert r.chosen == {"x", "y"} and not safe(r)


def test_safety_random_faults() -> None:
    for seed in range(300):
        r = run_paxos(3, ["x", "y", "z"], seed, drop=0.1, dup=0.1, crash_prob=0.01,
                      crash_mid=0.05, timeout_prob=0.1, stable_after=400)
        assert safe(r), seed
        assert len(r.learned) == 2, seed  # liveness after stabilization


def test_safety_unbounded_crashes() -> None:
    # Safety needs no bound on crashes: any number of acceptors may stop.
    for seed in range(150):
        r = run_paxos(5, ["x", "y", "z"], seed, drop=0.2, dup=0.2, crash_prob=0.02,
                      crash_mid=0.1, max_acceptor_crashes=5, keep_leader=False,
                      timeout_prob=0.1, max_steps=1500)
        assert safe(r), seed


def test_adversarial_schedules() -> None:
    for schedule in ("fifo", "lifo", "slow"):
        for seed in range(30):
            r = run_paxos(5, ["x", "y"], seed, drop=0.05, dup=0.1, schedule=schedule,
                          slow_target=("A", 0), timeout_prob=0.2, stable_after=600)
            assert safe(r), (schedule, seed)
            assert len(r.learned) == 2, (schedule, seed)


def test_dueling_proposers_safe() -> None:
    undecided = 0
    for seed in range(200):
        r = run_paxos(3, ["x", "y"], seed, timeout_prob=0.5, max_steps=400)
        assert safe(r), seed
        undecided += not r.chosen
    assert undecided > 0  # with frequent timeouts some runs choose nothing


def test_dueling_livelock_schedule() -> None:
    # The classic schedule: each PREPARE overtakes the other proposer's ACCEPT.
    px = Paxos(3, ["x", "y"], seed=0)
    p0, p1 = px.proposers
    for _ in range(20):
        for p in (p0, p1):
            p.start(px.net)
            deliver_matching(px, lambda d, m: m[0] == "PREPARE")
            deliver_matching(px, lambda d, m: m[0] == "PROMISE")
            other = p1 if p is p0 else p0
            deliver_matching(px, lambda d, m, o=other: m[0] == "ACCEPT" and m[1] == o.ballot)
            deliver_matching(px, lambda d, m: m[0] == "NACK")
    assert px.result(0).chosen == set()
    assert p1.ballot[0] >= 20


def test_broken_rule_fails_on_random_runs() -> None:
    bad = sum(not safe(run_paxos(3, ["x", "y"], s, timeout_prob=0.1, follow_rule=False,
                                 max_steps=1000)) for s in range(50))
    assert bad > 0
