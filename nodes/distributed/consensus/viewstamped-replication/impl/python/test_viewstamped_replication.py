# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/viewstamped-replication/. The authors are listed in prov/FP530T.jsonl.

from viewstamped_replication import VR

OPS = [f"op{i}" for i in range(10)]


def test_normal_operation() -> None:
    for f in (1, 2):
        for seed in range(20):
            sim = VR(f, seed, OPS, dup=0.1).run()
            assert sim.settled() and sim.view_changes == 0
            assert all(r.executed == sim.replicas[0].executed for r in sim.replicas)
            assert sorted(sim.replicas[0].executed) == sorted(OPS)


def test_view_changes_keep_committed_operations() -> None:
    for f in (1, 2):
        for seed in range(60):
            sim = VR(f, seed, OPS, dup=0.1, view_change_prob=0.01).run()
            assert sim.settled(), (f, seed)
            assert sim.committed_kept() and sim.executions_agree(), (f, seed)
            assert sorted(sim.replicas[0].executed) == sorted(OPS), (f, seed)


def test_crashes_recovery_and_view_changes() -> None:
    for f in (1, 2):
        for seed in range(60):
            sim = VR(f, seed, OPS, dup=0.1, crash_prob=0.01, view_change_prob=0.005).run()
            assert sim.settled(), (f, seed)
            assert sim.committed_kept() and sim.executions_agree(), (f, seed)
            assert sorted(sim.replicas[0].executed) == sorted(OPS), (f, seed)
    assert sim.recoveries > 0


def test_new_primary_must_pick_the_latest_log() -> None:
    bad = 0
    for seed in range(60):
        sim = VR(1, seed, OPS, view_change_prob=0.02, unsafe_pick=True).run()
        bad += not (sim.committed_kept() and sim.executions_agree())
    assert bad > 0


def test_rejoining_without_recovery_loses_committed_operations() -> None:
    bad = 0
    for seed in range(60):
        sim = VR(1, seed, OPS, crash_prob=0.02, view_change_prob=0.01, amnesia=True).run()
        bad += not (sim.committed_kept() and sim.executions_agree())
    assert bad > 0
