# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/leader-lease/. The authors are listed in prov/WTCD0Y.jsonl.

from leader_lease import LeaseSim, partition_scenario


def bad_runs(seeds: int, **kw) -> int:
    bad = 0
    for seed in range(seeds):
        sim = LeaseSim(seed, **kw).run()
        bad += sim.stale > 0 or sim.overlap > 0
    return bad


def test_safe_under_bounded_drift() -> None:
    for kw in ({}, {"n": 5}, {"delay": 2.0}):
        reads = 0
        for seed in range(60):
            sim = LeaseSim(seed, **kw).run()
            assert sim.stale == 0 and sim.overlap == 0, (kw, seed)
            reads += sim.reads
        assert reads > 1000


def test_safe_at_the_edge_of_the_bound() -> None:
    # the old leader runs at 1 - rho and the others at 1 + rho
    sim = partition_scenario(0.9, 1.1, margin=True)
    assert sim.stale == 0 and sim.overlap == 0
    assert sim.nodes[1].lease_end > sim.nodes[0].lease_end
    assert sim.commits > 5


def test_no_drift_margin_gives_two_leaders_and_a_stale_read() -> None:
    sim = partition_scenario(0.9, 1.1, margin=False)
    assert sim.overlap > 0 and sim.stale > 0
    assert bad_runs(60, margin=False) > 0


def test_drift_beyond_the_bound_gives_stale_reads() -> None:
    sim = partition_scenario(0.7, 1.3, margin=True)
    assert sim.overlap > 0 and sim.stale > 0
    assert bad_runs(60, true_rho=0.3) > 0


def test_lease_must_start_when_the_request_is_sent() -> None:
    assert bad_runs(100, rho=0.0, delay=2.0) == 0
    assert bad_runs(100, rho=0.0, delay=2.0, from_receipt=True) > 0
