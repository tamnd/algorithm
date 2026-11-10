# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zab/. The authors are listed in prov/M3MBBQ.jsonl.

from zab import Zab


def settle(z: Zab) -> None:
    """Deliver every pending message, in a fixed order."""
    while z.pending():
        z.deliver_one(*sorted(z.pending())[0])


def vals(seq) -> list[str]:
    return [t[2] for t in seq]


def test_no_failures() -> None:
    z = Zab(3)
    z.elect(0, {0, 1, 2})
    settle(z)
    assert z.procs[0].lead["phase"] == 4 and z.established == {1: 0}
    for _ in range(3):
        assert z.propose(0)
    settle(z)
    assert all(vals(p.delivered) == ["v1", "v2", "v3"] for p in z.procs)
    assert all(p.p == 1 and p.a == 1 for p in z.procs)
    assert z.check() == []


def test_uncommitted_suffix_is_dropped_and_order_kept() -> None:
    z = Zab(3)
    z.elect(0, {0, 1, 2})
    settle(z)
    z.propose(0)  # A = (1, 1)
    z.propose(0)  # B = (1, 2)
    z.deliver_one(0, 0)  # the leader logs A and B
    z.deliver_one(0, 0)
    z.deliver_one(0, 1)  # process 1 logs A only
    z.crash(0)
    z.elect(2, {1, 2})  # new epoch with processes 1 and 2
    settle(z)
    assert z.initial[2] == [(1, 1, "v1")]  # the history of process 1, the most recent
    z.propose(2)  # C = (2, 1)
    settle(z)
    assert vals(z.procs[1].delivered) == ["v1", "v3"]
    z.recover(0)  # process 0 still has A, B with f.a = 1
    assert vals(z.procs[0].hist) == ["v1", "v2"]
    z.elect(1, {0, 1, 2})
    settle(z)
    assert z.initial[3] == [(1, 1, "v1"), (2, 1, "v3")]  # f.a = 2 beats f.a = 1
    assert all(vals(p.delivered) == ["v1", "v3"] for p in z.procs)
    assert vals(z.procs[0].hist) == ["v1", "v3"]  # B is gone everywhere
    assert z.check() == []


def test_paxos_figure_1_breaks_primary_order() -> None:
    # Paxos may choose C (ballot 2) in slot 27, B (ballot 1) in slot 28 and D in slot 29,
    # although B was proposed after A, which no slot holds.
    z = Zab(3)
    A, B, C, D = (1, 1, "A"), (1, 2, "B"), (2, 1, "C"), (2, 2, "D")
    z.proposed = {1: [A, B], 2: [C, D]}
    z.initial = {1: [], 2: [A]}
    for p in z.procs:
        p.delivered = [C, B, D]
    problems = " ".join(z.check())
    assert "global primary order" in problems
    assert "local primary order in epoch 1" in problems
    assert "primary of epoch 2 broadcast without delivering (1, 2, 'B')" in problems


def test_no_commit_without_quorum() -> None:
    z = Zab(5)
    z.elect(0, set(range(5)))
    settle(z)
    for p in (2, 3, 4):
        z.crash(p)
    z.propose(0)
    settle(z)
    assert all(p.delivered == [] for p in z.procs)
    assert vals(z.procs[1].hist) == ["v1"]  # logged but not committed


def test_primary_order_on_seeded_runs() -> None:
    total = epochs = 0
    for n in (3, 5):
        for seed in range(120):
            z = Zab(n, seed)
            z.random_run(1200)
            assert z.check() == [], (n, seed)
            total += max(len(p.delivered) for p in z.procs)
            epochs += len(z.established)
    assert total > 2000 and epochs > 1000  # the runs commit a lot and change leader often


def test_random_history_choice_is_caught() -> None:
    bad = 0
    for seed in range(60):
        z = Zab(5, seed, bad_choice=True)
        z.random_run(1200)
        bad += bool(z.check())
    assert bad > 30
