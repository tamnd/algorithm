# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flexible-paxos/. The authors are listed in prov/4PEKRH.jsonl.

from flexible_paxos import FlexiblePaxos, by_size, grid, intersect, safe


def flush(sim: FlexiblePaxos, pred) -> None:
    while True:
        todo = [it for it in sim.net.queue if pred(*it)]
        if not todo:
            return
        sim.net.queue = [it for it in sim.net.queue if not pred(*it)]
        for dst, msg in todo:
            sim.deliver(dst, msg)


def test_counting_rule_by_brute_force() -> None:
    for n in range(1, 8):
        for q1 in range(1, n + 1):
            for q2 in range(1, n + 1):
                assert intersect(n, by_size(q1), by_size(q2)) == (q1 + q2 > n), (n, q1, q2)


def test_grid_quorums() -> None:
    for rows, cols in [(2, 2), (2, 3), (3, 3), (3, 2)]:
        col, row = grid(rows, cols)
        n = rows * cols
        assert intersect(n, col, row)
        assert not intersect(n, row, row) or rows == 1
        assert not intersect(n, col, col) or cols == 1


def test_safe_random_runs() -> None:
    configs = [(5, by_size(4), by_size(2), 1), (6, by_size(4), by_size(3), 2),
               (5, by_size(3), by_size(3), 2), (9, *grid(3, 3), 0)]
    for n, q1, q2, crashes in configs:
        for seed in range(50):
            sim = FlexiblePaxos(n, q1, q2, ["x", "y", "z"], seed, drop=0.1, dup=0.1,
                                crash_prob=0.01, max_acceptor_crashes=crashes,
                                timeout_prob=0.1, stable_after=400)
            r = sim.run()
            assert safe(r, sim.inputs), (n, seed)
            assert len(r.learned) == 2, (n, seed)


def test_unbounded_crashes_safe() -> None:
    for seed in range(80):
        sim = FlexiblePaxos(5, by_size(4), by_size(2), ["x", "y"], seed, drop=0.2, dup=0.2,
                            crash_prob=0.02, max_acceptor_crashes=5, timeout_prob=0.1)
        assert safe(sim.run(), sim.inputs), seed


def test_non_intersecting_quorums_break_safety() -> None:
    assert not intersect(4, by_size(2), by_size(2))
    bad = sum(not safe(FlexiblePaxos(4, by_size(2), by_size(2), ["x", "y"], s,
                                     timeout_prob=0.1, drop=0.1).run(), ["x", "y"])
              for s in range(100))
    assert bad > 0


def test_explicit_split_brain_with_small_quorums() -> None:
    sim = FlexiblePaxos(4, by_size(2), by_size(2), ["x", "y"], seed=0)
    p0, p1 = sim.proposers
    p0.start(sim.net)
    p1.start(sim.net)
    # P0 talks to A0 and A1 only; P1 talks to A2 and A3 only.
    flush(sim, lambda d, m: d[0] in ("P", "L") or (m[1][1] == 0) == (d[1] < 2))
    assert sim.learners[0].learned is not None
    assert sim.result().chosen == {"x", "y"}


def test_small_phase2_quorum_tolerates_more_crashes_in_steady_state() -> None:
    sim = FlexiblePaxos(5, by_size(4), by_size(2), ["x", "y"], seed=0)
    p0, p1 = sim.proposers
    p0.start(sim.net)
    flush(sim, lambda d, m: m[0] == "PREPARE" and m[1] == p0.ballot)
    flush(sim, lambda d, m: m[0] == "PROMISE")
    sim.crashed |= {("A", 2), ("A", 3), ("A", 4)}  # 3 of 5 acceptors are down
    flush(sim, lambda d, m: True)
    assert sim.result().chosen == {"x"}
    # A new leader cannot finish phase 1 with only 2 live acceptors.
    p1.start(sim.net)
    flush(sim, lambda d, m: True)
    assert p1.phase == 1
